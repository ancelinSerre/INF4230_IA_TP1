from cells.Cell import Cell


class PowerSource(Cell):
    """
    Classe PowerSource représentant une source
    d'électricité.

    - Une source d'électricité est toujours
    accessible par l'équipe de réparation.
    - Une source ne peut pas être endommagée.
    - Une source distribue son énergie à ses
    cellules voisines (Nord, Sud, Est, Ouest).
    """

    def __init__(self, position):
        """
        Constructeur de la classe PowerSource.

        :param Position position: position de la source d'énergie dans le monde.
        """
        super().__init__(position)


    def __str__(self):
        """
        Méthode permettant l'affichage de la source d'énergie.

        :return: représentation textuelle de la source.
        :rtype: str
        """
        return f"PowerSource({self.x}, {self.y})"


    def get_type(self):
        """
        Méthode permettant de connaître le type
        de la cellule.

        :return: un caractère représentant la cellule.
        :rtype: str
        """
        return "s"