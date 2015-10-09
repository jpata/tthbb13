from Categorize import CategorizationFromString, get_limit

old = """
  S=443.4, B=893181.3, S/sqrt(S+B)=0.47
    numJets__3__4 S=59.5, B=396442.4, S/sqrt(S+B)=0.09
       nBCSVM__2__4 S=59.5, B=396442.4, S/sqrt(S+B)=0.09
          nBCSVM__2__3 S=53.8, B=392793.8, S/sqrt(S+B)=0.09
          nBCSVM__3__4 S=5.7, B=3648.5, S/sqrt(S+B)=0.09
       nBCSVM__4__5 S=0.0, B=0.0, S/sqrt(S+B)=-1.00
    numJets__4__7 S=383.9, B=496738.9, S/sqrt(S+B)=0.54
       numJets__4__5 S=111.6, B=292447.0, S/sqrt(S+B)=0.21
          nBCSVM__2__4 S=109.0, B=292341.6, S/sqrt(S+B)=0.20
             nBCSVM__2__3 S=87.4, B=285937.2, S/sqrt(S+B)=0.16
             nBCSVM__3__4 S=21.6, B=6404.4, S/sqrt(S+B)=0.27
          nBCSVM__4__5 S=2.6, B=105.4, S/sqrt(S+B)=0.25
       numJets__5__7 S=272.3, B=204292.0, S/sqrt(S+B)=0.60
          nBCSVM__2__4 S=247.4, B=203679.2, S/sqrt(S+B)=0.55
             nBCSVM__2__3 S=169.8, B=195202.7, S/sqrt(S+B)=0.38
             nBCSVM__3__4 S=77.7, B=8476.5, S/sqrt(S+B)=0.84
          nBCSVM__4__5 S=24.9, B=612.8, S/sqrt(S+B)=0.99
"""

opt = """(File:  /scratch/gregor/foobar/shapes_iter_9_cats_98.txt )
  S=443.4, B=893181.3, S/sqrt(S+B)=0.47
    btag_LR_4b_2b_logit__m20_0__8_0 S=428.3, B=892902.1, S/sqrt(S+B)=0.45
       nBCSVM__2__3 S=311.0, B=873933.7, S/sqrt(S+B)=0.33
          numJets__3__5 S=141.2, B=678731.0, S/sqrt(S+B)=0.17
          numJets__5__7 S=169.8, B=195202.7, S/sqrt(S+B)=0.38
       nBCSVM__3__5 S=117.4, B=18968.4, S/sqrt(S+B)=0.85
          Wmass__40_0__53_3333333333 S=65.9, B=15117.7, S/sqrt(S+B)=0.53
             btag_LR_4b_2b_logit__m20_0__4_0 S=30.4, B=10403.3, S/sqrt(S+B)=0.30
             btag_LR_4b_2b_logit__4_0__8_0 S=35.5, B=4714.4, S/sqrt(S+B)=0.52
                numJets__3__5 S=14.7, B=3341.3, S/sqrt(S+B)=0.25
                numJets__5__7 S=20.9, B=1373.0, S/sqrt(S+B)=0.56
          Wmass__53_3333333333__120_0 S=51.5, B=3850.7, S/sqrt(S+B)=0.82
             btag_LR_4b_2b_logit__m20_0__4_0 S=21.4, B=2636.4, S/sqrt(S+B)=0.42
             btag_LR_4b_2b_logit__4_0__8_0 S=30.0, B=1214.3, S/sqrt(S+B)=0.85
                topCandidate_mass__100_0__166_666666667 S=18.1, B=806.2, S/sqrt(S+B)=0.63
                topCandidate_mass__166_666666667__200_0 S=11.9, B=408.1, S/sqrt(S+B)=0.58
    btag_LR_4b_2b_logit__8_0__20_0 S=15.1, B=279.2, S/sqrt(S+B)=0.88
       numJets__3__5 S=2.4, B=74.4, S/sqrt(S+B)=0.28
          btag_LR_4b_2b_logit__8_0__12_0 S=2.2, B=70.5, S/sqrt(S+B)=0.26
          btag_LR_4b_2b_logit__12_0__20_0 S=0.2, B=3.9, S/sqrt(S+B)=0.11
       numJets__5__7 S=12.6, B=204.9, S/sqrt(S+B)=0.86
"""


print "---------- BEGIN OLD TREE ----------"
r = CategorizationFromString(old)
r.print_tree() 
limit = r.eval_limit("test", get_limit)   
print "Old: ", limit
print "---------- END OLD TREE ----------"
print "\n\n"
print "---------- BEGIN OPTIMIZED TREE ----------"
r = CategorizationFromString(opt)
r.print_tree()    
limit = r.eval_limit("test", get_limit)   
print "Optimized: ", limit
print "---------- END OPTIMIZED TREE ----------"
