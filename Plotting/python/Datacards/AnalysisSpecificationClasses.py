import pdb
import os

class Sample:
    """
    Defines how an input sample should be mapped to an output histogram.
    Optionally 
    """
    def __init__(self, **kwargs):
        self.input_name = kwargs.get("input_name")
        self.output_name = kwargs.get("output_name")
        self.cuts = kwargs.get("cuts", [])
        self.xs_weight = kwargs.get("xs_weight", 1.0)

    # 
    # def __repr__(self):
    #     s = "Sample: maps {0}->{1} with cuts=[{2}], xsw={3}".format(
    #         self.input_name,
    #         self.output_name,
    #         ",".join(map(str, self.cuts)),
    #         self.xs_weight
    #     )
    #     return s

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
        self.samples = kwargs.get("samples", [])
        self.data_samples = kwargs.get("data_samples", [])
        self.signal_processes = kwargs.get("signal_processes", [])
        self.processes = list(set([s.output_name for s in self.samples]))

        #[process][syst]
        self.shape_uncertainties = {}
        self.scale_uncertainties = {}

        #[syst] -> scale factor, common for all processes
        self.common_shape_uncertainties = kwargs.get("common_shape_uncertainties", {})
        self.common_scale_uncertainties = kwargs.get("common_scale_uncertainties", {})
        for proc in self.processes:
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

class Analysis:
    def __init__(self, **kwargs):
        self.samples = kwargs.get("samples")
        self.categories = kwargs.get("categories")
        self.sparse_input_file = kwargs.get("sparse_input_file")

        # groups represent calls to combine, i.e. 
        # {"myCombination1": ["cat1", "cat2"] }
        # will calculate the combined limit myCombination1 of cat1 and cat2 
        self.groups = kwargs.get("groups", {})
        self.do_fake_data = kwargs.get("do_fake_data", False)
        self.do_stat_variations = kwargs.get("do_stat_variations", False)

    def to_JSON(self):
        return json.dumps(self.__dict__, indent=2)
    
    def __repr__(self):
        s = "Analysis:\n"
        s += "  input file: {0}\n".format(self.sparse_input_file)
        s += "  samples:\n"
        for samp in self.samples:
            s += "    {0}\n".format(samp)
        s += "  categories:\n"
        for cat in self.categories:
            s += "    {0}\n".format(cat)
        
        s += "  groups for combine:\n"
        for groupname, cats in self.groups.items():
            s += "    {0}: {1}\n".format(groupname, [c.name for c in self.groups[groupname]])
        return s

def make_csv_categories_abstract(di):

    import csv
    with open('analysis_specs.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')    

        csvwriter.writerow(['specfile', 'analysis', 'category', 'sparsefile'])
    
        # We want the analysis specification file
        # as make_csv is called from there we just take the filename of the outer stack    
        import inspect
    
        analysis_spec_file = inspect.getouterframes(inspect.currentframe())[1][1]
        analysis_spec_file =  os.path.dirname(os.path.abspath(analysis_spec_file)) + "/" + analysis_spec_file

        for analysis_name, analysis in di.iteritems():        

            unique_cat_names = list(set(c.name for c in analysis.categories))
            for cat_name in unique_cat_names:
                csvwriter.writerow([analysis_spec_file, analysis_name, cat_name, analysis.sparse_input_file])

    return [1]

def make_csv_groups_abstract(di):

    import csv
    with open('analysis_groups.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')    

        csvwriter.writerow(['specfile', 'analysis', 'group'])
    
        # We want the analysis specification file
        # as make_csv is called from there we just take the filename of the outer stack    
        import inspect
        analysis_spec_file = inspect.getouterframes(inspect.currentframe())[1][1]
        analysis_spec_file =  os.path.dirname(os.path.abspath(analysis_spec_file)) + "/" + analysis_spec_file

        for analysis_name, analysis in di.iteritems():        
            for group_name in analysis.groups.keys():
                csvwriter.writerow([analysis_spec_file, analysis_name, group_name])

    return [1]
