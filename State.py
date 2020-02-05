from Position import Position 

class State:

  def __init__(self, position):
    self.position = position
    self.parent = None
    self.f = 0
    self.g = 0
    self.h = 0

  @property
  def row(self):
    return self.position.row

  @property
  def column(self):
    return self.position.column
