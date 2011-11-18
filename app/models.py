from django.db import models
from studyspaces.app.named_decorator import Named
from studyspaces.app.TimeRange import *
from django.contrib.localflavor.us.models import PhoneNumberField

# Todo: potentially just 'import' the Registrar API for this model?

@Named
class Building(models.Model):
  name = models.CharField(max_length=80)
  latitude = models.FloatField(default=13.37)
  longitude = models.FloatField(default=42)
  def has_reservable_rooms(self): 
      return len(filter((lambda k: k.reserve_type == 'E'), self.roomkind_set.all())) > 0
    

  
@Named
class RoomKind(models.Model):
  # to add: contact person (phone/email?)
  building       = models.ForeignKey(Building)
  name           = models.CharField(max_length=80) #IE, gsr
  RESERVATION_CHOICES = (
    ('N', 'No reservation system available (first-come-first-serve)'),
    ('E', 'External Reservation System (IE, Huntsman GSRs)'),
    #('W', 'Location uses our own white-labeled reservation system'),
  )
  reserve_type   = models.CharField(max_length=1, choices=RESERVATION_CHOICES)
  reserve_url    = models.CharField(max_length=512, default='',  help_text="""Web address for room reservations""")
  
  max_occupancy  = models.IntegerField(
    blank=True, null=True, help_text="For large shared spaces, feel free to estimate")
  PRIVACY_LEVEL  = (
    ('S', 'Common Space'),
    ('P', 'Private Room'),
  )
  privacy        = models.CharField(max_length=1, choices=PRIVACY_LEVEL)
  #to add: image ? (using ImageField)
  has_computer   = models.BooleanField()
  has_big_screen = models.BooleanField(help_text="Such as a projector or a flat-screen TV")
  has_whiteboard = models.BooleanField()
  #potentially more attributes here, including things like 'is wharton'

  #contact info
  contact_name  = models.CharField(max_length=40)
  contact_phone = PhoneNumberField(blank=True, null=True, help_text="""This 
should be a number that students can call if they have questions about 
availability at a given time""")
  contact_email = models.EmailField(blank=True, null=True, help_text="""
Will be used for internal communications by the StudySpaces team""")
 
  #comments
  comments      = models.TextField(blank=True, help_text="""
We'd love your feedback on what you think this form is missing (IE, is there
some particular attribute of your study space that students should be able
to filter by (IE, are drinks allowed).  This is also a good place to leave
any questions you may have about the StudySpaces project.""")

class Room(models.Model):
  kind = models.ForeignKey(RoomKind)
  name = models.CharField(max_length=80) #IE, 412

class FetchedAvailability(models.Model):
  """ A list of availabilities (corresponding to one room) as retrieved by
      a scraper. Availabilties can be found in FreeTimeRange objects. 
  """
  room = models.ForeignKey(Room)
  # default: building|roomkind|roomname
  def __unicode__(self):
    return "%s|%s|%s" % (self.room.kind.building.name,
                         self.room.kind.name,
                         self.room.name)
  
def create_FetchedAvailability(room):
  """ Create and save a FetchedAvailability object for a given room. """
  # TODO: The room should have a fetchedavailability field, and
  #       the fetchedavailability should (maybe) have no fields (as a room
  #       only has one FA at any given time) . remember to update cron 
  #       accordingly.
  fa = FetchedAvailability(room=room)
  fa.save()  
  return fa

#used by fetchedavailability
class FreeTimeRange(models.Model):
  availability = models.ForeignKey(FetchedAvailability)
  date = models.DateField()
  time = TimeRangeField()

  def __unicode__(self):
    return "%s (%s)" % (self.time, self.date) 

class WeeklyAvailability(models.Model):
  room_type = models.ForeignKey(RoomKind) #for now
  # eventually, here: potential link to holiday rules for exceptions
  # note: for special holidays, these can be null
  monday    = TimeRangeField()
  tuesday   = TimeRangeField()
  wednesday = TimeRangeField()
  thursday  = TimeRangeField()
  friday    = TimeRangeField()
  saturday  = TimeRangeField()
  sunday    = TimeRangeField()

  def days(self):
    return (self.monday,self.tuesday,self.wednesday,self.thursday,self.friday,
            self.saturday,self.sunday)
  names = ("M","T","W","R","F","S","U") 

  def __unicode__(self):
    """for now: just the daily availabilities, joined"""
    return ", ".join(["%s%s" % (tup[0], unicode(tup[1])) for tup 
                    in zip(self.names, self.days()) 
                    if tup[1] is not None])

  def time_range_by_weekday(self, day_of_week):
    """returns zero-indexed TimeRangeField object (Wed=2, etc)"""
    return self.days()[day_of_week]
  
#eventually, special schedule stuff:
#class SpecialSchedules(models.Model) ...
#class HolidayList(models.Model) #each holiday has a date range and 
# potentially details for overriding default availability
# if we don't have what to override with, we display a warning instead
