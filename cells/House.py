from cells.Cell import Cell


class House(Cell):
    """
    Classe House représentant une maison du monde 
    dans lequel l'équipe de réparation va évoluer.

    - Une maison est toujours accessible pour l'équipe
    de réparation.
    - Une maison est alimentée ou non par au moins une
    ligne électrique.
    - Une maison sait pendant combien d'unités de temps
    elle n'a pas été alimentée.
    """

    def __init__(self, position):
        """
        Constructeur de la classe House.

        :param Position position: position de la maison dans le monde.
        """
        super().__init__(position)
        # - Quand on va lire le contenu de la carte, 
        # on ne va pas tout de suite se préoccuper de
        # l'état de chaque cellule.
        # - Cette étape sera réalisée après 
        # lecture complète du monde.
        self._is_powered = True

        # Temps de coupure (en unité de temps) pour la maison.
        # Devrait être mis à jour à chaque action effectuée
        # par l'équipe de réparation :
        # (déplacements/interrupteurs ON;OFF/réparations)
        self.outage_time = 0


    @property
    def is_powered(self):
        """
        Propriété permettant de savoir si la maison est alimentée ou non. 
        
        :return: statut d'alimentation de la maison.
        :rtype: bool
        """
        return self._is_powered


    @is_powered.setter
    def is_powered(self, powered):
        """
        Propriété permettant de mettre à jour le statut 
        d'alimentation de la maison. 
        
        :param bool powered: statut d'alimentation de la maison.
        :raises TypeError: si le type de l'argument 'powered' n'est pas booléen.
        """
        if isinstance(powered, bool):
            self._is_powered = powered
        else:
            raise TypeError("Argument 'powered' must be a boolean")


    def __str__(self):
        """
        Méthode permettant l'affichage de la maison. 
        
        :return: représentation textuelle de la maison.
        :rtype: str
        """
        powered_status = "powered" if self.is_powered else "not powered"
        status_str = f"-> status: {powered_status}"
        outage_str = f"-> outage time: {self.outage_time}"
        return f"House({self.x}, {self.y}) [\n{status_str}\n{outage_str}\n]"


    def get_type(self):
        """
        Méthode permettant de connaître le type
        de la cellule.

        :return: un caractère représentant la cellule.
        :rtype: str
        """
        return "m"