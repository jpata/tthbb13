import sys
import rootpy
import rootpy.io

tf = rootpy.io.File(sys.argv[1])

for path, dirs, objects in tf.walk():
    depth = path.count("/")
    lastdir = path.split("/")[-1]
    print depth*"-" + lastdir
    for obj in sorted(objects):
        o = tf.get(path + "/" + obj)
        print (depth+1)*"-" + "{0} ({1})".format(obj, o.__class__.__name__)
