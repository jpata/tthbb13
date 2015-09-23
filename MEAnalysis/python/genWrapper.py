import json, sys

# def classFromColl(collname, vars, maxlen):
#     s = "class %s{\n" % collname
#     for vname, v in vars.items():
#         vtype, vhelp = v
#         s += "  {0} {1}; //{2}\n".format(vtype, vname, vhelp)
#     s += "};\n"
#     return s

#map python typenames to C++ types
typemap = {
    "float": "double",
    "int": "int"
}

def makeWrapper(classname, data):
    #Name of the wrapper class
    tree_classname = "TreeData"

    treeclass = "class %s {\n" % tree_classname
    treeclass += "public:\n"
    for collname, coll in data["collections"].items() + data["globalObjects"].items():
        vars, maxlen = coll
        #print collname, maxlen
        #print classFromColl(collname, vars, maxlen)
        for vname, v in vars.items():
            vtype, vhelp = v
            treeclass += "  {0} {1}_{2}[{3}]; //{4}\n".format(typemap[vtype], collname, vname, maxlen, vhelp)
        #treeclass += "  {0} _{1}[{2}];\n".format(collname, collname, maxlen)

    for collname, dtype in data["globalVariables"].items():
        treeclass += "  {0} {1};\n".format(typemap[dtype], collname)
        #treeclass += "  {0} _{1}[{2}];\n".format(collname, collname, maxlen)


    treeclass += "  void loadTree(TTree* tree) {\n"
    for collname, coll in data["collections"].items() + data["globalObjects"].items():
        vars, maxlen = coll
        for vname, v in vars.items():
            treeclass += '    tree->SetBranchAddress(\"{0}_{1}\", this->{0}_{1});\n'.format(collname, vname)


    for collname, dtype in data["globalVariables"].items():
        treeclass += '    tree->SetBranchAddress(\"{0}\", &(this->{0}));\n'.format(collname, collname)

    treeclass += "  } //loadTree\n"
    treeclass += "}; //class\n"

    return treeclass


if __name__ == "__main__":
    infile = open(sys.argv[1])
    data = json.loads(infile.read())
    infile.close()
    wrapper = makeWrapper("TreeData", data)
    of = open(sys.argv[2], "w")
    of.write(wrapper)
    of.close()
