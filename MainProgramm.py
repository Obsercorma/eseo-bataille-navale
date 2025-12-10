from grid import *

def position_correcte(position, nbcases, dico_positions):
    # Vérifier que les positions sont dans la grille 10x5 et ne se chevauchent pas
    print()
    if len(position) != nbcases+1:
        print(f"Erreur: Il faut entrer {nbcases} positions plus la profondeur.")
        print('Camarade, vous n\'avez pas assez bu de Vodka.')
        return False
    if position[0] not in ['100', '200', '300']:
        print(f'Erreur: La profondeur {position[0]} n\'est pas valide.')
        print('Camarade, vous n\'avez pas assez bu de Vodka.')
        return False
    col_save, row_save = None, None
    coords = sorted(position[1:])
    for pos in coords:
        if len(pos) != 2:
            print(f'Erreur: La position {pos} n\'est pas valide.')
            print('Camarade, vous n\'avez pas assez bu de Vodka.')
            return False
        col = pos[0]
        row = pos[1]
        if col not in ['A', 'B', 'C', 'D', 'E'] or row not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            print(f'Erreur: La position {pos} est hors de la grille.')
            print('Camarade, vous n\'avez pas assez bu de Vodka.')
            return False
        if col_save is not None and row_save is not None:
            if col != col_save and row != row_save:
                print(f'Erreur: Les positions {coords} ne sont pas alignées.')
                print('Camarade, vous n\'avez pas assez bu de Vodka.')
                return False
            elif row == row_save and col == col_save:
                print(f'Erreur: Vous avez saisi plusieurs fois la position {pos}.')
                print('Camarade, vous n\'avez pas assez bu de Vodka.')
                return False
            elif row != row_save:
                expected_row = str(int(row_save) + 1)
                if row != expected_row:
                    print(f'Erreur: Les positions {coords} ne sont pas consécutives.')
                    print('Camarade, vous n\'avez pas assez bu de Vodka.')
                    return False
            elif col != col_save:
                expected_col = chr(ord(col_save) + 1)
                if col != expected_col:
                    print(f'Erreur: Les positions {coords} ne sont pas consécutives.')
                    print('Camarade, vous n\'avez pas assez bu de Vodka.')
                    return False
        col_save, row_save = col, row
    for key, value in dico_positions.items():
        for pos in value[2:]:
            if pos in position[1:] and value[1] == position[0]:
                print(f'Erreur: La position {pos} est déjà occupée par un autre sous-marin.')
                print('Camarade, vous n\'avez pas assez bu de Vodka.')
                return False
    return True

def initialize_new_game():
    print("Bien le bonsoir cher camarade!")
    print("On va s'entraîner à faire la guerre froide")
    J1 = input("Quel est le nom du joueur jouant les USA? ")
    J2 = input("Quel est le nom du joueur jouant l'URSS? ")
    print(f"Bienvenue {J1} et {J2}! On se positionne à Cuba en 1962.")
    print("Les règles sont simples: taper les communistes avant qu'ils ne vous tapent!")
    print('Vous disposez d\'un sous marin de 3 cases de long, 1 de 2 cases de long et 1 de 1 case de long.')

    # Demander les positions des sous-marins
    positions = {}
    print("================================")
    print("\n\nCommençons par positionner vos sous-marins.")
    print("Ne regardez pas l'écran pendant que l'autre joueur entre ses positions.")
    for joueur in [J1, J2]:
        positions[joueur] = {}
        print(f'Joueur {joueur}, c\'est à votre tour de positionner vos sous-marins.')
        print("Veuillez faire en sort de ne pas dépasser la grille de 10x5 cases et de ne pas superposer les sous-marins.")
        print('Veuillez entrer les positions de vos sous marins au format "Profondeur A1 A2 A3" pour le sous marin de 3 cases, etc.')
        print('Exemple: "100 A1 A2 A3" pour un sous marin de 3 cases en profondeur 100m')
        print('Vous pouvez choisir les profondeurs suivantes: 100m, 200m, 300m')
        while True:
            sub3 = input(f"{joueur}, entrez les positions de votre sous marin de 3 cases: ")
            sub3 = sub3.split(" ")
            if position_correcte(sub3, 3, positions[joueur]):
                positions[joueur][f"3cases"] = [3] + sub3
                break
            else:
                print("Veuillez réessayer.")
        while True:
            sub2 = input(f"{joueur}, entrez les positions de votre sous marin de 2 cases: ")
            sub2 = sub2.split(" ")
            if position_correcte(sub2, 2, positions[joueur]):
                positions[joueur][f"2cases"] = [2] + sub2
                break
            else:
                print("Veuillez réessayer.")
        while True:
            sub1 = input(f"{joueur}, entrez la position de votre sous marin de 1 case: ")
            sub1 = sub1.split(" ")
            if position_correcte(sub1, 1, positions[joueur]):
                positions[joueur][f"1cases"] = [1] + sub1
                break
            else:
                print("Veuillez réessayer.")
        print("Vos sous-marins ont étés positionnés avec succès!")
        print(225 * '\n')
    print(positions)

    #Création des joueurs et affectations des sous-marins

    j1 = Joueur(J1)
    j2 = Joueur(J2)

    ship1_J1 = Ship(positions[j1.name]["1cases"][2:], positions[j1.name]["1cases"][1], 1, j1.name)
    j1.ships.append(ship1_J1)
    ship2_J1 = Ship(positions[j1.name]["2cases"][2:], positions[j1.name]["2cases"][1], 2, j1.name)
    j1.ships.append(ship2_J1)
    ship3_J1 = Ship(positions[j1.name]["3cases"][2:], positions[j1.name]["3cases"][1], 3, j1.name)
    j1.ships.append(ship3_J1)

    ship1_J2 = Ship(positions[j2.name]["1cases"][2:], positions[j2.name]["1cases"][1], 1, j2.name)
    j2.ships.append(ship1_J2)
    ship2_J2 = Ship(positions[j2.name]["2cases"][2:], positions[j2.name]["2cases"][1], 2, j2.name)
    j2.ships.append(ship2_J2)
    ship3_J2 = Ship(positions[j2.name]["3cases"][2:], positions[j2.name]["3cases"][1], 3, j2.name)
    j2.ships.append(ship3_J2)

    return j1, j2



def main():
    j1, j2 = initialize_new_game()
    print("La partie commence !")
    current_player = j1
    for ships in j1.ships:
        print(f"Joueur {j1.name} a positionné un sous-marin de taille {ships.taille} en profondeur {ships.profondeur} aux coordonnées {ships.coords}.")
    for ships in j2.ships:
        print(f"Joueur {j2.name} a positionné un sous-marin de taille {ships.taille} en profondeur {ships.profondeur} aux coordonnées {ships.coords}.")
    while True:
        if current_player == j1:
            print(f"100m {j2.grill100}")
            print(f"200m {j2.grill200}")
            print(f"300m {j2.grill300}")
        else:
            print(f"100m {j1.grill100}")
            print(f"200m {j1.grill200}")
            print(f"300m {j1.grill300}")
        print("Ci dessus l'océan de tir:")
        print(f"C'est le tour de {current_player.name}.")
        while True:
            target = input(f"{current_player.name}, entrez les coordonnées de votre attaque au format 'profondeur coordonnées' (ex: '100 A1'): ")
            target = target.split(" ")
            if position_correcte(target, 1, {}):
                print('Cible acceptée.')
                break
            print('Cible invalide, veuillez réessayer.')
        if current_player == j1:
            j2.cases_affected(target[0], target[1])
            print(f"100m {j2.grill100}")
            print(f"200m {j2.grill200}")
            print(f"300m {j2.grill300}")
            if j2.a_perdu():
                print(f"Félicitations {j1.name}, vous avez gagné la guerre froide !")
                break
        else:
            j1.cases_affected(target[0], target[1])
            print(f"100m {j1.grill100}")
            print(f"200m {j1.grill200}")
            print(f"300m {j1.grill300}")
            if j1.a_perdu():
                print(f"Félicitations {j2.name}, vous avez gagné la guerre froide !")
                break
        print("Ci dessus l'état de l'océan de tir après l'attaque")
        input("Appuyez sur n'importe quelle touche pour continuer...")
        current_player = j2 if current_player == j1 else j1


if __name__ == "__main__":
    main()