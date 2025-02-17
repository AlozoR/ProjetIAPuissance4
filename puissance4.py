# https://colab.research.google.com/drive/1wHtBWBeEUUoQoFK2aN6ecgC_pd-LLRdW?usp=sharing

import numpy as np
import random as rd
import time

CRED = '\33[31m'
CEND = '\033[0m'
CBLUE = '\33[34m'


def print_grille():
    for i in range(6):
        print("|", end=' ')
        for j in range(12):
            if grille[i][j] == 1:
                print(CBLUE + '\u25cf' + CEND, end=' ')
            elif grille[i][j] == 2:
                print(CRED + '\u25cf' + CEND, end=' ')
            else:
                print(" ", end=' ')
            print("|", end=' ')
        print()
    print("|", end=' ')
    for i in range(12):
        print("\u0305 ", end=" ")
        print("|", end=' ')
    print()
    print("|", end=' ')
    for i in range(12):
        if i < 9:
            print(i + 1, end=" ")
        else:
            print(i + 1, end='')
        print("|", end=' ')
    print()


def place_pion(grid, colonne, j):
    for i in range(5, -1, -1):
        if grid[i][colonne] == 0:
            grid[i][colonne] = j
            return grid


def actions(s):
    rep = []
    for j in range(12):
        if s[0][j] == 0:
            rep.append(j)
    return rep


def result(s, a):
    s_prime = s.copy()
    s_prime = place_pion(s_prime, a, joueur_minimax)
    return s_prime


def terminal_test(s, numero_coup):
    res = (False, -1)
    if numero_coup < 7:
        return res
    if numero_coup == 42:
        res = (True, 0)
    # lignes
    for j in range(9):
        for i in range(5, -1, -1):
            if s[i][j] == s[i][j + 1] == s[i][j + 2] == s[i][j + 3] != 0:
                return True, s[i][j]
    # colonnes
    for i in range(5, 2, -1):
        for j in range(12):
            if s[i][j] == s[i - 1][j] == s[i - 2][j] == s[i - 3][j] != 0:
                return True, s[i][j]
    # diagonales montantes
    for i in range(5, 2, -1):
        for j in range(9):
            if s[i][j] == s[i - 1][j + 1] == s[i - 2][j + 2] \
                    == s[i - 3][j + 3] != 0:
                return True, s[i][j]
    # diagonales descendantes
    for i in range(5, 2, -1):
        for j in range(3, 12):
            if s[i][j] == s[i - 1][j - 1] == s[i - 2][j - 2] \
                    == s[i - 3][j - 3] != 0:
                return True, s[i][j]

    return res


def utility_tuple(x, next_is_us, s, i, j):
    somme = 0
    ones = x.count(1)
    twos = x.count(2)
    zeros = 4 - ones - twos
    if ones == 3 and zeros == 1:
        ind_z_rel = x.index(0)
        ind_z_abs = i - ind_z_rel if x[4] == 'dm' \
            else \
            i + ind_z_rel if x[4] == 'dd' \
                else i
        if next_is_us \
                and (x[4] == 'v'
                     or ind_z_abs == 5
                     or s[ind_z_abs + 1, j + ind_z_rel]):
            return 20000
        somme = 500
    elif ones == 2 and zeros == 2:
        somme = 200
    elif ones == 1 and zeros == 3:
        somme = 50
    elif twos == 3 and zeros == 1:
        ind_z_rel = x.index(0)
        ind_z_abs = i - ind_z_rel if x[4] == 'dm' \
            else \
            i + ind_z_rel if x[4] == 'dd' \
                else i
        if not next_is_us \
                and (x[4] == 'v'
                     or ind_z_abs == 5
                     or s[ind_z_abs + 1, j + ind_z_rel]):
            return -10000
        somme = -500
    elif twos == 2 and zeros == 2:
        somme = -200
    elif twos == 1 and zeros == 3:
        somme = -50

    return somme


def utility(s, w=-1, next_is_us=0):
    # next_is_us = 1 : ia va jouer
    # next_is_us = 0 : adv va jouer
    if w == 1:
        return 1000000
    elif w == 0:
        return 0
    elif w == 2:
        return -1000000

    somme = 0
    for i in range(5, -1, -1):
        for j in range(12):
            # lignes
            if j < 9:
                x = (s[i, j], s[i, j + 1], s[i, j + 2], s[i, j + 3], 'l')
                somme += utility_tuple(x, next_is_us, s, i, j)
            # colonnes
            if i > 2 and not s[i, j]:
                x = (s[i, j], s[i - 1, j], s[i - 2, j], s[i - 3, j], 'v')
                somme += utility_tuple(x, next_is_us, s, i, j)
            # diagonales montantes
            if j < 9 and i > 2:
                x = (s[i, j], s[i - 1, j + 1], s[i - 2, j + 2], s[i - 3, j + 3],
                     'dm')
                somme += utility_tuple(x, next_is_us, s, i, j)
            # diagonales descendantes
            if j < 9 and i < 3:
                x = (s[i, j], s[i + 1, j + 1], s[i + 2, j + 2], s[i + 3, j + 3],
                     'dd')
                somme += utility_tuple(x, next_is_us, s, i, j)

    return somme


"""Partie 2"""


def minimax_decision(s):
    # print(s)
    a = actions(s)
    # print(a)
    return max(a, key=lambda x: min_value(
        result(s, x), numero_coup_partie))


def max_value(s, numero_coup=1, profondeur=1):
    t = terminal_test(s, numero_coup)
    if t[0] or profondeur >= limite_profondeur:
        return utility(s, t[1], 1)
    v = -10000000
    for a in actions(s):
        global joueur_minimax
        joueur_minimax = 1
        v = max(v, min_value(result(s, a), numero_coup + 1, profondeur + 1))
    return v


def min_value(s, numero_coup=1, profondeur=1):
    t = terminal_test(s, numero_coup)
    if t[0] or profondeur >= limite_profondeur:
        return utility(s, t[1], 0)
    v = 10000000
    for a in actions(s):
        global joueur_minimax
        joueur_minimax = 2
        v = min(v, max_value(result(s, a), numero_coup + 1, profondeur + 1))
    joueur_minimax = 1
    return v


def alpha_beta_search(s):
    a = actions(s)
    # print(a)
    return max(a, key=lambda x: min_value_ab(
        result(s, x), -10000000, 10000000, numero_coup_partie))


def max_value_ab(s, alpha, beta, numero_coup=1, profondeur=1):
    t = terminal_test(s, numero_coup)
    if t[0] or profondeur >= limite_profondeur:
        return utility(s, t[1])
    v = -10000000
    for a in actions(s):
        global joueur_minimax
        global action
        joueur_minimax = 1
        temp = min_value_ab(result(s, a), alpha, beta, numero_coup + 1,
                            profondeur + 1)
        if temp > v:
            v = temp
            action = a
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value_ab(s, alpha, beta, numero_coup=1, profondeur=1):
    t = terminal_test(s, numero_coup)
    if t[0] or profondeur >= limite_profondeur:
        return utility(s, t[1])
    v = 10000000
    for a in actions(s):
        global joueur_minimax
        joueur_minimax = 2
        v = min(v, max_value_ab(result(s, a), alpha, beta, numero_coup + 1,
                                profondeur + 1))
        if v <= alpha:
            return v
        beta = min(beta, v)
    joueur_minimax = 1
    return v


"""Test"""
# print(terminal_test(s))
# print(actions(s))
# print(result(s,[0,0]))
# print(s)
# print(terminal_test(s))
# print(utility(s))


if __name__ == '__main__':
    continuer = 1
    while continuer:
        print('\n\nDébut de partie\n')
        limite_profondeur = 3
        numero_coup_partie = 1
        grille = np.zeros((6, 12), dtype=int)
        # grille = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        #                    [0, 0, 1, 2, 0, 0, 0, 2, 0, 0, 0, 0],
        #                    [0, 2, 2, 1, 0, 0, 2, 2, 0, 0, 0, 0],
        #                    [1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 0, 0]])
        # grille = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0]])
        # grille = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0],
        #                    [0, 0, 2, 1, 2, 1, 2, 0, 0, 0, 0, 0],
        #                    [0, 1, 2, 1, 1, 2, 2, 0, 1, 0, 0, 0]])
        # grille = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0],
        #                    [0, 0, 2, 1, 0, 0, 1, 2, 2, 0, 0, 0],
        #                    [2, 0, 1, 1, 0, 0, 1, 1, 2, 2, 0, 0],
        #                    [1, 0, 2, 1, 1, 0, 2, 2, 1, 1, 1, 2]])
        # grille = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0],
        #                    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        #                    [2, 0, 2, 0, 2, 1, 1, 1, 0, 0, 0, 0]])
        # print(grille)
        # affichage(grille)
        print_grille()
        print('Tour numéro ', numero_coup_partie)
        action = 0
        joueur = 0
        while not (joueur == 1 or joueur == 2):
            try:
                joueur = int(input('Entrer le joueur qui commence ' +
                                   '(1: ordinateur, 2: joueur)\n> '))
            except ValueError:
                joueur = 0
        joueur_minimax = 1
        # print(minimax_decision(grille))
        # print(alpha_beta_search(grille))
        while not terminal_test(grille, numero_coup_partie - 1)[0]:
            if joueur == 1:
                print("Tour de l'ordinateur")
                start = time.time()
                action = 0
                # decision = minimax_decision(grille)
                decision = alpha_beta_search(grille)
                end = time.time()
                print("Décision de l'IA : ", decision + 1)
                print('Temps de la décision :', end - start, 'secondes')
            else:
                print("Tour du joueur")
                actions_possibles = actions(grille)
                actions_possibles = [x + 1 for x in actions_possibles]
                print("Actions possibles : ", actions_possibles)
                decision = -1
                while decision not in actions_possibles:
                    try:
                        decision = int(input('Entrer la colonne\n> '))
                    except ValueError:
                        decision = -1
                decision -= 1

            grille = place_pion(grille, decision, joueur)
            numero_coup_partie += 1
            joueur = joueur % 2 + 1
            # print(grille)
            # affichage(grille)
            print_grille()
            print('Tour numéro ', numero_coup_partie)

        etat = terminal_test(grille, numero_coup_partie - 1)[1]
        if etat == 1:
            print("Victoire de l'ordinateur")
        elif etat == 2:
            print("Victoire du joueur")
        else:
            print("Égalité")

        continuer = -1
        while not (continuer == 1 or continuer == 0):
            try:
                continuer = int(input('Voulez-vous rejouer ? (0/1)\n> '))
            except ValueError:
                continuer = -1

