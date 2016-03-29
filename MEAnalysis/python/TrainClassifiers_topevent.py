########################################
# Imports
########################################

from TrainClassifiersBase import *


########################################
# Configuration
########################################

MAX_PERM=20

brs = ["evt", "good_perm_in_event", "good_perm_in_first_n"]

for ic in range(MAX_PERM):
    brs.extend(["c{0}_mass".format(ic), 
                "c{0}_frec".format(ic), 
                "c{0}_meanCSV".format(ic), 
                "c{0}_varCSV".format(ic)])

train_vars = []
for ic in range(MAX_PERM):
    train_vars.extend(["c{0}_mass".format(ic), 
                       "c{0}_frec".format(ic), 
                       "c{0}_meanCSV".format(ic), 
                       "c{0}_varCSV".format(ic)])

colors = ['black', 'red','blue','green','orange','green','magenta']

class_names = {0: "no top",
               1: "top in event"}

plot_inputs = False

default_params = {        

    # Parameters for 1d architecture    
    # "n_dense_layers" : 2,
    # "n_dense_nodes"  : 80,
    # "dense_dropout"  : 0.2,


    # Parameters for 2d architecture    
    "n_blocks"       : 2,    
    "n_conv_layers"  : 2,        
    "pool_size"      : 0,
    "n_dense_layers" : 1,
    "n_dense_nodes"  : 20,
    "n_features"     : 8,
    "do_reshape"     : 0,
    "dense_dropout"  : 0.2,
    "conv_dropout"   : 0.2,

    # Common parameters
    "lr"          : 0.01,
    "decay"       : 1e-6,
    "momentum"    : 0.9,            
    "nb_epoch"    : 10,
}


infname = "ttHTobb_M125_13TeV_powheg_pythia8.root"


########################################
# Prepare Data
########################################

d = root_numpy.root2rec(infname, branches=brs, treename="topevent")
df = pandas.DataFrame(d)    

# Shuffle
df = df.iloc[np.random.permutation(len(df))]


# Remove cat -1 and shuffle
df = df.iloc[np.random.permutation(len(df))]

df["is_signal_new"] = df["good_perm_in_event"]

print df.shape
print df.groupby('is_signal_new')["is_signal_new"].count()

classes = np.unique(df["is_signal_new"].values).tolist()

dtrain = df[df["evt"] % 4 == 1]
dtest  = df[df["evt"] % 4 == 3]
    
print "Training Sample:"
print dtrain.groupby('is_signal_new')["is_signal_new"].count()
print "Test Sample:"
print dtest.groupby('is_signal_new')["is_signal_new"].count()
    
print "Preparing Data: Done..."


########################################
# Read in parameters
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

def get_data_flat_unscaled(df):
    arr = np.array([df[["c{0}_mass".format(ic), 
                        "c{0}_frec".format(ic), 
                        "c{0}_meanCSV".format(ic), 
                        "c{0}_varCSV".format(ic)]].values for ic in range(MAX_PERM)])        
    return np.reshape( np.swapaxes( np.swapaxes(arr,0,1), 1,2), (-1, 80))


# Also prepare a scaler
scaler = StandardScaler()  
scaler.fit(get_data_flat_unscaled(df))

def get_data_flat(df):
    return scaler.transform(get_data_flat_unscaled(df))

def get_data_2d(df):
    return np.expand_dims(scaler.transform(get_data_flat_unscaled(df)).reshape(-1, 4, 20), axis=1)


def model_2dconv(params):

    activ = lambda : Activation('relu')

    model = Sequential()

    current_rows = 4

    # 2D Convolutional Model
    for i_block in range(params["n_blocks"]):
        for i_conv_layer in range(params["n_conv_layers"]):

            if i_conv_layer == 0 and i_block == 0:
                model.add(Convolution2D(params["n_features"], current_rows,1, input_shape=(1, 4, 20)))
            else:
                model.add(Convolution2D(params["n_features"], current_rows,1))

            if params["conv_dropout"] > 0.:         
                model.add(Dropout(params["conv_dropout"]))

            model.add(activ())
            
            if params["do_reshape"]:
                model.add(Reshape((1,params["n_features"],20)))                
                current_rows = params["n_features"]
            else:
                current_rows = 1

        if params["pool_size"] > 0:
            model.add(MaxPooling2D(pool_size=(params["pool_size"], 1)))
            current_rows /= params["pool_size"]
            
    model.add(Flatten())

    for i_dense_layer in range(params["n_dense_layers"]):
        model.add(Dense(params["n_dense_nodes"]))
        
        if params["dense_dropout"] > 0.:         
            model.add(Dropout(params["dense_dropout"]))

        model.add(activ())    

    model.add(Dense(2))
    model.add(Activation('softmax'))

    return model


def model_1d(params):

    activ = lambda : Activation('relu')
    model = Sequential()

    for i_dense_layer in range(params["n_dense_layers"]):
        if i_dense_layer == 0:
            model.add(Dense(params["n_dense_nodes"], input_dim = 80))
        else:
            model.add(Dense(params["n_dense_nodes"]))
        model.add(Dropout(params["dense_dropout"]))
        model.add(activ())    

    model.add(Dense(2))
    model.add(Activation('softmax'))

    return model


classifiers = [
    Classifier("NN", 
               "keras",              
               params,
               False,
               get_data_2d,
               model_2dconv(params)
           )]


########################################
# Train/Load classifiers and make ROCs
########################################

# firstiiter: 4 features, reshaping
# second-iter: different features, also test wo/ reshaping
# third-iter: 1d test
# fourth-iter: bigger 1d test
# fifth-iter: 2d network parameter tuning
# sixth-tier: 2d mostly fixed network, play with learning setting

[clf.prepare(dtrain, dtest) for clf in classifiers]
[rocplot(clf, dtest, classes, class_names) for clf in classifiers]
multirocplot(classifiers, dtest, False)



