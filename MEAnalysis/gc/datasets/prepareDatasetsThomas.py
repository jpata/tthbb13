from TTH.MEAnalysis.samples_base import lfn_to_pfn
import ROOT

f_in = open( 'RootFilenames.txt', 'r' )
f_out = open( 'filenameswithcount.dat', 'w' )

filenames = []

while True:
    filename = f_in.readline()
    if not filename: break
    filenames.append( filename )

for f in filenames:

    f = f.strip()

    root_file = ROOT.TFile.Open(lfn_to_pfn(f))

    root_tree = root_file.Get("tree")

    f_out.write( '{0} = {1}\n'.format( f, root_tree.GetEntries() ) )

f_out.close()
f_in.close()
