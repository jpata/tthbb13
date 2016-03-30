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
import psutil
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
from keras.layers import AutoEncoder
from keras.layers import containers
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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OutputCodeClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.preprocessing import normalize
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler  

print "Imported sklearn"

from TTH.Plotting.joosep.plotlib import *

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
                 inpath = ".",
                 plot_name = "",
             ):
        self.name = name
        self.backend = backend
        self.params = params
        self.load_from_file = load_from_file
        self.datagen_train = datagen_train
        self.datagen_test  = datagen_test
        self.model = model
        self.inpath = inpath

        if plot_name:
            self.plot_name = plot_name
        else:
            self.plot_name = name

    def prepare(self):

        if not self.load_from_file:
            if self.backend == "scikit":
                train_scikit(dtrain, self)
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

def train_scikit(df, clf):

    df_shuf = df.iloc[np.random.permutation(np.arange(len(df)))]

    # TODO: rewrite to use datagen
    X = clf.get_data(df_shuf)
    y = df_shuf["is_signal_new"].values

    clf.model.fit(X, y)

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
    clf.model.compile(loss='mean_squared_error', optimizer=sgd)

    print clf.datagen_test
                
    ret = clf.model.fit_generator(clf.datagen_train,
                                  samples_per_epoch = clf.params["samples_per_epoch"], 
                                  nb_epoch = clf.params["nb_epoch"],
                                  verbose=2, 
                                  validation_data=clf.datagen_test.next(),
                                  show_accuracy=True)
  
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

def rocplot(clf, tmp_df, classes, class_names):

    # Predict all probabilities

    # TODO: rewrite to use datagen
    X_test = clf.get_data(tmp_df)
    all_probs = clf.model.predict_proba(X_test)    

    # And add them to (copy of) dataframe
    df = tmp_df.copy()
    for cls in classes:
        df[cls] = all_probs[:,cls]
        
    for sig_class in classes:
                
        other_classes = [cls for cls in classes if not cls==sig_class]

        nbins = 100
        min_prob = df[sig_class].min()
        max_prob = df[sig_class].max()
        
        if min_prob >= max_prob:
            max_prob = 1.1 * abs(min_prob)
        
        plt.clf()
        plt.yscale('log')

        # Signal Efficiency
        sig = df["is_signal_new"]==sig_class
        probs1 = df[sig][sig_class].values
        h1 = make_df_hist((nbins*5,min_prob,max_prob), probs1)

        plt.hist(probs1, label=class_names[sig_class], bins=np.linspace(min_prob,max_prob,nbins), alpha=0.4)

        rocs = []
        
        for bkg_class in other_classes:

            # Background efficiency
            bkg = df["is_signal_new"]==bkg_class
            probs2 = df[bkg][sig_class].values
            h2 = make_df_hist((nbins*5,min_prob,max_prob), probs2)

            plt.hist(probs2, label=class_names[bkg_class], bins=np.linspace(min_prob,max_prob,nbins), alpha=0.4)
            # And turn into ROC
            r, e = calc_roc(h1, h2)
            rocs.append(r)


        plt.xlabel("classifier response", fontsize=16)
        plt.ylabel("entries", fontsize=16)
        plt.legend(loc=1)
        plt.xlim(min_prob,max_prob)
        plt.show()
        plt.savefig(clf.name + "-" + str(sig_class) + "-proba.png")

        plt.clf()
        
        # Add the ROCs
        plt.yscale('log')
        for r,bkg_class in zip(rocs, other_classes):
            plt.plot(r[:, 0], r[:, 1], label=class_names[sig_class] + " vs " +class_names[bkg_class], lw=1, ls="--")

        if sig_class == 1:
            sig = rocs[0][:, 0]
            bkg = rocs[0][:, 1]

            # Integrate:
            # bin width * value at left edge
            integral = 0
            for left_edge, right_edge, y in zip(sig[:-1],sig[1:],bkg[:-1]):
                integral += abs(right_edge-left_edge) * y

            print "Area under ROC:", integral

            roc_out = open("roc.txt", "w")
            roc_out.write(str(integral) + "\n")
            roc_out.close()

        # Setup nicely
        plt.legend(loc=2)
        plt.xlabel( class_names[sig_class] + " match efficiency", fontsize=16)
        plt.ylabel("fake match efficiency", fontsize=16)
        plt.legend(loc=2)
        plt.xlim(0,1)
        plt.ylim(0,1)

        plt.show()
        plt.savefig(clf.name + "-" + str(sig_class) + "-ROC.png")


########################################
# Helper: multirocplot
########################################

def multirocplot(clfs, tmp_df, logy=True):

    df = tmp_df.copy()

    plt.clf()
    if logy:
        plt.yscale('log')
    else:
        plt.yscale('linear')
        
    sig_class = 1
    bkg_class = 0
    
    nbins = 100
    min_prob = 0
    max_prob = 1    

    rocs = []

    for clf in clfs:
        
        # TODO: rewrite to use datagen
        X_test = clf.get_data(df)
        df["proba_" + clf.plot_name] = clf.model.predict_proba(X_test)[:,sig_class]

        # Signal Efficiency
        sig = df["is_signal_new"]==sig_class
        probs1 = df[sig]["proba_" + clf.plot_name].values
        h1 = make_df_hist((nbins*5,min_prob,max_prob), probs1)
        
        # Background efficiency
        bkg = df["is_signal_new"]==bkg_class
        probs2 = df[bkg]["proba_" + clf.plot_name].values
        h2 = make_df_hist((nbins*5,min_prob,max_prob), probs2)

        # And turn into ROC
        r, e = calc_roc(h1, h2)
        rocs.append(r)
        
        plt.plot(r[:, 0], r[:, 1], label=clf.plot_name, lw=1, ls="--")

    # Setup nicely
    plt.legend(loc=2)
    plt.xlabel("true top match efficiency", fontsize=16)
    plt.ylabel("fake match efficiency", fontsize=16)
    plt.legend(loc=2)
    plt.xlim(0,1)
    plt.ylim(0,1)

    plt.show()
    plt.savefig("All-ROC.png")


########################################
# Helper: datagen
########################################

def datagen(sel, brs, infname_sig, infname_bkg, n_batches=10):

    f_sig = ROOT.TFile.Open(infname_sig)
    sig_entries = f_sig.Get("tree").GetEntries()
    f_sig.Close()

    f_bkg = ROOT.TFile.Open(infname_bkg)
    bkg_entries = f_bkg.Get("tree").GetEntries()
    f_bkg.Close()

    # Initialize
    step_sig = sig_entries/n_batches
    step_bkg = bkg_entries/n_batches

    i_start_sig = 0
    i_start_bkg = 0        

    # Generate data forever
    while True:
        
        d_sig = root_numpy.root2rec(infname_sig, branches=brs, selection = sel, start=i_start_sig, stop = i_start_sig + step_sig)
        d_bkg = root_numpy.root2rec(infname_bkg, branches=brs, selection = sel, start=i_start_bkg, stop = i_start_bkg + step_bkg)

        i_start_sig += step_sig
        i_start_bkg += step_bkg
        # roll over
        if ((i_start_sig + step_sig >= sig_entries) or 
            (i_start_bkg + step_bkg >= bkg_entries)):
            i_start_sig = 0
            i_start_bkg = 0
        
        df_sig = pandas.DataFrame(d_sig)    
        df_sig["is_signal_new"] = 1

        df_bkg = pandas.DataFrame(d_bkg)    
        df_bkg["is_signal_new"] = 0

        df = pandas.concat([df_sig, df_bkg], ignore_index=True)
                    
        # Shuffle
        df = df.iloc[np.random.permutation(len(df))]
    
        yield df


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
