from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.Interfaces.API.Job import Job
from DIRAC.Interfaces.API.Dirac import Dirac
from DIRAC.Core.Workflow.Workflow import Workflow
from DIRAC.Core.Workflow.Module import ModuleDefinition
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.Core.Workflow.Step import StepDefinition

d = Dirac()

moduledefinition = ModuleDefinition("DummyModule")
moduledefinition.setBody("from GlastDIRAC.Workflow.dummymodule import dummymodule")#Tells the code where to get the class
moduledefinition.setDescription("This is a small and dummy module")
moduledefinition.addParameter(Parameter('something', '12', 'string',  "", "", False, False, "A dummy parameter"))

stepdefinition = StepDefinition("step_1")
stepdefinition.addModule(moduledefinition)

m1i = stepdefinition.createModuleInstance(moduledefinition.getType(), stepdefinition.getType())#This is needed!
#It's what creates the instance, it goes beyond definition
m1i.setValue('something', '14')#This is optional

wo = Workflow(name = 'a_test')
wo.addStep(stepdefinition)
stepInstance = wo.createStepInstance(stepdefinition.getType(), "step_1") #In fact this is used to create the instance
#so it is needed

#add a parameter to the global workflow, just because we can
wo.addParameter(Parameter("MyParam","SomeParam","string","","",False,  False, "a  workflow parameter"))
j = Job(script = wo)
d.submit(j)

