from Position import Position
from Breakage import Breakage
from Team import Team
from State import State
from Network import Network

from cells.Cell import Cell
from cells.House import House
from cells.Obstacle import Obstacle
from cells.PowerLine import PowerLine
from cells.PowerSource import PowerSource
from cells.Switch import Switch


class World:

	def __init__(self, world_map):
		"""
		Constructeur de la classe world.
		
		:param list(str) world_map: lignes de la carte.
		"""
		# Liste des sources d'électricités.
		# Permettra d'identifier les différents réseaux
		# et sous-réseaux du monde.
		self.power_sources = []

		self.houses = []

		# Liste des réseaux du monde.
		self.networks = []

		# Position initiale de l'équipe, à déterminer.
		self.initial_position = None

		self.rows = len(world_map)
		# Ce calcul permettra d'ajouter automatiquement des cellules
		# vides dans le cas où on a un élément en dehors des obstacles.
		self.columns = max([len(row) for row in world_map])

		# Cette variable va contenir l'ensemble des cellules du monde.
		self.content = []
		for _ in range(0, self.rows):
			self.content.append([])

		# Remplissage du monde avec des cellules
		for x, row in enumerate(world_map):
			if len(row) < self.columns:
				row += " "
			for y, character in enumerate(row):
				pos = Position(x, y)
				self.content[x].append(self.create_cell(pos, character))

		self.analyze_world()
		exit()

		# self.team = None
		# self.obstacles = []
		# self.states = []
		# self.switches = []
		# self.breakages = []
		# self.elems = []
		# self.visited = set() 

		# for i_l, line in enumerate(world_map):
		# 	for i_c, character in enumerate(line):
		# 		if character == "*":
		# 			self.team = Team(Position(i_l, i_c))
		# 		elif character == "I" or character == "i":
		# 			switch_tmp = Switch(Position(i_l, i_c), Switch.ON)
		# 			self.states.append(switch_tmp)
		# 			self.switches.append(switch_tmp)
		# 		elif character == "j" or character == "J":
		# 			switch_tmp = Switch(Position(i_l, i_c), Switch.OFF)
		# 			self.states.append(switch_tmp)
		# 			self.switches.append(switch_tmp)
		# 		elif character == "b":
		# 			breakage_tmp = Breakage(Position(i_l, i_c))
		# 			self.states.append(breakage_tmp)
		# 			self.breakages.append(breakage_tmp)
		# 		elif character == "#":
		# 			self.obstacles.append(Position(i_l, i_c))
		# 		elif character == "m" or character == "c":
		# 			self.elems.append(Position(i_l, i_c))


	def create_cell(self, position, representation):
		"""
		Méthode permettant de créer une cellule de type
		approprié à sa représentation.

		:param Position position: position de la cellule dans le monde.
		:param str representation: caractère représentant la cellule.
		:return: une nouvelle cellule.
		:rtype: Cell
		:raises TypeError: 
			- si le type de l'argument 'position' n'est pas Position.
			- si le type de l'argument 'representation' n'est pas str.
		"""
		if not isinstance(position, Position):
			raise TypeError("Argument 'position' must be a Position")
		elif not isinstance(representation, str):
			raise TypeError("Argument 'representation' must be a str")

		c = representation
		cell = None
		if c == "*":
			cell = Cell(position)
			self.initial_position = cell
		elif c == " ":
			cell = Cell(position)
		elif c == "I" or c == "i":
			cell = Switch(position, True)
		elif c == "J" or c == "j":
			cell = Switch(position, False)
		elif c == "B" or c == "b":
			cell = PowerLine(position, True)
		elif c == "C" or c == "c":
			cell = PowerLine(position, False)
		elif c == "M" or c == "m":
			cell = House(position)
			self.houses.append(cell)
		elif c == "S" or c == "s":
			cell = PowerSource(position)
			self.power_sources.append(cell)
		elif c == "#":
			cell = Obstacle(position)
		return cell


	def get_cell(self, x, y, default=None):
		"""
		Fonction utilitaire permettant d'accéder
		sans risque à une liste en retournant
		une valeur par défaut si l'index n'est pas présent.

		:param int x: coordonnée x du monde.
		:param int y: coordonnée y du monde.
		:return: cellule aux coordonnées données ou 'default'
		:rtype: Cell ou type('default')
		"""
		try:
			return self.content[x][y]
		except IndexError:
			return default


	def get_neighbours(self, cell):
		"""
		Méthode permettant d'accéder aux voisins
		d'une cellule donnée.
		La cellule n'a pas nécessairement 4 voisins,
		les voisins inexistants seront remplacés par None.

		:param Cell cell: cellule du monde.
		:return: liste de voisins de taille 4 (N, S, E, O).
		:rtype: list
		"""
		x = cell.x
		y = cell.y
		return [
			self.get_cell(x - 1, y),
			self.get_cell(x + 1, y),
			self.get_cell(x, y + 1),
			self.get_cell(x, y - 1)
		]


	def _find_source(self, current_cell, visited):
		"""
		Méthode chargée de trouver une source d'énergie
		à partir d'une cellule donnée (en l'occurrence
		on l'utilise pour les maisons pour savoir si ces
		dernières sont alimentées ou non).

		:param Cell current_cell: cellule courante à inspecter.
		:param Set visited: set contenant les cellules déjà visitées.
		:return: True si on arrive sur une source, False sinon.
		:rtype: bool 
		"""
		neighbours = self.get_neighbours(current_cell)
		if current_cell is None or current_cell in visited:
			return False
		else:
			visited.add(current_cell)
			n_type = current_cell.get_type()
			if n_type == "s":
				return True
			elif n_type == "i":
				if current_cell.is_on:
					return self._find_source(neighbours[0], visited) \
						or self._find_source(neighbours[1], visited) \
						or self._find_source(neighbours[2], visited) \
						or self._find_source(neighbours[3], visited)
				else:
					return False
			elif n_type == "c":
				if current_cell.is_down:
					return False
				else:
					return self._find_source(neighbours[0], visited) \
						or self._find_source(neighbours[1], visited) \
						or self._find_source(neighbours[2], visited) \
						or self._find_source(neighbours[3], visited)
			else:
				return False


	def check_powered(self, house):
		"""
		Méthode chargée de vérifier si une maison est 
		alimentée en électricité ou non.

		:param House house: maison à vérifier.
		:return: True si alimentée, False sinon.
		:rtype: bool
		:raises TypeError:
			- le type de l'argument 'house' n'est pas House.
		"""
		if not isinstance(house, House):
			raise TypeError("Argument 'house' must be a House")

		visited = set()
		neighbours = self.get_neighbours(house)
		return self._find_source(neighbours[0], visited) \
			or self._find_source(neighbours[1], visited) \
			or self._find_source(neighbours[2], visited) \
			or self._find_source(neighbours[3], visited)


	def analyze_world(self):
		"""
		Méthode chargée d'analyser le contenu du monde lu
		par le programme en définissant les choses suivantes:
		- définir le réseau associé à chaque source et interrupteur.
		- définir la responsabilité de chaque interrupteur.
		"""
		for house in self.houses:
			house.is_powered = self.check_powered(house)
			print(house)


	# Position --> impl. getType() --> enum plus simple ?
	# => state impl. getType()
	def follow_path(self, current, b_list):
		self.visited.add(current)
		nb = [n for n in self.get_neighbours(current) if n is not None]
		for n in nb:
			n_b = self.is_breakages(n)
			if self.is_elem(n) and not self.is_visited(n):
				self.visited.add(n)
				self.follow_path(n, b_list)
			elif n_b != None and not self.is_visited(n):
				b_list.append(n_b)
				self.visited.add(n)
				self.follow_path(n, b_list)

	# def is_breakages(self, position):
    # 	for breakage in self.breakages:
    #   		if breakage.row == position.row and breakage.column == position.column:
    #     		return breakage
    # 	return None
  
  	# def is_elem(self, position):
    # 	for elem in self.elems:
    #   		if elem.row == position.row and elem.column == position.column:
    #     		return True
    # 	return False

	# def is_visited(self, position):
	# 	for v in self.visited:
	# 	if position.row == v.row and position.column == v.column:
	# 		return True
	# 	return False

	# def is_obstacles(self, position):
	# 	for o in self.obstacles:
	# 	if position.row == o.row and position.column == o.column:
	# 		return True
	# 	return False

	# def link_switch_breakages(self):
	# 	for switch in self.switches:
	# 	self.visited = set()
	# 	self.follow_path(switch.position, switch.breakages)

	# def switches_on(self):
	# 	for switch in self.switches:
	# 	if switch.status == 0:
	# 		return False
	# 	return True

	# def goal(self):
	# 	return (not self.breakages) and self.switches_on()
	
	# # Peut etre qu'on pourrait mettre cette méthode
	# # dans la classe Switch en mode :
	# # - on ajoute un param dans breakages qu'on appelle self.accessible
	# # - ce param est mis à jour à chaque fois qu'on fait une interaction
	# # avec un interrupteur de la manière suivante :
	# #   -- *set switch to off* --> for each breakages of this switch: 
	# #                                 updateCurrentBreakageAccessibility
	# # c'est peut etre un peu plus propre et sa rendra ce fichier plus digeste

	# def breakage_accessible(self, b):
	# 	for switch in self.switches:
	# 	if switch.status == 1 and b in switch.breakages:
	# 		return False
	# 	return True

	# # Idem qu'au dessus, le switch pourrait avoir un param accessible
	# # qu'on mettrait à jour à chaque fois qu'on réparerait un bris
	# # --> conclusion de ces deux commentaires :
	# # - on pourrait généraliser en ajoutant un param accessible à Position
	# # utile pour les switchs, breakages et obstacles !
	# # - breakages devrait peut etre au moins connaitre ses switchs responsables

	# # Accessible si il est allumé avec des bris ou éteint sans bris
	# def switch_accessible(self, s):
	# 	return (s.status == 1 and s.breakages) or (s.status == 0 and not s.breakages)

	# # Je pense que ça c'est good, l'idée est bonne.
	# def next_states(self):
	# 	next_states = []
	# 	for state in self.states:
	# 	if state in self.breakages and self.breakage_accessible(state):
	# 		next_states.append(state)
	# 	# Retirer la deuxieme condition quand l'heuristique sera implémentée
	# 	elif state in self.switches and self.switch_accessible(state):
	# 		next_states.append(state)
	# 	return next_states

	# # Distance de manhattan ?
	# # On pourrait aussi utiliser la distance euclidienne comme conseillé dans l'énoncé du tp
	# def distance(self, n1, n2):
	# 	return abs(n1.row - n2.row) + abs(n1.column - n2.column) 

	# # Je reviens sur ce dont on avait parlé mais
	# # on peut envisager d'utiliser une classe Team qui effectue des actions
	# # et garde une trace de son déplacement optimal et aussi de ses opérations
	# # réalisées au cours des déplacements
	# # la classe pourrait afficher à l'écran son activité comme demandée dans le tp
	# def do_action(self, state):
	# 	if state in self.breakages:
	# 	# self.move(state.parent.position, state.position)
	# 	print("R")
	# 	self.states.remove(state)
	# 	self.breakages.remove(state)
	# 	for switch in self.switches:
	# 		if state in switch.breakages:
	# 		switch.breakages.remove(state)
	# 	elif state in self.switches:
	# 	# self.move(state.parent.position, state.position)
	# 	if state.status == 0:
	# 		print("1")
	# 		state.status = 1
	# 	elif state.status == 1:
	# 		print("0")
	# 		state.status = 0

	# def find_in_graph(self, team):
	# 	open_l = []
	# 	closed = []
	# 	# Ajout de l'etat initial
	# 	open_l.append(team)
	# 	while True:
		
	# 	# Si la liste est vide alors il n'y a pas de solution
	# 	if not open_l:
	# 		print("IMPOSSIBLE")
	# 		exit()
	# 	# On prend le premier element de la liste open
	# 	n1 = open_l.pop(0)
	# 	# Do the action - A SORTIR DE LA BOUCLE
	# 	if n1.parent:
	# 		self.do_action(n1)
	# 	# Pour tester
	# 	print(n1.row)
	# 	print(n1.column)
	# 	closed.append(n1)
	# 	# Si on a fini l'objectif, on sort de la boucle
	# 	if self.goal():
	# 		exit()
	# 	# On determine les prochains états possibles
	# 	open_l = self.next_states()
	# 	for n2 in open_l:
	# 		n2.g = n1.g + self.distance(n1,n2)
	# 		n2.parent = n1
	# 	# Trier open selon la valeur de f
	# 	sorted(open_l, key=lambda state: state.g)

	# # Plutôt que de recréer des positions, on devrait tenter
	# # d'accéder directement au contenu de la map qui ressemble ni plus
	# # ni moins à une grille sachant que meme si la grille est de forme
	# # différente d'un rectangle ça gênera pas car on pourra pas sortir
	# # de la zone limitée par des obstacles ou alors il n'y aura pas de sol possible
	# def neighbours_path(self, cell):
	# 	neighbours = []
	# 	north = Position(cell.row - 1, cell.column)
	# 	south = Position(cell.row + 1, cell.column)
	# 	east = Position(cell.row, cell.column + 1)
	# 	west = Position(cell.row, cell.column - 1)
	# 	# North
	# 	if not self.is_obstacles(north):
	# 	neighbours.append(State(north))
	# 	# South
	# 	if not self.is_obstacles(south):
	# 	neighbours.append(State(south))
	# 	# East
	# 	if not self.is_obstacles(east):
	# 	neighbours.append(State(east))
	# 	# West
	# 	if not self.is_obstacles(west):
	# 	neighbours.append(State(west))
	# 	return neighbours
	

	# def state_in_list(self, s, l):
	# 	for e in l:
	# 	# On pourrait peut être déplacer ça dans la classe positions en 
	# 	# ajoutant la possibilité de comparer des positions via des opérateurs < = > <= etc..
	# 	if e.row == s.row and e.column == s.column and s.g < e.g:
	# 		return e
	# 	return None

	# # ajouter des property pour accéder à row et column aux états
	# # ce sera plus lisible et propre
	# def find_path(self, source, dest):
	# 	open_l = []
	# 	closed = []
	# 	open_l.append(source)
	# 	while True:
	# 	# Aucun chemin possible
	# 	if not open_l:
	# 		return None
	# 	# On prend le premier element de la liste open
	# 	n1 = open_l.pop(0)
	# 	closed.append(n1)
	# 	if n1.row == dest.row and n1.column == dest.column:
	# 		return closed
	# 	next_node = self.neighbours_path(n1)
	# 	for n2 in next_node:
	# 		n2.g = n1.g + 1 + (abs(n1.row - n1.row)+abs(n1.column - n1.column))
	# 		n2.parent = n1
	# 		n3 = self.state_in_list(n2, open_l)
	# 		if n3 != None:
	# 		open_l.remove(n3)
	# 		n3 = self.state_in_list(n2, closed)
	# 		if n3 != None:
	# 		closed.remove(n3)
	# 		open_l.append(n2)
	# 	# Trier open selon la valeur de f
	# 	sorted(open_l, key=lambda state: state.g)
			
			
      




    

