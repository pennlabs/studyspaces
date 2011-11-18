import django
def fetch_updates(date):
  """
     purpose: get all of this type's availability for that date.
     date: python Date object
     return: a dictionary from (django) Room objects -> list of time_ranges
     time_range: tuple (from, to), each being a 4-digit int. IE, (1330, 1530)
  """
  
