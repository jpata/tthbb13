plotter:
	python python/joosep/codeGen.py
	c++ `root-config --cflags --libs` -lPyROOT -I`pwd`/../.. bin/Event.cc bin/MELooper.cc bin/gen.cc bin/categories.cc bin/gason.cpp -o melooper
