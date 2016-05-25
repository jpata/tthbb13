import sys

f1 = "KIT_1kEvents_NoSubSel_2016-05-19-1521.csv"
f2 = "out.txt"


col_event = 2

header1 =  open(f1).readline().strip()
header2 =  open(f2).readline().strip()

if not header1 == header2:
    print "Headers do not agree. Exiting.."

    print header1
    print "  "
    print header2

    sys.exit()



test_vars = [

    "run","lumi","event",
    #"is_SL",
    #"lep1_pt","lep1_eta","lep1_phi","lep1_iso","lep1_pdgId",
    #"n_jets","n_btags",
    #"jet1_pt","jet2_pt","jet3_pt","jet4_pt","jet1_CSVv2","jet2_CSVv2","jet3_CSVv2","jet4_CSVv2",
"n_fatjets","pt_fatjet_1","pt_fatjet_2","eta_fatjet_1","eta_fatjet_2","pt_nonW_1","pt_nonW_2","pt_W1_1","pt_W1_2","pt_W2_1","pt_W2_2","csv_nonW_1","csv_nonW_2","csv_W1_1","csv_W1_2","csv_W2_1","csv_W2_2","pt_top_1","pt_top_2","eta_top_1","eta_top_2","m_top_1","m_top_2","pt_sf_filterjet1_1","pt_sf_filterjet1_2","pt_sf_filterjet2_1","pt_sf_filterjet2_2","pt_sf_filterjet3_1","pt_sf_filterjet3_2","csv_sf_filterjet1_1","csv_sf_filterjet1_2","csv_sf_filterjet2_1","csv_sf_filterjet2_2","csv_sf_filterjet3_1","csv_sf_filterjet3_2","pt_pruned_subjet1_1","pt_pruned_subjet1_2","pt_pruned_subjet2_1","pt_pruned_subjet2_2","csv_pruned_subjet1_1","csv_pruned_subjet1_2","csv_pruned_subjet2_1","csv_pruned_subjet2_2","pt_sd_subjet1_1","pt_sd_subjet1_2","pt_sd_subjet2_1","pt_sd_subjet2_2","csv_sd_subjet1_1","csv_sd_subjet1_2","csv_sd_subjet2_1","csv_sd_subjet2_2","pt_sdz2b1_subjet1_1","pt_sdz2b1_subjet1_2","pt_sdz2b1_subjet2_1","pt_sdz2b1_subjet2_2","csv_sdz2b1_subjet1_1","csv_sdz2b1_subjet1_2","csv_sdz2b1_subjet2_1","csv_sdz2b1_subjet2_2",

#    #"pt_fatjet_1", "pt_fatjet_2",
#    #"pt_top_1", "pt_top_2",
#    #"m_top_1", "m_top_2",
#    #"pt_nonW_1","pt_nonW_2", "pt_W1_1","pt_W1_2", "pt_W2_1","pt_W2_2",
#    #"csv_nonW_1", "csv_nonW_2","csv_W1_1","csv_W1_2","csv_W2_1","csv_W2_2",
#
#    #"pt_pruned_subjet1_1", "pt_pruned_subjet1_2", "pt_pruned_subjet2_1", "pt_pruned_subjet2_2",    
#    #"pt_sd_subjet1_1", "pt_sd_subjet1_2", "pt_sd_subjet2_1", "pt_sd_subjet2_2",    
#    #"pt_sdz2b1_subjet1_1", "pt_sdz2b1_subjet1_2", "pt_sdz2b1_subjet2_1", "pt_sdz2b1_subjet2_2",    
#
#    #"csv_pruned_subjet1_1", "csv_pruned_subjet1_2", "csv_pruned_subjet2_1", "csv_pruned_subjet2_2",    
#    #"csv_sd_subjet1_1", "csv_sd_subjet1_2", "csv_sd_subjet2_1", "csv_sd_subjet2_2",    
#    #"csv_sdz2b1_subjet1_1", "csv_sdz2b1_subjet1_2", "csv_sdz2b1_subjet2_1", "csv_sdz2b1_subjet2_2",    
#
#    #"pt_sf_filterjet1_1", 
#    #"pt_sf_filterjet1_2", 
#    #"pt_sf_filterjet2_1", 
#    #"pt_sf_filterjet2_2",     
#    #"pt_sf_filterjet3_1", 
#    #"pt_sf_filterjet3_2", 
#
#    "csv_sf_filterjet1_1", 
#    "csv_sf_filterjet1_2", 
#    "csv_sf_filterjet2_1", 
#    "csv_sf_filterjet2_2",     
#    "csv_sf_filterjet3_1", 
#    "csv_sf_filterjet3_2", 


    ]

cols = {v:header1.split(",").index(v) for v in test_vars}


events_1 = [l.split(",")[col_event] for l in open(f1)]
events_2 = [l.split(",")[col_event] for l in open(f2)]

events_1 = [ x for x in events_1 if not x=="event"]
events_2 = [ x for x in events_2 if not x=="event"]

# Get list of events from both sources
events = list(set(events_1) & set(events_2))

header = "{0: >6} ".format("event")
for var in test_vars:
    header += "{0: >10} {1: >10} {2: >8} ".format("kit_"+var, "eth_"+var, "good?")

print header

for line1 in open(f1):

    atoms1 = line1.split(",")
    
    evt = atoms1[col_event]
    
    if not evt in events:
        continue
    
    for line2 in open(f2):

        atoms2 = line2.split(",")
        
        if not atoms2[col_event] == evt:
            continue

        output = "{0: >6} ".format(evt)
        
        for var in test_vars:
            output += "{0: >10} {1: >10} {2: >8} ".format(atoms1[cols[var]], atoms2[cols[var]], str(atoms1[cols[var]] ==atoms2[cols[var]]))
            
        print output
            
        
    
