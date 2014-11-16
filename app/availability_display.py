from models import *
from django.template import Context, loader
from django.http import HttpResponse
from datetime import date, timedelta, datetime
from math import floor, ceil
from django.db.models import Count
from room_search import get_availabilities_many

BLOCKS_PER_HOUR = 4
BLOCKS_PER_DAY = BLOCKS_PER_HOUR * 24


def timeint2block(timeint, round='down'):
    """ convert a time integer (hour*100 + minute) to a block index, rounding
            either up or down """
    (hr, mn) = (timeint / 100, timeint % 100)
    hfloat = hr + mn / 60.0
    return int({'up': ceil, 'down': floor}[round](hfloat * BLOCKS_PER_HOUR))


def timerange2blockrange(timerange):
    """ convert a TimeRange to a list of block indices including that range """
    startidx = timeint2block(timerange.start, 'down')
    endidx = timeint2block(timerange.end, 'up')
    endidx = min(endidx, BLOCKS_PER_DAY)    # stop checking at midnight.
    # TODO: when getting timeranges, get the previous day's post-midnight range
    return range(startidx, endidx)


def hour2shortstr(timeint):
    """ convert an hour (in [0..23]) to a short string, e.g. "9a" for 9am """
    return "%d%s" % (1 + (timeint - 1) % 12, 'ap'[(timeint / 12) % 12])


def availability_display(request):
    t = loader.get_template('availability_display.html')
    ctex = {}  # context dictionary

    try:
        startdate = datetime.strptime(request.GET["date"], "%Y-%m-%d").date()
    except:
        startdate = date.today()

    roomid = request.GET.get("room", None)
    try:
        building = Room.objects.get(id=roomid).kind.building
        buildid = building.id
    except:
        buildid = request.GET.get("building", None)
        try:
                building = Building.objects.get(id=buildid)
        except:
                building = None

    if building is None:
        bdl = (Building.objects.annotate(
            rk=Count('roomkind__room', distinct=True),
            rkc=Count('roomkind', distinct=True))
            .filter(rkc__gt=0).order_by('-rk'))
        for b in bdl:
            # don't save!
            b.name = "%s (%d kinds, %d rooms)" % (b.name, b.rkc, b.rk)
        ctex['bd_list'] = bdl
    else:
        ctex['building'] = building
        display_list = []  # list of tuples:
        #  ('name', 'link', weekly TimeRange, [fetched TimeRange list...])
        if roomid is None:  # building view
            room_list = (Room.objects.filter(kind__building=building).
                         order_by('name').select_related('kind__reserve_type'))

            ctex['room_list'] = room_list
            room = None
            if len(room_list) == 0:
                ctex['errormsg'] = "No rooms found for this building."

            display_list = []
            for (room, avdict) in get_availabilities_many(room_list,
                                                          [startdate]):
                (weekly, fetched) = avdict[startdate]
                name = "%s (%s)" % (room.name, room.kind.reserve_type)
                link = "availability?room=%d" % room.id
                tup = (name, link, weekly, fetched or [])
                display_list.append(tup)

        else:  # room view
            room = Room.objects.get(id=roomid)
            ctex['room'] = room

            days = [startdate + timedelta(days=i) for i in range(-3, 4)]

            if FetchedAvailability.objects.filter(room=room).count() == 0:
                ctex['errormsg'] = "This room has no fetched availabilities."

            (_, avdict) = get_availabilities_many([room], days)[0]

            display_list = []
            for d in days:
                (weekly, fetched) = avdict[d]
                tup = (d.strftime("%a %m/%d"), None, weekly, fetched or [])
                display_list.append(tup)

        # render table
        if display_list:
            avail_data = [[0] * BLOCKS_PER_DAY for d in display_list]

            for (idx, (name, l, weeklyr, fetchedrs)) in \
                    enumerate(display_list):
                for a in fetchedrs:
                    for b in timerange2blockrange(a):
                        avail_data[idx][b] += 1
                for b in timerange2blockrange(weeklyr):
                    avail_data[idx][b] += 8

            # [0,1,8,9] -> [closed, BUG!, open/unavailable, open/available]
            ctex['headers'] = [hour2shortstr(x) for x in range(24)]
            ctex['blocks_per_hour'] = BLOCKS_PER_HOUR
            ctex['avail_table'] = zip([i[0:2] for i in display_list],
                                      avail_data)
    return HttpResponse(t.render(Context(ctex)))
