import streamlit as st
import random

choices = ["pierre", "feuille", "ciseaux"]
alias_dict = {
    "pierre": ["p", "pi", "pier", "pierre", "pierres", "pieres"],
    "feuille": ["f", "fe", "feu", "feuille", "feuilles", "feuil", "feuile"],
    "ciseaux": ["c", "ci", "cis", "ciseaux", "ciseau", "cizeaux", "cizeau", "cize"],
}

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

st.title("Pierre Feuille Ciseaux")
mode = st.radio("Choisissez le mode :", ["Joueur vs Ordinateur", "Ordinateur vs Ordinateur"])

if mode == "Joueur vs Ordinateur":
    player_raw = st.text_input("Votre choix (pierre, feuille, ciseaux ou alias)")
    if st.button("Jouer"):
        player = normalize_choice(player_raw)
        if player is None:
            st.warning("Choix invalide, réessayez.")
        else:
            computer = random.choice(choices)
            st.write(f"L'ordinateur a choisi : {computer}")
            st.write(f"Vous avez choisi : {player}")
            st.success(get_winner(player, computer))
elif mode == "Ordinateur vs Ordinateur":
    n = st.number_input("Nombre de parties à simuler", min_value=1, value=10)
    if st.button("Simuler"):
        stats = {"ordi1": 0, "ordi2": 0, "egalite": 0}
        for _ in range(int(n)):
            ordi1 = random.choice(choices)
            ordi2 = random.choice(choices)
            result = get_winner(ordi1, ordi2)
            if result == "Égalité !":
                stats["egalite"] += 1
            elif result == "Vous gagnez !":
                stats["ordi1"] += 1
            else:
                stats["ordi2"] += 1
        st.write(f"Ordi1 victoires : {stats['ordi1']}")
        st.write(f"Ordi2 victoires : {stats['ordi2']}")
        st.write(f"Égalités : {stats['egalite']}")
