

def main():
    print("Bien le bonsoir cher caramade!")
    print("On va s'entraîner à faire la guerre froide")
    J1 = input("Quel est le nom du premier joueur jouant les USA? ")
    J2 = input("Quel est le nom du second joueur jouant l'URSS? ")
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
                positions[joueur]['3cases'] = sub3
                break
            else:
                print("Positions incorrectes, veuillez réessayer.")
        while True:
            sub2 = input(f"{joueur}, entrez les positions de votre sous marin de 2 cases: ")
            sub2 = sub2.split(" ")
            if position_correcte(sub2, 2, positions[joueur]):
                positions[joueur]['2cases'] = sub2
                break
            else:
                print("Positions incorrectes, veuillez réessayer.")
        while True:
            sub1 = input(f"{joueur}, entrez la position de votre sous marin de 1 case: ")
            sub1 = sub1.split(" ")
            if position_correcte(sub1, 1, positions[joueur]):
                positions[joueur]['1cases'] = sub1
                break
            else:
                print("Positions incorrectes, veuillez réessayer.")
        print("Vos sous-marins ont été positionnés avec succès!")
        print(50 * '\n')
    print(positions)


def position_correcte(position, nbcases, dico_positions):
    # Vérifier que les positions sont dans la grille 10x5 et ne se chevauchent pas
    print()
    print(position)
    if len(position) != nbcases+1:
        print(f"Erreur: Il faut entrer {nbcases} positions plus la profondeur.")
        print('Camarade, vous n\'avez pas assez bu de Vodka.')
        return False
    if position[0] not in ['100', '200', '300']:
        print(f'Erreur: La profondeur {position[0]} n\'est pas valide.')
        print('Camarade, vous n\'avez pas assez bu de Vodka.')
        return False
    col_save, row_save = None, None
    for pos in position[1:].sorted():
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
                print(f'Erreur: Les positions {position[1:]} ne sont pas alignées.')
                print('Camarade, vous n\'avez pas assez bu de Vodka.')
                return False
            elif row == row_save and col == col_save:
                print(f'Erreur: Vous avez saisi plusieurs fois la position {pos}.')
                print('Camarade, vous n\'avez pas assez bu de Vodka.')
                return False
            elif col != col_save:
                expected_row = str(int(row_save) + 1)
                if row != expected_row:
                    print(f'Erreur: Les positions {position[1:]} ne sont pas consécutives.')
                    print('Camarade, vous n\'avez pas assez bu de Vodka.')
                    return False
            elif row != row_save:
                expected_col = chr(ord(col_save) + 1)
                if col != expected_col:
                    print(f'Erreur: Les positions {position[1:]} ne sont pas consécutives.')
                    print('Camarade, vous n\'avez pas assez bu de Vodka.')
                    return False
        col_save, row_save = col, row
    for key, value in dico_positions.items():
        for pos in value[1:]:
            if pos in position[1:]:
                print(f'Erreur: La position {pos} est déjà occupée par un autre sous-marin.')
                print('Camarade, vous n\'avez pas assez bu de Vodka.')
                return False
    return True


if __name__ == "__main__":
    main()