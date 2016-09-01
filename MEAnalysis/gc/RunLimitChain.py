"""Execute limit setting chain starting from sparse histogram."""

import os
import sys
import pdb

sys.path.append(os.path.abspath(os.path.join("grid-control", 'packages')))

import shutil
import copy
import TTH.Plotting.Datacards.AnalysisSpecification as anaSpec


# Prepare Analysis specs
anaSpec.main()

# Cleanup work directory for makeCategory
try:
    shutil.rmtree("work.makecategory")
except:
    pass

import grid_control
import gcTool    

config = gcTool.gc_create_config(["confs/makecategory.conf", "-Gc"])
global_config = config.changeView(setSections = ['global'])
global_config.setState(True, 'init')
grid_control.utils.ensureDirExists(global_config.getWorkPath(), 'work directory')
workflow = global_config.getPlugin('workflow', 'Workflow:global', cls = 'Workflow')
config.factory.freezeConfig(writeConfig = config.getState('init', detail = 'config'))
workflow.run() # will get control back when batch running has finished


makecat_task_id = config.get("task id")


makecat_output = os.path.join(os.environ["HOME"], "tth/gc/makecategory", makecat_task_id)

print makecat_output


