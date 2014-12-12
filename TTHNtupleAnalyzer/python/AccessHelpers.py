#!/usr/bin/env python
"""
Helper functions to add branches to a tree when creating a flat
ntuple. Also create TLVs.
"""

########################################
# Imports
########################################

import sys
import time
import array

import ROOT


########################################
# printProgress
########################################

def printProgress( i, total, interval = 1000):
    if not i % interval:
        print "{0:.1f}%".format( 100.*i/total), time.clock()
    

########################################
# addVectorBranches
########################################

def addVectorBranches( vars_dictionary, 
                       vars_type_dictionary, 
                       tree, 
                       branch_list, 
                       common_prefix = None,
                       datatype = 'float'):   
    """ Helper function to create and add multiple vector branches to
    a tree. A vector branch can hold a list of entries and is implemented
    using a ROOT.std.vector( float ).
    Arguments:
    vars_dictionary      -  dictionary to store the data in. A
                            key/value per will be added for each 
                            entry of branch_list  with an emty
                            vector (len=0) as value.
    vars_type_dictionary -  dictionary to store the type (vector or scalar)
                            data in vars dictionary. This avoids many calls
                            to isinstance for introspection.
                            A key/value pair will be added for each element
                            of branch_list with the string "V" as entry.
    tree                 -  ROOT TTree object to which the branches will be
                            added
    branch_list          -  list of strings containing the names of branches
                            to create
    common_prefix        -  Optional. Additional string that is added to the
                            beginning of each element of branch_list. Simple
                            way to generate many similar branch names at once.                       
    datatype             -  Optional. String for the type of the branch. 
                            Can be "float" (default) or "int".
    """
    
    # Loop over all branches
    for br in branch_list:

        # Build the name
        if common_prefix:
            branch_name = common_prefix + "_" + br
        else:
            branch_name = br

        # Create the variable and add to the dictionaries
        if datatype == "int":
            vars_dictionary[ branch_name ] =  ROOT.std.vector( int )()
        elif datatype == "float":
            vars_dictionary[ branch_name ] =  ROOT.std.vector( float )()

        vars_type_dictionary[branch_name] = "V" 
        # Link the variable to the tree
        setattr( tree, branch_name, vars_dictionary[branch_name] )
        tree.Branch( branch_name, vars_dictionary[branch_name] )          
    # End of loop over branches


########################################
# addScalarBranches
########################################

def addScalarBranches( vars_dictionary, 
                       vars_type_dictionary, 
                       tree, 
                       branch_list, 
                       common_prefix = None,  
                       datatype      = "int"
                       ):   
    """ Helper function to create and add multiple scalar branches to
    a tree. A scalar branch can hold one value (for example an integer
    or a float).
    Arguments:
    vars_dictionary      -  dictionary to store the data in. A
                            key/value per will be added for each 
                            entry of branch_list with the
                            with 0 as default value.
    vars_type_dictionary -  dictionary to store the type (vector or scalar)
                            data in vars dictionary. This avoids many calls
                            to isinstance for introspection.
                            A key/value pair will be added for each element
                            of branch_list with the string "S" as entry
    tree                 -  ROOT TTree object to which the branches will be
                            added
    branch_list          -  list of strings containing the names of branches
                            to create
    common_prefix        -  Optional. Additional string that is added to the
                            beginning of each element of branch_list. Simple
                            way to generate many similar branch names at once.                       
    datatype             -  Optional. String for the type of the branch. 
                            Can be "int" (default) or "float".
    """

    # Make sure that the requested datatype is valid
    if datatype not in ("int", "float"):
        print "In AccessHelpers/addScalarBranches: Invalid datatype: ", datatype
        print "Exiting..."
        sys.exit()

    # Loop over all branches
    for br in branch_list:
        
        # Build the name
        if common_prefix:
            branch_name = common_prefix + "_" + br
        else:
            branch_name = br
            
        # Create the variable and add to dictionaries. An array object
        # with one entry is used because ROOT wants a address of the
        # object.
        if datatype == "int":
            vars_dictionary[ branch_name ] =  array.array('i',[0])
        elif datatype == "float":
            vars_dictionary[ branch_name ] =  array.array('f',[0])

        vars_type_dictionary[branch_name] = "S" # avoid many isinstance calls

        # Link the variable to the tree
        setattr( tree, branch_name, vars_dictionary[branch_name])        
        if datatype == "int":
            tree.Branch( branch_name,   
                         vars_dictionary[branch_name],branch_name+"/I")          
        elif datatype == "float":
            tree.Branch( branch_name,   
                         vars_dictionary[branch_name],branch_name+"/F")          
        

########################################
# resetBranches
########################################

def resetBranches( dic_vars, dic_var_types ):
    for k in dic_vars.keys():
        if dic_var_types[k] == "S": # Scalar branch
            dic_vars[k][0] = 0
        elif dic_var_types[k] == "V": # Vector branch
            dic_vars[k].resize( 0 )
    # end of loop over keys
# end resetBranches


########################################
# buildTlv
########################################

def buildTlv( pt, eta, phi, m):
    
   # Init the lorentz vector
   tlv = ROOT.TLorentzVector()
   
   # Get the variables and build object (if index valid)

   tlv.SetPtEtaPhiM( pt,
                     eta,
                     phi,
                     m )
         
   return tlv
# end of buildTlv


########################################
# getter
########################################

def getter( tree, name_branch, name_leaf = ""):    
    """ Function to retrieve a branch/leaf from a tree. Either:
    tree.branch
    or 
    tree.branch.leaf
    Arguments:
    tree        : ROOT.TTree
    name_branch : string
    name_leaf   : string [optional]
    """

    if name_leaf:
        branch = tree.GetBranch( name_branch ) 
        leaf   = branch.GetLeaf( name_leaf)
        return leaf.GetValue()
    else:
        return getattr( tree, name_branch )
# End of getter
