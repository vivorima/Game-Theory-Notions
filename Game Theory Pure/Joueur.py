import copy
from itertools import product


class Joueur:

    def __init__(self, nom):
        self.nom = nom
        self.strats = None

    def ajouter_strats(self, strats):
        self.strats = strats

    def __repr__(self):
        if self.strats is None:
            return self.nom
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

    def best(self, Joueurs):

        bests = copy.deepcopy(self.strats[0].profils)

        for s in self.strats[1:]:
            for i in range(len(s.profils)):
                if s.profils[i].gains[Joueurs.index(self)] > bests[i].gains[Joueurs.index(self)]: bests[
                    i] = copy.deepcopy(s.profils[i])

        return bests

    def Niv_Secu(self, Joueurs):

        """MAX DES NIV DES SECU(Min) DES STRATS DU JOUEURS"""
        niv = copy.deepcopy(self.strats[0].Niv_Secu(Joueurs))

        for s in self.strats:
            if s.Niv_Secu(Joueurs) > niv:
                niv = copy.deepcopy(s.Niv_Secu(Joueurs))
        return niv

    def securite(self, Joueurs):

        """MAX DES NIV DES SECU(Min) DES STRATS DU JOUEURS"""
        niv = copy.deepcopy(self.strats[0].Niv_Secu(Joueurs))
        ss = copy.deepcopy(self.strats[0])
        for s in self.strats:
            if s.Niv_Secu(Joueurs) > niv:
                niv = copy.deepcopy(s.Niv_Secu(Joueurs))
                ss = copy.deepcopy(s)
        return [ss,niv]

    def punition(self, Joueurs):

        """Min DES MAX DES STRATS DU JOUEURS"""
        niv = copy.deepcopy(self.strats[0].Niv_Punition(Joueurs))
        ss = copy.deepcopy(self.strats[0])
        for s in self.strats:
            if s.Niv_Punition(Joueurs) < niv:
                niv = copy.deepcopy(s.Niv_Punition(Joueurs))
                ss = copy.deepcopy(s)
        return [ss , niv]
