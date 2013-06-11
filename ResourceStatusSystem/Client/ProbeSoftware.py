'''
Created on Jun 11, 2013

@author: stephane
'''
from DIRAC import S_OK, S_ERROR, gConfig, gLogger
from GlastDIRAC.ResourceStatusSystem.Client.SoftwareTagClient import SoftwareTagClient
import os
from GlastDIRAC.ResourceStatusSystem.Client.ProbeSoftwareArea import getMappingTagToDirectory
#from GlastDIRAC.ResourceStatusSystem.Client.ProbeSoftwareArea import getMappingTagFromDirectory
class ProbeSoftware(object):
    '''
    This module probes the software area to find the specified tag
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.tag  =''
        self.stc = SoftwareTagClient()
        #site = siteName()
        self.ce = ''
        self.log = gLogger.getSubLogger('ProbeSoftwareArea')

    def getParameters(self):
        if 'tag' in self.step_commons:
            self.tag =  self.step_commons['tag']
        else:
            return S_ERROR("Tag not defined")
          
        self.ce = gConfig.getValue('/LocalSite/GridCE', '')
        if not self.ce:
          return S_ERROR("CE undefined, cannot proceed")    
        return S_OK()
    
    def execute(self):
        """ Called by the Workflow machinery
        """
        
        res = self.getParameters()
        if not res['OK']:
            return res

        if not 'VO_GLAST_ORG_SW_DIR' in os.environ:
            res = self.stc.updateCEStatus("", self.ce, "Bad")
            if not res['OK']:
                return S_ERROR("Failed to report Bad site, missing software area.")
            return S_ERROR("Missing VO_GLAST_ORG_SW_DIR environment variable")
    
        base_sw_dir = os.environ['VO_GLAST_ORG_SW_DIR']
        
        self.log.notice("Found the following software directory:", base_sw_dir)
        message = None
        
        directory_list = []  
        for root, dirnames, files in os.walk(os.path.join(base_sw_dir,"glast/ground/releases")):
            if "bin" in dirnames:
                directory_list.append(root)
         
        res = getMappingTagToDirectory(self.tag)
        tag_dir = os.path.join(base_sw_dir, res["Value"])
        self.log.info("Tag should be at", tag_dir)
        if tag_dir in directory_list:
            self.log.info("Found tag directory")
            res = self.stc.updateCEStatus(self.tag, self.ce, 'Valid')
            if not res['OK']:
                self.log.error("Failed to report back:", res['Message'])
                message = res['Message']
            else:
                self.log.notice("Tag now Valid!")
        
        #for directory in directory_list:
        #    self.log.notice("Decoding %s and tries to make a tag out of it" % directory)
        #    #Need mapping between Tag name and local software directory name
        #    res = getMappingTagFromDirectory(directory)
        #    if not res['OK']:
        #        self.log.error("Failed finding relation between directory and Tag")
        #        continue
        #    tag = res['Value']
        #    self.log.notice("Found tag ", tag)
        #    res = self.stc.updateCEStatus(self.tag, self.ce, 'Valid')
        #    if not res['OK']:
        #        self.log.error("Failed to report back: %s" %res['Message'])
        #        message = res['Message']
        #    else:
        #        self.log.notice("Tag now Valid!")
        
        if message:
            return S_ERROR(message)
        
        return S_OK()
        