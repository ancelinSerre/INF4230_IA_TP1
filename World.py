from copy import deepcopy

from Position import Position
from Heuristic import Heuristic

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
		self.houses = []
		self.states = []
		self.obstacles = []

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
			self.states.append(cell)
		elif c == "J" or c == "j":
			cell = Switch(position, False)
			self.states.append(cell)
		elif c == "B" or c == "b":
			cell = PowerLine(position, True)
			self.states.append(cell)
		elif c == "C" or c == "c":
			cell = PowerLine(position, False)
		elif c == "M" or c == "m":
			cell = House(position)
			self.houses.append(cell)
		elif c == "S" or c == "s":
			cell = PowerSource(position)
		elif c == "#":
			cell = Obstacle(position)
			self.obstacles.append(cell)
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
		if current_cell is None or current_cell in visited:
			return False
		else:
			visited.add(current_cell)
			c_type = current_cell.get_type()
			if c_type == "s":
				return True
			elif (c_type == "i" and current_cell.is_on) \
				or (c_type == "c" and not current_cell.is_down):
				
				neighbours = self.get_neighbours(current_cell)
				return self._find_source(neighbours[0], visited) \
					or self._find_source(neighbours[1], visited) \
					or self._find_source(neighbours[2], visited) \
					or self._find_source(neighbours[3], visited)
			else:
				return False


	def _find_breakages(self, switch, current_cell, visited):
		"""
		Méthode chargée de trouver et d'ajouter les différents 
		bris sous la responsabilité d'un interrupteur.

		:param Switch switch: l'interrupteur responsable.
		:param Cell current_cell: cellule à inspecter.
		:param Set visited: set contenant les cellules déjà visitées.
		"""
		if current_cell not in visited:
			c_type = current_cell.get_type()
			visited.add(current_cell)
			if c_type == "c":
				if current_cell.is_down:
					switch.network["breakages"].append(current_cell)
				neighbours = self.get_neighbours(current_cell)
				for nb in neighbours:
					self._find_breakages(switch, nb, visited)


	def check_powered(self, cell):
		"""
		Méthode chargée de vérifier si une cellule est 
		alimentée en électricité ou non.

		:param Cell cell: cellule à vérifier.
		:return: True si alimentée, False sinon.
		:rtype: bool
		:raises TypeError:
			- si le type de l'argument 'cell' n'est pas Cell.
		"""
		if not isinstance(cell, Cell):
			raise TypeError("Argument 'cell' must be a Cell")

		visited = set()
		neighbours = self.get_neighbours(cell)
		return self._find_source(neighbours[0], visited) \
			or self._find_source(neighbours[1], visited) \
			or self._find_source(neighbours[2], visited) \
			or self._find_source(neighbours[3], visited)


	def add_breakages(self, switch):
		"""
		Méthode chargée d'ajouter de potentiels bris
		à l'interrupteur responsable donné.

		:param Switch switch: interrupteur donné.
		:raise TypeError:
			- si le type de l'argument 'switch' n'est pas Switch.
		"""
		if not isinstance(switch, Switch):
			raise TypeError("Argument 'switch' must be a Switch")

		visited = set()
		neighbours = [n for n in self.get_neighbours(switch) if n is not None]
		for nb in neighbours:
			self._find_breakages(switch, nb, visited)


	def analyze_world(self):
		"""
		Méthode chargée d'analyser le contenu du monde lu
		par le programme en définissant les choses suivantes:
		- définir le réseau associé à chaque source et interrupteur.
		- définir la responsabilité de chaque interrupteur.
		""" 
		# On met à jour le statut 'powered' pour chaque état.
		for state in self.states:
			state.powered = self.check_powered(state)

		# On récupère ensuite tous les interrupteurs alimentés
		# pour leur ajouter leurs bris respectifs.
		switches = [s for s in self.states if s.get_type() == "i" and s.powered]	
		for s in switches:
			self.add_breakages(s)

		# On met à jour le statut 'powered' pour chaque maison.
		for house in self.houses:
			house.is_powered = self.check_powered(house)


	def mission_success(self):
		"""
		Méthode indiquant si l'équipe de réparation a fini
		son travail dans le monde ou non.

		:return: True si travail terminé, False sinon.
		:rtype: bool
		"""
		success = True
		for state in self.states:
			c_type = state.get_type()
			# Si on a un bris ou un interrupteur éteint, alors
			# la mission n'est pas terminée.
			if c_type == "c" or (c_type == "i" and not state.is_on):
				success = False
				break

		return success


	def astar_path(self, src, dest, heuristic=Heuristic.euclidean):
		"""
		Recherche d'un chemin optimal entre une source et une
		destination via l'implémentation de l'algorithme A*.
		
		:param Cell src: cellule source (départ).
		:param Cell dest: cellule destination (arrivée).
		:param function heuristic: fonction heuristique à utiliser.
		:return: liste d'états représentants le chemin à emprunter.
		:rtype: list(Cell)
		"""
		opened_states = []
		closed_states = []
		# Ajout de l'état de départ dans la liste d'états ouverts.
		opened_states.append(src)
		while opened_states:
			# Récupération de l'état avec la valeur f la plus petite.
			current_state = opened_states.pop(0)
			closed_states.append(current_state)
			# Verification de l'objectif.
			if current_state.x == dest.x and current_state.y == dest.y:
				return closed_states
			# Récupération des cellules voisines.
			neighbours = self.get_neighbours(current_state)
			for nb in neighbours:
				# Vérification que la cellule n'est pas un obstacle 
				# ou n'est pas déjà dans la liste closed.
				if nb not in closed_states and not nb in self.obstacles:
					x = nb.x
					y = nb.y
					ng = current_state.gp + 1
					# Si la cellule n'est pas dans la liste open
					# ou si le chemin actuel est plus rapide que celui trouvé précédement.
					if nb not in opened_states or ng < nb.gp:
						nb.gp = ng
						nb.hp = heuristic(nb, dest)
						nb.fp = nb.gp + nb.hp
						nb.parentp = current_state
						# Ajout de la cellule dans open, si elle n'y est pas déjà.
						if nb not in opened_states:
							opened_states.append(nb)

			# Tri croissant des états ouverts selon la valeur de leur 'f'.				
			opened_states = sorted(opened_states, key=lambda state: state.fp)
			
		# Si on arrive ici, c'est qu'il est impossible de trouver un chemin
		# menant à l'objectif qu'est la cellule 'dest'.
		raise ValueError("Impossible path !")


	def print_move(self, state):
		"""
		Méthode permettant d'afficher les déplacements
		effectués par l'équipe de réparation au fur
		et à mesure de son avancée.
		On détermine ce déplacement en regardant le 
		parent de l'état actuel de l'équipe.
		
		:param Cell state: état où l'équipe est actuellement.
		:return: Déplacement de l'équipe.
		:rtype: str
		"""
		parent = state.parentp
		# Déplacelement vers le Sud.
		if state.x == parent.x + 1:
			return "S "
		# Déplacement vers le Nord.
		elif state.x == parent.x - 1:
			return "N "
		# Déplacement vers l'Est.
		elif state.y == parent.y + 1:
			return "E "
		# Déplacement vers l'Ouest.
		elif state.y == parent.y - 1:
			return "W "
		# Déplacement inconnu.
		else:
			raise ValueError("Unexpected move !")


	def move(self, src, dest):
		"""
		Méthode permettant le déplacement de l'équipe
		d'une cellule source vers une destination
		ainsi que l'affichage de ce déplacement.
		
		:param Cell src: cellule source (départ).
		:param Cell dest: cellule destination (arrivée).
		:return: Déplacement de l'équipe vers la destination.
		:rtype: str
		"""
		path_str = ""
		# Détermination du chemin à parcourir.
		path = self.astar_path(dest.parentr, dest)
		current = path[-1]
		real_path = []
		# Remonté des cellules parents pour obtenir le chemin.
		while current != src:
			real_path.append(current)
			current = current.parentp
		# Affichage du mouvement réalisé entre chaque cellule du chemin.
		for n in reversed(real_path):
			path_str += self.print_move(n)
		
		return path_str

	def do_action(self, state):
		"""
		Méthode permettant à l'équipe
		de réparation d'effectuer une action sur
		son état actuel si ce dernier est modifiable
		(interrupteur ou ligne électrique à réparer)
		
		:param Cell state: état courant de l'équipe.
		"""
		# Récupération du type de l'état courant.
		c_type = state.get_type()

		# On est sur une ligne électrique à réparer.
		if c_type == "c":
			self.states.remove(state)
			state.is_down = False
			# On supprime le bris de tous les interrupteurs
			# qui l'ont pour responsables.
			switches = [s for s in self.states if s.get_type() == "i"]
			for s in switches:
				if state in s.network["breakages"]:
					s.network["breakages"].remove(state)

		# On est sur un interrupteur.
		elif c_type == "i":
			# Si l'interrupteur est éteint, on l'allume.
			if not state.is_on:
				state.is_on = True
			# Si l'interrupteur est allumé, on l'éteint.
			else:
				state.is_on = False
				for b in state.network["breakages"]:
					b.powered = False
					
		# On met à jour le monde.
		for house in self.houses:
			if not house.is_powered:
				house.outage_time += 1
			house.is_powered = self.check_powered(house)


	def path_length(self, path, end):
		"""
		Méthode permettant de calculer 
		la longueur d'un chemin entre deux cellules.
		
		:param list path: liste des cellules du chemin.
		:param Cell end: Cellule représentant la fin du chemin.
		:return: la longueur du chemin.
		:rtype: int
		"""
		current_state = path[-1]
		length = 0
		while current_state != end:
			current_state = current_state.parentp
			length += 1

		return length


	def next_accessible_states(self):
		"""
		Méthode permettant de déterminer les états
		qui sont accessibles dans l'état actuel.

		:return: une liste d'états accessibles.
		:rtype: list.
		"""
		next_states = []
		# Pour chaque état du monde
		for state in self.states:
			c_type = state.get_type()
			# Si l'état est un bris et qu'il n'est pas alimenté en éléctricité.
			# Ajout du bris dans la liste des états accessibles.
			if (c_type == "c" and not state.powered):
				next_states.append(state)
			# Si l'état est un interrupteur allumé et qu'il a des bris sur son réseau.
			# Ajout de l'interrupteur dans la liste des états accessibles.
			elif c_type == "i" and state.network["breakages"] and state.is_on:
				next_states.append(state)
			# Si l'état est un interrupteur éteint et qu'il n'a plus de bris sur son réseau.
			# Ajout de l'interrupteur dans la liste d'états accessibles.				
			elif c_type == "i" and not state.network["breakages"] and not state.is_on:
				next_states.append(state)

		return next_states


	def heuristic_breakages(self, next_state):
		"""
		Méthode calculant une heuristique
		basée sur le nombre de bris restants à réparer.

		:param Cell next_state: l'état pour lequel on va calculer l'heuristique.
		:return: heuristique
		:rtype: float
		"""
		breakages = len([s for s in self.states if s.get_type() == "c"])
		if next_state.get_type() == "c" and breakages > 0:
			breakages = 1 - 1 / (breakages + 1)
		elif next_state.get_type() == "i" and breakages > 0:
			breakages = 1 - 1 / breakages
		return round(breakages, 3)


	def heuristic_houses(self, next_state):
		"""
		Méthode calculant une heuristique
		basée sur le nombre de maisons non alimentées.

		:param Cell next_state: l'état pour lequel on va calculer l'heuristique.
		:return: heuristique
		:rtype: float
		"""
		nb_houses = 0
		if next_state.get_type() == "c" and next_state.is_down:
			next_state.is_down = False
			for house in self.houses:
				if not self.check_powered(house):
					nb_houses += 1
			next_state.is_down = True
		elif next_state.get_type() == "i" and next_state.is_on:
			next_state.is_on = False
			for house in self.houses:
				if not self.check_powered(house):
					nb_houses += 1
			next_state.is_on = True
		elif next_state.get_type() == "i" and not next_state.is_on:
			next_state.is_on = True
			for house in self.houses:
				if not self.check_powered(house):
					nb_houses += 1
			next_state.is_on = False
		
		return round(1 - 1 / nb_houses, 3) if nb_houses > 0 else 0


	def astar_repair(self, heuristic=heuristic_houses):
		"""
		Recherche du chemin à emprunter afin de réparer le monde.
		Cette méthode utilise l'algorithme A*.

		:param function heuristic: fonction heuristique à utiliser.
		:return: liste d'état que l'équipe devra suivre pour réparer le monde.
		:rtype: list.
		"""
		opened_states = []
		closed_states = []
		opened_states.append(self.initial_position)
		# Tant que la liste open n'est pas vide.
		while opened_states:
			# Récuparartion de l'élément avec le plus petit f dans la liste open.
			current_state = opened_states.pop(0)
			closed_states.append(deepcopy(current_state))
			# Réalisation de l'action pour rejoindre deux états différents.
			# Met également le monde à jour pour la suite.
			if current_state.parentr is not None:
				# On récupère toutes les maisons non alimentées.
				not_powered_houses = [h for h in self.houses if not h.is_powered]
				for house in not_powered_houses:
					house.outage_time += current_state.path_length
				self.do_action(current_state)
			# Si la monde est réparer, on retourne la liste closed.
			if self.mission_success():
				return closed_states
			# On met dans open, les états accessibles.
			opened_states = self.next_accessible_states()
			# trie des états de open selon la valuer de f.
			for next_state in opened_states:
				try:
					# Si il n'y a pas de chemin, la résolution est impossible.
					path = self.astar_path(current_state, next_state)
				except ValueError:
					# Renvoie de la valeur None qui sera analyser et afficher IMPOSSIBLE.
					return None
				else:
					# remonter chemin emprunté et compter le nombre de cellules empruntées.
					next_state.path_length = self.path_length(path, current_state)
					next_state.gr = current_state.gr + next_state.path_length
					next_state.hr = heuristic(self, next_state)
					# next_state.hr = 0
					next_state.fr = next_state.gr + next_state.hr
					next_state.parentr = current_state

			# Trie de la liste open.
			opened_states = sorted(opened_states, key=lambda state: state.fr)

	def analyze_solution(self, close_states):
		"""
		Méthode permettant d'analyser le chemin retourné par
		l'algorithme A* afin de l'afficher dans le terminal.

		:param list close_states: liste des états représentant le chemin
		"""
		actions_str = ""
		# Si la liste n'est pas vide, l'équipe d'entretien a réaliser des actions.
		if close_states is not None:
			for s in close_states:
				if s.parentr:
					# Déplacement le l'équipe.
					actions_str += self.move(s.parentr, s)
					c_type = s.get_type()
					# Si on est sur un interrupteur allumé,
					# l'équipe est allé l'éteindre.
					if c_type == 'i' and s.is_on:
						actions_str += "0 "
					# A l'inverse, si on est sur un interrupteur éteint,
					# L'équipe va le rallumer.
					elif c_type == 'i' and not s.is_on:
						actions_str += "1 "
					# Si c'est un bris, l'équipe le répare.
					elif c_type == 'c':
						actions_str += "R "

			return actions_str
		# Si la liste est vide, la résolution est impossible.
		else:
			return "IMPOSSIBLE"
