# Seas-specific scraper, using BeautifulSoup.
# Seas allows users to book rooms at any point in the future.

from BeautifulSoup import BeautifulSoup
import mechanize
import codecs, urllib2, datetime, time, re

# Create browser instance for mechanize
br = mechanize.Browser()

# Mappings from room codes parsed to room names in database
B_LEVINE = "Levine Hall"

roommappings = {
"CIS_Levine_307_Public": ("Levine Hall Conference Room 307", B_LEVINE),
"CIS_Levine_315_Public": ("Levine Hall Conference Room 315", B_LEVINE),
"CIS_Levine_512_Public": ("Levine Hall Conference Room 512", B_LEVINE),
"CIS_Levine_612_Public": ("Levine Hall Conference Room 612", B_LEVINE),
"Dean_Levine_Lobby_Public": ("Levine Hall Lobby and Mezzanine", B_LEVINE),
"Dean_Wu_Chen_Public": ("Levine Hall Room 101 - Wu and Chen Auditorium", B_LEVINE),
}      

def fetch_updates(date):
  availabilities = {} # map from room_name => (start_time, end_time) tuples
  for room in roommappings:    
    # Construct dynamic availability url based on input date and room
    availability_url = 'https://cal.seas.upenn.edu/?CalendarName=%s&Op=ShowIt&NavType=Absolute&Date=%s/%s/%s&Amount=Day&Type=Block' % (room, str(date.year), str(date.month), str(date.day))
    # translates to database mappings
    availabilities[roommappings[room]] = parse_room(availability_url)
  return availabilities
  
def parse_room(a_url):
  f = br.open(a_url)
  data = f.read()
  avails = parse_seas_calendar(data)    # parse from seas calendar
  return avails

# returns a list of tuples of free times
def parse_seas_calendar(html_uni):
  """Input: seas html page.
     Output: Map of [room_name => list of freetime_tuples (start, end)
                                  each time_block being a 4-digit num, IE 0830)
  """ 
  soup = BeautifulSoup(html_uni)
  unavailable_times = soup.findAll('span', {'class':'TimeLabel'})
  formatted = []
  for i in unavailable_times:
    # times is of the general format "hh:mmAM - hh:mmPM"
    times = str(i.contents[0]).strip()
    # groups the start and end times apart
    m = re.match(r"(\w{1,2}:\w{4}) - (\w{1,2}:\w{4})", times)
    # to hold 4-digit tupled version of unavailable times
    formatted_time = []
    for j in range(2):
      temp = m.group(j+1).split(":")
      time = int(temp[0])*100+int(temp[1][:-2])
      if m.group(j+1)[-2:] == "pm" and not temp[0] == "12":
        time += 1200
      formatted_time.append(time)
    formatted.append(tuple(formatted_time))
  unique_hours = []
  if len(formatted) > 0:
    hours = []
    # finds complementary time slots such that we now have a list of available times
    hours.append((0000,formatted[0][0]))
    for i in range(len(formatted)-1):
      hours.append((formatted[i][1],formatted[i+1][0]))
    hours.append((formatted[len(formatted)-1][1],2400))
    # removes inconsistencies produced in the complementing process
    for i in hours:
      if i[0] != i[1] and i[0] < i[1]:
        unique_hours.append(i)
  else:
    #if there are no unavailable time slots, the whole day is open
    unique_hours.append((0000,2400))
  return unique_hours
