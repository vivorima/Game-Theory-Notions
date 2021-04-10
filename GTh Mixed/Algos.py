import itertools
from itertools import product
from Joueur import Joueur as j
from Strat import Strat as s
from Profil import Profil as p
from fractions import Fraction
import numpy as np


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def isfraction(value):
    try:
        Fraction(value)
        return True
    except (ValueError, ZeroDivisionError):
        return False


def isaccepted(value):
    return (isfraction(value) and not isfloat(value)) or value == "1" or value == "0"


def get_Profils(game):
    """nous donne les profils du jeu en combinant les stratégies des joueurs"""
    strats = []
    for j in game:
        strats.append(j.strats)

    combined = []
    for pair in product(*strats):
        profil = p(pair)
        combined.append(profil)

    return combined


def Ajouter_Gains(Profils, Gains):
    """Ajoute pour chaque profil son gain --- Affectation directe"""
    for i in range(len(Profils)):
        Profils[i].ajouter_gain(Gains[i])


def Attribuer_Profils(Joueurs, Profils):
    """Attribue a chaque stratégie les profils où elle apparait"""
    for j in range(len(Joueurs)):
        for s in Joueurs[j].strats:
            liste = []
            for p in Profils:
                if p.strats[j] == s: liste.append(p)
            s.ajouter_Profils(liste)


# 𝜎=(𝜎𝑖,𝜎−𝑖) est un équilibre de Nash si et seulement si
# ∀𝑠𝑖,𝑠′𝑖 ∈ 𝑠𝑢𝑝𝑝(𝜎𝑖)    𝑢𝑖(𝑠𝑖,𝜎−𝑖)=𝑢𝑖(𝑠′𝑖,𝜎−𝑖)=𝑢𝑖(𝜎𝑖,𝜎−𝑖)
# et ∀𝑠𝑖∉𝑠𝑢𝑝𝑝(𝜎𝑖)       𝑢𝑖(𝑠𝑖,𝜎−𝑖)=𝑢𝑖(𝑠𝑖,𝜎−𝑖)≤𝑢𝑖(𝜎𝑖,𝜎−𝑖)

def isNash(joueurs):
    # check si les données dont valides
    for j in joueurs:
        som = 0
        for m in j.mixte:
            if m < 0 or m > 1: return False, "\nProbas > 1 ou < 0"
            som = som + m
        if som > 1 or som < 0: return False, "\nSomme > 1 ou < 0"

    Affichage = ""
    # Indifference sur le support
    support = [[], []]
    horsSupport = [[], []]
    for j in range(len(joueurs)):
        for i in range(len(joueurs[j].strats)):
            if joueurs[j].mixte[i] > 0:
                support[j].append(joueurs[j].strats[i])
            else:
                horsSupport[j].append(joueurs[j].strats[i])
    listToStr = ','.join([str(elem) for elem in support])
    Affichage = Affichage + "\nSupport = " + str(listToStr)

    # Calcul gain des support
    # calcul du gain d'une strat
    # 𝑢𝑖(𝑠𝑖,𝜎−𝑖) = Somme ui(si,s-i) * 𝜎−𝑖(s-i) ex u1 = 2q+4(1-q)
    for j in range(len(support)):
        Affichage = Affichage + "\n Gains Des Strats Du Joueur " + str(j + 1)
        his = 2200650022  # initialisation random
        adv = joueurs[(j + 1) % 2]
        gain = 0
        for s in support[j]:
            gain = 0
            if s is not None:
                for u in range(len(s.profils)):
                    gain = Fraction(gain) + Fraction(s.profils[u].gains[j]) * Fraction(adv.mixte[u])
                print(s, gain)
                Affichage = Affichage + "\nu" + str(j) + " (" + str(s.nom) + ",𝜎" + str((j + 1) % 2) + ") = " \
                            + str(gain)
                if his == 2200650022:  # si c'est la premiere strategie
                    his = Fraction(gain)
                elif gain != his:
                    Affichage = Affichage + "\n Ce profil n'est pas un Equilibre de Nash car: " + str(
                        gain) + " != " + str(
                        his) + "\n∀𝑠𝑖,𝑠′𝑖 ∈ 𝑠𝑢𝑝𝑝(𝜎𝑖) on doit avoir 𝑢𝑖(𝑠𝑖,𝜎−𝑖)=𝑢𝑖(𝑠′𝑖,𝜎−𝑖)"
                    return False, Affichage
        #     on arrive ici à la fin du support du J1 si tous les gains sont ==
        for h in horsSupport[j]:
            hgain = 0
            if h is not None:
                for u in range(len(h.profils)):
                    hgain = Fraction(hgain) + Fraction(h.profils[u].gains[j]) * Fraction(adv.mixte[u])
                print(h, hgain)
                Affichage = Affichage + "\nu" + str(j) + " (" + str(h.nom) + ",𝜎" + str((j + 1) % 2) + ") = " \
                            + str(hgain)
                if Fraction(gain) < Fraction(hgain):
                    Affichage = Affichage + "\n Ce profil n'est pas un Equilibre de Nash car:" + str(
                        his) + " < " + str(
                        hgain) + "\n∀𝑠𝑖 ∉ 𝑠𝑢𝑝𝑝(𝜎𝑖) on doit avoir 𝑢𝑖(𝑠𝑖,𝜎−𝑖)=𝑢𝑖(𝑠𝑖,𝜎−𝑖)≤𝑢𝑖(𝜎𝑖,𝜎−𝑖) "
                    return False, Affichage
    listToStr = ','.join([str(elem) for elem in joueurs[0].mixte])
    Affichage = Affichage + "\n(" + listToStr + ")"
    listToStr = ','.join([str(elem) for elem in joueurs[1].mixte])
    Affichage = Affichage + "(" + listToStr + ")" + " est un Equilibre de Nash"
    return True, Affichage


def trouver_Nash(joueurs, profils):
    Affichage = ""
    Nashs = []
    # For all 1≤k≤min(m,n) : on commence par 2 car les support à 1 sont les strats pures
    for k in range(2, min(len(joueurs[0].strats), len(joueurs[1].strats)) + 1):
        Affichage = Affichage + "\n" + "Supports de Taille = " + str(k)
        # get les supports possibles de taille k
        combos1k = list(itertools.combinations(joueurs[0].strats, k))
        combos2k = list(itertools.combinations(joueurs[1].strats, k))
        # For all pairs of support de taille k
        for pair in list(itertools.product(combos1k, combos2k)):
            SoluPair = []
            Affichage = Affichage + "\n\n" + "Pour la pair de support = " + str(pair) + "\n"
            # cherchons la strat mixte pour chaque joueur pour cette combo de support
            for mixte in pair:
                moi = pair.index(mixte)
                adv = (pair.index(mixte) + 1) % 2
                # initialisations des listes equations
                eqs = [[0 for i in range(len(joueurs[adv].strats))] for j in range(k)]
                cond = [1 for i in range(len(joueurs[adv].strats))]
                # Creating the system equations ---> on parcoure les gains de nos strats
                for strat in range(len(mixte)):
                    for profil in range(len(mixte[strat].profils)):
                        # si la strat appartient au support
                        if mixte[strat].profils[profil].strats[adv] in pair[adv]:
                            eqs[strat][profil] = mixte[strat].profils[profil].gains[moi]
                        else:
                            # la strategie qui napparait dans le support de lautre joueur
                            cond[profil] = 0
                Affichage = Affichage + "\n         " + "Equations du joueurs " + joueurs[adv].nom + ":  " + str(
                    eqs)[1:-1] + "," + str(cond)

                # Solving the system of equations so im creating 2 equations if k =2 and 3 if k=3
                if k == 2:
                    try:
                        # cleaning the data to solve it
                        temp = []
                        for g, gg in zip(eqs[0], eqs[1]):
                            temp.append(g - gg)
                            # si le joueur a 3 strats et support = 2 ---> i remove le 0 cuz i have 2 vars and i dont have 3 equations
                        if cond.__contains__(0):
                            temp.pop(cond.index(0))
                        #     Essayer de trouver une solution**************************************
                        A = np.array([temp, [1] * k])
                        b = np.array([0, 1])
                        x = np.linalg.solve(A, b)
                        sol = list(x)
                        if cond.__contains__(0):  # si le joueur a 3 strats et support = 2
                            sol.insert(cond.index(0), 0)
                        SoluPair.append(sol)
                    except np.linalg.LinAlgError as e:
                        if 'Singular matrix' in str(e):
                            Affichage = Affichage + "\n         -->Contradiction"
                elif k == 3:
                    try:
                        temp = []
                        for g, gg in zip(eqs[0], eqs[1]):
                            temp.append(g - gg)
                        temp1 = []
                        for g, gg in zip(eqs[1], eqs[2]):
                            temp1.append(g - gg)
                        #     Essayer de trouver une solution
                        A = np.array([temp, temp1, [1] * k])
                        b = np.array([0, 0, 1])
                        x = np.linalg.solve(A, b)
                        sol = list(x)
                        SoluPair.append(sol)
                    except np.linalg.LinAlgError as e:
                        if 'Singular matrix' in str(e):
                            Affichage = Affichage + "\n         -->Contradiction"

            if len(SoluPair) != 2:  # si il ya une contradiction donc ya pas de solution
                Affichage = Affichage + "\n-->Aucune Solution Possible"
            else:
                SoluPair.reverse()
                for liste in range(len(SoluPair)):
                    SoluPair[liste] = [Fraction(ele).limit_denominator() for ele in SoluPair[liste]]

                listToStr = ""
                for l in SoluPair:
                    listToStr = listToStr + "("
                    for f in l:
                        listToStr = listToStr + str(f) + ","
                    listToStr = listToStr + ")"

                Affichage = Affichage + "\n-->Solution trouvée: " + str(listToStr)

                # On doit vérifier les conditions de maximisations dans le cas ou m != n ou m=n=3 et k =2
                # Cette étape est triviale pour le cas m=n=2 ou m=n=3 avec k==3 car il n'existe pas de gains hors supp
                if len(joueurs[0].strats) != len(joueurs[1].strats) or (
                        len(joueurs[0].strats) == len(joueurs[1].strats) == 3 and k == 2):
                    # Find who has 3 strats and multiply ses gains f la mixte de lautre joueur and then verify si ses
                    # Gains dans son support sont == et > 3la les gains hors support u can use cond to do that
                    # we call is nash qui va faire cette verification puisque c'est l'invariance au support
                    Affichage = Affichage + "\nVerification des conditions de maximisation:"
                    joueurs[0].ajouter_mixte(SoluPair[0])
                    joueurs[1].ajouter_mixte(SoluPair[1])
                    b, ch = isNash(joueurs)
                    Affichage = Affichage + ch
                    if b: Nashs.append(SoluPair)
                else:  # pas de verification de maximisation necessaire pas de hors support
                    good = True
                    for j in SoluPair:
                        som = 0
                        for m in j:
                            if m < 0 or m > 1:
                                Affichage = Affichage + "\nProbas <0 ou >1"
                                good = False
                                break
                            som = som + m
                        if som > 1 or som < 0:
                            Affichage = Affichage + "\nSomme <0 ou >1"
                            good = False
                            break
                    if good:
                        Nashs.append(SoluPair)
    listToStr = ""
    for l in Nashs:
        for e in l:
            listToStr = listToStr + "(" + ','.join([str(elem) for elem in e]) + ")  "
        listToStr = listToStr + "\n"
    if len(Nashs) > 0:
        Affichage = Affichage + "\n\nLes Equilibres de Nash:\n" + listToStr
    else:
        Affichage = Affichage + "\n\nAucun Equilibre de Nash"
    return Affichage

# def trouver_Nash(joueurs, profils):
#     # check si game n'est pas degenré
#     # nb best response à une strat n'est pas > taille du support
#     # print(profils)
#     # For all 1≤k≤min(m,n) : on commence par 2 car les support à 1 sont les strats pures so call nash des strats pures
#     for k in range(2, min(len(joueurs[0].strats), len(joueurs[1].strats)) + 1):
#         # get les supports possibles de taille k
#         combos1k = list(itertools.combinations(joueurs[0].strats, k))
#         combos2k = list(itertools.combinations(joueurs[1].strats, k))
#         # For all pairs of support de taille k
#         for pair in list(itertools.product(combos1k, combos2k)):
#             # Creating the system equations
#             print("Pour les supports = ", pair, "----------------------------------------------")
#             eqs = [[0] * len(Joueurs[0].strats), [0] * len(Joueurs[1].strats)]
#             # Build les equation avec les gains à partir des pairs que t'as
#             for j in range(len(pair)):
#                 print("Pour sigma de " , Joueurs[(j + 1) % 2])
#                 for strat in pair[j]:
#                     print(strat, "**")
#                     for profil in strat.profils:
#                         print(profil, "--")
#                         if profil.strats[(j + 1) % 2] in pair[(j + 1) % 2]:
#                             sign = -1
#                             nb = Joueurs[(j + 1) % 2].strats.index(profil.strats[(j + 1) % 2])
#                             # eqs[(j + 1) % 2][nb] = sign*-1*eqs[(j + 1) % 2][nb] +profil.gains[(j + 1) % 2]
#                             print(profil.strats[(j + 1) % 2].nom, "exists in", pair[(j + 1) % 2])
#                             # print(eqs)
#                         else:
#                             print(profil.strats[(j + 1) % 2].nom, "NOT IN", pair[(j + 1) % 2])
#                             pass
#             #                 0 pour les autres strat
#
#             # Solving the equations
#             A = np.array([[1 / 2 + 1, -1 - 3], [1] * 2])
#             b = np.array([0, 1])
#             x = np.linalg.solve(A, b)
#             # print(x)
#     return ""

    # check si game n'est pas degenré
    # nb best response à une strat n'est pas > taille du support