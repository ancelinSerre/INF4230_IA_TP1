from Position import Position
from Switch import Switch
from Breakage import Breakage
from Team import Team
from State import State

class World:

  def __init__(self, world_map):

    self.team = None
    self.obstacles = []
    self.states = []
    self.switches = []
    self.breakages = []
    self.elems = []
    self.visited = set() 

    for i_l, line in enumerate(world_map):
        for i_c, character in enumerate(line):
            if character == "*":
                self.team = Team(Position(i_l, i_c))
            elif character == "I" or character == "i":
                switch_tmp = Switch(Position(i_l, i_c), Switch.ON)
                self.states.append(switch_tmp)
                self.switches.append(switch_tmp)
            elif character == "j" or character == "J":
                switch_tmp = Switch(Position(i_l, i_c), Switch.OFF)
                self.states.append(switch_tmp)
                self.switches.append(switch_tmp)
            elif character == "b":
                breakage_tmp = Breakage(Position(i_l, i_c))
                self.states.append(breakage_tmp)
                self.breakages.append(breakage_tmp)
            elif character == "#":
                self.obstacles.append(Position(i_l, i_c))
            elif character == "m" or character == "c":
                self.elems.append(Position(i_l, i_c))
  
  def get_neighbours(self, pos):
    x = pos.row
    y = pos.column
    return [
        Position(x - 1, y), # Nord
        Position(x + 1, y), # Sud
        Position(x, y + 1), # Est
        Position(x, y - 1)  # Ouest
    ]

  # Position --> impl. getType() --> enum plus simple ?
  # => state impl. getType()
  def follow_path(self, current, b_list):
    self.visited.add(current)
    nb = self.get_neighbours(current)
    for n in nb:
        n_b = self.is_breakages(n)
        if self.is_elem(n) and not self.is_visited(n):
            self.visited.add(n)
            self.follow_path(n, b_list)
        elif n_b != None and not self.is_visited(n):
            b_list.append(n_b)
            self.visited.add(n)
            self.follow_path(n, b_list)

  def is_breakages(self, position):
    for breakage in self.breakages:
      if breakage.position.row == position.row and breakage.position.column == position.column:
        return breakage
    return None
  
  def is_elem(self, position):
    for elem in self.elems:
      if elem.row == position.row and elem.column == position.column:
        return True
    return False

  def is_visited(self, position):
    for v in self.visited:
      if position.row == v.row and position.column == v.column:
        return True
    return False

  def is_obstacles(self, position):
    for o in self.obstacles:
      if position.row == o.row and position.column == o.column:
        return True
    return False

  def link_switch_breakages(self):
    for switch in self.switches:
      self.visited = set()
      self.follow_path(switch.position, switch.breakages)

  def switches_on(self):
    for switch in self.switches:
      if switch.status == 0:
        return False
    return True

  def goal(self):
    return (not self.breakages) and self.switches_on()
  
  # Peut etre qu'on pourrait mettre cette méthode
  # dans la classe Switch en mode :
  # - on ajoute un param dans breakages qu'on appelle self.accessible
  # - ce param est mis à jour à chaque fois qu'on fait une interaction
  # avec un interrupteur de la manière suivante :
  #   -- *set switch to off* --> for each breakages of this switch: 
  #                                 updateCurrentBreakageAccessibility
  # c'est peut etre un peu plus propre et sa rendra ce fichier plus digeste

  def breakage_accessible(self, b):
    for switch in self.switches:
      if switch.status == 1 and b in switch.breakages:
        return False
    return True

  # Idem qu'au dessus, le switch pourrait avoir un param accessible
  # qu'on mettrait à jour à chaque fois qu'on réparerait un bris
  # --> conclusion de ces deux commentaires :
  # - on pourrait généraliser en ajoutant un param accessible à Position
  # utile pour les switchs, breakages et obstacles !
  # - breakages devrait peut etre au moins connaitre ses switchs responsables

  # Accessible si il est allumé avec des bris ou éteint sans bris
  def switch_accessible(self, s):
    return (s.status == 1 and s.breakages) or (s.status == 0 and not s.breakages)

  # Je pense que ça c'est good, l'idée est bonne.
  def next_states(self):
    next_states = []
    for state in self.states:
      if state in self.breakages and self.breakage_accessible(state):
        next_states.append(state)
      # Retirer la deuxieme condition quand l'heuristique sera implémentée
      elif state in self.switches and self.switch_accessible(state):
        next_states.append(state)
    return next_states

  # Distance de manhattan ?
  # On pourrait aussi utiliser la distance euclidienne comme conseillé dans l'énoncé du tp
  def distance(self, n1, n2):
    return abs(n1.position.row - n2.position.row) + abs(n1.position.column - n2.position.column) 

  # Je reviens sur ce dont on avait parlé mais
  # on peut envisager d'utiliser une classe Team qui effectue des actions
  # et garde une trace de son déplacement optimal et aussi de ses opérations
  # réalisées au cours des déplacements
  # la classe pourrait afficher à l'écran son activité comme demandée dans le tp
  def do_action(self, state):
    if state in self.breakages:
      # self.move(state.parent.position, state.position)
      print("R")
      self.states.remove(state)
      self.breakages.remove(state)
      for switch in self.switches:
        if state in switch.breakages:
          switch.breakages.remove(state)
    elif state in self.switches:
      # self.move(state.parent.position, state.position)
      if state.status == 0:
        print("1")
        state.status = 1
      elif state.status == 1:
        print("0")
        state.status = 0

  def find_in_graph(self, team):
    open_l = []
    closed = []
    # Ajout de l'etat initial
    open_l.append(team)
    while True:
      
      # Si la liste est vide alors il n'y a pas de solution
      if not open_l:
        print("IMPOSSIBLE")
        exit()
      # On prend le premier element de la liste open
      n1 = open_l.pop(0)
      # Do the action - A SORTIR DE LA BOUCLE
      if n1.parent:
        self.do_action(n1)
      # Pour tester
      print(n1.position.row)
      print(n1.position.column)
      closed.append(n1)
      # Si on a fini l'objectif, on sort de la boucle
      if self.goal():
        exit()
      # On determine les prochains états possibles
      open_l = self.next_states()
      for n2 in open_l:
        n2.g = n1.g + self.distance(n1,n2)
        n2.parent = n1
      # Trier open selon la valeur de f
      sorted(open_l, key=lambda state: state.g)

  # Plutôt que de recréer des positions, on devrait tenter
  # d'accéder directement au contenu de la map qui ressemble ni plus
  # ni moins à une grille sachant que meme si la grille est de forme
  # différente d'un rectangle ça gênera pas car on pourra pas sortir
  # de la zone limitée par des obstacles ou alors il n'y aura pas de sol possible
  def neighbours_path(self, cell):
    neighbours = []
    north = Position(cell.position.row - 1, cell.position.column)
    south = Position(cell.position.row + 1, cell.position.column)
    east = Position(cell.position.row, cell.position.column + 1)
    west = Position(cell.position.row, cell.position.column - 1)
    # North
    if not self.is_obstacles(north):
      neighbours.append(State(north))
    # South
    if not self.is_obstacles(south):
      neighbours.append(State(south))
    # East
    if not self.is_obstacles(east):
      neighbours.append(State(east))
    # West
    if not self.is_obstacles(west):
      neighbours.append(State(west))
    return neighbours
  

  def state_in_list(self, s, l):
    for e in l:
      # On pourrait peut être déplacer ça dans la classe positions en 
      # ajoutant la possibilité de comparer des positions via des opérateurs < = > <= etc..
      if e.position.row == s.position.row and e.position.column == s.position.column and s.g < e.g:
        return e
    return None

  # ajouter des property pour accéder à row et column aux états
  # ce sera plus lisible et propre
  def find_path(self, source, dest):
    open_l = []
    closed = []
    open_l.append(source)
    while True:
      # Aucun chemin possible
      if not open_l:
        return None
      # On prend le premier element de la liste open
      n1 = open_l.pop(0)
      closed.append(n1)
      if n1.position.row == dest.position.row and n1.position.column == dest.position.column:
        return closed
      next_node = self.neighbours_path(n1)
      for n2 in next_node:
        n2.g = n1.g + 1 + (abs(n1.position.row - n1.position.row)+abs(n1.position.column - n1.position.column))
        n2.parent = n1
        n3 = self.state_in_list(n2, open_l)
        if n3 != None:
          open_l.remove(n3)
        n3 = self.state_in_list(n2, closed)
        if n3 != None:
          closed.remove(n3)
        open_l.append(n2)
      # Trier open selon la valeur de f
      sorted(open_l, key=lambda state: state.g)
        
        
      




    

