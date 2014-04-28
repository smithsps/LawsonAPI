class User:
  
  //name, username, timestamp
  def __init__(self, username, timestamp)
    self.username = username
    self.name = discovery.getName(username)
    self.timestamp = timestamp
    self.locations = []
    
  //[computer, view]
  def addLocation(self, location)
    self.locations.append(location)
  
  
  
