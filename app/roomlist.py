from models import *
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from datetime import date
import time
from availability_display import availability_display # this is a View
from app.room_search import (search_and_rank_rooms, group_rooms_by_roomkind,
                             model_id_dict, get_availabilities_many)
import json
from reserve_url import get_reserve_url
from urllib import urlencode

# Testing precommit hook

class StudySpacesEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, RoomKind):
      return {"name": obj.name,
              #"building": obj.building.name,
              "reserve_type": obj.reserve_type,
              "max_occupancy": obj.max_occupancy,
              "has_computer": obj.has_computer,
              "has_big_screen": obj.has_big_screen,
              "has_whiteboard": obj.has_whiteboard,
              "privacy": obj.privacy,
              "comments": obj.comments,
              "rooms": obj.rooms}
    elif isinstance(obj, Building):
      return {"name": obj.name,
              "latitude": obj.latitude, "longitude": obj.longitude,
              "roomkinds": obj.roomkinds}
    elif isinstance(obj, Room):
      try:
        av = obj.availabilities
      except:
        av = None
      return {"name": obj.name, "id": obj.id, "availabilities": av}
    elif isinstance(obj, TimeRange):
      return (obj.start, obj.end)
    elif isinstance(obj, date):
      return obj.strftime("%Y-%m-%d")
    return json.JSONEncoder.default(self, obj)

def annotate_buildings(roomkinds):
  """ Given a list of RoomKinds, prefetch the Building field for each one. 
      Returns a list of all fetched Buildings.
      (The RoomKinds are updated in-place.)

      Also: in each Building, add a "roomkinds" variable, containing a list of
        RoomKinds for that Building.
      
      The input argument must be a list, not an arbitrary iterable. ??? """
  
  bd_ids = set(rk.building_id for rk in roomkinds)
  bd_map = model_id_dict(Building, bd_ids)
  bd_list = list(bd_map.values())
  for bd in bd_list:
    bd.roomkinds = []
  for rk in roomkinds:
    rk.building = bd_map[rk.building_id]
    rk.building.roomkinds.append(rk)
  return bd_list

def deeplink_url(room_id, date, start, end):
  """ Compute the proper deep linking reservation url for a room """
  return "deeplink?" + urlencode((("date",      date.strftime("%Y-%m-%d")),
                                  ("time_from", start),
                                  ("time_to",   end),
                                  ("room",      room_id)))

def roomlist(request):  
  """ajax request that finds available rooms by filters. also handles API"""
  reserve_urls = {}
  if 'showall' in request.GET:
    # == return all the rooms
    rk_map_items = group_rooms_by_roomkind(Room.objects.all()).items()
    # note: we will only return buildings that actually have rooms.

    # adding reservation urls to the data being passed to template
    for (rk, l) in rk_map_items:
      rk.deeplink_reserve_url = rk.reserve_url
      #TODO: we should never use rk.reserve_url, it's deprecated for outward-
      #  facing urls
      
  else:
    # == return only relevant rooms
    rk_list = RoomKind.objects
   
    num_people = request.GET['capacity'] 
    # filter by options
    if 'capacity' in request.GET:
      rk_list = rk_list.filter(max_occupancy__gte=num_people)    
    if 'private' in request.GET:
      rk_list = rk_list.filter(privacy__exact='P')
    if 'whiteboard' in request.GET:
      rk_list = rk_list.filter(has_whiteboard__exact=True)
    if 'computer' in request.GET:
      rk_list = rk_list.filter(has_computer__exact=True)
    if 'monitor' in request.GET:
      rk_list = rk_list.filter(has_big_screen__exact=True)       
    
    # prepare date/time filter variables
    startTime = int(request.GET['shr'])*100 + int(request.GET['smin'])
    endTime = int(request.GET['ehr'])*100 + int(request.GET['emin'])
    
    unixtime = int(request.GET['date'])/1000
    unixtime = time.localtime(unixtime)
    filter_date = date(unixtime.tm_year, unixtime.tm_mon, unixtime.tm_mday)
    
    # put all rooms that satisfy non-time-based conditions...
    r_list = list(Room.objects.filter(kind__in=(rk_list)))
    
    # rk_map_items - list of (room_kind, list_of_its_rooms) tuples, 
    #                all with the same room kind.
    #                ordered by the proper order they should appear in
    rk_map_items = search_and_rank_rooms(start__lte=startTime, 
                                         end__gte=endTime, 
                                         date=filter_date, 
                                         room_list=r_list)

    # adding reservation urls to the data being passed to template
    for (rk, l) in rk_map_items:
      rk.deeplink_reserve_url = deeplink_url(l[0].id, filter_date,
                                             startTime, endTime)


  # bd_list - list of relevant building objects (for map)
  bd_list = annotate_buildings([rk for (rk,l) in rk_map_items])
  bd_reservable_dict = dict((bd, bd.has_reservable_rooms())
                             for bd in bd_list) # TODO slow?

  format = request.GET.get('format', '')
  if format.startswith('json'):
    is_html = format == 'jsonhtml'
    indent_amt = 2 if is_html else None
    
    for (roomkind, list_of_rooms) in rk_map_items:
      roomkind.rooms = list_of_rooms

    json_obj = {'buildings': bd_list}

    days = [date.today() + datetime.timedelta(days=i) for i in range(0,3+1)]
    for (r, av) in get_availabilities_many([r for (k,v) in rk_map_items
                                            for r in v], days):
      av = dict((k.strftime("%Y-%m-%d"), v) for (k,v) in av.iteritems())
      r.availabilities = av
    j = json.dumps(json_obj, cls=StudySpacesEncoder, indent=indent_amt)
    if is_html:
      j = "<html><head/><body><pre>%s</pre></body></html>" % j
    return HttpResponse(j)
  else:
    contextd = {
      'rk_map_items': rk_map_items,
      'bd_reservable_dict': bd_reservable_dict,
    }
    t = loader.get_template('roomlist.html')
    return HttpResponse(t.render(Context(contextd)))
