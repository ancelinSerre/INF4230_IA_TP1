from State import State

class Breakage(State):

  def __init__(self, position):
    super().__init__(position)
    self.switches = []