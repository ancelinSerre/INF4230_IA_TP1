from State import State

class Switch(State):

  ON = 1
  OFF = 0

  def __init__(self, position, status):
    super().__init__(position)
    self.status = status
    self.breakages = []
