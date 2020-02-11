from Position import Position


class Cell:
    """
    Classe Cell représentant une cellule du monde
    dans lequel l'équipe de réparation va évoluer
    pour résoudre les problèmes d'électricité/pannes.
    """

    def __init__(self, position):
        """
        Constructeur de la classe Cell.

        :param Position position: position de la cellule dans le monde.
        :raises TypeError: si le type de l'argument 'position' n'est pas Position.
        """
        # Parent de la cellule (utilisé pour retrouver le chemin
        # emprunté par l'équipe de réparation)
        self.parentr = None
        self.parentp = None

        # Indique si la cellule est alimentée ou non en énergie.
        self.powered = False

        # Métrique pour l'algorithme A* concernant l'objectif principal.
        self.gr = 0
        self.hr = 0
        self.fr = 0

        # Métrique pour l'algorithme A* concernant la recherche de chemin.
        self.gp = 0
        self.hp = 0
        self.fp = 0

        self.path_length = 0

        if isinstance(position, Position):
            self.position = position
        else:
            raise TypeError("Argument 'position' must be a Position")


    @property
    def x(self):
        """
        Propriété permettant d'accéder à la position 'x' de la cellule.

        :return: position 'x' de la cellule.
        :rtype: int
        """
        return self.position.row


    @property
    def y(self):
        """
        Propriété permettant d'accéder à la position 'y' de la cellule.

        :return: position 'y' de la cellule.
        :rtype: int
        """
        return self.position.column


    def is_accessible(self):
        """
        Méthode indiquant si l'équipe de réparation peut se déplacer
        sur la cellule ou non.

        :return: le statut d'accessibilité de la cellule.
        :rtype: bool
        """
        return True


    def __str__(self):
        """
        Méthode permettant l'affichage de la cellule.

        :return: représentation textuelle de la cellule.
        :rtype: str
        """
        return f"Cell({self.x}, {self.y})"


    def get_type(self):
        """
        Méthode permettant de connaître le type
        de la cellule.

        :return: un caractère représentant la cellule.
        :rtype: str
        """
        return "d"
