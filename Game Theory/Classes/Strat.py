import copy


class Strat:

    def __init__(self, nom, joueur):
        self.nom = nom
        self.joueur = joueur
        self.profils = None

    def ajouter_Profils(self, liste_Profils):
        self.profils = liste_Profils

    def __str__(self):
        if self.profils == None:
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

    def strict_domine(self, other, Joueurs):

        for i in range(len(self.profils)):
            if self.profils[i].gains[Joueurs.index(self.joueur)] <= other.profils[i].gains[
                Joueurs.index(self.joueur)]: return False

        return True

    def faible_domine(self, other, Joueurs):

        for i in range(len(self.profils)):
            if self.profils[i].gains[Joueurs.index(self.joueur)] < other.profils[i].gains[
                Joueurs.index(self.joueur)]: return False

        return True

    def Niv_Secu(self, Joueurs):
        """MIN DES GAINS DU JOUEURS"""
        niv = copy.deepcopy(self.profils[0].gains[Joueurs.index(self.joueur)])

        for p in self.profils:
            if p.gains[Joueurs.index(self.joueur)] < niv:
                niv = copy.deepcopy(p.gains[Joueurs.index(self.joueur)])

        return niv

    def Niv_Punition(self, Joueurs):
        """MAX DES GAINS DU JOUEURS"""
        niv = copy.deepcopy(self.profils[0].gains[Joueurs.index(self.joueur)])

        for p in self.profils:
            if p.gains[Joueurs.index(self.joueur)] > niv:
                niv = copy.deepcopy(p.gains[Joueurs.index(self.joueur)])

        return niv
