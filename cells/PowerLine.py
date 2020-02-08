
from cells.Cell import Cell


class PowerLine(Cell):
    """
    Class PowerLine représentant une ligne électrique.

    - Lorsqu'elle est alimentée, une ligne électrique 
    fournit du courant à toutes ses cellules voisines 
    (Nord, Sud, Est, Ouest).
    - Une ligne électrique est alimentée lorsqu'elle
    est reliée sur un réseau en état de marche.
    (=> Reliée à au moins une source avec interrupteur sur ON)
    - Une ligne électrique tombe en panne lorsqu'un
    bris est détecté sur son emplacement.
    """

    def __init__(self, position, is_down):
        """
        Constructeur de la classe PowerLine.

        :param Position position: position de la ligne électrique dans le monde.
        :param bool is_down: état de marche de la ligne (en panne ou non).
        :raises TypeError: si le type de l'argument 'is_down' n'est pas booléen.
        """
        super().__init__(position)
        if isinstance(is_down, bool):
            self.is_down = is_down
        else:
            raise TypeError("Argument 'is_down' must be a boolean")

    def is_accessible(self):
        """
        Méthode indiquant si l'équipe de réparation peut se déplacer
        sur la ligne électrique ou non.

        :return: le statut d'accessibilité de la ligne.
        :rtype: bool
        """
        #### MAL FAIT A REFAIRE
        return not self.is_down

    def __str__(self):
        """
        Méthode permettant l'affichage de la ligne électrique. 
        
        :return: représentation textuelle de la ligne.
        :rtype: str
        """
        status = "down" if self.is_down else "working"
        return f"PowerLine({self.x}, {self.y}) [\n-> status: {status}\n]"

    def get_type(self):
        """
        Méthode permettant de connaître le type
        de la cellule.

        :return: un caractère représentant la cellule.
        :rtype: str
        """
        return "c"