import WMCore
import WMCore.FwkJobReport
from WMCore.FwkJobReport.Report import Report
report = Report("cmsRun")
report.parse('FrameworkJobReport.xml', "cmsRun")
