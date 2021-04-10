import copy
from itertools import product


class Joueur:

    def __init__(self, nom):
        self.nom = nom
        self.strats = None
        self.mixte = None

    def ajouter_strats(self, strats):
        self.strats = strats

    def ajouter_mixte(self, proba):
        self.mixte = proba

    def __repr__(self):
        if self.strats is None:
            return self.nom
        elif self.mixte is not None:
            return self.nom + str(self.strats) + str(self.mixte)
        else:
            return self.nom + str(self.strats)

    def __eq__(self, other):
        return self.nom == other.nom

    def get_ProfilsAdv(self, game):
        """me retourne les profils adv de mon joueur"""
        advs = self.get_StratsAdv(game)

        combined = []
        for pair in product(*advs):
            combined.append(pair)

        return combined

    def get_StratsAdv(self, game):
        """retourne une liste des listes des strats adv de mon joueur"""
        strats_adv = []

        cp = copy.deepcopy(game)
        cp.remove(self)

        for p in cp:
            strats_adv.append(p.strats)

        return strats_adv
