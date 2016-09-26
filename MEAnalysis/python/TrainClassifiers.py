########################################
# Imports
########################################

from TrainClassifiersBase import *

########################################
# Configuration
########################################


# All branches to load from file
brs = [#"l_pt", "l_eta", "l_phi", "l_pdgid",
       #"met_pt", "met_phi",
       #"j0_pt", "j0_eta", "j0_phi", "j0_mass", "j0_btagCSV", 
       #"j1_pt", "j1_eta", "j1_phi", "j1_mass", "j1_btagCSV", 
       #"j2_pt", "j2_eta", "j2_phi", "j2_mass", "j2_btagCSV", 
       #"j3_pt", "j3_eta", "j3_phi", "j3_mass", "j3_btagCSV", 
       #"j4_pt", "j4_eta", "j4_phi", "j4_mass", "j4_btagCSV", 
       #"j5_pt", "j5_eta", "j5_phi", "j5_mass", "j5_btagCSV", 

"j0_btagCSV",     
"j1_btagCSV",     
"j2_btagCSV",     
"j3_btagCSV",     
"j4_btagCSV",     
"j5_btagCSV",     
"blr",


       "tt_class", "evt",       
]

# Variables to feed to BDT
input_vars = [    

#   "j0_pt", "j0_eta",  "j0_mass",     "j0_btagCSV",     
#   "j1_pt", "j1_eta",  "j1_mass",     "j1_btagCSV",     
#   "j2_pt", "j2_eta",  "j2_mass",     "j2_btagCSV",     
#   "j3_pt", "j3_eta",  "j3_mass",     "j3_btagCSV",     
#   "j4_pt", "j4_eta",  "j4_mass",     "j4_btagCSV",     
#   "j5_pt", "j5_eta",  "j5_mass",     "j5_btagCSV",     

"j0_btagCSV",     
"j1_btagCSV",     
"j2_btagCSV",     
"j3_btagCSV",     
"j4_btagCSV",     
"j5_btagCSV",     
"blr",

]
              

default_params = {        

    # Common parameters

    "n_chunks"          : 1,

    "n_estimators"   : 100,
    #"max_depth"      : 2, 
    "max_leaf_nodes" : 3,
    "learning_rate"  : 0.05,    
    "subsample"      : 0.8,     
    "verbose"        : 2,    

    "samples_per_epoch" : None, # later filled from input files
}

# Madgraph :
infname_train = "/mnt/t3nfs01/data01/shome/gregor/tth/gc/mvatuple/v6/out_madgraph.root" 
# Powheg:
infname_test = "/mnt/t3nfs01/data01/shome/gregor/tth/gc/mvatuple/v6/out_powheg.root"

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
# Count effective training samples
########################################

# We want to know the "real" number of training samples
# This is a bit tricky as we read the file in "chunks" and then divide each chunk into "batches"
# both operations might loose a few events at the end
# So we actually do this procedure on a "cheap" branch

n_train_samples = 0 
# Loop over signal and background sample

# get the number of events in the root file so we can determin the chunk size
rf = ROOT.TFile.Open(infname_train)
print rf
entries = rf.Get("multiclass_6j").GetEntries()
rf.Close()

step = entries/params["n_chunks"]    
i_start = 0

# Loop over chunks from file
for i_chunk in range(params["n_chunks"]):

    # get the samples in this chunk that survive the fiducial selection + training sample selection
    n_samples = len(root_numpy.root2array(infname_train, treename="multiclass_6j", branches=["evt"], start=i_start, stop=i_start+step).view(np.recarray))

    # round to batch_size
    n_train_samples += n_samples
    i_start += step

print "Total number of training samples = ", n_train_samples
params["samples_per_epoch"] = n_train_samples



########################################
# Prepare data and scalers
########################################

datagen_train = datagen("(1)", brs, infname_train, n_chunks=params["n_chunks"])
datagen_test  = datagen("(1)", brs, infname_test, n_chunks=params["n_chunks"])

# This function produces the necessary shape for MVA training/evaluation
# (batch_size,1,40,40)
# However it uses the raw values in the image
# If we want a rescaled one, use to_image_scaled 
def to_image(df):
    return df[input_vars].values


def model(params):

    classif =GradientBoostingClassifier(
        n_estimators  = params["n_estimators"],   
        max_leaf_nodes = params["max_leaf_nodes"],      
        learning_rate = params["learning_rate"],  
        subsample     = params["subsample"],      
        verbose       = params["verbose"],        
    )

    return classif



classifiers = [
    Classifier("BDT", 
               "scikit",
               params,
               True,
               datagen_train,
               datagen_test,               
               model(params),
               image_fun = to_image,               
               class_names = {
#                   0: "ttb", 
#                   1: "tt2b",
#                   2: "ttbb",
#                   3: "ttcc",
#                   4: "ttll",

                   0: "rest", 
                   1: "ttbb",

               },
               input_vars = input_vars
               )    
]




########################################
# Train/Load classifiers and make ROCs
########################################

[clf.prepare() for clf in classifiers]
[analyze(clf) for clf in classifiers]


 




