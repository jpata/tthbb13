from TTH.TTHNtupleAnalyzer.CrabHelpers import hadd_from_file, replicate
import argparse

version = "s1_eb733a1__s2_c084f2b"

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--action',
	choices=['replicate'], type=str,
    required=True,
	help="the action to perform"
)

args = parser.parse_args()

if args.action == "replicate":
    replicate("to-replica.txt", "T3_CH_PSI", "/store/user/jpata/tth/" + version)
    replicate("to-replica.txt", "T2_EE_Estonia", "/store/user/jpata/tth/" + version)
