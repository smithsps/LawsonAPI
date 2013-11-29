class User:
  
  locations = []

  def __init__(self, username, name, location = ()):
    self.username = username
    self.name = name
    self.locations.append(location) #tuple (name, timestamp)
    

  def __repr__(self):
        return '[ ' + self.username + ', ' + self.name + ', ' + self.timestamp + ', ' + self.locations + ' ]'
