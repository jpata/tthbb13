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
from sklearn.metrics import log_loss

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
    y = df["tt_class_new"].values
            
    tmp_weight_dic = df["tt_class_new"].value_counts().to_dict()    
    weight_dic = {}
    for k,v in tmp_weight_dic.iteritems():
        weight_dic[k] = float(len(X))/v 
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

def rocplot(clf, 
            df):
    
    sig_class = 2
    #prob = "proba_{0}".format(1)
    prob = "blr".format(1)

    plt.clf()
    plt.yscale('log')

    orig_names = {0: "ttb", 
                  1: "tt2b",
                  2: "ttbb",
                  3: "ttcc",
                  4: "ttll"}


    for bkg_class in 0,1,3,4:
        
        nbins = 100
        min_prob = min(df[prob])
        max_prob = max(df[prob])

        print min_prob, max_prob

        if min_prob >= max_prob:
            max_prob = 1.1 * abs(min_prob)

        # Signal 
        h1 = make_df_hist((nbins*200,min_prob,max_prob), df.loc[df["tt_class"] == sig_class,prob])    

        # Background
        h2 = make_df_hist((nbins*200,min_prob,max_prob), df.loc[df["tt_class"] == bkg_class,prob])    

        # And turn into ROC
        r, e = calc_roc(h1, h2)

        plt.plot(r[:, 0], 1/r[:, 1], 
                 lw=1, 
                 ls="--",                 
                 label = "BLR vs {0}".format(orig_names[bkg_class])
             )
        
    plt.plot( [0.1088], [1/0.0309], ls = 'None', marker = "o",color='black',  label =  "4tag vs ttb")
    plt.plot( [0.1088], [1/0.0374], ls = 'None', marker = "^", color='black', label = "4tag vs tt2b") 
    plt.plot( [0.1088], [1/0.0140], ls = 'None', marker = "v", color='black', label = "4tag vs ttcc")
    plt.plot( [0.1088], [1/0.0025], ls = 'None', marker = "s", color='black', label = "4tag vs ttll") 

    plt.plot( [0.0577], [1/0.0115], ls = 'None', marker = "o",color='black',  fillstyle = 'full', label = "4tag, highBLR vs ttb")
    plt.plot( [0.0577], [1/0.0157], ls = 'None', marker = "^", color='black', fillstyle = 'full', label = "4tag, highBLR vs tt2b") 
    plt.plot( [0.0577], [1/0.0025], ls = 'None', marker = "v", color='black', fillstyle = 'full', label = "4tag, highBLR vs ttcc")
    plt.plot( [0.0577], [1/0.0003], ls = 'None', marker = "s", color='black', fillstyle = 'full', label = "4tag, highBLR vs ttll") 

         
    # Setup nicely
    plt.legend(loc=2)
    plt.xlabel( "signal match efficiency", fontsize=16)
    plt.ylabel("1/fake match efficiency", fontsize=16)
    plt.legend(loc=2)
    plt.xlim(0,1)
    plt.ylim(1,1000000)

    plt.legend(loc=1)

    plt.show()
    plt.savefig(clf.name + "-ROC.png")


########################################
# Helper: datagen
########################################

def new_class(c):

#    return c

    if c == 0:
        return 0
    elif c == 1:
        return 0
    elif c == 2:
        return 1
    elif c == 3:
        return 0
    elif c == 4:
        return 0
    else:
        return 0
    

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
         

        df["tt_class_new"] = df.apply(lambda x:new_class(x["tt_class"]),axis=1)


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
    
    for ic in clf.classes:
        df_test["proba_{0}".format(ic)] = 0
    df_test[["proba_{0}".format(ic) for ic in clf.classes]] = clf.model.predict_proba(X_test)

    print "Eval train"
    X_train = clf.image_fun(df_train)
    df_train["output"] = clf.model.predict(X_train)

    for ic in clf.classes:
        df_train["proba_{0}".format(ic)] = 0
    df_train[["proba_{0}".format(ic) for ic in clf.classes]] = clf.model.predict_proba(X_train)


    # Generate the training weight dictionary 
    # (using weights derived on testing sample would be cheating)            

    tmp_weight_dic = df_train["tt_class_new"].value_counts().to_dict()    
    weight_dic = {}
    for k,v in tmp_weight_dic.iteritems():
        weight_dic[k] = float(len(X_train))/v 

    # and apply to both samples
    weights_train = np.vectorize(weight_dic.get)(df_train["tt_class_new"].values)
    weights_test  = np.vectorize(weight_dic.get)(df_test["tt_class_new"].values)

    # Generate category matrix
    matrix = np.zeros((len(clf.classes),len(clf.classes)))
    for true_class in clf.classes:        
        num = float( len(df_test.loc[ (df_test["tt_class_new"] == true_class),"evt"]))
        for found_class in clf.classes:            
            matrix[true_class][found_class] = len(df_test.loc[ (df_test["tt_class_new"] == true_class) & (df_test["output"] == found_class),"evt"])/num
            
    # Plot the category matrix
    fig, ax = plt.subplots()
    min_val, max_val, diff = 0., float(len(clf.classes)), 1.

    #imshow portion
    ax.imshow(matrix, 
              interpolation='nearest',
              cmap=plt.get_cmap("summer")
    )

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



    rocplot(clf, df_test)

    # Plot different reco probaility distribtuons for each true class
    for true_class in clf.classes:

        plt.clf()

        min_prob = min([min( df_test.loc[ df_test["tt_class_new"] == true_class, "proba_{0}".format(reco_class) ]) for reco_class in clf.classes])
        max_prob = max([max( df_test.loc[ df_test["tt_class_new"] == true_class, "proba_{0}".format(reco_class) ]) for reco_class in clf.classes])

        colors = ['black', 'red','blue','green','orange','green','magenta']

        for reco_class in clf.classes:
            
            # Test Sample
            prob = df_test.loc[ df_test["tt_class_new"] == true_class, "proba_{0}".format(reco_class) ]            
            plt.hist(prob, 
                     label="{0} proba (Test)".format(clf.class_names[reco_class]), 
                     bins=np.linspace(min_prob,max_prob,60), 
                     histtype = 'step',
                     ls="-",
                     color = colors[reco_class],
                     normed=True)

            # Train Sample
            prob = df_train.loc[ df_train["tt_class_new"] == true_class, "proba_{0}".format(reco_class) ]            
            plt.hist(prob, 
                     label="{0} proba (Train)".format(clf.class_names[reco_class]), 
                     bins=np.linspace(min_prob,max_prob,60), 
                     histtype = 'step',
                     ls=':', 
                     color = colors[reco_class],
                     normed=True)

            plt.title("True {0} Events".format(clf.class_names[true_class]))
            plt.xlabel("Probability", fontsize=16)
            plt.ylabel("Events", fontsize=16)        
            plt.legend(loc=1)
            plt.xlim(min_prob,max_prob)
            plt.show()
            plt.savefig("{0}_probas.png".format(clf.class_names[true_class]))


    # Plot different classfiers outputs for all true classes
    for reco_class in clf.classes:

        plt.clf()

        min_prob = min(df_test[  "proba_{0}".format(reco_class) ]) 
        max_prob = max(df_test[  "proba_{0}".format(reco_class) ])

        colors = ['black', 'red','blue','green','orange','green','magenta']

        for true_class in clf.classes:
            
            # Test Sample
            prob = df_test.loc[ df_test["tt_class_new"] == true_class, "proba_{0}".format(reco_class) ]            
            plt.hist(prob, 
                     label="True {0} (Test)".format(clf.class_names[true_class]), 
                     bins=np.linspace(min_prob,max_prob,60), 
                     histtype = 'step',
                     ls="-",
                     color = colors[true_class],
                     normed=True)

            # Train Sample
            prob = df_train.loc[ df_train["tt_class_new"] == true_class, "proba_{0}".format(reco_class) ]            
            plt.hist(prob, 
                     label="True {0} (Train)".format(clf.class_names[true_class]), 
                     bins=np.linspace(min_prob,max_prob,60), 
                     histtype = 'step',
                     ls=':', 
                     color = colors[true_class],
                     normed=True)

        plt.title("{0} Classifier".format(clf.class_names[reco_class]))
        plt.xlabel("Probability", fontsize=16)
        plt.ylabel("Events", fontsize=16)        
        plt.legend(loc=1)
        plt.xlim(min_prob,max_prob)
        plt.show()
        plt.savefig("{0}_classifier.png".format(clf.class_names[reco_class]))

    
    # Loss function/time    
    
#    print "Calculating test scores for all iterations. Samples:", len(X_test)
#    predictor_test  = clf.model.staged_predict(X_test)	
#    predictor_test_proba  = clf.model.staged_predict_proba(X_test)	
#
#    test_scores  = [log_loss(df_test["tt_class_new"], 
#                             predictor_test_proba.next(), 
#                             normalize = True,
#                             sample_weight=weights_test) for _ in range(clf.params["n_estimators"])]
#
#    print "Calculating train scores for all iterations. Samples:", len(X_train)
#    predictor_train  = clf.model.staged_predict(X_train)	
#    predictor_train_proba  = clf.model.staged_predict_proba(X_train)	
#    train_scores  = [log_loss(df_train["tt_class_new"], 
#                              predictor_train_proba.next(), 
#                              normalize = True,
#                              sample_weight=weights_train) for _ in range(clf.params["n_estimators"])]
#
#    print "Last Train:", train_scores[-1]
#    print "Last Test:",  test_scores[-1]
#
#    plt.clf()
#
#    plt.plot(train_scores, label="Train", color = 'blue')
#    plt.plot(test_scores, label="Test", color = 'red')
#
#    plt.title('Cross Entropy', fontsize=16)
#    plt.xlabel('Iterations', fontsize=16)
#    plt.ylabel('Score', fontsize=16)
#    plt.grid(False)
#    plt.legend(loc=0)
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
