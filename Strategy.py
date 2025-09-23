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

# === Affichage de la box de victoire juste après la grille ===
if st.session_state.base_j1 <= 0 or st.session_state.base_j2 <= 0:
    st.markdown("---")
    st.markdown(
        "<div style='display:flex;justify-content:center;align-items:center;height:60vh;'>"
        "<div style='background:white;padding:2em 3em;border-radius:20px;box-shadow:0 0 30px #222;text-align:center;'>"
        "<h2>🏆 Partie terminée !</h2>"
        "<p>{}</p>"
        "<p><b>👇 Cliquez ci-dessous pour rejouer 👇</b></p>"
        "</div></div>".format(
            "La base du Joueur 1 est détruite ! Joueur 2 gagne !" if st.session_state.base_j1 <= 0
            else "La base du Joueur 2 est détruite ! Joueur 1 gagne !"
        ),
        unsafe_allow_html=True
    )
    col_center = st.columns([1,2,1])[1]
    if col_center.button("Rejouer / Réinitialiser la partie"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# Sélection de l'action
actions = ["Placer un soldat", "Construire un soldat", "Couper du bois", "Miner de l'or", "Attaquer"]
if st.session_state.tour == 1:
    action = st.selectbox("Choisissez une action :", actions, key="action_j1")
else:
    action = st.selectbox("Choisissez une action :", actions, key="action_j2")

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
        elif st.session_state.action_en_cours == "Construire un soldat":
            if st.session_state.bois_j1 >= 10 and st.session_state.or_j1 >= 5:
                st.session_state.bois_j1 -= 10
                st.session_state.or_j1 -= 5
                st.session_state.max_soldats_j1 += 1
                msg_joueur = "Joueur 1 a construit un soldat !"
            else:
                msg_joueur = "Pas assez de ressources pour construire un soldat."
        elif st.session_state.action_en_cours == "Couper du bois":
            bois = random.randint(1, 10)
            st.session_state.bois_j1 += bois
            msg_joueur = f"Vous avez coupé {bois} bois."
        elif st.session_state.action_en_cours == "Miner de l'or":
            or_miner = random.randint(1, 5)
            st.session_state.or_j1 += or_miner
            msg_joueur = f"Vous avez miné {or_miner} ors."
        elif st.session_state.action_en_cours == "Attaquer":
            msg_joueur = ""
            for ligne in range(3):
                # Soldats du joueur sur la ligne
                if st.session_state.tour == 1:
                    soldat_j1 = [j for j in range(3) if st.session_state.grid[ligne][j] == 1]
                    soldat_j2 = [j for j in range(3) if st.session_state.grid[ligne][j] == 2]
                    if soldat_j1:
                        if not soldat_j2:
                            degats = random.randint(3, 5)
                            st.session_state.base_j2 -= degats
                            msg_joueur += f"Soldat rouge sur ligne {ligne+1} inflige {degats} dégâts à la base ennemie.\n"
                        else:
                            j1_pos = soldat_j1[0]
                            j2_pos = soldat_j2[0]
                            roll_j1 = random.randint(1, 6)
                            roll_j2 = random.randint(1, 6)
                            msg_joueur += f"Sur ligne {ligne+1} : Rouge lance {roll_j1}, Bleu lance {roll_j2}. "
                            if roll_j1 > roll_j2:
                                st.session_state.grid[ligne][j2_pos] = 0
                                msg_joueur += "Le soldat rouge tue le bleu.\n"
                            elif roll_j2 > roll_j1:
                                st.session_state.grid[ligne][j1_pos] = 0
                                msg_joueur += "Le soldat bleu tue le rouge.\n"
                            else:
                                msg_joueur += "Égalité, rien ne se passe.\n"
                else:
                    soldat_j2 = [j for j in range(3) if st.session_state.grid[ligne][j] == 2]
                    soldat_j1 = [j for j in range(3) if st.session_state.grid[ligne][j] == 1]
                    if soldat_j2:
                        if not soldat_j1:
                            degats = random.randint(3, 5)
                            st.session_state.base_j1 -= degats
                            msg_joueur += f"Soldat bleu sur ligne {ligne+1} inflige {degats} dégâts à la base ennemie.\n"
                        else:
                            j2_pos = soldat_j2[0]
                            j1_pos = soldat_j1[0]
                            roll_j2 = random.randint(1, 6)
                            roll_j1 = random.randint(1, 6)
                            msg_joueur += f"Sur ligne {ligne+1} : Bleu lance {roll_j2}, Rouge lance {roll_j1}. "
                            if roll_j2 > roll_j1:
                                st.session_state.grid[ligne][j1_pos] = 0
                                msg_joueur += "Le soldat bleu tue le rouge.\n"
                            elif roll_j1 > roll_j2:
                                st.session_state.grid[ligne][j2_pos] = 0
                                msg_joueur += "Le soldat rouge tue le bleu.\n"
                            else:
                                msg_joueur += "Égalité, rien ne se passe.\n"
            st.success(msg_joueur if msg_joueur else "Aucun soldat à vous sur la grille pour attaquer.")

        st.success(msg_joueur)

        # IA joue immédiatement après
        if mode == "Joueur vs IA" and st.session_state.base_j2 > 0:
            ia_action = random.choice(actions)
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
            elif ia_action == "Construire un soldat":
                if st.session_state.bois_j2 >= 10 and st.session_state.or_j2 >= 5:
                    st.session_state.bois_j2 -= 10
                    st.session_state.or_j2 -= 5
                    st.session_state.max_soldats_j2 += 1
                    msg_ia = "L'IA a construit un soldat !"
                else:
                    msg_ia = "L'IA n'a pas assez de ressources pour construire un soldat."
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
            # IA intelligente
            msg_ia = ""
            # 1. Placer un soldat en face d'un soldat joueur si possible
            player_soldiers = [(i, j) for i in range(3) for j in range(3) if st.session_state.grid[i][j] == 1]
            ia_soldiers = [(i, j) for i in range(3) for j in range(3) if st.session_state.grid[i][j] == 2]
            can_place = st.session_state.soldats_j2 < st.session_state.max_soldats_j2

            placed = False
            if can_place and player_soldiers:
                for i, _ in player_soldiers:
                    empty_cols = [j for j in range(3) if st.session_state.grid[i][j] == 0]
                    if empty_cols:
                        j = random.choice(empty_cols)
                        st.session_state.grid[i][j] = 2
                        st.session_state.soldats_j2 += 1
                        msg_ia = f"L'IA place un soldat bleu sur la ligne {i+1} en face d'un soldat rouge."
                        placed = True
                        break

            # 2. Attaquer la base si possible et si IA a autant ou plus de soldats placés que le joueur
            if not placed and len(ia_soldiers) >= len(player_soldiers):
                if st.session_state.base_j2 < st.session_state.base_j1 + 20:
                    # Attaque la base
                    degats = random.randint(3, 5)
                    st.session_state.base_j1 -= degats
                    msg_ia = f"L'IA attaque la base du joueur et inflige {degats} dégâts."
                    placed = True

            # 3. Récolte si IA a au moins 20 points de vie de plus que le joueur
            if not placed and st.session_state.base_j2 >= st.session_state.base_j1 + 20:
                # Priorité à la ressource la plus faible
                if st.session_state.bois_j2 < st.session_state.or_j2:
                    bois = random.randint(1, 10)
                    st.session_state.bois_j2 += bois
                    msg_ia = f"L'IA récolte {bois} bois."
                else:
                    or_miner = random.randint(1, 5)
                    st.session_state.or_j2 += or_miner
                    msg_ia = f"L'IA récolte {or_miner} or."

            # Si aucune action prioritaire, construit un soldat si possible
            if not placed and st.session_state.bois_j2 >= 10 and st.session_state.or_j2 >= 5:
                st.session_state.bois_j2 -= 10
                st.session_state.or_j2 -= 5
                st.session_state.max_soldats_j2 += 1
                msg_ia = "L'IA a construit un soldat !"

            # Si rien n'est possible, récolte aléatoirement
            if not msg_ia:
                if random.choice([True, False]):
                    bois = random.randint(1, 10)
                    st.session_state.bois_j2 += bois
                    msg_ia = f"L'IA récolte {bois} bois."
                else:
                    or_miner = random.randint(1, 5)
                    st.session_state.or_j2 += or_miner
                    msg_ia = f"L'IA récolte {or_miner} or."

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
        elif st.session_state.action_en_cours == "Construire un soldat":
            if st.session_state.bois_j2 >= 10 and st.session_state.or_j2 >= 5:
                st.session_state.bois_j2 -= 10
                st.session_state.or_j2 -= 5
                st.session_state.max_soldats_j2 += 1
                msg_joueur2 = "Joueur 2 a construit un soldat !"
            else:
                msg_joueur2 = "Pas assez de ressources pour construire un soldat."
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
    st.markdown("---")
    st.markdown(
        "<div style='display:flex;justify-content:center;align-items:center;height:60vh;'>"
        "<div style='background:white;padding:2em 3em;border-radius:20px;box-shadow:0 0 30px #222;text-align:center;'>"
        "<h2>🏆 Partie terminée !</h2>"
        "<p>{}</p>"
        "<p><b>👇 Cliquez ci-dessous pour rejouer 👇</b></p>"
        "</div></div>".format(
            "La base du Joueur 1 est détruite ! Joueur 2 gagne !" if st.session_state.base_j1 <= 0
            else "La base du Joueur 2 est détruite ! Joueur 1 gagne !"
        ),
        unsafe_allow_html=True
    )
    col_center = st.columns([1,2,1])[1]
    if col_center.button("Rejouer / Réinitialiser la partie"):
        st.session_state.clear()
        st.rerun()
    st.stop()
