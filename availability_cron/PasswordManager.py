import json
import base64

"""

Passwords are protected by several layers of security by obscurity.

passwords_path_path is a file in this directory, containing one line, 
which is a path. This file should not be checked into the repo.

This path is a file containing a JSON object with password info:

{
  "passwords" : {
    "identifier-1": {
      "username": "USERNAME",
      "password_base64": "password+encoded+in+base64" 
    },
    ...
  }
}

base64.b64encode can be used for encoding.

"""

passwords_path_path = "passworddbpath.txt"

def getcredentials(key):
  """Return a tuple (username, password) for the given identifier."""
  passwords_path = open(passwords_path_path).readlines()[0].strip()
  passworddb = json.load(open(passwords_path))["passwords"]
  creds = passworddb[key]
  username = creds["username"]
  password = base64.b64decode(creds["password_base64"])
  return (username, password)
