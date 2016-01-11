Plotting code
=============

This is a description of the new C++-based histogram projector.

The main code is in `TTH/Plotting/bin/MELooper.cc`. The code can be compiled using `make` in the `TTH/Plotting` directory. This will produce an executable `melooper`, which takes as input a simple json steering file:

~~~
./melooper conf.json
~~~

You can create a list of steering files using the command:
~~~
python TTH/Plotting/python/joosep/makeJobfiles.py
~~~
In the `makeJobfiles.py` script, the variable `sampstorun` configures which samples are enabled. Each file will be opened and split into chunks across jobfiles. The script will create a list of `job_{N}.json` files, which should all be run. The output of these jobs should be merged together.

Command for running on 20 json files in parallel (needs http://www.gnu.org/software/parallel/):
~~~
parallel -j 20  ./melooper  ::: *.json
~~~

The categories are currently configured by a compiled list, which is specified in https://github.com/jpata/tthbb13/blob/sync_spring15/Plotting/bin/MELooper.cc#L145

There you will also find documentation on the category syntax.

In short, the looper works as follows:

1. A configuration is loaded from the json
2. the cut parameters in the json configure the categories, which are then `const`
3. each category is named with a list consisting of `CategoryKey::CategoryKey` enums, which will be used for naming.
4. Each event is loaded into an `Event` separately for each systematic scenario (indexed by `SystematicKey::SystematicKey`) where the objects change with the systematic variation, e.g. JES variations.
5. The event loading happens through helper methods (`EventFactory`, `JetFactory`) which connect the machine-generated `TreeData` structure representing the MEM output tree to the physical event interpretation.
6. all events are looped over
  5. All systematic events are looped over
    6. for each event, there will be a multiple possible weight scenarios, e.g. the nominal event may need to be   re-weighted.
      7. Each category will then be evaluated with `CategoryProcessor::process`, along with its subcategories. The categories check if they pass using `CategoryProcessor::()` and if yes, create their respective histograms using `CategoryProcessor::fillHistograms`.
      8. All histograms are kept in memory in the `results`.
9. Once the program completes, all results will be saved to a file which is configured using the json.
