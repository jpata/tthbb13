########################################
# Imports
########################################

print "Imports: Starting..."

import sys

def fixPath():
    newpath = []
    for v in sys.path:
        if "cvmfs" in v and "pandas" in v:
            continue
        newpath += [v]
    return newpath

sys.path = fixPath()

import os
import pickle
import pdb

print "Imported basics"

import ROOT

print "Imported ROOT"

import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import pandas
import root_numpy
from matplotlib.colors import LogNorm

print "Imported numpy"

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import SGD
from keras.utils import np_utils, generic_utils
from keras.layers.advanced_activations import PReLU
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Convolution2D, MaxPooling2D, AveragePooling2D, ZeroPadding2D
from keras.layers.core import Reshape
from keras.models import model_from_yaml


print "Imported keras"

import sklearn
from sklearn import preprocessing
from sklearn.tree  import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OutputCodeClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.preprocessing import normalize
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler  
from sklearn.svm import SVC


print "Imported sklearn"

from plotlib import *


print "Imports: Done..."


########################################
# Class: Classifier
########################################

class Classifier:
    def __init__(self,
                 name,
                 backend,
                 params,
                 load_from_file,
                 datagen_train,
                 datagen_test,
                 model,
                 image_fun,
                 class_names,
                 inpath = ".",
                 plot_name = "",                 
                 input_vars = [],
             ):
        self.name = name
        self.backend = backend
        self.params = params
        self.load_from_file = load_from_file
        self.datagen_train = datagen_train
        self.datagen_test  = datagen_test
        self.model = model
        self.image_fun = image_fun
        self.inpath = inpath
        
        self.class_names = class_names
        self.classes = sorted(class_names.keys())
        
        if plot_name:
            self.plot_name = plot_name
        else:
            self.plot_name = name

        self.input_vars = input_vars

    def prepare(self):

        if not self.load_from_file:
            if self.backend == "scikit":
                train_scikit(self)
            elif self.backend == "keras":
                train_keras(self)
        else:
            if self.backend == "scikit":
                f = open(os.path.join(self.inpath,self.name + ".pickle"), "r")
                self.model = pickle.load(f)
                f.close()
                                
            elif self.backend == "keras":
                f = open(os.path.join(self.inpath,self.name + ".yaml"), "r")
                yaml_string = f.read()
                f.close()
                self.model = model_from_yaml(yaml_string)                
                self.model.load_weights(os.path.join(self.inpath,self.name + "_weights.h5"))
            print "Loading", self.name, "from file: Done..."


########################################
# Helper: train_scitkit
########################################

def train_scikit(clf):

    print "Starting train_scikit with the parameters: "
    for k,v in clf.params.iteritems():
        print "\t", k,"=",v
      
    df = clf.datagen_train.next()
    X = clf.image_fun(df)
    y = df["tt_class"].values
            
    weight_dic = df["tt_class"].value_counts().to_dict()
    weight_dic = {k:float(len(X))/v for k,v in weight_dic.iteritems()}
    weights = np.vectorize(weight_dic.get)(y)
    
    clf.model.fit(X, y, sample_weight=weights)

    f = open(clf.name + ".pickle","wb")
    pickle.dump(clf.model, f)
    f.close()


########################################
# Helper: train_keras
########################################

def train_keras(clf):

    print "Starting train_keras with the parameters: "
    for k,v in clf.params.iteritems():
        print "\t", k,"=",v
      
    # Prepare model and train
    sgd = SGD(lr = clf.params["lr"], 
              decay = clf.params["decay"], 
              momentum = clf.params["momentum"], 
              nesterov=True)
    clf.model.compile(loss='mean_squared_error', optimizer=sgd, metrics=["accuracy"])
                
    print "Calling fit_generator"

    def generator(dg):
        while True:
            df = dg.next()
            X = clf.image_fun(df)
            y = np_utils.to_categorical(df["is_signal_new"].values)

            yield X,y

    train_gen = generator(clf.datagen_train)
    test_gen  = generator(clf.datagen_test)
    
    ret = clf.model.fit_generator(train_gen,
                                  samples_per_epoch = clf.params["samples_per_epoch"],
                                  nb_epoch = clf.params["nb_epoch"],
                                  verbose=2, 
                                  validation_data=test_gen,
                                  nb_val_samples = clf.params["samples_per_epoch"]/2)

    print "Done"
  
    plt.clf()
    plt.plot(ret.history["acc"])
    plt.plot(ret.history["val_acc"])
    plt.savefig("acc.png")
 
    plt.clf()
    plt.plot(ret.history["loss"])
    plt.plot(ret.history["val_loss"])
    plt.savefig("loss.png")
  
    valacc_out = open("valacc.txt", "w")
    valacc_out.write(str(ret.history["val_acc"][-1]) + "\n")
    valacc_out.close()

    maxvalacc_out = open("maxvalacc.txt", "w")
    maxvalacc_out.write(str(max(ret.history["val_acc"])) + "\n")
    maxvalacc_out.close()
    
    deltaacc_out = open("deltaacc.txt", "w")
    deltaacc_out.write(str(ret.history["val_acc"][-1] - ret.history["acc"][-1]) + "\n")
    deltaacc_out.close()
 
    # save the architecture
    model_out_yaml = open(clf.name + ".yaml", "w")
    model_out_yaml.write(clf.model.to_yaml())
    model_out_yaml.close()
    
    # And the weights
    clf.model.save_weights(clf.name + '_weights.h5', 
                           overwrite=True)



########################################
# Helper: rocplot
########################################

def rocplot(clf, df):
    
    nbins = 100
    min_prob = min(df["sigprob"])
    max_prob = max(df["sigprob"])
        
    if min_prob >= max_prob:
        max_prob = 1.1 * abs(min_prob)
        
    plt.clf()

    #plt.yscale('log')
                
    # Signal 
    h1 = make_df_hist((nbins*5,min_prob,max_prob), df.loc[df["is_signal_new"] == 1,"sigprob"])    
    
    # Background
    h2 = make_df_hist((nbins*5,min_prob,max_prob), df.loc[df["is_signal_new"] == 0,"sigprob"])    

    # And turn into ROC
    r, e = calc_roc(h1, h2)

    plt.clf()        
    plt.plot(r[:, 0], r[:, 1], lw=1, ls="--")
        
    # Setup nicely
    plt.legend(loc=2)
    plt.xlabel( "signal match efficiency", fontsize=16)
    plt.ylabel("fake match efficiency", fontsize=16)
    plt.legend(loc=2)
    plt.xlim(0,1)
    plt.ylim(0,1)
    
    plt.show()
    plt.savefig(clf.name + "-ROC.png")


########################################
# Helper: datagen
########################################

def datagen(sel, brs, infname, n_chunks=10):

    f = ROOT.TFile.Open(infname)
    entries = f.Get("multiclass_6j").GetEntries()
    f.Close()

    # Initialize
    step = entries/n_chunks
    i_start = 0

    # Generate data forever
    while True:
        
        d = root_numpy.root2array(infname, treename="multiclass_6j", branches=brs, selection = sel, start=i_start, stop = i_start + step)

        i_start += step

        # roll over
        if i_start + step >= entries:
            i_start = 0
            
        df = pandas.DataFrame(d)
                    
        # Shuffle
        df = df.iloc[np.random.permutation(len(df))]
                
        yield df




def analyze(clf):

    # Get the data
    # We need test and train as we want to plat to evolution as well
    print "Get train sample"
    df_train = clf.datagen_train.next()            
    print "Get test sample"
    df_test  = clf.datagen_test.next()            

    # Evaluate models
    print "Eval test"
    X_test = clf.image_fun(df_test)
    df_test["output"] = clf.model.predict(X_test)

    print "Eval train"
    X_train = clf.image_fun(df_train)
    df_train["output"] = clf.model.predict(X_train)

    # Generate the training weight dictionary 
    # (using weights derived on testing sample would be cheating)            
    weight_dic = df_train["tt_class"].value_counts().to_dict()
    weight_dic = {k:float(len(X_train))/v for k,v in weight_dic.iteritems()}

    # and apply to both samples
    weights_train = np.vectorize(weight_dic.get)(df_train["tt_class"].values)
    weights_test  = np.vectorize(weight_dic.get)(df_test["tt_class"].values)

    # Generate category matrix
    matrix = np.zeros((len(clf.classes),len(clf.classes)))
    for true_class in clf.classes:        
        num = float( len(df_test.loc[ (df_test["tt_class"] == true_class),"evt"]))
        for found_class in clf.classes:            
            matrix[true_class][found_class] = len(df_test.loc[ (df_test["tt_class"] == true_class) & (df_test["output"] == found_class),"evt"])/num
            
    # Plot the category matrix
    fig, ax = plt.subplots()
    min_val, max_val, diff = 0., float(len(clf.classes)), 1.

    #imshow portion
    ax.imshow(matrix, interpolation='nearest')

    print matrix

    #text portion
    ind_array = np.arange(min_val, max_val, diff)
    x, y = np.meshgrid(ind_array, ind_array)

    for x_val, y_val in zip(x.flatten(), y.flatten()):
        x_pos = int(x_val)
        y_pos = int(y_val)
        c = "{0:.2f}".format(matrix[y_val, x_val])
        ax.text(x_val, y_val, c, va='center', ha='center')

    ax.set_xticks(clf.classes)
    ax.set_yticks(clf.classes)
    ax.set_xticklabels( [clf.class_names[c] for c in clf.classes])
    ax.set_yticklabels( [clf.class_names[c] for c in clf.classes])

    ax.text(0.6, -0.1, 'Reco Class',
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes,
            color='black', fontsize=15)

    ax.text(-0.1, 0.6, 'True \n Class',
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes,
            color='black', fontsize=15)

    plt.show()
    plt.savefig("matrix.png")
    
    feautures = sorted(zip(clf.input_vars, clf.model.feature_importances_), key = lambda x:x[1])    
    for f in feautures:
        print "{0: <15}: {1:.4f}".format(f[0],f[1])


    plt.clf()

    pdb.set_trace()

#    # Loss function/time    
#    print "Calculating test scores for all iterations. Samples:", len(X_test)
#    predictor_test  = clf.model.staged_predict(X_test)	
#    test_scores  = [clf.model.score(X_test ,predictor_test.next(), weights_test)   for _ in range(clf.params["n_estimators"])]
#
#    print "Calculating train scores for all iterations. Samples:", len(X_train)
#    predictor_train  = clf.model.staged_predict(X_train)	
#    train_scores  = [clf.model.score(X_train ,predictor_train.next(), weights_train)   for _ in range(clf.params["n_estimators"])]
#
#    print "Train:", train_scores
#    print "Test:",  test_scores
#
#    plt.plot(train_scores, label="Train", color = 'blue')
#    plt.plot(test_scores, label="Test", color = 'red')
#
#    plt.xlabel('Iterations')
#    plt.ylabel('Score')
#    plt.grid(False)
#    plt.show()
#    plt.savefig("score.png")

    



########################################
# Data access helpers
########################################

def get_data_vars(df, varlist):        
    return df[varlist].values

def get_data_flatten(df, varlist):
    
    # tmp is a 1d-array of 1d-arrays
    # so we need to convert it to 2d array
    tmp = df[varlist].values.flatten() # 
    ret = np.vstack([tmp[i] for i in xrange(len(tmp))])
     
    return ret 
