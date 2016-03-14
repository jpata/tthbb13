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
# Configuration
########################################

brs = ["evt", 
       "pt", "eta", "top_size", 
       "ak08_pt",
       "ak08_tau3", "ak08_tau2",
       "ak08softdropz10b00forbtag_btag", 
       "ak08softdropz10b00_mass",
       "ak08_emap", 
       #"ak08_ptmap", 
       #"ak08_massmap", 
       #"ak08_chargemap"
]

to_plot = ["pt", "eta", "top_size", 
           "ak08_tau3", "ak08_tau2",
           "ak08softdropz10b00forbtag_btag", 
           "ak08softdropz10b00_mass"]

# 1D
# default_mdl = {        
#     "n_layers"    : 1,
#     "n_nodes"     : 512,
#     "dropout"     : 0.3,
# 
#     "lr"          : 0.01,
#     "decay"       : 1e-6,
#     "momentum"    : 0.9,            
# 
#     "nb_epoch"    : 50,
# }


default_mdl = {        
    "n_blocks" : 2,    

    "n_conv_layers" : 2,        
    "conv_nfeat" : 1,
    "conv_size"  : 4,

    "pool_size"  : 2,

    "n_dense_layers" : 2,
    "n_dense_nodes"  : 16,

    "lr"          : 0.01,
    "decay"       : 1e-6,
    "momentum"    : 0.9,            

    "nb_epoch"    : 50,
}

colors = ['black', 'red','blue','green','orange','green','magenta']

class_names = {0: "background",
               1: "signal"}

classes = sorted(class_names.keys())

plot_inputs    = False

min_pt = 801
max_pt = 999
max_eta = 1.5
min_reco_pt = 500

infname_sig = "ntop_x1_zprime_m2000-tagging-weighted.root"
infname_bkg = "ntop_x1_qcd_800_1000-tagging-weighted.root"


########################################
# Prepare Data
########################################

# Get signal events
d_sig = root_numpy.root2rec(infname_sig, branches=brs)
df_sig = pandas.DataFrame(d_sig)    
df_sig["is_signal_new"] = 1

# Get background events
d_bkg = root_numpy.root2rec(infname_bkg, branches=brs)
df_bkg = pandas.DataFrame(d_bkg)    
df_bkg["is_signal_new"] = 0

print "Reading Data: Done..."

# Combine
df_tmp = pandas.concat([df_sig, df_bkg], ignore_index=True)

# Apply fiducial
df_tmp["keep"] = np.where( df_tmp["pt"] > min_pt, True, False)
df_tmp["keep"] = np.where( df_tmp["pt"] < max_pt, df_tmp["keep"], False)
df_tmp["keep"] = np.where( abs(df_tmp["eta"]) < max_eta, df_tmp["keep"], False)
df_tmp["keep"] = np.where( df_tmp["ak08_pt"] > min_reco_pt, df_tmp["keep"], False)
df_tmp["keep"] = np.where( df_tmp["ak08softdropz10b00_mass"] >= 0., df_tmp["keep"], False)
df_tmp["keep"] = np.where( df_tmp["ak08softdropz10b00forbtag_btag"] >= 0., df_tmp["keep"], False)
df_tmp["keep"] = np.where( len(df_tmp["ak08_emap"]) > 0., df_tmp["keep"], False)

df = df_tmp[df_tmp["keep"]==True]

# Shuffle
df = df.iloc[np.random.permutation(len(df))]

# Split into test and training
dtrain = df[df["evt"] % 4 == 1]
dtest  = df[df["evt"] % 4 == 3]

print "\nTraining Sample:"
print dtrain.groupby('is_signal_new')["is_signal_new"].count()
print "\nTest Sample:"
print dtest.groupby('is_signal_new')["is_signal_new"].count()
    
print "Preparing Data: Done..."


########################################
# Read in NN parameters
########################################

mdl = {}
for param in default_mdl.keys():

    if param in os.environ.keys():

        cls = default_mdl[param].__class__
        value = cls(os.environ[param])
        mdl[param] = value
        print "Setting ", param, value
    else:
        mdl[param] = default_mdl[param]

    for k,v in mdl.iteritems():
        print k,v


########################################
# Classifiers
########################################

def get_data_vars(df, varlist):        
    return df[varlist].values

def get_data_flatten(df, varlist):
    
    # tmp is a 1d-array of 1d-arrays
    # so we need to convert it to 2d array
    tmp = df[varlist].values.flatten() # 
    ret = np.vstack([tmp[i] for i in xrange(len(tmp))])
     
    return ret 


# TODO: make more elegant, interface properly
# Also prepare a scaler
scaler = StandardScaler()  
scaler.fit(get_data_flatten(dtrain, ["ak08_emap"]))

def get_data_emap(df, varlist):
    return scaler.transform(get_data_flatten(df, varlist))

def get_data_emap_2d(df, varlist):
    tmp  = get_data_emap(df, varlist)
    tmp2 =  np.expand_dims(tmp, axis=-1)
    n_lines = tmp2.shape[0]
    tmp3 = tmp2.reshape(n_lines, 16, 16)
    tmp4 = np.expand_dims(tmp3, axis=1)    

    print tmp.shape
    print tmp2.shape
    print tmp3.shape
    print tmp4.shape

    return tmp4


classifiers = {

    "BDT" : ["scikit", 
             ["ak08_tau3", "ak08_tau2", "ak08softdropz10b00forbtag_btag", "ak08softdropz10b00_mass"],            
             GradientBoostingClassifier(
                 n_estimators=200,
                 learning_rate=0.1,
                 max_leaf_nodes = 6,
                 min_samples_split=1,
                 min_samples_leaf=1,
                 subsample=0.8,
                 verbose = True,
             ),
             True,
             get_data_vars,
         ],

    "BDT-nob" : ["scikit", 
                 ["ak08_tau3", "ak08_tau2", "ak08softdropz10b00_mass"],            
                 GradientBoostingClassifier(
                     n_estimators=200,
                     learning_rate=0.1,
                     max_leaf_nodes = 6,
                     min_samples_split=1,
                     min_samples_leaf=1,
                     subsample=0.8,
                     verbose = True,
                 ),
                 True,
                 get_data_vars,
             ],

#    "NN" : ["keras",
#            ["ak08_emap"],
#            mdl,
#            False,
#            get_data_emap
#        ],

    "NN2d" : ["keras",
              ["ak08_emap"],
              mdl,
              False,
              get_data_emap_2d
        ],
    
}


########################################
# Helper: train_scitkit
########################################

def train_scikit(df, var, clf, get_data):

    df_shuf = df.iloc[np.random.permutation(np.arange(len(df)))]

    X = get_data(df_shuf,var)
    y = df_shuf["is_signal_new"].values

    clf.fit(X, y)
    clf.varlist = var

    return clf


########################################
# Helper: train_keras
########################################

def train_keras(df_train, df_val, var, mdl, get_data):

    print "Starting train_keras with the parameters: ",
    for k,v in mdl.iteritems():
        print k,v

    channels = 1
    nclasses = 2
    
    X_train = get_data(df_train, var)
    X_val   = get_data(df_val, var)
 
    y_train = df_train["is_signal_new"].values
    y_val   = df_val["is_signal_new"].values
 
    activ = lambda : Activation('relu')



# 1D Model 

#    model = Sequential()
#
#    model.add(Dense(mdl["n_nodes"], input_dim = 256))
#    model.add(activ())
#    model.add(Dropout(mdl["dropout"]))
#
#    for ilayer in range(mdl["n_layers"]):  
#        model.add(Dense(mdl["n_nodes"]))
#        model.add(activ())                   
#        model.add(Dropout(mdl["dropout"]))
#
#    model.add(Dense(nclasses))
#    model.add(Activation('softmax'))
#
#    sgd = SGD(lr=mdl["lr"], 
#              decay=mdl["decay"], 
#              momentum=mdl["momentum"], 
#              nesterov=True)
#    model.compile(loss='mean_squared_error', optimizer=sgd)
#
#    ret = model.fit(X_train, 
#                    np_utils.to_categorical(y_train), 
#                    nb_epoch = mdl["nb_epoch"],
#                    verbose=2, 
#                    validation_data=(X_val, np_utils.to_categorical(y_val)),
#                    show_accuracy=True)


    model = Sequential()

    for i_block in range(mdl["n_blocks"]):
        for i_conv_layer in range(mdl["n_conv_layers"]):

            if i_conv_layer == 0 and i_block ==0:
                model.add(ZeroPadding2D(padding=(1, 1), input_shape=(1, 16, 16)))
            else:
                model.add(ZeroPadding2D(padding=(1, 1)))

            model.add(Convolution2D(mdl["conv_nfeat"],
                                    mdl["conv_size" ], 
                                    mdl["conv_size" ]))
            model.add(activ())
        
        if mdl["pool_size"] > 0:
            model.add(MaxPooling2D(pool_size=(mdl["pool_size"], mdl["pool_size"])))

    model.add(Flatten())

    for i_dense_layer in range(mdl["n_dense_layers"]):
        model.add(Dense(mdl["n_dense_nodes"]))
        model.add(activ())    

    model.add(Dense(nclasses))
    model.add(Activation('softmax'))

    sgd = SGD(lr = mdl["lr"], 
              decay = mdl["decay"], 
              momentum = mdl["momentum"], 
              nesterov=True)
    model.compile(loss='mean_squared_error', optimizer=sgd)
                
    ret = model.fit(X_train, 
                    np_utils.to_categorical(y_train), 
                    nb_epoch = mdl["nb_epoch"],
                    verbose=2, 
                    validation_data=(X_val, np_utils.to_categorical(y_val)),
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
            
    model.varlist = var
 
    return model

    
########################################
# Helper: rocplot
########################################

def rocplot(name, clf, tmp_df, classes, class_names, get_data):

    # Predict all probabilities

    X_test = get_data(tmp_df,clf.varlist)
    all_probs = clf.predict_proba(X_test)    

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
        plt.savefig(name + "-" + str(sig_class) + "-proba.png")

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
        plt.savefig(name + "-" + str(sig_class) + "-ROC.png")



def multirocplot(names, 
                 clfs, 
                 get_datas,
                 tmp_df):

    df = tmp_df.copy()

    plt.clf()
    plt.yscale('log')

    sig_class = 1
    bkg_class = 0
    
    nbins = 100
    min_prob = 0
    max_prob = 1    

    rocs = []

    for name, clf, get_data in zip(names, clfs, get_datas):
        
        X_test = get_data(df, clf.varlist)
        df["proba_" + name] = clf.predict_proba(X_test)[:,sig_class]

        # Signal Efficiency
        sig = df["is_signal_new"]==sig_class
        probs1 = df[sig]["proba_" + name].values
        h1 = make_df_hist((nbins*5,min_prob,max_prob), probs1)
        
        # Background efficiency
        bkg = df["is_signal_new"]==bkg_class
        probs2 = df[bkg]["proba_" + name].values
        h2 = make_df_hist((nbins*5,min_prob,max_prob), probs2)

        # And turn into ROC
        r, e = calc_roc(h1, h2)
        rocs.append(r)
        
        plt.plot(r[:, 0], r[:, 1], label=name, lw=1, ls="--")

    # Setup nicely
    plt.legend(loc=2)
    plt.xlabel("true top match efficiency", fontsize=16)
    plt.ylabel("fake match efficiency", fontsize=16)
    plt.legend(loc=2)
    plt.xlim(0,1)
    plt.ylim(0,1)

    plt.show()
    plt.savefig("All-ROC.png")


def prepare(name, backend, variables, classifier, get_data, load_from_file):

    if not load_from_file:
        if backend == "scikit":
            clf = train_scikit(dtrain, variables, classifier, get_data)
        elif backend == "keras":
            clf = train_keras(dtrain, dtest, variables, classifier, get_data)
    else:
        if backend == "scikit":
            f = open(name + ".pickle", "r")
            clf = pickle.load(f)
            f.close()
            print "Loading from file: Done..."
        elif backend == "keras":
            #f = open(name + ".yaml", "r")
            #model = model_from_yaml(yaml_string)
            print "Sorry, can't load keras from file yet"
            clf = None

    return clf


########################################
# Plot inputs
########################################

if plot_inputs:
    
    # 1D Variables
    for br in to_plot:

        xmin = min(df[br])
        xmax = max(df[br])

        plt.clf()

        for cls in classes:
            plt.hist(df.loc[df["is_signal_new"]==cls,br].as_matrix(),
                     color=colors[cls+1], 
                     bins=np.linspace(xmin,xmax,50),
                     normed=True, 
                     alpha=0.4,
                     label = class_names[cls]
            )    
        
        plt.savefig("input_{0}.png".format(br))

    print "Plotting 1D inputs: Done..."

    # 2D maps
    
    X = get_data_emap(dtrain, ["ak08_emap"])

    for idx in range(20):
        map_1d = X[idx]
        map_2d = map_1d.reshape(16,16)

        plt.clf()

        plt.imshow(map_2d, interpolation = 'spline36')
        #plt.colorbar(map_2d)
        plt.savefig("maps/{0}_{1}.png".format("emap", idx))

    print "Plotting 2D inputs: Done..."




# Handle all classifiers
#for k,v in classifiers.iteritems():
if False:

    print "Doing: ", k

    backend        = v[0]
    variables      = v[1]
    classifier     = v[2]
    load_from_file = v[3]
    get_data       = v[4]

    clf =  prepare(k, variables, classifier, get_data, load_from_file)
        
    rocplot(k, clf, dtest, classes, class_names, get_data)

    # And store    
    if not load_from_file:
        if backend == "scikit":
            f = open(k + ".pickle","wb")
            pickle.dump(clf, f)
            f.close()
        elif backend == "keras":            
            model_out = open(k + ".yaml", "w")
            model_out.write(clf.to_yaml())
            model_out.close()
            
all_names = classifiers.keys()

multirocplot([n for n in all_names],
             [prepare(n, 
                      classifiers[n][0], 
                      classifiers[n][1], 
                      classifiers[n][2], 
                      classifiers[n][4], 
                      classifiers[n][3]) for n in all_names],
             [classifiers[n][4] for n in all_names],
             dtest)

 






