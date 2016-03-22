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



classifiers = [
    Classifier("NN", 
               "keras",              
               {},
               True,
               get_data_flat,
               None,
               inpath = "/shome/gregor/tth/gc/best-topevent/1d",
               plot_name = "1d NN"
           ),
    Classifier("NN", 
               "keras",              
               params = {},
               load_from_file = True,
               get_data = get_data_2d,
               model = None,
               inpath = "/shome/gregor/tth/gc/best-topevent/conv",
               plot_name = "Conv NN"
           ),
    Classifier("NN", 
               "keras",              
               params = {},
               load_from_file = True,
               get_data = get_data_2d,
               model = None,
               inpath = "/shome/gregor/tth/gc/GC12603af43460/907",
               plot_name = "Conv NN v2"
           ),

]


########################################
# Train/Load classifiers and make ROCs
########################################

[clf.prepare(dtrain, dtest) for clf in classifiers]
multirocplot(classifiers, dtest, False)



