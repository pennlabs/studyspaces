import datetime
from datetime import date
import urllib2
import json

json_url = 'http://spike.wharton.upenn.edu/webservices/api/v0.1/gsrs/?apiKey=WHARTONAPIKEY'
B_HUNTSMAN = 'Jon M. Huntsman Hall'
rooms = {'241': ('241', B_HUNTSMAN),
         '242': ('242', B_HUNTSMAN),
         '243': ('243', B_HUNTSMAN),
         '246': ('246', B_HUNTSMAN),
         '247': ('247', B_HUNTSMAN),
         '248': ('248', B_HUNTSMAN),
         '251': ('251', B_HUNTSMAN),
         '252': ('252', B_HUNTSMAN),
         '256': ('256', B_HUNTSMAN),
         '257': ('257', B_HUNTSMAN),
         '258': ('258', B_HUNTSMAN),
         '261': ('261', B_HUNTSMAN),
         '262': ('262', B_HUNTSMAN),
         '266': ('266', B_HUNTSMAN),
         '267': ('267', B_HUNTSMAN),
         '268': ('268', B_HUNTSMAN),
         '276': ('276', B_HUNTSMAN),
         '277': ('277', B_HUNTSMAN),
         '278': ('278', B_HUNTSMAN),
         '341': ('341', B_HUNTSMAN),
         '342': ('342', B_HUNTSMAN),
         '343': ('343', B_HUNTSMAN),
         '346': ('346', B_HUNTSMAN),
         '347': ('347', B_HUNTSMAN),
         '348': ('348', B_HUNTSMAN),
         '351': ('351', B_HUNTSMAN),
         '352': ('352', B_HUNTSMAN),
         '356': ('356', B_HUNTSMAN),
         '357': ('357', B_HUNTSMAN),
         '358': ('358', B_HUNTSMAN),
         '361': ('361', B_HUNTSMAN),
         '362': ('362', B_HUNTSMAN),
         '366': ('366', B_HUNTSMAN),
         '367': ('367', B_HUNTSMAN),
         '368': ('368', B_HUNTSMAN),
         '376': ('376', B_HUNTSMAN),
         '377': ('377', B_HUNTSMAN),
         '378': ('378', B_HUNTSMAN),
         'F46': ('F46', B_HUNTSMAN),
         'F47': ('F47', B_HUNTSMAN),
         'F51': ('F51', B_HUNTSMAN),
         'F52': ('F52', B_HUNTSMAN),
         'F56': ('F56', B_HUNTSMAN),
         'F57': ('F57', B_HUNTSMAN),
         'F61': ('F61', B_HUNTSMAN),
         'F62': ('F62', B_HUNTSMAN),
         'F66': ('F66', B_HUNTSMAN),
         'F67': ('F67', B_HUNTSMAN),
         'G51': ('G51', B_HUNTSMAN),
         'G56': ('G56', B_HUNTSMAN),
         'G57': ('G57', B_HUNTSMAN),
         'G58': ('G58', B_HUNTSMAN),
         'G61': ('G61', B_HUNTSMAN),
         'G62': ('G62', B_HUNTSMAN),
         'G66': ('G66', B_HUNTSMAN),
         'G67': ('G67', B_HUNTSMAN),
         'G68': ('G68', B_HUNTSMAN)
         }
def fetch_updates(date):
  # map from room_name => (start_time, end_time) tuples
  availabilities = {}
  page = urllib2.build_opener().open(json_url)
  json_str = page.read()
  json_dict = json.loads(json_str)
  
  #create string from requested date
  today = stringDate(date)
  yesterday = stringDate(date + datetime.timedelta(-1))
  
  today_dict = json_dict[today]
  yesterday_dict = {}
  if yesterday in json_dict:
    yesterday_dict = json_dict[yesterday]
  
  for room in today_dict:
    unavailable = []
    for time_dict in today_dict[room]:
      split = time_dict.partition('-')
      if int(split[0]) > int(split[2]):
        unavailable.append((int(split[0]), 2400))
      else:
        unavailable.append((int(split[0]), int(split[2])))
    if room in yesterday_dict:
      for time_dict in yesterday_dict[room]:
        split = time_dict.partition('-')
        if int(split[0]) > int(split[2]):
          unavailable.append((0, int(split[2])))
    #must sort each time list before this process
    unavailable = sorted(unavailable)
    availabilities[rooms[room.strip(' ')]] = invert(unavailable)
  for rtup in rooms.values():
    if rtup not in availabilities:
      availabilities[rtup] = [(0,2400)]
  return availabilities

# returns a string representing an input date in the form:
# YYYY-MM-DD
def stringDate(date):
  return date.strftime("%Y-%m-%d")

# takes a sorted list of unavailable times of the form:
# [(start, end), (start, end), ...]
# and returns the inverse (i.e. a list of tuples of available times)
def invert(unavailable):
  available = [] 
  if len(unavailable) > 0:
    hours = []
    # finds complementary time slots such that we now have a list of available times
    hours.append((0000,unavailable[0][0]))
    for i in range(len(unavailable)-1):
      hours.append((unavailable[i][1],unavailable[i+1][0]))
    hours.append((unavailable[len(unavailable)-1][1],2400))
    # removes inconsistencies produced in the complementing process
    for i in hours:
      if i[0] != i[1] and i[0] < i[1]:
        available.append(i)
  else:
    #if there are no unavailable time slots, the whole day is open
    available.append((0000,2400))
  return available

def main():
  print fetch_updates(date(2011,3,31))

if __name__ == "__main__":
  main()
