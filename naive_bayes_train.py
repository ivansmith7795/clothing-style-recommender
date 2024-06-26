import h2o
import pandas as pd
from h2o.estimators.naive_bayes import H2ONaiveBayesEstimator

#Specify the number of threads the H20 framework will consume
h2o.init(nthreads = -1, max_mem_size = 8)

#Load the data from the labeled data set
data_csv = "datasets/dataset-dresses-labeled-processed-bayes.csv"
labeled_dataset = pd.read_csv(data_csv)

#Drop unused columns
labeled_dataset = labeled_dataset.drop(columns=['Unnamed: 0'])

data = h2o.H2OFrame(labeled_dataset)

splits = data.split_frame(ratios=[0.8, 0.10], seed=1)  

train = splits[0]
valid = splits[1]
test = splits[2]

y = 'Style'
x = list(data.columns)


#remove the response from our independent variable list along with the link and style options categories
x.remove(y) 

#Train the model and produce the model file nb_fit1
nb_fit1 = H2ONaiveBayesEstimator(model_id='nb_style_classifier', seed=1)
nb_fit1.train(x=x, y=y, training_frame=train)

#Produce the performance metrics
nb_perf1 = nb_fit1.model_performance(test)

#Print the RMSE score of the model
print("Naive Bayes Estimator:")
print(nb_perf1.rmse())
print(nb_perf1)
# calculate variable importance and export to a csv file
nb_permutation_varimp = nb_fit1.permutation_importance(train, use_pandas=True)
print(nb_permutation_varimp)
nb_permutation_varimp.reset_index(level=0, inplace=True)
frame = h2o.H2OFrame(nb_permutation_varimp)
h2o.export_file(frame, path = "results/naive_bayes_permutation_importance.csv", force=True)

# Retrieve the confusion matrix
conf_matrix = nb_perf1.confusion_matrix()
print(conf_matrix)

# Export the confusion matrix
frame = h2o.H2OFrame(conf_matrix.as_data_frame())
h2o.export_file(frame, path = "results/naive_bayes_confusion_matrix.csv", force=True)

model_path = h2o.save_model(model=nb_fit1, path="models", force=True)


