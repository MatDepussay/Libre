import random

choices = ["pierre", "feuille", "ciseaux"]

# Dictionnaire d'alias pour chaque combinaison
alias_dict = {
    "pierre": ["p", "pi", "pier", "pierre", "pierres", "pieres"],
    "feuille": ["f", "fe", "feu", "feuille", "feuilles", "feuil", "feuile"],
    "ciseaux": ["c", "ci", "cis", "ciseaux", "ciseau", "cizeaux", "cizeau", "cize"],
}

# Fonction pour normaliser l'entrée utilisateur
def normalize_choice(user_input):
    user_input = user_input.lower().replace(" ", "")
    for key, aliases in alias_dict.items():
        if user_input in aliases:
            return key
    return None

def get_winner(player, computer):
    if player == computer:
        return "Égalité !"
    elif (player == "pierre" and computer == "ciseaux") or \
         (player == "feuille" and computer == "pierre") or \
         (player == "ciseaux" and computer == "feuille"):
        return "Vous gagnez !"
    else:
        return "L'ordinateur gagne !"

while True:
    mode = input("Mode : 1 = joueur vs ordinateur, 2 = ordinateur vs ordinateur, q = quitter : ").lower().replace(" ", "")
    if mode == 'q':
        print("Merci d'avoir joué !")
        break
    elif mode == '2':
        try:
            n = int(input("Combien de parties ordinateur vs ordinateur ? "))
        except ValueError:
            print("Nombre invalide.")
            continue
        stats = {"ordi1": 0, "ordi2": 0, "egalite": 0}
        for _ in range(n):
            ordi1 = random.choice(choices)
            ordi2 = random.choice(choices)
            result = get_winner(ordi1, ordi2)
            if result == "Égalité !":
                stats["egalite"] += 1
            elif result == "Vous gagnez !":
                stats["ordi1"] += 1
            else:
                stats["ordi2"] += 1
        print(f"Ordi1 victoires : {stats['ordi1']}")
        print(f"Ordi2 victoires : {stats['ordi2']}")
        print(f"Égalités : {stats['egalite']}")
        continue
    elif mode == '1':
        player_raw = input("Choisissez pierre, feuille ou ciseaux (ou 'q' pour quitter) : ")
        if player_raw.lower().replace(" ", "") == 'q':
            print("Merci d'avoir joué !")
            break
        player = normalize_choice(player_raw)
        if player is None:
            print("Choix invalide, réessayez.")
            continue
        computer = random.choice(choices)
        print(f"L'ordinateur a choisi : {computer}")
        print(get_winner(player, computer))
        continue