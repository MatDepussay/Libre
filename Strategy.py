import streamlit as st
import random

st.title("Mini jeu de stratégie : Actions et placement des soldats")

mode = st.radio("Choisissez le mode de jeu :", ["Joueur vs IA", "Joueur vs Joueur"])

# Initialisation des variables de session
if 'grid' not in st.session_state:
    st.session_state.grid = [[0 for _ in range(3)] for _ in range(3)]  # 0 = vide, 1 = joueur 1, 2 = joueur 2/IA
if 'selected' not in st.session_state:
    st.session_state.selected = (0, 0)
if 'tour' not in st.session_state:
    st.session_state.tour = 1  # 1 = joueur 1, 2 = joueur 2/IA
if 'soldats_j1' not in st.session_state:
    st.session_state.soldats_j1 = 0
if 'soldats_j2' not in st.session_state:
    st.session_state.soldats_j2 = 0
if 'max_soldats_j1' not in st.session_state:
    st.session_state.max_soldats_j1 = 0
if 'max_soldats_j2' not in st.session_state:
    st.session_state.max_soldats_j2 = 0
if 'bois_j1' not in st.session_state:
    st.session_state.bois_j1 = 0
if 'bois_j2' not in st.session_state:
    st.session_state.bois_j2 = 0
if 'or_j1' not in st.session_state:
    st.session_state.or_j1 = 0
if 'or_j2' not in st.session_state:
    st.session_state.or_j2 = 0
if 'base_j1' not in st.session_state:
    st.session_state.base_j1 = 100
if 'base_j2' not in st.session_state:
    st.session_state.base_j2 = 100
if 'action_en_cours' not in st.session_state:
    st.session_state.action_en_cours = None
if 'action_validee' not in st.session_state:
    st.session_state.action_validee = False

# Affichage des ressources et soldats
st.write(f"Joueur 1 : 🌲 {st.session_state.bois_j1} | 🪙 {st.session_state.or_j1} | Soldats placés : {st.session_state.soldats_j1}/{st.session_state.max_soldats_j1} | Base : {st.session_state.base_j1}")
st.write(f"Joueur 2{' (IA)' if mode == 'Joueur vs IA' else ''} : 🌲 {st.session_state.bois_j2} | 🪙 {st.session_state.or_j2} | Soldats placés : {st.session_state.soldats_j2}/{st.session_state.max_soldats_j2} | Base : {st.session_state.base_j2}")

# Affichage de la grille avec clés uniques
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        cell = st.session_state.grid[i][j]
        if cell == 0:
            label = "🟩"
        elif cell == 1:
            label = "🟥🪖"
        else:
            label = "🟦🪖"
        if cols[j].button(label, key=f"grid-btn-{i}-{j}"):
            st.session_state.selected = (i, j)

st.write(f"Case sélectionnée : {st.session_state.selected}")

# Sélection de l'action
if st.session_state.tour == 1:
    action = st.selectbox("Choisissez une action :", ["Placer un soldat", "Couper du bois", "Miner de l'or", "Attaquer"], key="action_j1")
else:
    action = st.selectbox("Choisissez une action :", ["Placer un soldat", "Couper du bois", "Miner de l'or", "Attaquer"], key="action_j2")

st.session_state.action_en_cours = action

# Bouton pour valider le tour
if st.button("Valider le tour"):
    # Joueur 1 joue
    if st.session_state.tour == 1:
        msg_joueur = ""
        if st.session_state.action_en_cours == "Placer un soldat":
            i, j = st.session_state.selected
            if st.session_state.grid[i][j] == 0:
                if st.session_state.soldats_j1 < st.session_state.max_soldats_j1:
                    st.session_state.grid[i][j] = 1
                    st.session_state.soldats_j1 += 1
                    msg_joueur = "Soldat rouge placé !"
                else:
                    msg_joueur = "Nombre maximum de soldats placés !"
            else:
                msg_joueur = "Il y a déjà un soldat ici."
        elif st.session_state.action_en_cours == "Couper du bois":
            bois = random.randint(1, 10)
            st.session_state.bois_j1 += bois
            msg_joueur = f"Vous avez coupé {bois} bois."
        elif st.session_state.action_en_cours == "Miner de l'or":
            or_miner = random.randint(1, 5)
            st.session_state.or_j1 += or_miner
            msg_joueur = f"Vous avez miné {or_miner} ors."
        elif st.session_state.action_en_cours == "Attaquer":
            if st.session_state.soldats_j1 > 0:
                degats = random.randint(5, 15)
                st.session_state.base_j2 -= degats
                msg_joueur = f"Vous avez infligé {degats} dégâts à la base ennemie."
            else:
                msg_joueur = "Vous n'avez pas de soldat pour attaquer."
        st.success(msg_joueur)

        # IA joue immédiatement après
        if mode == "Joueur vs IA" and st.session_state.base_j2 > 0:
            ia_action = random.choice(["Placer un soldat", "Couper du bois", "Miner de l'or", "Attaquer"])
            msg_ia = ""
            if ia_action == "Placer un soldat":
                empty_cells = [(i, j) for i in range(3) for j in range(3) if st.session_state.grid[i][j] == 0]
                if empty_cells and st.session_state.soldats_j2 < st.session_state.max_soldats_j2:
                    i, j = random.choice(empty_cells)
                    st.session_state.grid[i][j] = 2
                    st.session_state.soldats_j2 += 1
                    msg_ia = f"L'IA place un soldat bleu en case {i},{j}"
                else:
                    msg_ia = "L'IA ne peut pas placer de soldat."
            elif ia_action == "Couper du bois":
                bois = random.randint(1, 10)
                st.session_state.bois_j2 += bois
                msg_ia = f"L'IA a coupé {bois} bois."
            elif ia_action == "Miner de l'or":
                or_miner = random.randint(1, 5)
                st.session_state.or_j2 += or_miner
                msg_ia = f"L'IA a miné {or_miner} ors."
            elif ia_action == "Attaquer":
                if st.session_state.soldats_j2 > 0:
                    degats = random.randint(5, 15)
                    st.session_state.base_j1 -= degats
                    msg_ia = f"L'IA a infligé {degats} dégâts à votre base."
                else:
                    msg_ia = "L'IA n'a pas de soldat pour attaquer."
            st.info(msg_ia)
        # Passage au tour suivant
        st.session_state.tour = 1 if mode == "Joueur vs IA" else 2

    # Joueur 2 (si mode JcJ)
    elif st.session_state.tour == 2 and mode == "Joueur vs Joueur":
        msg_joueur2 = ""
        if st.session_state.action_en_cours == "Placer un soldat":
            i, j = st.session_state.selected
            if st.session_state.grid[i][j] == 0:
                if st.session_state.soldats_j2 < st.session_state.max_soldats_j2:
                    st.session_state.grid[i][j] = 2
                    st.session_state.soldats_j2 += 1
                    msg_joueur2 = "Soldat bleu placé !"
                else:
                    msg_joueur2 = "Nombre maximum de soldats placés !"
            else:
                msg_joueur2 = "Il y a déjà un soldat ici."
        elif st.session_state.action_en_cours == "Couper du bois":
            bois = random.randint(1, 10)
            st.session_state.bois_j2 += bois
            msg_joueur2 = f"Joueur 2 a coupé {bois} bois."
        elif st.session_state.action_en_cours == "Miner de l'or":
            or_miner = random.randint(1, 5)
            st.session_state.or_j2 += or_miner
            msg_joueur2 = f"Joueur 2 a miné {or_miner} ors."
        elif st.session_state.action_en_cours == "Attaquer":
            if st.session_state.soldats_j2 > 0:
                degats = random.randint(5, 15)
                st.session_state.base_j1 -= degats
                msg_joueur2 = f"Joueur 2 a infligé {degats} dégâts à la base ennemie."
            else:
                msg_joueur2 = "Vous n'avez pas de soldat pour attaquer."
        st.success(msg_joueur2)
        st.session_state.tour = 1

# Construction de soldats
if st.session_state.tour == 1:
    if st.button("Construire un soldat (coût : 10 bois, 5 or)", key="construire_j1"):
        if st.session_state.bois_j1 >= 10 and st.session_state.or_j1 >= 5:
            st.session_state.bois_j1 -= 10
            st.session_state.or_j1 -= 5
            st.session_state.max_soldats_j1 += 1
            st.success("Joueur 1 a construit un soldat !")
        else:
            st.warning("Pas assez de ressources pour construire un soldat.")

elif st.session_state.tour == 2 and mode == "Joueur vs Joueur":
    if st.button("Construire un soldat (coût : 10 bois, 5 or)", key="construire_j2"):
        if st.session_state.bois_j2 >= 10 and st.session_state.or_j2 >= 5:
            st.session_state.bois_j2 -= 10
            st.session_state.or_j2 -= 5
            st.session_state.max_soldats_j2 += 1
            st.success("Joueur 2 a construit un soldat !")
        else:
            st.warning("Pas assez de ressources pour construire un soldat.")

# Fin de partie si une base est détruite
if st.session_state.base_j1 <= 0 or st.session_state.base_j2 <= 0:
    st.write("Une base a été détruite !")
    if st.session_state.base_j1 <= 0:
        st.write("La base du Joueur 1 est détruite ! Le Joueur 2 remporte la partie.")
    else:
        st.write("La base du Joueur 2 est détruite ! Le Joueur 1 remporte la partie.")
    if st.button("Rejouer"):
        st.session_state.clear()

# Réinitialisation de la partie
if st.button("Réinitialiser la partie"):
    st.session_state.clear()
