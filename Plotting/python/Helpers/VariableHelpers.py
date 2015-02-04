#!/usr/bin/env python
"""
Simple convenience class to store information for plotting variables
"""

########################################
# Imports and Macros
########################################

# initializer: simple creation of bag-of-object classes
from Initializer import initializer


########################################
# class variable
########################################

class variable:
    """ Helper class to store a variable used as TMVA input """
    
    # Dictionary of all available variables
    #  -newly created objects register automatically
    #  -keys = variable bane
    di = {}

    @initializer
    def __init__(self,
                 name,              # (string) name of the variable in the n-tuple
                 pretty_name,       # (string) nicer name (for printing)
                 range_min,         # (float) minimal reasonable value
                 range_max,         # (float) maximal reasonable value 
                 unit = "",         # (string) for axis labels
                 extra_cut = "(1)"  # additional cut to apply
             ):
        variable.di[self.name] = self
    # end __init__

# end of variable class

