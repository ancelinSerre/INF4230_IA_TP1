#!/usr/bin/env python3

# Imports bibliothèque standard.
import argparse
from datetime import datetime

# Imports projet.
from Position import Position
from World import World

if __name__ == "__main__":
		
	# Gestion des arguments du programme.
	parser = argparse.ArgumentParser()
	# Lecture du nom de fichier pour la carte.
	parser.add_argument("map", help="A text file containing a map")
	# Lecture de l'argument concernant l'utilisation ou non de la métrique 1.
	parser.add_argument("-m1", help="Use the metric considering the impact of actions", action="store_true")
	# Lecture de l'argument concernant l'utilisation ou non de la métrique 2.
	parser.add_argument("-m2", help="Use the metric considering the impact of outages", action="store_true")
	# Lecture de l'argument concernant l'affichage ou non du temps d'exécution
	parser.add_argument("-t", help="Show runtime", action="store_true")
	args = parser.parse_args()

	text_map = args.map 
	lines = []
	with open(text_map, "r") as f:
		lines = f.read().split("\n")

	start = datetime.now()
	w = World(lines)
	cs = w.astar_repair()
	res = w.analyze_solution(cs)
	end = datetime.now()
	duration = end - start
	print(res)
	
	# Utilisation de la métrique M1.
	if args.m1:
		print("---------------------------")
		print(f"M1: Total actions = {len(res.split())}")

	# Utilisation de la méttrique M2.
	if args.m2:
		print("---------------------------")
		total_outage_time = sum((x.outage_time for x in w.houses))
		for h in sorted(w.houses, key=lambda x: x.outage_time):
			print(f"House ({h.x}, {h.y}) : {h.outage_time} TU")

		print("---------------------------")
		print(f"M2: Total outage time = {total_outage_time} Time Unit")

	# Affichage du temps d'exécution.
	if args.t:
		print("---------------------------")
		print(f"Runtime = {duration}")		
