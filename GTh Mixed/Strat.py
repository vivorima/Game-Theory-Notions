import copy


class Strat:

    def __init__(self, nom, joueur):
        self.nom = nom
        self.joueur = joueur
        self.profils = None

    def ajouter_Profils(self, liste_Profils):
        self.profils = liste_Profils

    def __str__(self):
        if self.profils is None:
            return self.nom
        else:
            return self.nom + " ,profils:" + str(self.profils)

    def __repr__(self):
        return self.nom

    # pour pouvoir comparer deux strats
    def __eq__(self, other):
        return self.joueur == other.joueur and self.nom == other.nom

    # Pour pouvoir la stocker dans un dict
    def __hash__(self):
        return hash(tuple(self.joueur.nom + self.nom))
