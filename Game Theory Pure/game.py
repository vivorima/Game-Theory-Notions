import copy
from itertools import product

import numpy as np

from Joueur import Joueur as j
from Strat import Strat as s
from Profil import Profil as p


def get_Profils(game):
    """nous donne les profils du jeu"""
    strats = []
    for j in game:
        strats.append(j.strats)

    combined = []
    for pair in product(*strats):
        profil = p(pair)
        combined.append(profil)

    return combined


def Ajouter_Gains(Profils, Gains):
    """Ajoute pour chaque profil son gain"""
    for i in range(len(Profils)):
        Profils[i].ajouter_gain(Gains[i])


def Attribuer_Profils(Joueurs, Profils):
    """Attribue a chaque strat ses profils"""
    for j in range(len(Joueurs)):
        for s in Joueurs[j].strats:
            liste = []
            for p in Profils:
                if p.strats[j] == s: liste.append(p)
            s.ajouter_Profils(liste)


def remove(s2, Eq):
    """supprime les profils contenant la strat s2"""
    for j in Eq:
        for s in j.strats:
            for p in s.profils:
                if s2 in p.strats:
                    s.profils.remove(p)


def strats_strict_dominantes(Joueurs):
    Eq = copy.deepcopy(Joueurs)

    delete = True
    affichage = ""
    # tant que je trouve des strats à supprimer
    while delete:
        delete = False
        # pour chaque joueur
        for j in range(len(Eq)):
            # je prends une strat d'un joueur et je la compare avec ses autres strats
            for s1 in list(Eq[j].strats):
                for s2 in list(Eq[j].strats):
                    # si c'est pas elle
                    if s1 != s2:
                        if s1.strict_domine(s2, Eq):
                            affichage = affichage + "\n" + Joueurs[
                                j].nom + ": " + s2.nom + " strictement dominée par " + s1.nom + "\n"
                            # si une strat est dominée je la supp des strats du joueur
                            Eq[j].strats.remove(s2)
                            delete = True
                            # je dois aussi supprimer les profils contenant cette strat chez les autres joueurs
                            remove(s2, Eq)

    print(Eq)
    for j in Eq:
        if len(j.strats) != 1:
            affichage = affichage + "\n Pas d'equilibre itératif"
            return affichage

    affichage = affichage + "\n Equilibre itératif: " + str(get_Profils(Eq))
    return affichage


def strats_faible_dominantes(Joueurs):
    Eq = copy.deepcopy(Joueurs)

    delete = True
    affichage = ""
    while delete:
        delete = False
        for j in range(len(Eq)):
            for s1 in list(Eq[j].strats):
                for s2 in list(Eq[j].strats):
                    if s1 != s2:
                        if s1.faible_domine(s2, Eq):
                            affichage = affichage + "\n" + Joueurs[
                                j].nom + ": " + s2.nom + " faiblement dominée par " + s1.nom + "\n"
                            Eq[j].strats.remove(s2)
                            delete = True
                            remove(s2, Eq)
    print(Eq)
    for j in Eq:
        if len(j.strats) != 1:
            affichage = affichage + "\n Pas d'equilibre itératif"
            return affichage

    affichage = affichage + "\n Equilibre itératif: " + str(get_Profils(Eq))
    return affichage


def affiche_Nivs(Joueurs):
    affichage = ""
    for j in Joueurs:
        affichage = affichage + "\nNiveau du Joueur " + j.nom + ": " + str(j.Niv_Secu(Joueurs)) + "\n"
        for s in j.strats:
            affichage = affichage + "Niveau de la stratégie " + s.nom + ": " + str(s.Niv_Secu(Joueurs)) + "\n"
    return affichage


def Optimum_Pareto(Profils):
    nbJ = len(Profils[0].gains)
    # il ya au max nbJ profils pareto dominants
    pareto = [copy.deepcopy(Profils[0])]

    # 3 player solution
    for pro in Profils:
        # je compare ce profil avec les profils pareto déja
        for i in range(len(pareto)):
            if pro > pareto[i] and not pro.gainEqual(pareto[i]):
                # si au moins un gain et sup et les autres ==
                pareto[i] = copy.deepcopy(pro)
                # si je duplique le profil, c'est pas grave je vais le supprimer later mais waste of time
                # pour enlever ge3 les profils qui vont etre dominé par ce profil
        if all(not pro > x and not pro < x and not pro.gainEqual(x) for x in pareto):
            # si je ne domine personne et persn ne me domine donc je suis comme eux
            # il est pareto aussi --> exemple (  [4, 4, 1], [-4, 1, 4])
            pareto.append(pro)

    #         pour enlever les soubles
    pareto = list(dict.fromkeys(pareto))

    # works perfectly for 2 players
    # for pr in Profils:
    #     for i in range(nbJ):
    #         if pr.gains[i] > pareto[i].gains[i]:  # max gain du J1
    #             pareto[i] = copy.deepcopy(pr)
    #         elif pr.gains[i] == pareto[i].gains[i]:
    #             if pr > pareto[i]:
    #                 pareto[i] = copy.deepcopy(pr)

    # pareto = list(dict.fromkeys(pareto))

    return '\n'.join(str(ele) for ele in pareto)


def Nash(Joueurs):
    Affichage = ""
    bests = []
    for j in range(len(Joueurs)):
        temp = Joueurs[j].best(Joueurs)
        Affichage = Affichage + "\n\nPour " + Joueurs[j].nom + ":"
        for p in temp:
            Affichage = Affichage + "\n" + p.strats[j].nom + " est la meilleure réponse au profil " + str(
                p.strats)
        bests.append(Joueurs[j].best(Joueurs))

    nashs = set(bests[0]).intersection(*bests)
    if len(nashs) != 0:
        Affichage = Affichage + "\n\nLes équilibres de Nash " + str(nashs)
    return Affichage


def valeur(joueurs):
    # MinMax
    affichage = ""
    for j in joueurs:
        pun = j.punition(joueurs)[1]
        sec = j.securite(joueurs)[1]

        affichage = affichage + "\n\nMinmax(" + j.nom + ") = " + str(pun) + "\nMaxMin(" + j.nom + ") = " + str(sec)

        if pun == sec:

            affichage = affichage + "\n-->Nous avons une stratégie prudente optimale en pure pour " + j.nom
        else:
            affichage = affichage + "\n-->Nous devons trouver une stratégie prudente en mixte pour " + j.nom

    affichage = affichage + "\n\nPaiement de Punition: MinMax \nPaiement de Sécurité: MaxMin"
    return affichage


def SommeNulle(joueurs, profils):
    Affichage = ""
    if len(joueurs) > 2:
        Affichage = Affichage + "\nJeu >2 Joueurs: Jeu pas à somme nulle."
        Affichage = Affichage + valeur(joueurs)
        return Affichage
    Jeu = [[] for i in range(len(joueurs[0].strats))]
    #     verifier si le jeu est somme nulle

    i = 0
    for p in range(len(profils)):
        if profils[p].gains[0] + profils[p].gains[1] != 0:
            Affichage = Affichage + "\nJeu pas à somme nulle."
            Affichage = Affichage + valeur(joueurs)
            return Affichage
        else:
            # Creation du jeu
            Jeu[i].append(profils[p].gains[0])

        if p + 1 < len(profils) and profils[p].strats[0] != profils[p + 1].strats[0]:
            i += 1

    matrix = np.array(Jeu)
    Affichage = Affichage + "\nJeu à somme nulle: \n"
    Affichage = Affichage + str(matrix)

    maxmin = np.amax(np.amin(matrix, axis=1))
    minmax = np.amin(np.amax(matrix, axis=0))

    Affichage = Affichage + "\nMaxMin = " + str(maxmin) + "\nMinMax = " + str(minmax)
    if maxmin == minmax:
        Affichage = Affichage + "\nminmax == maxmin --> Ce jeu admet une valeur"
    else:
        Affichage = Affichage + "\nminmax != maxmin --> Ce jeu n'admet pas de valeur"

    return Affichage


# Joueurs = [j("Leo"), j("Phil"), j("Eden")]
#
# Joueurs[0].ajouter_strats([s("Movies", Joueurs[0]), s("Home", Joueurs[0])])
# Joueurs[1].ajouter_strats([s("Movies", Joueurs[1]), s("Home", Joueurs[1])])
# Joueurs[2].ajouter_strats([s("Movies", Joueurs[2]), s("Home", Joueurs[2])])
#
# Profils = get_Profils(Joueurs)
# Gains = [
#     [-4, -4, -4],
#     [4, 4, 1],
#     [-4, 1, 4],
#     [-1, 1, 1],
#     [1, -4, 4],
#     [1, -1, 1],
#     [1, 1, -4],
#     [1, 1, 1],
#
# ]

Joueurs = [j("J1"), j("J2"), j("J3")]

Joueurs[0].ajouter_strats([s("X", Joueurs[0]), s("Y", Joueurs[0]), s("Z", Joueurs[0])])
Joueurs[1].ajouter_strats([s("T", Joueurs[1]), s("U", Joueurs[1]), s("V", Joueurs[1])])
Joueurs[2].ajouter_strats([s("A", Joueurs[2]), s("B", Joueurs[2])])

Profils = get_Profils(Joueurs)
Gains = [
    [3, 2, 1],  # (X, T, A)
    [4, 0, 3],  # (X, T, B)
    [5, 1, 2],  # (X, U, A)
    [1, 0, 0],  # (X, U, B)
    [7, 3, 2],  # (X, V, A)
    [2, 5, 0],  # (X, V, B)
    [2, 0, -1],  # (Y, T, A)
    [8, 5, 2],  # (Y, T, B)
    [1, 7, 8],  # (Y, U, A)
    [0, 2, 3],  # (Y, U, B)
    [2, 0, 1],  # (Y, V, A)
    [3, 1, -1],  # (Y, V, B)
    [1, 2, 0],  # (Z, T, A),
    [2, 3, 4],  # (Z, T, B),
    [1, 4, 2],  # (Z, U, A),
    [3, 1, 2],  # (Z, U, B),
    [0, 0, 2],  # (Z, V, A),
    [1, 3, 4]  # (Z, V, B)
]
Ajouter_Gains(Profils, Gains)
Attribuer_Profils(Joueurs, Profils)
print(Optimum_Pareto(Profils))
