'''
Created on Jun 8, 2013

@author: stephane
'''

from DIRAC.Interfaces.API.Job import Job
from DIRAC import S_OK, S_ERROR
from DIRAC.Core.Workflow.Module import ModuleDefinition
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.Core.Workflow.Step import StepDefinition

class GlastJob(Job):
    '''
    classdocs
    '''


    def __init__(self,script = None, stdout = 'std.out', stderr = 'std.err'):
        '''
        Constructor
        '''
        super(GlastJob,self).__init__(script, stdout, stderr)
        
    def addTagValidation(self, tag = ''):
        """ Probe the software area for the given tag
        """
        if not tag:
            return S_ERROR("Tag not defined")
        tag = str(tag)

        stepDefn = 'ProbeStep'
        stepName = 'RunProbeStep'

        moduleName = 'ProbeSoftware'
        module = ModuleDefinition( moduleName )
        module.setDescription( 'The utility that calls the pipeline_wrapper.' )
        body = 'from GlastDIRAC.ResourceStatusSystem.Client.ProbeSoftware import ProbeSoftware\n'
        module.setBody( body )
        # Create Step definition
        step = StepDefinition( stepDefn )
        step.addModule( module )
        moduleInstance = step.createModuleInstance( 'ProbeSoftware', stepDefn )
        # Define step parameters
        step.addParameter( Parameter( "tag", "", "string", "", "", False, False, 'Tag to validate' ) )
        self.addToOutputSandbox.append( tag )
        self.workflow.addStep( step )

        # Define Step and its variables  
        stepInstance = self.workflow.createStepInstance( stepDefn, stepName )
        stepInstance.setValue( "tag", tag )
        
        return S_OK()
      
      
    def addWrapper(self, logFile = ''):
        """ Overload the DIRAC.Job.setExecutable
        """
        logFile = str(logFile)
        stepDefn = 'WrapperStep'
        stepName = 'RunWrapperStep'

        moduleName = 'GlastWrapperCall'
        module = ModuleDefinition( moduleName )
        module.setDescription( 'The utility that calls the pipeline_wrapper.' )
        body = 'from GlastDIRAC.PipelineSystem.Modules.GlastWrapperCall import GlastWrapperCall\n'
        module.setBody( body )
        # Create Step definition
        step = StepDefinition( stepDefn )
        step.addModule( module )
        moduleInstance = step.createModuleInstance( 'GlastWrapperCall', stepDefn )
        # Define step parameters
        step.addParameter( Parameter( "logFile", "", "string", "", "", False, False, 'Log file name' ) )
        self.addToOutputSandbox.append( logFile )
        self.workflow.addStep( step )

        # Define Step and its variables  
        stepInstance = self.workflow.createStepInstance( stepDefn, stepName )
        stepInstance.setValue( "logFile", logFile )

        return S_OK()
      