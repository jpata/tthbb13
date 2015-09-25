Plotting code
=============

This is a description of the new C++-based histogram projector.

The main code is in `TTH/Plotting/bin/MELooper.cc`. The code can be compiled using `make` in the `TTH/Plotting` directory. This will produce an executable `melooper`, which takes as input a simple json steering file:

~~~
./melooper conf.json
~~~

You can create a list of steering files using the command:
~~~
python TTH/Plotting/python/makeJobfiles.py
~~~
In the `makeJobfiles.py` script, the variable `sampstorun` configures which samples are enabled. Each file will be opened and split into chunks across jobfiles. The script will create a list of `job_{N}.json` files, which should all be run. The output of these jobs should be merged together.

The categories are currently configured by a compiled list of categories, which is specified in https://github.com/jpata/tthbb13/blob/sync_spring15/Plotting/bin/MELooper.cc#L145

There you will also find documentation on the category syntax.


