
from cells.Cell import Cell


class Obstacle(Cell):
    """
    Classe Obstacle représentant un obstacle
    dans le monde.

    - Un obstacle est toujours inaccessible pour
    l'équipe de réparation.
    """

    def __init__(self, position):
        """
        Constructeur de la classe Obstacle.

        :param Position position: position de l'obstacle dans le monde.
        """
        super().__init__(position)
        
    def is_accessible(self):
        """
        Méthode indiquant si l'équipe de réparation peut se déplacer
        sur la cellule ou non.

        :return: le statut d'accessibilité de la cellule.
        :rtype: bool
        """
        return False

    def __str__(self):
        """
        Méthode permettant l'affichage de l'obstacle. 
        
        :return: représentation textuelle de l'obstacle.
        :rtype: str
        """
        return f"Obstacle({self.x}, {self.y})"

    def get_type(self):
        """
        Méthode permettant de connaître le type
        de la cellule.

        :return: un caractère représentant la cellule.
        :rtype: str
        """
        return "#"