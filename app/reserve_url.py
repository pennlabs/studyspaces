import sys, os
from urllib import urlencode
# pretty painful way to get library map imported
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__),"../availability_cron")))
from library_map import library_map, library_name_to_ids

PENN_LIBRARY_BASE_URL = "http://bookit.library.upenn.edu/cgi-bin/rooms/rooms?"
HUNTSMAN_BUILDING_NAME = "Jon M. Huntsman Hall"
WHARTON_SPIKE_BASE_URL = "http://spike.wharton.upenn.edu/Calendar/gsr.cfm?"

def library_name_to_shortlib(name):
  prefix = name.split(":")[0]
  prefix_map = {"USC" :"vpusc",
                "Lipp":"lippincott",
                "WIC" :"vp",
                "VP"  :"vp34"
               }
  return prefix_map[prefix]

def get_reserve_url(room, day, time_from, time_to):
  """Figures out where to send the user if they click the "reserve" button"""
  ss_to_library = dict([(v,k) for k, v in library_map().iteritems()])
  # when passing library argument to IDs 
  library_to_ids = dict([(v,k) for k, v in library_name_to_ids().iteritems()])
  key = (room.name, room.kind.building.name)

  if key in ss_to_library: # set up parameters for library
    library_name = ss_to_library[key]
    library_id = library_to_ids[library_name]
    date = day.strftime("%A, %B %d, %Y")
    time = "%d:%02d" % (time_from/100, time_from%100)
    (hour_diff, min_diff) = (time_to/100 - time_from/100,
                             time_to%100 - time_from%100)
    num_people = room.kind.max_occupancy
    duration = 60*hour_diff + min_diff
    return PENN_LIBRARY_BASE_URL + urlencode((
              ("library", library_name_to_shortlib(library_name)),
              ("date", date),
              ("inquiry", "roomBook"),
              ("dev", 0),
              ("roomid", library_id),
              ("time", time),
              ("length", duration),
              ("numPeople", num_people)))
  elif room.kind.building.name == HUNTSMAN_BUILDING_NAME:
    #Huntsman Deep Linking
    date = day.strftime("%m/%d/%Y")
    time = "%02d:%02d" % (time_from/100, time_from%100)
    (hour_diff, min_diff) = (time_to/100 - time_from/100,
                             time_to%100 - time_from%100)
    duration = 60*hour_diff + min_diff
    return WHARTON_SPIKE_BASE_URL + urlencode((
              ("date", date),
              ("start_time", time),
              ("duration", duration),
              ("room_number", room.name)))
    # TODO: verify that things on the G floor work
  #else no deep linking
  return room.kind.reserve_url
