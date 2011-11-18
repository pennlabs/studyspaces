#sample fetcher to see if the system works
from BeautifulSoup import BeautifulSoup
import codecs
import random

B_SAMPLE = '3913 Baltimore'

def fetch_updates(date):
  if date.month == 4 and date.day == 1:
    return {("PennApps Headquarters", B_SAMPLE): [(0,2400)]}
  else:
    return {}
