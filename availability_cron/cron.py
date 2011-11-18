#!/usr/bin/python

# This script runs every 5 minutes.
# What it does: finds every file starting w/ fetch_ in its current directory,
# This file must contain:
#    a method fetch_updates(date)
# The script will import that file and calls the fetch_foo.fetch_updates(date) 
# method on every day in the coming week or two.
#
# fetch_updates(date) specification: 
#   input: date - datetime.date object
#   returns: a dictionary
#     ("room name", "building name") -> [list of time_ranges]
#     the room names must be exactly the same as room names in the database
#   where time_range is a tuple (from, to), each being a 4-digit int. 
#     e.g. (1330, 1530)
#
# The script then updates the availabilities of the relevant rooms

LOOK_AHEAD_DAYS = 7
# LOOK_AHEAD_DAYS = 7

#problem - cross-day availabilities (IE, book 2330-0030)  
# temporary solution: when searching for space, consider the 
# cross-day as an explicit 'OR' 

from datetime import date, datetime, timedelta
import sys, os
sys.path.append("..")
sys.path.append("../..")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from app.models import Room, RoomKind, Building, FreeTimeRange
from app.models import create_FetchedAvailability, FetchedAvailability
from glob import glob
import imp

def get_fa_for_room(building_name, room_name):
  """ Returns a FetchedAvailability corresponding to a given room. """
  #TODO: move to models.py?
  building = Building.objects.get(name=building_name)
  rooms = (Room.objects.filter(kind__building=building)
                       .filter(name=room_name))
  if len(rooms) != 1:
    errmsg = ("%d rooms with name %s in building %s (expected 1)" % 
              (len(rooms), room_name, building_name))
    raise Exception(errmsg)
  room = rooms[0]
  avail_set = room.fetchedavailability_set.all()
  if len(avail_set) == 0: # object needs to be created
    avail_set = [create_FetchedAvailability(room)]
  return avail_set[0]

def get_db_avails(building_name, room_name, date):
  """Queries django for the current list of time_ranges of when that room is
     free on that date (string in YYYY-MM-DD format or datetime.date) 
     
     Returns: list of time_ranges (NOT a list of FreeTimeRanges)"""
  # 1. find room. 2. find avail object. 3. get avails filtered by date.
  fa = get_fa_for_room(building_name, room_name)
  freetimeranges =  fa.freetimerange_set.filter(date=date)
  return [(ftr.time.start, ftr.time.end) for ftr in freetimeranges]

def update_avails(building_name, room_name, date, new_avails):
  """Updates DB with the new list of time_ranges, deleting the old list
     Note: This can cause some faulty DB data at some point, but just for one 
     room. That's an acceptable and rare error"""
  # note: potentially, in the future, queue these up and then exec all of 'em
  fa = get_fa_for_room (building_name, room_name) 
  # remove old
  for old_avail in fa.freetimerange_set.filter(date=date):
    old_avail.delete()
  # add new
  for new_avail in new_avails:
    (na_from, na_to) = new_avail
    time = na_from * 10000 + na_to
    FreeTimeRange(availability=fa, date=date, time=time).save()

def try_update(datastr, building_name, room_name, fetchdate, fetched_avails):
  db_avails = get_db_avails(building_name, room_name, fetchdate)
  if set(db_avails) != set(fetched_avails):
    print "updating %s" % datastr
    update_avails(building_name, room_name,
                  fetchdate, fetched_avails)
  else:
    print "skipped %s (no change)" % datastr

#---------------------- MAIN CODE:

def main():
  # if dry run is on, no availability changes will be made to the database.
  # warning: even with dry-run on, minor changes may be made to the database
  # (e.g. adding an empty fetchedavailability)
  dry_run = '--dry-run' in sys.argv

  for filename in glob("fetch_*.py"):
    print "==== Current time: %s ====" % datetime.now()
    print "==== LOADING FETCHER %s ====" % filename 
    try:
      fetcher = imp.load_source('fetcher', filename)
      run_scraper(fetcher, dry_run)
    except Exception as e:
      print "==== FAILURE ===="
      print e
      import traceback
      traceback.print_exc()
    print

def run_scraper(fetcher, dry_run=False):
  #every day in the coming week....
  today = date.today()
  for fetchdate in [today + timedelta(days=x) for x in range(LOOK_AHEAD_DAYS)]:
    all_fetched_avails = fetcher.fetch_updates(fetchdate)
    #every room....
    for room_tuple, fetched_avails in all_fetched_avails.iteritems():
      (room_name, building_name) = room_tuple
      datastr = "%s/%s (%s)" % (building_name, room_name, fetchdate)
      
      #update avails if out of date
      try:
        if not dry_run:
          try_update(datastr, building_name, room_name, fetchdate, fetched_avails);
      except Exception as e:
        print "FAILED %s\n  %s" % (datastr, e)

if __name__ == "__main__":
  main()
