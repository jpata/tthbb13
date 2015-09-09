
barrel_50 = """
|           full5x5_sigmaIetaIeta <  |  0.012  |  0.0105  |  0.0101 | 0.0101 |
|                     abs(dEtaIn) <  |  0.0126 |  0.00976 |  0.0094 | 0.0095 |
|                     abs(dPhiIn) <  |  0.107  |  0.0929  |  0.0296 | 0.0291 |
|                          hOverE <  |  0.186  |  0.0765  |  0.0372 | 0.0372 |
|                    relIsoWithEA <  |  0.161  |  0.118   |  0.0987 | 0.0468 |
|                         ooEmooP <  |  0.239  |  0.184   |  0.118  | 0.0174 |
|                         abs(d0) <  |  0.0621 |  0.0227  |  0.0151 | 0.0144 |
|                         abs(dz) <  |  0.613  |  0.379   |  0.238  | 0.323  |
|       expectedMissingInnerHits *<=*  |    2    |     2    |    2    |    2   |
|       pass conversion veto     |  yes  |  yes  |  yes  |  yes  |
"""
endcap_50 = """
|           full5x5_sigmaIetaIeta <  |  0.0339  |  0.0318  |  0.0287  | 0.0287 |
|                     abs(dEtaIn) <  |  0.0109  |  0.00952  |  0.00773  | 0.00762 |
|                     abs(dPhiIn) <  |  0.219  |  0.181  |  0.148  | 0.0439 |
|                          hOverE <  |  0.0962  |  0.0824  |  0.0546  | 0.0544 |
|                    relIsoWithEA <  |  0.193  |  0.118  |  0.0902  | 0.0759 |
|                         ooEmooP <  |  0.141  |  0.125  |  0.104  | 0.01 |
|                         abs(d0) <  |  0.279  |  0.242  |  0.0535  | 0.0377 |
|                         abs(dz) <  |  0.947  |  0.921  |  0.572  | 0.571 |
|        expectedMissingInnerHits *<=*  |  3  |  1  |  1  | 1 |
|       pass conversion veto     |  yes  |  yes  |  yes  |  yes  |
"""

barrel_25 = """
| full5x5_sigmaIetaIeta < | 0.0114 | 0.0103 | 0.0101 | 0.0101 |
| abs(dEtaIn) < | 0.0152 | 0.0105 | 0.0103 | 0.00926 |
| abs(dPhiIn) < | 0.216 | 0.115 | 0.0336 | 0.0336 |
| hOverE < | 0.181 | 0.104 | 0.0876 | 0.0597 |
| relIsoWithEA < | 0.126 | 0.0893 | 0.0766 | 0.0354 |
| ooEmooP < | 0.207 | 0.102 | 0.0174 | 0.012 |
| abs(d0) < | 0.0564 | 0.0261 | 0.0118 | 0.0111 |
| abs(dz) < | 0.472 | 0.41 | 0.373 | 0.0466 |
| expectedMissingInnerHits <= | 2 | 2 | 2 | 2 |
|       pass conversion veto     |  yes  |  yes  |  yes  |  yes  |
"""

endcap_25 = """
| full5x5_sigmaIetaIeta < | 0.0352 | 0.0301 | 0.0283 | 0.0279 |
| abs(dEtaIn) < | 0.0113 | 0.00814 | 0.00733 | 0.00724 |
| abs(dPhiIn) < | 0.237 | 0.182 | 0.114 | 0.0918 |
| hOverE < | 0.116 | 0.0897 | 0.0678 | 0.0615 |
| relIsoWithEA < | 0.144 | 0.121 | 0.0678 | 0.0646 |
| ooEmooP < | 0.174 | 0.126 | 0.0898 | 0.00999 |
| abs(d0) < | 0.222 | 0.118 | 0.0739 | 0.0351 |
| abs(dz) < | 0.921 | 0.822 | 0.602 | 0.417 |
| expectedMissingInnerHits <= | 3 | 1 | 1 | 1 |
|       pass conversion veto     |  yes  |  yes  |  yes  |  yes  |
"""

# 
# (abs(el.eleDEta)    < 0.008925) and
# (abs(el.eleDPhi)    < 0.035973) and
# (el.eleSieie        < 0.009996) and
# (el.eleHoE          < 0.050537) and
# (abs(el.dxy)        < 0.012235) and
# (abs(el.dz)         < 0.042020) and
# (el.pfRelIso03      < 0.107587) and #delta-beta corrected relative iso
# (getattr(el, "eleExpMissingInnerHits", 0) <= 1) and
# (getattr(el, "eleooEmooP", 0) < 0.091942)

loose_cuts = {"barrel": [], "endcap":[]}
medium_cuts = {"barrel": [], "endcap":[]}

if __name__ == "__main__":
    
    for name, cblock in [("barrel", barrel_25), ("endcap", endcap_25)]:
        for line in cblock.split("\n"):
            spl = line.split("|")
            spl = map(lambda x: x.strip(), spl)
            spl = filter(lambda x: len(x)>0, spl)
            #spl = filter(lambda x: x!="|", spl)
            if len(spl)==0:
                continue
            if len(spl)!=5:
                print "Could not parse", spl
                continue
            cutname, veto, loose, medium, tight = spl
            if not "pass conversion veto" in cutname:
                veto = float(veto)
                loose = float(loose)
                medium = float(medium)
                tight = float(tight)
            
            pycut = "X"
            if "full5x5_sigmaIetaIeta".lower() in cutname.lower():
                pycut = "el.eleSieie"
            elif "abs(dEtaIn)".lower() in cutname.lower():
                pycut = "abs(el.eleDEta)"
            elif "abs(dPhiIn)".lower() in cutname.lower():
                pycut = "abs(el.eleDPhi)"
            elif "hOverE".lower() in cutname.lower():
                pycut = "el.eleHoE"
            elif "relIsoWithEA".lower() in cutname.lower():
                pycut = "el.relIso03"
            elif "ooEmooP".lower() in cutname.lower():
                pycut = "el.eleooEmooP"
            elif "abs(d0)".lower() in cutname.lower():
                pycut = "abs(el.dxy)"
            elif "abs(dz)".lower() in cutname.lower():
                pycut = "abs(el.dz)"
            elif "expectedMissingInnerHits".lower() in cutname.lower():
                pycut = "el.eleExpMissingInnerHits"
            elif "pass conversion veto".lower() in cutname.lower():
                pycut = "el.convVeto"
            sign = "=="
            if "<=" in cutname:
                sign = "<="
            elif "<" in cutname:
                sign = "<"
            elif ">=" in cutname:
                sign = ">="
            elif ">" in cutname:
                sign = ">"
            loose_cuts[name] += ["({0} {1} {2})".format(pycut, sign, loose)]
            medium_cuts[name] += ["({0} {1} {2})".format(pycut, sign, medium)]
            #print pycut, sign, veto, loose, medium, tight, "and"

def print_block(bl):
    s = "if (sca <= 1.479):\n"
    s += "ret = ret and (\n" + " and\n".join(bl["barrel"]) + "\n)\n"
    s += "\nelif (sca < 2.5):\n"
    s += "ret = ret and (\n" + " and\n".join(bl["endcap"]) + "\n)\n"
    print s

print "#Loose Spring15"
print_block(loose_cuts)

print "#Medium Spring15"
print_block(medium_cuts)
