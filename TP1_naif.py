#!/usr/bin/env python3
import argparse
from Position import Position

def move(source, destination):
    s_row = source.row
    d_row = destination.row
    s_column = source.column
    d_column = destination.column
    if s_row < d_row:
        for r in range(s_row, d_row):
            print("S ",end = '')
    if s_row > d_row:
        for r in range(s_row, d_row,-1):
            print("N ",end = '')
    if(s_column < d_column):
        for r in range(s_column, d_column):
            print("E ",end = '')
    if(s_column > d_column):
        for r in range(s_column,d_column,-1):
            print("W ", end = '')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="A text file containing a map")
    args = parser.parse_args()

    switches = []
    breakages = []
    team = None

    text_map = args.map 
    lines = []
    with open(text_map, "r") as f:
        lines = f.read().split("\n")

    for i_l, line in enumerate(lines):
        for i_c, character in enumerate(line):
            if character == "*":
                team = Position(i_l, i_c)
                break
            elif character == "I" or character == "i":
                switches.append(Position(i_l, i_c))
                break
            elif character == "b":
                breakages.append(Position(i_l, i_c))
                break


    # --- Plan simple d'un algorithme naïf --- 
    # Mettre à OFF tous les interrupteurs
    for p in switches:
        move(team, p)
        team = p
        print("0 ",end = '')
    # Réparer tous les bris
    for p in breakages:
        move(team, p)
        team = p
        print("R ",end = '')
    # Mettre à ON tous les interrupteurs
    for p in switches:
        move(team, p)
        team = p
        print("1 ",end = '')

    
