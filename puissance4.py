import numpy as np
import random as rd

numero_coup = 0


def actions(s):
    rep = []
    for j in range(12):
        if s[0][j] == 0:
            rep.append(j)
    return rep


def result(s, a):
    s_prime = s.copy()
    for i in range(5, -1, -1):
        if s[i][a] == 0:
            s_prime[i][a] = joueur_minimax
    return s_prime


def terminal_test(s):
    res = {False, 0}
    if numero_coup < 7:
        return res
    if numero_coup == 42:
        res = {True, 0}
    # lignes
    for j in range(9):
        for i in range(5, -1, -1):
            if s[i][j] == s[i][j + 1] == s[i][j + 2] == s[i][j + 3] != 0:
                return {True, s[i][j]}
    # colonnes
    for i in range(5, 2, -1):
        for j in range(12):
            if s[i][j] == s[i - 1][j] == s[i - 2][j] == s[i - 3][j] != 0:
                return {True, s[i][j]}
    # diagonales montantes
    for i in range(5, 2, -1):
        for j in range(9):
            if s[i][j] == s[i - 1][j + 1] == s[i - 2][j + 2]\
                    == s[i - 3][j + 3] != 0:
                return {True, s[i][j]}
    # diagonales descendantes
    for i in range(5, 2, -1):
        for j in range(3, 12):
            if s[i][j] == s[i - 1][j - 1] == s[i - 2][j - 2]\
                    == s[i - 3][j - 3] != 0:
                return {True, s[i][j]}

    return res


def utility(s):
    rep = 0
    if (s[0][0] == s[0][1] == s[0][2] == 1
            or s[0][0] == s[1][0] == s[2][0] == 1
            or s[0][0] == s[1][1] == s[2][2] == 1
            or s[1][0] == s[1][1] == s[1][2] == 1
            or s[2][0] == s[2][1] == s[2][2] == 1
            or s[0][1] == s[1][1] == s[2][1] == 1
            or s[2][0] == s[1][1] == s[0][2] == 1
            or s[0][2] == s[1][2] == s[2][2] == 1):
        rep = 1
    elif (s[0][2] == s[1][2] == s[2][2] == 2
          or s[0][1] == s[1][1] == s[2][1] == 2
          or s[0][0] == s[0][1] == s[0][2] == 2
          or s[0][0] == s[1][0] == s[2][0] == 2
          or s[0][0] == s[1][1] == s[2][2] == 2
          or s[1][0] == s[1][1] == s[1][2] == 2
          or s[2][0] == s[2][1] == s[2][2] == 2
          or s[2][0] == s[1][1] == s[0][2] == 2):
        rep = -1
    return rep


"""Partie 2"""


def minimax_decision(s):
    # print(s)
    a = actions(s)
    print(a)
    return max(a, key=lambda x: min_value(
        result(s, x)))  # TODO: random pour varier


def max_value(s, max_depth, depth):
    if terminal_test(s)[0] or depth > max_depth:
        return utility(s)
    v = -10000
    for a in actions(s):
        global joueur_minimax
        joueur_minimax = 1
        v = max(v, min_value(result(s, a), max_depth, depth + 1))
    return v


def min_value(s, max_depth, depth):
    if terminal_test(s)[0] or depth > max_depth:
        return utility(s)
    v = 10000
    for a in actions(s):
        global joueur_minimax
        joueur_minimax = 2
        v = min(v, max_value(result(s, a), max_depth, depth + 1))
    joueur_minimax = 1
    return v


def alpha_beta_search(s):
    a = actions(s)
    print(a)
    return max(a, key=lambda x: min_value_ab(
        result(s, x), -10000, 10000))


def max_value_ab(s, alpha, beta):
    if terminal_test(s):
        return utility(s)
    v = -10000
    for a in actions(s):
        global joueur_minimax
        global action
        joueur_minimax = 1
        temp = min_value_ab(result(s, a), alpha, beta)
        if temp > v:
            v = temp
            action = a
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value_ab(s, alpha, beta):
    if terminal_test(s):
        return utility(s)
    v = 10000
    for a in actions(s):
        global joueur_minimax
        joueur_minimax = 2
        v = min(v, max_value_ab(result(s, a), alpha, beta))
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
    grille = np.zeros((6, 12), dtype=int)
    print(grille)
    action = 0
    joueur = rd.randrange(1, 3)
    joueur_minimax = 1
    # print(minimax_decision(grille))
    # print(alpha_beta_search(grille))
    while not terminal_test(grille):
        if joueur == 1:
            print("Tour de l'ordinateur")
            action = 0
            # decision = minimax_decision(grille)
            decision = alpha_beta_search(grille)
        else:
            print("Tour du joueur")
            actions_possibles = actions(grille)
            print("Actions possibles : ", actions_possibles)
            decision = [3, 3]
            while decision not in actions_possibles:
                decision[0] = int(input("Entrer la ligne"))
                decision[1] = int(input("Entrer la colonne"))

        grille[decision[0]][decision[1]] = joueur
        joueur = joueur % 2 + 1
        print(grille)

    etat = utility(grille)
    if etat == 1:
        print("Victoire de l'ordinateur")
    elif etat == -1:
        print("Victoire du joueur")
    else:
        print("Égalité")
