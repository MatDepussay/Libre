import random

choices = ["pierre", "papier", "ciseaux"]

def get_winner(player, computer):
    if player == computer:
        return "Égalité !"
    elif (player == "pierre" and computer == "ciseaux") or \
         (player == "papier" and computer == "pierre") or \
         (player == "ciseaux" and computer == "papier"):
        return "Vous gagnez !"
    else:
        return "L'ordinateur gagne !"

while True:
    player = input("Choisissez pierre, papier ou ciseaux (ou 'q' pour quitter) : ").lower()
    if player == 'q':
        print("Merci d'avoir joué !")
        break
    if player not in choices:
        print("Choix invalide, réessayez.")
        continue
    computer = random.choice(choices)
    print(f"L'ordinateur a choisi : {computer}")
    print(get_winner(player, computer))