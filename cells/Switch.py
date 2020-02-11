from cells.Cell import Cell

class Switch(Cell):
    """
    Class Switch représentant un interrupteur sur le
    réseau électrique.

    - Un interrupteur peut être allumé (ON) ou
    éteint (OFF) par l'équipe de réparation.
    - Lorsque l'interrupteur est éteint et que
    le réseau dont il est responsable est réparé,
    l'équipe de réparation peut y accéder pour l'allumer (ON).
    - Lorsque l'interrupteur est allumé et que
    le réseau dont il est responsable est endommagé,
    l'équipe de réparation peut y accéder pour l'éteindre (OFF).
    - Un interrupteur a une responsabilité comprise entre 0 et 1
    selon l'impact qu'aurait son extinction sur le réseau.
    """

    def __init__(self, position, is_on):
        """
        Constructeur de la classe Switch.

        :param Position position: position de l'interrupteur dans le monde.
        :param bool is_on: état de marche de l'interrupteur (ON/OFF).
        :raises TypeError: si le type de l'argument 'is_on' n'est pas booléen.
        """
        super().__init__(position)
        if isinstance(is_on, bool):
            self.is_on = is_on
        else:
            raise TypeError("Argument 'is_on' must be a boolean")

        # Réseau dont l'interrupteur est responsable.
        # Sera mis à jour dans la phase d'analyse du monde.
        self.network = {
            "breakages": [],
            "houses": []
        }

        # La responsabilité de l'interrupteur est initialisée
        # à 1 mais sera mise à jour lors de la phase d'analyse du monde.
        self.responsibility = 1

    def is_network_repaired(self):
        """
        Méthode indiquant si le réseau sous la responsabilité de
        l'interrupteur est réparé ou non.

        :return: état du réseau (fonctionnel/endommagé)
        :rtype: bool
        """
        return len(self.network["breakages"]) == 0

    def is_accessible(self):
        """
        Méthode indiquant si l'équipe de réparation peut se déplacer
        sur l'interrupteur ou non.

        :return: le statut d'accessibilité de l'interrupteur.
        :rtype: bool
        """
        network_repaired = self.is_network_repaired()
        return (not self.is_on and network_repaired) or (self.is_on and not network_repaired)

    def __str__(self):
        """
        Méthode permettant l'affichage de l'interrupteur. 

        :return: représentation textuelle de l'interrupteur.
        :rtype: str
        """
        responsibility_str = f"-> responsibility: {self.responsibility}"
        network_status = "working" if self.is_network_repaired() else "damaged"
        network_str = f"-> network status: {network_status}"
        return f"Switch({self.x}, {self.y}) [\n{responsibility_str}\n{network_str}\n]"

    def get_type(self):
        """
        Méthode permettant de connaître le type
        de la cellule.

        :return: un caractère représentant la cellule.
        :rtype: str
        """
        return "i"