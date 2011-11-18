from django.db import models
from django.forms.widgets import *
from django.forms.fields import *
from django.contrib.admin.widgets import *
import datetime
# A top-to-bottom implementation of a TimeRange

# Introspection rules for South
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^studyspaces\.app\.TimeRange\.TimeRangeField"])

class TimeRange:
  def __init__(self,start,end,hr24=False):
    """From, To are 4-digit ints, IE 0800 = 8 am"""
    self.start = start
    self.end = end
    self.hr24 = hr24

  def start_str(self):
    return self.pretty_time(self.start)

  def end_str(self):
    return self.pretty_time(self.end)

  def pretty_time(self, val):
    return "%02i:%02i" % (int(val/100), val%100)

  def __unicode__(self):
    return "%s to %s" % (self.start_str(), self.end_str()) 

  def __repr__(self):
    return "[%s]" % (unicode(self))

  def toField(self):
    '''Converts to 8-digit int for parsing.'''
    return self.start * 10000 + self.end

def TimeRangeFromField(field_val):
  '''Takes an 8-digit int that indicates when a place is open from.'''
  if field_val==2400:
    return TimeRange(0000,2400,True)
  else:
    return TimeRange(field_val / 10000, field_val % 10000)

def EmptyTimeRange():
  return TimeRange(0, 0)

class TimeRangeField(models.Field):
  description = """An 8-digit int, IE 10002230 that indicates a place is 
                   open from, for example, 10:00 - 22:30"""

  __metaclass__ = models.SubfieldBase

  def get_internal_type(self): return "TimeRangeField"

  def db_type(self, connection): return "int"

  #read TimeRange from DB
  def to_python(self, value):
    if isinstance(value, TimeRange) or value is None:
      return value
    elif value == "":#user inputs empty string
      return EmptyTimeRange()
    elif type(value) in (int, long, str, unicode): #we have 8-digit integer:
      return TimeRangeFromField(int(value))
    else: 
      raise Exception("Can't convert %s of type %s to TimeRange" % 
                      (value, type(value)))

  #write TimeRange to DB
  def get_prep_value(self, value):
    return value.toField()

  def formfield(self, **kwargs):
    defaults = {'form_class' : TimeRangeFormField}
    defaults.update(kwargs)
    return super(TimeRangeField, self).formfield(**defaults)
  
class TimeRangeWidget(forms.MultiWidget):
  def __init__(self, attrs=None):
    hours = [(int(hour*100+minute), "%i:%02i%s" % 
             (hour%24, minute, " (+1 day)" if hour>23 else "")) 
              for hour in range(0,28) for minute in (0, 30)]    

    widgets = (forms.Select(attrs=attrs, choices=hours),
               forms.Select(attrs=attrs, choices=hours),
               CheckboxInput(attrs=attrs))
    super(TimeRangeWidget, self).__init__(widgets, attrs)

  def decompress(self, value):
    if value:
      return [value.start, value.end, value.hr24]
    return [800, 2200, False]
    

class TimeRangeFormField(MultiValueField):
  """Two Time Fields: from and to"""
  widget = TimeRangeWidget

  def __init__(self, *args, **kwargs):
    fields = (IntegerField(), IntegerField(), BooleanField())
    super(TimeRangeFormField, self).__init__(fields, *args, **kwargs)

  def compress(self, data_list):
    #todo: error handling
    if data_list[2]:
      return 2400
    else:
      return data_list[0] * 10000 + data_list[1]
