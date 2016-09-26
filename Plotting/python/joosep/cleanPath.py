def fixPythonPath(path):
    newpath = []
    for p in path:
        if "cvmfs" in p and "pandas" in p:
            continue
        newpath += [p]
    return newpath
