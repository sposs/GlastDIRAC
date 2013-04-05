"""
Client for the glast software tables
Exposes for free the methods 

getSitesForTag(tag)
getTagsAtSite(tag)
addTagAtSite(tag,site)
removeTagAtSite(tag,site)

"""

from DIRAC.Core.Base.Client                               import Client

class GlastClient (Client):
  """ Client of the GlastHandler.
  """
  def __init__(self, **kwargs ):
    Client.__init__(self, **kwargs )
    self.setServer("Glast/Glast")
