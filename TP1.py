#!/usr/bin/env python3

# Imports bibliothèque standard.
import argparse

# Imports projet.
from Position import Position
from World import World
from State import State

if __name__ == "__main__":
		
	# Gestion des arguments du programme.
	parser = argparse.ArgumentParser()
	# Lecture du nom de fichier pour la carte.
	parser.add_argument("map", help="A text file containing a map")
	# Lecture de l'argument concernant l'utilisation ou non de la métrique 2.
	parser.add_argument("-m2", help="Use the metric considering the impact of outages", action="store_true")
	args = parser.parse_args()

	team = None

	text_map = args.map 
	lines = []
	with open(text_map, "r") as f:
		lines = f.read().split("\n")

	w = World(lines)
	w.link_switch_breakages()
	# w.find_in_graph(w.team)
	path = w.find_path(State(Position(5,1)), State(Position(5,3)))

	for p in path:
		print(f"- ({p.row}, {p.column})")
		if p.parent:
			print(f"Parent ({p.parent.row}, {p.parent.column})")



		
