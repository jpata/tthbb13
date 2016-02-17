########################################
# Cut
########################################

class Cut(object):
    """ Helper class for Categoize: simple cut that knows the number of the axis
    (wrt/ to the static axes list) and the low (lo) and high (hi) bin
    to include.
    """
    
    axes = None # List of Axis objects (Axis.py)


    def __init__(self, *args):
        """ Constructor:
        - 0 arguments: default constructor
        - 1 argument: construct from string (inverse of repr)
        - 3 arguments: construct from numbers [axis number, low, high]
        """
        
        # Default constructor
        if len(args) == 0:
            self.axis = None
            self.iaxis = -1
            self.lo   = -1
            self.hi   = -1

        # From String
        elif len(args) == 1 and isinstance(args[0], str):
            
            # Example: btag_LR_4b_2b_logit__m20_0__8_0
            # First split according to __
            atoms = args[0].split("__")
            
            # Extract the variable name and convert back the numbers
            axis_name = atoms[0]
            low  = float(atoms[1].replace("m","-").replace("_","."))
            high = float(atoms[2].replace("m","-").replace("_","."))

            # Loop over the axis and see if one of the name is available
            axis_found = False
            for iax, ax in enumerate(self.axes.values()):
                if ax.name == axis_name:
                    self.axis = ax
                    self.iaxis = iax
                    axis_found = True
                    break
            if not axis_found:
                raise Exception('Cut Constructor', 'Axis not found', axis_name, self.axes.keys())
                                        
            # Go from cut values to bins
            axis = self.axis
            binsize = (axis.xmax - axis.xmin)/(1.*axis.nbins)            
            self.lo = int( round((low-axis.xmin)/binsize) ) + 1 # Start bin counting at 1
            self.hi = int( round((high-axis.xmin)/binsize) ) # The upper edge is not included (so basically +1-1=0)
            
            # Make sure the conversion worked
            if not str(self) == args[0]:
                raise Exception('Cut Constructor', 'Building from string failed', str(self), args[0])

        # From numbers
        elif len(args) == 3:
            try: 
                self.axis = self.axes[args[0]]
                self.iaxis = self.axes.keys().index(self.axis.name)
                self.lo   = int(args[1])
                self.hi   = int(args[2])
            except Exception as e:
                raise Exception("Could not parse 3-argument constructor", e)
        else:
             raise Exception('Cut Constructor', 'Invalid number/type of arguments')
            
                
    def __nonzero__(self):
        if self.axis is None:
            return False
        else:
            return True

    def __repr__(self):

        if self.axis:
            axis = self.axis
            binsize = (axis.xmax - axis.xmin)/(1.*axis.nbins)
            lower = axis.xmin + (self.lo-1)*binsize
            upper = axis.xmin + (self.hi)*binsize
            
            # Binsize of 1 means we have integer bins 
            if binsize==1.:
                lower = int(lower)
                upper = int(upper)
            
            return "{0}__{1}__{2}".format(axis.name, lower, upper).replace(".","_").replace("-","m")
                
        else:
            return ""

    def is_subset_of(self, other_cut):
        """Is self a subset (or identical to) other cut"""
        if self.axis == other_cut.axis and self.lo >= other_cut.lo and self.hi <= other_cut.hi:
            return True
        else:
            return False

    def latex_string(self):

        if self.axis:
            axis = self.axis
            binsize = (axis.xmax - axis.xmin)/(1.*axis.nbins)
            lower = axis.xmin + (self.lo-1)*binsize
            upper = axis.xmin + (self.hi)*binsize
            
            # Binsize of 1 means we have integer bins 
            if binsize==1.:
                lower = int(lower)
                upper = int(upper)

            axis_name = axis.name
            if axis_name == "btag_LR_4b_2b_logit":
                axis_name = "btag LR"
            elif axis_name == "common_bdt":
                axis_name = "\mathrm{BDT}"
            elif axis_name == "topCandidate_n_subjettiness":
                axis_name = r"top\; \tau_{3}/\tau_{2}"
            elif axis_name == "topCandidate_fRec":
                axis_name = r"top\; f_{Rec}"
            elif axis_name == "n_excluded_bjets":
                axis_name = r"n_{boost}\; b"
            elif axis_name == "n_excluded_ljets":
                axis_name = r"n_{boost}\; l"
            elif axis_name == "numJets":
                axis_name = r"n_{j}"
            elif axis_name == "nBCSVM":
                axis_name = r"n_{b}"
            
            if upper == int(upper):
                string_upper = "{0}".format(upper)
            else:
                string_upper = "{0:.2f}".format(upper)

            if lower == int(lower):
                string_lower = "{0}".format(lower)
            else:
                string_lower = "{0:.2f}".format(lower)


            if self.lo == 1:       
                return r"${0} < {1:} $".format(axis_name, string_upper)
            elif self.hi == axis.nbins:
                return r"${0:} \le {1}$".format(string_lower, axis_name)
            else:
                return r"${0:} \le {1} < {2:} $".format(string_lower, axis_name, string_upper)
                
        else:
            return "Combined"
