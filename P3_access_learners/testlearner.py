""""""  		  	   		 	   			  		 			     			  	 
"""  		  	   		 	   			  		 			     			  	 
Test a learner.  (c) 2015 Tucker Balch  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	   			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		 	   			  		 			     			  	 
All Rights Reserved  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Template code for CS 4646/7646  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	   			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		 	   			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		 	   			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		 	   			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	   			  		 			     			  	 
or edited.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		 	   			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		 	   			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	   			  		 			     			  	 
GT honor code violation.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
-----do not edit anything above this line---  		  	   		 	   			  		 			     			  	 
"""  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
import numpy as np
import DTLearner as dtl
import RTLearner as rtl
import BagLearner as bl
import matplotlib.pyplot as plt
import time
import sys


def data_preprocess(filename):
    """
    Read and preprocess data.
    """
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)
    if filename.endswith("Istanbul.csv"):
        data = data[:, 1:]
    np.random.seed(3)
    np.random.shuffle(data)
    train_rows = int(0.6 * len(data))
    Xtrain = data[:train_rows, :-1]
    Ytrain = data[:train_rows, -1]
    Xtest = data[train_rows:, :-1]
    Ytest = data[train_rows:, -1]
    return Xtrain, Ytrain, Xtest, Ytest

def compute_metric(y,predY,metric):
    if metric == 'rmse':
        return np.sqrt(((y - predY) ** 2).mean())
    elif metric == 'mae':
        return np.mean(np.abs(y - predY))


def plot_results(x, y1, y2, title, xlabel, ylabel, legend, filename, xticks=None):
    """
    Utility function for plotting results.
    """
    plt.plot(x, y1, label=legend[0])
    plt.plot(x, y2, label=legend[1])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xticks is not None:
        plt.xticks(xticks)
    plt.grid()
    plt.legend()
    plt.savefig(filename)
    plt.clf()

def exp_1(Xtrain, Ytrain, Xtest, Ytest):
    leaf_sizes = range(1, 51)
    training_rsme, test_rsme = [], []

    for leaf_size in leaf_sizes:
        learner = dtl.DTLearner(leaf_size=leaf_size,verbose = False)
        learner.add_evidence(Xtrain, Ytrain)
        training_rsme.append(compute_metric(Ytrain, learner.query(Xtrain),'rmse'))
        test_rsme.append(compute_metric(Ytest, learner.query(Xtest),'rmse'))

    plot_results(leaf_sizes, training_rsme, test_rsme,
                 "Figure 1 - Overfitting in DT", "Leaf Size", "RMSE",
                 ["Training error", "Test error"], "Figure_1.png",np.arange(1, 51, 5))


def exp_2(Xtrain, Ytrain, Xtest, Ytest, bags=20):
    leaf_sizes = range(1, 51)
    training_rsme, test_rsme = [], []

    for leaf_size in leaf_sizes:
        learner = bl.BagLearner(learner=dtl.DTLearner, kwargs={"leaf_size": leaf_size}, bags=bags, boost=False,
                                verbose=False)
        learner.add_evidence(Xtrain, Ytrain)
        training_rsme.append(compute_metric(Ytrain, learner.query(Xtrain),'rmse'))
        test_rsme.append(compute_metric(Ytest, learner.query(Xtest),'rmse'))

    plot_results(list(leaf_sizes), training_rsme, test_rsme,
                 "Figure 2 - Reduction of overfitting with bagging",
                 "Leaf Size", "RMSE", ["Training error", "Test error"],
                 "Figure_2.png", np.arange(1, 51, 5))

def exp_3(Xtrain, Ytrain, Xtest, Ytest):
    leaf_sizes = range(1, 51)
    dt_train_time, rt_train_time = [], []
    dt_mae_train, rt_mae_train = [], []
    dt_mae_test, rt_mae_test = [], []

    for leaf_size in leaf_sizes:
        # DTLearner
        start_time = time.time()
        dt_learner = dtl.DTLearner(leaf_size=leaf_size, verbose=False)
        dt_learner.add_evidence(Xtrain, Ytrain)
        dt_train_time.append(time.time() - start_time)
        dt_mae_train.append(compute_metric(Ytrain, dt_learner.query(Xtrain),'mae'))
        dt_mae_test.append(compute_metric(Ytest, dt_learner.query(Xtest),'mae'))

        # RTLearner
        start_time = time.time()
        rt_learner = rtl.RTLearner(leaf_size=leaf_size, verbose=False)
        rt_learner.add_evidence(Xtrain, Ytrain)
        rt_train_time.append(time.time() - start_time)
        rt_mae_train.append(compute_metric(Ytrain, rt_learner.query(Xtrain),'mae'))
        rt_mae_test.append(compute_metric(Ytest, rt_learner.query(Xtest),'mae'))

    plt.plot(leaf_sizes, dt_mae_train, 'b-', label='DTLearner Training error', linewidth=2, markersize=5)
    plt.plot(leaf_sizes, rt_mae_train, 'r--', label='RTLearner Training error', linewidth=2, markersize=5)
    plt.plot(leaf_sizes, dt_mae_test, 'g-', label='DTLearner Test error', linewidth=2, markersize=5)
    plt.plot(leaf_sizes, rt_mae_test, 'm--', label='RTLearner Test error', linewidth=2, markersize=5)

    plt.title("Figure 3 - DTLearner VS RTLearner (MAE)")
    plt.xlabel("Leaf Size")
    plt.ylabel("MAE")
    plt.xticks(np.arange(1, 51, 5))
    plt.grid(True)
    plt.legend()
    plt.savefig("Figure_3.png")
    plt.clf()

    plot_results(leaf_sizes, dt_train_time, rt_train_time,
                 "Figure 4 - DTLearner VS RTLearner (Training Time)", "Leaf Size", "Time (seconds)",
                 ["DTLearner", "RTLearner"], "Figure_4.png", np.arange(1, 51, 5))




def main():
    if len(sys.argv) != 2:
        print("Usage: python testlearner.py <datafile>")
        sys.exit(1)  # Exit the script if filename is not provided

    filename = sys.argv[1]  # Get the filename from command-line arguments
    Xtrain, Ytrain, Xtest, Ytest = data_preprocess(filename)

    exp_1(Xtrain, Ytrain, Xtest, Ytest)
    exp_2(Xtrain, Ytrain, Xtest, Ytest, bags=20)
    exp_3(Xtrain, Ytrain, Xtest, Ytest)


if __name__ == "__main__":
    main()
