import math

class Heuristic:

  def manhattan(src, dest):
    """
      Méthode permettant de calculer 
      l'heuristique de Manhattan entre deux cellules.

      :param Cell src: Cellule d'origine.
      :param Cell dest: Cellule destination.
      :return: La distance de Manhattan entre les deux cellules.
      :rtype: int
    """
    return abs(src.x - dest.x) + abs(src.y - dest.y)

  def euclidean(src, dest):
    """
      Méthode permettant de calculer 
      la distance euclidienne entre deux cellules.

      :param Cell src: Cellule d'origine.
      :param Cell dest: Cellule destination.
      :return: La distance euclidienne entre les deux cellules.
      :rtype: 
    """
    return int(math.sqrt(((src.x - dest.x) ** 2) + ((src.y - dest.y) ** 2)))

  
