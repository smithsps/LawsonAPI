class User:
  def __init__(self, username, name, timestamp, location):
    self.username = username
    self.name = name
    self.timestamp = timestamp
    self.locations = location

  def __repr__(self):
        return '[ ' + self.username + ', ' + self.name + ', ' + self.timestamp + ', ' + self.locations + ' ]'
