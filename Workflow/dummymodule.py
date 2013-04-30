'''
@since: Apr 30, 2013

@author: sposs
'''
from DIRAC import S_OK, gLogger

class dummymodule(object):
    '''
    This is a dummy module to show how this business works
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.something = ''
        self.log = gLogger.getSubLogger('DummyModule')
        
    def execute(self):
        """ Method called by the Workflow code
        """
        self.log.info("Something = ", self.something)
        
        if "MyParam" in self.workflow_commons:
            self.log.info("A workflow param:", self.workflow_commons["MyParam"] )
            
        return S_OK("All OK")