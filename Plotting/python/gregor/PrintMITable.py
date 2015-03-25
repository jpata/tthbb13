import pickle

input_filename = "pt-300-to-470_interesting_v37_mi.pickle"

f = open(input_filename, "r")

m = pickle.load(f)

keys = [
    'ca15trimmedr2f6forbtag_btag',
    'ca15trimmedr2f6_mass', 
    'ca15softdropz15b10_mass',     
    'ca15softdropz30b15_mass', 
    'ca15_tau3/ca15_tau2',
    'looseMultiRHTT_mass',
    'looseMultiRHTT_fW',
    'looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected',
]




key_btag = 'ca15trimmedr2f6forbtag_btag'

for key in keys:

    try:
        v = m[key][key_btag]
    except:
        v = m[key_btag][key]
    
    print "{0} {1:.2f} {2:.2f}".format(key, m[key][key],v)
