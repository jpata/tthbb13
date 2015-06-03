from TTH.MEAnalysis.samples_base import lfn_to_pfn

f_in = open( 'RootFilenames.txt', 'r' )
f_out = open( 'filenameswithcount.dat', 'w' )

filenames = []

while True:
    filename = f_in.readline()
    if not filename: break
    filenames.append( filename )

for f in filenames:

    f = f.strip()

    f_out.write( '"{0}",\n'.format( f ) )

f_out.close()
f_in.close()
