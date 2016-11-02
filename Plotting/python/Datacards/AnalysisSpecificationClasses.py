import os
import ConfigParser
from itertools import izip

from TTH.MEAnalysis import samples_base
from TTH.MEAnalysis.samples_base import get_files, getSitePrefix

# From:
# http://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

def triplewise(iterable):
    "s -> (s0, s1, s2), (s3, s4, s5), (s5, s6, s7), ..."
    a = iter(iterable)
    return izip(a, a, a)

def string_to_cuts(s):
    cuts = []
    for cut_name, lower, upper in triplewise(s):
        cuts.append((cut_name, float(lower), float(upper)))
    return cuts

def cuts_to_string(cuts):
    s = ""
    for cut_name, lower, upper in cuts:
        s += "{0} {1} {2}\n".format(cut_name, lower, upper)
    return s

class Cut(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")
        self.sparsinator = kwargs.get("sparsinator")
        self.skim = kwargs.get("skim")

    @staticmethod
    def fromConfigParser(config, name):
        return Cut(
            name = name,
            sparsinator = string_to_cuts(config.get(name, "sparsinator").split()),
            skim = config.get(name, "skim")
        )

    def updateConfig(self, config):
        config.set(self.name, "sparsinator", cuts_to_string(self.sparsinator))
        config.set(self.name, "skim", cuts_to_string(self.skim))

class Sample(object):
    def __init__(self, *args, **kwargs):
        self.debug = kwargs.get("debug")
        self.name = kwargs.get("name")
        self.schema = kwargs.get("schema")
        self.process = kwargs.get("process")
        self.is_data = bool(kwargs.get("is_data"))
        self.files_load = kwargs.get("files_load")
        self.step_size_sparsinator = int(kwargs.get("step_size_sparsinator"))
        self.debug_max_files = int(kwargs.get("debug_max_files"))
        self.file_names = [getSitePrefix(fn) for fn in get_files(self.files_load)]
        if self.debug:
            self.file_names = self.file_names[:self.debug_max_files]
        self.ngen = int(kwargs.get("ngen"))
        self.xsec = kwargs.get("xsec")
        
        #temporary workaround for old way of specifying xs in python file
        if not self.xsec:
            self.xsec = samples_base.xsec_sample[self.name]

        self.classifier_db_path = kwargs.get("classifier_db_path")
        self.skim_file = kwargs.get("skim_file")

    @staticmethod
    def fromConfigParser(config, sample_name):
        sample = Sample(
            debug = config.getboolean("general", "debug"),
            name = sample_name,
            process = config.get(sample_name, "process"),
            files_load = config.get(sample_name, "files_load"),
            schema = config.get(sample_name, "schema"),
            is_data = config.get(sample_name, "is_data"),
            step_size_sparsinator = config.get(sample_name, "step_size_sparsinator"),
            debug_max_files = config.get(sample_name, "debug_max_files"),
            ngen = config.getfloat(sample_name, "ngen"),
            classifier_db_path = config.get(sample_name, "classifier_db_path", None),
            skim_file = config.get(sample_name, "skim_file", None),
            xsec = config.getfloat(sample_name, "xsec"),
        )
        return sample

    def updateConfig(self, config):
        for field in dir(self):
            if field.startswith("__"):
                continue
            config.set(self.name, field, str(getattr(self, field)))

class Process(object):
    """
    Defines how an input process should be mapped to an output histogram.
    """
    def __init__(self, *args, **kwargs):
        self.input_name = kwargs.get("input_name")
        self.output_name = kwargs.get("output_name")
        self.cuts = kwargs.get("cuts", [])
        self.xs_weight = kwargs.get("xs_weight", 1.0)
    
    def __repr__(self):
        s = "Process: maps {0}->{1} with cuts=[{2}], xsw={3}".format(
            self.input_name,
            self.output_name,
            ",".join(map(str, self.cuts)),
            self.xs_weight
        )
        return s

class DataProcess(Process):
    def __init__(self, *args, **kwargs):
        super(DataProcess, self).__init__(self, *args, **kwargs)
        self.lumi = kwargs.get("lumi", 1.0)

class Category:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.discriminator = kwargs.get("discriminator")
        self.full_name = "{0}_{1}".format(self.name, self.discriminator)
        self.src_histogram = kwargs.get("src_histogram")
        self.rebin = kwargs.get("rebin", 1)
        self.do_limit = kwargs.get("do_limit", True)

        self.scale_uncertainties = kwargs.get("scale_uncertainties", {})

        self.cuts = kwargs.get("cuts", [])

        self.processes = kwargs.get("processes", [])
        self.data_processes = kwargs.get("data_processes", [])
        #self.lumi = sum([d.lumi for d in self.data_samples])

        self.signal_processes = kwargs.get("signal_processes", [])
        self.out_processes = list(set([s.output_name for s in self.processes]))

        #[process][syst]
        self.shape_uncertainties = {}
        self.scale_uncertainties = {}

        #[syst] -> scale factor, common for all processes
        self.common_shape_uncertainties = kwargs.get("common_shape_uncertainties", {})
        self.common_scale_uncertainties = kwargs.get("common_scale_uncertainties", {})
        for proc in self.out_processes:
            self.shape_uncertainties[proc] = {}
            self.scale_uncertainties[proc] = {}
            for systname, systval in self.common_shape_uncertainties.items():
                self.shape_uncertainties[proc][systname] = systval
            for systname, systval in self.common_scale_uncertainties.items():
                self.scale_uncertainties[proc][systname] = systval

        self.proc_shape_uncertainties = kwargs.get("shape_uncertainties", {})
        self.proc_scale_uncertainties = kwargs.get("scale_uncertainties", {})
        
        for k, v in self.proc_shape_uncertainties.items():
            self.shape_uncertainties[k].update(v)

        for k, v in self.proc_scale_uncertainties.items():
            self.scale_uncertainties[k].update(v)

    
    def __repr__(self):
        s = "Category: {0} ({1}) discr={2} cuts={3} do_limit={4}".format(
            self.name,
            self.full_name,
            self.discriminator,
            self.cuts,
            self.do_limit
        )
        return s

    # Define equality via the representation string
    def __eq__(self,other):
        return self.__repr__() == other.__repr__()

    # hash(object) = hash(representation(object))
    def __hash__(self):
        return self.__repr__().__hash__()


class Analysis:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")
        self.debug = kwargs.get("debug", False)
        self.samples = kwargs.get("samples", [])
        self.cuts = kwargs.get("cuts", {})
        self.processes = kwargs.get("processes")
        self.processes_unsplit = kwargs.get("processes_unsplit")
        self.categories = kwargs.get("categories")
        self.sparse_input_file = kwargs.get("sparse_input_file")

        # groups represent calls to combine, i.e. 
        # {"myCombination1": ["cat1", "cat2"] }
        # will calculate the combined limit myCombination1 of cat1 and cat2 
        self.groups = kwargs.get("groups", {})
        self.do_fake_data = kwargs.get("do_fake_data", False)
        self.do_stat_variations = kwargs.get("do_stat_variations", False)

    def get_sample(self, sample_name):
        sample_d = dict([(s.name, s) for s in self.samples])
        return sample_d[sample_name]

    def to_JSON(self):
        return json.dumps(self.__dict__, indent=2)
    
    def __repr__(self):
        s = "Analysis:\n"
        s += "  input file: {0}\n".format(self.sparse_input_file)
        s += "  processes:\n"
        for proc in self.processes:
            s += "    {0}\n".format(proc)
        s += "  categories:\n"
        for cat in self.categories:
            s += "    {0}\n".format(cat)
        
        s += "  groups for combine:\n"
        for groupname, cats in self.groups.items():
            s += "    {0}: {1}\n".format(groupname, [c.name for c in self.groups[groupname]])
        return s

    @staticmethod
    def getConfigParser(config_file_name):
        config = ConfigParser.SafeConfigParser()
        config.optionxform = str # Turn on case-sensitivity
        config.read(config_file_name)
        return config

def make_csv_categories_abstract(di):

    import csv
    with open('analysis_specs.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')    

        csvwriter.writerow(['specfile', 'analysis', 'category'])
    
        # We want the analysis specification file
        # as make_csv is called from there we just take the filename of the outer stack
        import inspect
        analysis_spec_file = os.path.abspath(inspect.getouterframes(inspect.currentframe())[1][1])

        for analysis_name, analysis in di.iteritems():        

            unique_cat_names = list(set(c.name for c in analysis.categories))
            for cat_name in unique_cat_names:
                csvwriter.writerow([analysis_spec_file, analysis_name, cat_name])

    return [1]

def make_csv_groups_abstract(di):

    import csv
    with open('analysis_groups.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')    

        csvwriter.writerow(['specfile', 'analysis', 'group'])
    
        # We want the analysis specification file
        # as make_csv is called from there we just take the filename of the outer stack    
        import inspect
        analysis_spec_file = os.path.abspath(inspect.getouterframes(inspect.currentframe())[1][1])

        for analysis_name, analysis in di.iteritems():        
            for group_name in analysis.groups.keys():
                csvwriter.writerow([analysis_spec_file, analysis_name, group_name])

    return [1]
