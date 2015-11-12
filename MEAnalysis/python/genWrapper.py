import json, sys

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
        treeclass += "  int n{0};\n".format(collname)
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
        treeclass += '    tree->SetBranchAddress(\"n{0}\", &(this->n{0}));\n'.format(collname)
        for vname, v in vars.items():
            treeclass += '    tree->SetBranchAddress(\"{0}_{1}\", this->{0}_{1});\n'.format(collname, vname)


    for collname, dtype in data["globalVariables"].items():
        treeclass += '    tree->SetBranchAddress(\"{0}\", &(this->{0}));\n'.format(collname, collname)

    treeclass += "  } //loadTree\n"
    treeclass += "}; //class\n"
    
    prefix = """
#ifndef METREE_H
#define METREE_H
#include "TTree.h"
{0}
#endif
""".format(treeclass)
    return prefix


if __name__ == "__main__":
    infile = open(sys.argv[1])
    data = json.loads(infile.read())
    infile.close()
    wrapper = makeWrapper("TreeData", data)
    of = open(sys.argv[2], "w")
    of.write(wrapper)
    of.close()
