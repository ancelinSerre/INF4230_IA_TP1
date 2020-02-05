#!/usr/bin/env python3
import argparse
from Position import Position
from World import World
from State import State

breakages = []
switches = []

obstacles = []

'''
def goal():
  return not breakages and not switches_off


# Actions possibles 
def move_south(position):
  # On verifie si la case au sud n'est pas un obstacle
  if(Position(position.row,position.column+1) in obstacles):
    # mouvement impossible
  else:
    return Position(position.row,position.column+1)

def move_north(position):
  # On verifie si la case au nord n'est pas un obstacle
  if(Position(position.row,position.column-1) in obstacles):
    # mouvement impossible
  else:
    return Position(position.row,position.column-1)

def move_east(position):
  # On verifie si la case à l'est n'est pas un obstacle
  if(Position(position.row+1,position.column) in obstacles):
    # mouvement impossible
  else:
    return Position(position.row+1,position.column)

def move_west(position):
  # On verifie si la case à l'ouest n'est pas un obstacle
  if(Position(position.row-1,position.column) in obstacles):
    # mouvement impossible
  else:
    return Position(position.row-1,position.column)

# Allumer un interrupteur
def switch_on(position):
  # On verifie que l'interrupteur est un interrupteur et qu'il est eteint
  if(position in switches_off):
    # Supprimer l'interrupteur de la liste des interrupteurs eteint
    switches_off.remove(position)
    # Ajouter l'interrupteur dans la liste des interrupteurs allumes
    switches_on.append(position)

# Eteindre un interrupteur
def switches_off(position):
  if(position in switches_on):
    # Supprimer l'interrupteur de la liste des interrupteurs allumes
    switches_on.remove(position)
    # Ajouter l'interrupteur dans la liste des interrupteurs eteint
    switches_off.append(position)

# Reparer un bris
# COMMENT verifier que l'interrupteur du bris est bien eteint
def repare(position):
  # On verifie que la position est bien un bris
  if(position in breakages):
    # On supprime le bris de la liste puisqu'il est maintenant repare
    breakages.remove(position)
'''
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="A text file containing a map")
    args = parser.parse_args()

    team = None

    text_map = args.map 
    lines = []
    with open(text_map, "r") as f:
        lines = f.read().split("\n")

    w = World(lines)
    w.link_switch_breakages()
    #w.find_in_graph(w.team)
    path = w.find_path(State(Position(5,1)), State(Position(5,3)))
    
    for p in path:
      print(p.position.row, end=" ")
      print(p.position.column)
      if p.parent:
        print("parent ", end="")
        print(p.parent.position.row,end=" ")
        print(p.parent.position.column)



    
