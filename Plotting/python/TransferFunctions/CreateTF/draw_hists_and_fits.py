#!/usr/bin/env python
"""
Dictionay and pickle test

"""

########################################
# Imports
########################################

import pickle
import ROOT

from TFClasses import function
from TFClasses import TF

########################################
# Main
########################################

def Draw_Hists_and_Fits(conffile):

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
    #ROOT.gStyle.SetOptFit(1011)

    # Don't display standard statistics
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptStat(0)

    # Load config.dat
    pickle_f = open( conffile, 'rb' )
    config = pickle.load( pickle_f )
    pickle_f.close()

    outputdir = config['outputdir']

    # Load the single bin histograms
    pickle_f = open( config['SBF_fitted_hists_pickle_filename'] , 'rb' )
    SB_dicts = pickle.load( pickle_f )
    pickle_f.close()

    # Load the found transfer functions
    pickle_f = open( '{0}/TFMatrix.dat'.format(outputdir), 'rb' )
    TFMat = pickle.load( pickle_f )
    pickle_f.close()


    c1 = ROOT.TCanvas("c1","c1",500,400)
    c1.SetGrid()

    for particle in config['particles']:
        for i_eta in range( len(config['eta_axis']) - 1 ):
            for i_E in range( config['n_E_bins'] ):

                SB_dicts[particle][i_eta][i_E]['hist'].Draw()

                f1 = SB_dicts[particle][i_eta][i_E]['hist'].GetFunction('hfit')
                
                ABF = TFMat[particle][i_eta].Make_Formula(False)
                ABF.SetParameter( 0, SB_dicts[particle][i_eta][i_E]['E_value'] )
                ABF.SetParameter( 1, f1.GetParameter(0) )
                ABF.SetLineColor(1)
                ABF.SetLineStyle(7)
                ABF.SetLineWidth(3)
                ABF.SetRange(0,config['E_bounds'][1])
                ABF.Draw("LPSAME")

                
                ########################################
                # Labels: displaying par values in plots
                ########################################

                # Set label specifics
                lbl = ROOT.TText()
                lbl.SetNDC()
                lbl.SetTextSize(0.04)
                lbl.SetTextColor(1)

                # Coordinates for the histogram specifics
                anchorx = 0.13
                anchory = 0.85
                nl = 0.05

                lbl.SetTextColor(4)
                lbl.DrawText( anchorx, anchory, 'Hist spec.')
                lbl.SetTextColor(1)
                anchory-=nl

                lbl.DrawText( anchorx, anchory , 'Entries' )
                lbl.DrawText( anchorx+0.11, anchory , '{0:0.0f}'.format(
                    SB_dicts[particle][i_eta][i_E]['hist'].GetEntries()) )
                anchory-=nl

                lbl.DrawText( anchorx, anchory , 'Mean' )
                lbl.DrawText( anchorx+0.11, anchory , '{0:.2f}'.format(
                    SB_dicts[particle][i_eta][i_E]['hist'].GetMean()) )
                anchory-=nl

                lbl.DrawText( anchorx, anchory , 'RMS' )
                lbl.DrawText( anchorx+0.11, anchory ,'{0:.2f}'.format(
                    SB_dicts[particle][i_eta][i_E]['hist'].GetRMS()) )

                # Coordinates for the fit values
                anchorx = 0.58
                anchory = 0.85

                lbl.SetTextColor(2)
                lbl.DrawText( anchorx, anchory, 'Bin spec. fit')
                lbl.SetTextColor(1)
                anchory-=nl

                for i in range( len( config['ABFunctions'][particle] ) ):
                    lbl.DrawText( anchorx, anchory , '[{0}] ='.format(i) )
                    lbl.DrawText( anchorx+0.08, anchory ,
                        '{0:.2f}'.format(f1.GetParameter(i)) )
                    lbl.DrawText( anchorx+0.20, anchory ,
                        '({0:.2f})'.format(f1.GetParError(i)) )
                    anchory-=nl

                anchorx += 0.1
                anchory-=nl
                lbl.DrawText( anchorx, anchory, 'fit from ABF')
                anchory-=nl

                for (ABFnr, func) in enumerate(
                    TFMat[particle][i_eta].AcrossBinFuncs ):

                    lbl.DrawText( anchorx, anchory , '[{0}] ='.format(ABFnr) )

                    ABF_TF1 = ROOT.TF1(
                        "point",
                        func.str )

                    if ABFnr == 0:
                        # This is always the normalization parameter
                        abf_eval = f1.GetParameter(0)
                    elif func.str == "1":
                        abf_eval = 1
                    else:
                        for ( i, par ) in enumerate(func.par_values):
                            ABF_TF1.SetParameter( i, par )

                        abf_eval = ABF_TF1.Eval(
                            SB_dicts[particle][i_eta][i_E]['E_value'] ,0,0)
                    
                    lbl.DrawText( anchorx+0.08, anchory ,
                        '{0:.2f}'.format(abf_eval) )
                    anchory-=nl


                ########################################
                # Outputting to file
                ########################################

                # to pdf
                c1.Print('{3}/{2}/{2}-{0}-{1}'.format(
                    i_eta, i_E, particle, outputdir ), 'pdf')

                # to png
                if i_E == 0:
                    print 'Writing {0}-{1}-(0 to {2}).png'.format(
                        particle, i_eta, config['n_E_bins']-1 )

                img = ROOT.TImage.Create()
                img.FromPad(c1)
                img.WriteImage('{3}/{2}/{2}-{0}-{1}.png'.format(
                    i_eta, i_E, particle, outputdir ) )


    # Write an html-file which will be an overview of all png's
    for p in config['particles']:

        hf = open( '{0}/overview-{1}.html'.format(outputdir, p), 'w' )

        hf.write( '<html><body>\n<h1>Run Summary:\n</h1>\n<br>\n<hr />' )
        hf.write( '<h2>Title</h2>' )


        for i_E in range( config['n_E_bins'] ):
            for i_eta in range( len(config['eta_axis']) - 1 ):

                filename = '{0}/{0}-{1}-{2}'.format(
                    p, i_eta, i_E )
                hf.write('<a href="{0}"><img width="350" src="{0}.png"></a>\n'.format(filename) )
            hf.write('<br>\n')
        hf.write( '<br>\n<hr />\n<br>\n</body></html>' )



########################################
# End of Main
########################################
def main():
    Draw_Hists_and_Fits()

if __name__ == "__main__":
  main()
