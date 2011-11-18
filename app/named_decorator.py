# defined outside of class to avoid disambiguation
def __unicode__(self):
  return self.name
def Named(model):
  """decorator: Adds default __unicode__ implementation to return self.name"""
  model.__unicode__ =__unicode__ 
  return model
