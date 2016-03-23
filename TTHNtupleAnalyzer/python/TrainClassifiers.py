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
       "ak08softdropz10b00_masscal",

       "ak08puppi_tau3", "ak08puppi_tau2",
       "ak08puppisoftdropz10b00forbtag_btag", 
       "ak08puppisoftdropz10b00_mass",
       "ak08puppisoftdropz10b00_masscal",

       #"ak08_emap", 
       #"ak08_ptmap", 
       #"ak08_massmap", 
       #"ak08_chargemap"
]

to_plot = [["pt", 800, 1000, "Parton pT [GeV]"],
           ["eta", -3, 3, "Parton eta"],
           ["top_size", 0, 3, "Top Size"],
           ["ak08_tau3_over_tau2",0, 1., "AK08 tau3/tau2"],
           ["ak08softdropz10b00forbtag_btag", 0, 1., "AK08 b-tag discriminator"],
           ["ak08softdropz10b00_mass", 0, 300, "AK08 softdrop mass [GeV]"],
           ["ak08softdropz10b00_masscal", 0, 300, "AK08 softdrop mass [GeV]"],

           ["ak08puppi_tau3_over_tau2",0, 1., "AK08 Puppi tau3/tau2"],
           ["ak08puppisoftdropz10b00forbtag_btag", 0, 1., "AK08 Puppi b-tag discriminator"],
           ["ak08puppisoftdropz10b00_mass", 0, 300, "AK08 Puppi softdrop mass [GeV]"],
           ["ak08puppisoftdropz10b00_masscal", 0, 300, "AK08 Puppi calibrated softdrop mass [GeV]"],
           ]




default_params = {        

    "architecture" : "2dconv",

    # Parameters for 1d architecture
    "1d_n_layers"    : 1,
    "1d_n_nodes"     : 512,
    "1d_dropout"     : 0.3,

    # Parameters for 2d or 3d convolutional architecture    
    "n_blocks"       : 1,    
    "n_conv_layers"  : 2,        
    "conv_nfeat"     : 2,
    "conv_size"      : 4,
    "pool_size"      : 0,
    "n_dense_layers" : 1,
    "n_dense_nodes"  : 8,

    # Common parameters
    "lr"          : 0.01,
    "decay"       : 1e-6,
    "momentum"    : 0.9,            
    "nb_epoch"    : 10,
}

colors = ['black', 'red','blue','green','orange','green','magenta']

class_names = {0: "background",
               1: "signal"}

classes = sorted(class_names.keys())

plot_inputs    = True

min_pt = 801
max_pt = 999
max_eta = 1.5
min_reco_pt = 500

infname_sig = "ntop_x3_zprime_m2000-tagging-weighted.root"
infname_bkg = "ntop_x3_qcd_800_1000-tagging-weighted.root"


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
#df_tmp["keep"] = np.where( df_tmp["ak08softdropz10b00_mass"] >= 0., df_tmp["keep"], False)
#df_tmp["keep"] = np.where( df_tmp["ak08softdropz10b00forbtag_btag"] >= 0., df_tmp["keep"], False)
#df_tmp["keep"] = np.where( len(df_tmp["ak08_emap"]) > 0., df_tmp["keep"], False)

df_tmp["ak08_tau3_over_tau2"] = df_tmp["ak08_tau3"]/df_tmp["ak08_tau2"]
df_tmp["ak08puppi_tau3_over_tau2"] = df_tmp["ak08puppi_tau3"]/df_tmp["ak08puppi_tau2"]

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

params = {}
for param in default_params.keys():

    if param in os.environ.keys():
        cls = default_params[param].__class__
        value = cls(os.environ[param])
        params[param] = value
    else:
        params[param] = default_params[param]

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


#scaler_emap = StandardScaler()  
#scaler_emap.fit(get_data_flatten(dtrain, ["ak08_emap"]))

def get_data_emap(df, varlist):
    return scaler_emap.transform(get_data_flatten(df, varlist))

#scaler_chargemap = StandardScaler()  
#scaler_chargemap.fit(get_data_flatten(dtrain, ["ak08_chargemap"]))

def get_data_chargemap(df, varlist):
    return scaler_chargemap.transform(get_data_flatten(df, varlist))


def get_data_emap_2d(df, varlist):
    tmp  = get_data_emap(df, varlist)
    print tmp.shape
    tmp2 =  np.expand_dims(tmp, axis=-1)
    print tmp2.shape
    n_lines = tmp2.shape[0]
    tmp3 = tmp2.reshape(n_lines, 32, 32)
    print tmp3.shape
    tmp4 = np.expand_dims(tmp3, axis=1)    
    print tmp4.shape
    return tmp4


def get_data_3d(df, varlist):

    emap      = get_data_emap(df, ["ak08_emap"])
    chargemap = get_data_chargemap(df, ["ak08_chargemap"])

    n_lines = len(emap)

    emap_shaped      = np.expand_dims(np.expand_dims(emap,      axis=-1).reshape(n_lines, 32,32), axis=1)
    chargemap_shaped = np.expand_dims(np.expand_dims(chargemap, axis=-1).reshape(n_lines, 32,32), axis=1)

    return np.append(emap_shaped, chargemap_shaped, axis=1)


if params["architecture"] == "2dconv":
    variables = ["ak08_emap"]
    get_data_function = get_data_emap_2d
else:
    variables = ["ak08_emap", "ak08_chargemap"]
    get_data_function = get_data_3d



class Classifier:
    def __init__(self,
                 name,
                 varlist,
                 backend,
                 params,
                 load_from_file,
                 get_data,
                 model=None):
        self.name = name
        self.varlist = varlist
        self.backend = backend
        self.params = params
        self.load_from_file = load_from_file
        self.get_data = get_data
        self.model = model

    def prepare(self):

        if not self.load_from_file:
            if self.backend == "scikit":
                train_scikit(dtrain, self)
            elif self.backend == "keras":
                train_keras(dtrain, dtest, self)
        else:
            if self.backend == "scikit":
                f = open(self.name + ".pickle", "r")
                self.model = pickle.load(f)
                f.close()
            elif self.backend == "keras":
                f = open(self.name + ".yaml", "r")
                yaml_string = f.read()
                f.close()
                self.model = model_from_yaml(yaml_string)                
                self.model.load_weights(self.name + "_weights.h5")
            print "Loading", self.name, "from file: Done..."

classifiers = [

    Classifier("BDT",
               ["ak08_tau3", "ak08_tau2", "ak08softdropz10b00forbtag_btag", "ak08softdropz10b00_mass"],            
               "scikit", 
               {},
               True,
               get_data_vars,
               model = GradientBoostingClassifier(
                   n_estimators=200,
                   learning_rate=0.1,
                   max_leaf_nodes = 6,
                   min_samples_split=1,
                   min_samples_leaf=1,
                   subsample=0.8,
                   verbose = True,
               )),

    Classifier("BDT-nob",
               ["ak08_tau3", "ak08_tau2", "ak08softdropz10b00_mass"],            
               "scikit", 
               {},
               True,
               get_data_vars,                              
               model = GradientBoostingClassifier(
                   n_estimators=200,
                   learning_rate=0.1,
                   max_leaf_nodes = 6,
                   min_samples_split=1,
                   min_samples_leaf=1,
                   subsample=0.8,
                   verbose = True,
                 )),

#    Classifier("NN", 
#               ["ak08_emap"],
#               "keras",              
#               {"architecture" : "1d",
#                "1d_n_layers"    : 1,
#                "1d_n_nodes"     : 100,
#                "1d_dropout"     : 0.3,                   
#                "lr"             : 0.01,
#                "decay"          : 1e-6,
#                "momentum"       : 0.9,            
#                "nb_epoch"       : 10},               
#               True,
#               get_data_emap),
#
    Classifier("NNXd", 
               variables,
               "keras",              
               params,
               False,
               get_data_function)
    
]


########################################
# Helper: train_scitkit
########################################

def train_scikit(df, clf):

    df_shuf = df.iloc[np.random.permutation(np.arange(len(df)))]

    X = clf.get_data(df_shuf,clf.varlist)
    y = df_shuf["is_signal_new"].values

    clf.model.fit(X, y)

    f = open(clf.name + ".pickle","wb")
    pickle.dump(clf.model, f)
    f.close()


########################################
# Helper: train_keras
########################################

def train_keras(df_train, df_val, clf):

    print "Starting train_keras with the parameters: "
    for k,v in clf.params.iteritems():
        print "\t", k,"=",v

    channels = 1
    nclasses = 2
    
    X_train = clf.get_data(df_train, clf.varlist)
    X_val   = clf.get_data(df_val, clf.varlist)
 
    y_train = df_train["is_signal_new"].values
    y_val   = df_val["is_signal_new"].values
 
    activ = lambda : Activation('relu')

    clf.model = Sequential()

    # 1D Model
    if clf.params["architecture"] == "1d":

        clf.model.add(Dense(clf.params["1d_n_nodes"], input_dim = 256))
        clf.model.add(activ())
        clf.model.add(Dropout(clf.params["1d_dropout"]))

        for ilayer in range(clf.params["1d_n_layers"]):  
            clf.model.add(Dense(clf.params["1d_n_nodes"]))
            clf.model.add(activ())                   
            clf.model.add(Dropout(clf.params["1d_dropout"]))

        clf.model.add(Dense(nclasses))
        clf.model.add(Activation('softmax'))

    # 2D Convolutional Model
    elif clf.params["architecture"] == "2dconv":

        for i_block in range(clf.params["n_blocks"]):
            for i_conv_layer in range(clf.params["n_conv_layers"]):

                if i_conv_layer == 0 and i_block ==0:
                    clf.model.add(ZeroPadding2D(padding=(1, 1), input_shape=(1, 32, 32)))
                else:
                    clf.model.add(ZeroPadding2D(padding=(1, 1)))

                clf.model.add(Convolution2D(clf.params["conv_nfeat"],
                                        clf.params["conv_size" ], 
                                        clf.params["conv_size" ]))
                clf.model.add(activ())

            if clf.params["pool_size"] > 0:
                clf.model.add(MaxPooling2D(pool_size=(clf.params["pool_size"], clf.params["pool_size"])))

        clf.model.add(Flatten())

        for i_dense_layer in range(clf.params["n_dense_layers"]):
            clf.model.add(Dense(clf.params["n_dense_nodes"]))
            clf.model.add(activ())    

        clf.model.add(Dense(nclasses))
        clf.model.add(Activation('softmax'))

    # 3D Convolutional Model
    elif clf.params["architecture"] == "3dconv":

        for i_block in range(clf.params["n_blocks"]):
            for i_conv_layer in range(clf.params["n_conv_layers"]):

                if i_conv_layer == 0 and i_block ==0:
                    clf.model.add(ZeroPadding2D(padding=(1, 1), input_shape=(2, 32, 32)))
                else:
                    clf.model.add(ZeroPadding2D(padding=(1, 1)))

                clf.model.add(Convolution2D(clf.params["conv_nfeat"],
                                        clf.params["conv_size" ], 
                                        clf.params["conv_size" ]))
                clf.model.add(activ())

            if clf.params["pool_size"] > 0:
                clf.model.add(MaxPooling2D(pool_size=(clf.params["pool_size"], clf.params["pool_size"])))

        clf.model.add(Flatten())

        for i_dense_layer in range(clf.params["n_dense_layers"]):
            clf.model.add(Dense(clf.params["n_dense_nodes"]))
            clf.model.add(activ())    

        clf.model.add(Dense(nclasses))
        clf.model.add(Activation('softmax'))


    # Prepare model and train
    sgd = SGD(lr = clf.params["lr"], 
              decay = clf.params["decay"], 
              momentum = clf.params["momentum"], 
              nesterov=True)
    clf.model.compile(loss='mean_squared_error', optimizer=sgd)
                
    ret = clf.model.fit(X_train, 
                    np_utils.to_categorical(y_train), 
                    nb_epoch = clf.params["nb_epoch"],
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

    X_test = clf.get_data(tmp_df,clf.varlist)
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

def multirocplot(clfs, tmp_df):

    df = tmp_df.copy()

    plt.clf()
    plt.yscale('log')

    sig_class = 1
    bkg_class = 0
    
    nbins = 100
    min_prob = 0
    max_prob = 1    

    rocs = []

    for clf in clfs:
        
        X_test = clf.get_data(df, clf.varlist)
        df["proba_" + clf.name] = clf.model.predict_proba(X_test)[:,sig_class]

        # Signal Efficiency
        sig = df["is_signal_new"]==sig_class
        probs1 = df[sig]["proba_" + clf.name].values
        h1 = make_df_hist((nbins*5,min_prob,max_prob), probs1)
        
        # Background efficiency
        bkg = df["is_signal_new"]==bkg_class
        probs2 = df[bkg]["proba_" + clf.name].values
        h2 = make_df_hist((nbins*5,min_prob,max_prob), probs2)

        # And turn into ROC
        r, e = calc_roc(h1, h2)
        rocs.append(r)
        
        plt.plot(r[:, 0], r[:, 1], label=clf.name, lw=1, ls="--")

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
# Plot inputs
########################################

if plot_inputs:
    
    # 1D Variables
    for plotvar in to_plot:

        br = plotvar[0]
        xmin = plotvar[1]
        xmax = plotvar[2]
        name = plotvar[3]

        plt.clf()

        for cls in classes:
            plt.hist(df.loc[df["is_signal_new"]==cls,br].as_matrix(),
                     color=colors[cls+1], 
                     bins=np.linspace(xmin,xmax,50),
                     normed=True, 
                     alpha=0.4,
                     label = class_names[cls]
            )    
            
        plt.xlabel(name, fontsize=16)
        plt.ylabel("Fraction of Jets", fontsize=16)
        plt.legend(loc=0)

        plt.savefig("input_{0}.png".format(br))


    for cls in classes:

        plt.clf()
        for i_br, br in enumerate(["ak08softdropz10b00_mass",
                                   "ak08softdropz10b00_masscal", 
                                   "ak08puppisoftdropz10b00_mass",
                                   "ak08puppisoftdropz10b00_masscal"]):
       
            xmin = 0
            xmax = 300
            name = br

            names = {"ak08softdropz10b00_mass"         : "CHS, Uncal.",
                     "ak08softdropz10b00_masscal"      : "CHS, Cal.",
                     "ak08puppisoftdropz10b00_mass"    : "Puppi, Uncal.",
                     "ak08puppisoftdropz10b00_masscal" : "Puppi, Cal.",
                     }

            plt.hist(df.loc[df["is_signal_new"]==cls,br].as_matrix(),
                     color=colors[i_br], 
                     edgecolor = colors[i_br], 
                     bins=np.linspace(xmin,xmax,50),
                     normed=True, 
                     histtype="step",
                     label = names[br]
                )    

        plt.xlabel("Mass [GeV]", fontsize=16)
        plt.ylabel("Fraction of Jets", fontsize=16)
        plt.legend()

        plt.savefig("input_mass_{0}.png".format(cls))


    print "Plotting 1D inputs: Done..."

#    # 2D maps
#    for map_name in ["ak08_emap", "ak08_chargemap"]:
#
#        X = dtrain[map_name].values.flatten()
#
#        for idx in range(20):
#            map_1d = X[idx]
#            map_2d = map_1d.reshape(32,32)
#
#            plt.clf()
#
#            plt.imshow(map_2d, interpolation = 'spline36')
#            #plt.colorbar(map_2d)
#            plt.savefig("maps/{0}_{1}.png".format(map_name, idx))
#
#    print "Plotting 2D inputs: Done..."
#


########################################
# Train/Load classifiers and make ROCs
########################################

#[clf.prepare() for clf in classifiers]
#[rocplot(clf, dtest, classes, class_names) for clf in classifiers]
#multirocplot(classifiers, dtest)

 






