from app.models import (Room, RoomKind, Building, WeeklyAvailability,
                        FreeTimeRange)
from collections import defaultdict

#TODO move to the utilities library once it exists
def build_dict(l, f):
  """ Given an iterable l and a function f that returns a (key, val)
      tuple for each element of l, return a dictionary
      {k: [all val that match k]}
      
      The values in each list appear in the same order as in l. """
  d = {}
  for i in l:
    (k, v) = f(i) 
    if k not in d:
      d[k] = [v]
    else:
      d[k].append(v)
  return d

def get_availabilities_many(room_list, date_list):
  """ Given an iterable of rooms room_list and an iterable of dates date_list,
      return a list [(room, {date: (weeklyav, [fetchedav...])...})...]
        (room is a Room
         date is a datetime.date (or whatever was in date_list)
         weeklyav is a TimeRange, or None on failure
           (note: failure shouldn't happen)
         [fetchedav] is a list of TimeRanges, or None if no FetchedAvailability
           could be found (e.g. for non-reservable rooms)
  """
  # fetchedranges_all_dict = {(room_id, date): [time ranges...]}
  ftr_all = (FreeTimeRange.objects.filter(availability__room__in=room_list,
                                          date__in=date_list).
             select_related('availability__room_id').order_by('time'))
  ftrmap = lambda i: ((i.availability.room_id, i.date), i.time)
  fetchedranges_all_dict = build_dict(ftr_all, ftrmap)
  
  # weeklyrange_all_dict = {roomkind_id: [weekly availabilities...]}
  #   (there should be exactly one weekly availability in each list)
  roomkinds = RoomKind.objects.filter(room__in=room_list)
  wr_all = WeeklyAvailability.objects.filter(room_type__in=roomkinds)
  weeklyrange_all_dict = build_dict(wr_all, lambda i: (i.room_type_id, i))
  
  def roomdata(r, d):
    """ Return (weekly, fetched) availabilities for a (room, date) pair,
        returning None for either if it can't be found. """
    try:
      wd = d.weekday()
      weekly = weeklyrange_all_dict[r.kind_id][0].time_range_by_weekday(wd)
    except LookupError:
      weekly = None
    fetched = fetchedranges_all_dict.get((r.id, d), None)
    return (weekly, fetched)
 
  all_availabilities = []
  for r in room_list:
    av = dict((d, roomdata(r, d)) for d in date_list)
    all_availabilities.append((r, av))

  return [(r, dict((d, roomdata(r, d)) for d in date_list)) for r in room_list]

def model_id_dict(modelclass, idlist=None):
  """ Given a model class (e.g. Room), and an optional iterable of ids,
      return a dictionary {id: model object} """
  # TODO look into django in_bulk method
  insts = modelclass.objects.all()
  if idlist is not None:
    insts = insts.filter(id__in=idlist)
  return dict((m.id, m) for m in insts)

def group_rooms_by_roomkind(roomlist):
  """ Given a list of rooms, return a dictionary
      {roomkind: [list of rooms for that roomkind]}
  """
  kind_map = model_id_dict(RoomKind, set(r.kind_id for r in roomlist))

  rk_map = defaultdict(list)
  for room in roomlist:
    rk_map[kind_map[room.kind_id]].append(room)
  return rk_map

def search_and_rank_rooms(**kwargs):
  """ Wraps search_rooms_by_time, incorporating our ranking function for order.
      Uses same arguments as search_rooms_by_time
      Returns a sorted list of (RoomKind, [Room]) tuples that are available
  """
  # first, filter the rooms using a sql query
  filtered_list = list(search_rooms_by_time(**kwargs))

  # group rooms by their roomkind
  rk_map = group_rooms_by_roomkind(filtered_list)
  rk_map_items = rk_map.items()

  # rank the mapped rooms by their decided order
  rk_map_items.sort(key=rank_room)

  return rk_map_items

def rank_room(rk_item):
  """ Returns an tuple of comparables values (compare first tup, then second...)
      giving a value for each room kind during ranking
  """
  rk, rlist = rk_item
  reserve_map = {'N': 10, 'E': 0}
  # ranking algorithm: smaller rooms are better, reservable is better
  return (reserve_map[rk.reserve_type] + rk.max_occupancy)

def search_rooms_by_time(start__gte=None, start__lte=None,
                         end__gte=None, end__lte=None,
                         date=None, room_list=None):
  """ Search for rooms that are available at some time. Input:
      start__lte - room opens at this time or earlier (4 digit int 0000-2400)
      end__gte - room closes at this time or later (4 digit int 0000-2400)
        (start__gte and end__lte also work but are less useful)
      date - the room is open on this date (datetime.date object) REQUIRED
      room_list - an iterable of Room objects the search should be restricted to

      Returns: an iterable of rooms as search results

      Sample: 
        d = datetime.date.today()
        rl = Room.objects.filter(name__startswith="34")
        rl = search_rooms_by_time(start__lte=2200, date=d, room_list=rl)
  """

  #TODO TODOTODOTODO stop sql injection

  #data = start*10000 + end
  #filter for rooms available at that time within reservation periods
  fetched_filters = generate_filters("time", start__gte, start__lte, 
                                             end__gte, end__lte)
  if date is not None: fetched_filters.append(
    "date='%s'" % date.strftime('%Y-%m-%d'))
  fetched_filters_str = filter_str(fetched_filters)

  #filter for opening/closing hours within range 
  #TODO: some fun holiday stuff here
  weekday = ("monday", "tuesday", "wednesday", "thursday", "friday", 
                   "saturday", "sunday")[date.weekday()]
  weekly_filters = generate_filters(weekday, start__gte, start__lte,
                                             end__gte, end__lte)
  weekly_filters_str = filter_str(weekly_filters)

  """ Search for rooms that:
      a) Has a reservation system and has space, OR has no reservation system
  AND b) have opening hours that include the query time """ 
  
  query =  ("""SELECT * from app_room WHERE (
                 id IN ( 
                   SELECT room_id FROM app_fetchedavailability WHERE id IN (
                     SELECT availability_id FROM app_freetimerange WHERE %s
                   )
                 ) OR kind_id IN (
                   SELECT id FROM app_roomkind WHERE reserve_type = "N"
                 )
               ) AND kind_id IN (
                 SELECT room_type_id FROM app_weeklyavailability WHERE %s
               )"""
              % (fetched_filters_str, weekly_filters_str))
 
  #print query
  
  db_rooms = Room.objects.raw(query)

  if room_list is None:
    return db_rooms
  else: #array intersection
    room_id_set = set(r.id for r in room_list)
    return [r for r in db_rooms if r.id in room_id_set]

def filter_str(filter_list):
  if len(filter_list) == 0:
    return "1"
  else:
    return " AND ".join(filter_list)

def generate_filters(row_name, start__gte=None, start__lte=None,
                           end__gte=None, end__lte=None):
  filters = []
  if start__gte is not None: filters.append(
    "%s>=%d" % (row_name, start__gte*10000))
  if start__lte is not None: filters.append(
    "%s<=%d" % (row_name, start__lte*10000 + 9999))
  if end__gte is not None: filters.append(
    "MOD(%s,10000)>=%d" % (row_name, end__gte))
  if end__lte is not None: filters.append(
    "MOD(%s,10000)<=%d" % (row_name, end__lte))
  return filters
