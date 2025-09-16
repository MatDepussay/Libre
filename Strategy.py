import streamlit as st
import random

# Initialisation de la grille et des variables
if 'grid' not in st.session_state:
    st.session_state.grid = [[0 for _ in range(3)] for _ in range(3)]
if 'selected' not in st.session_state:
    st.session_state.selected = (0, 0)
if 'tour' not in st.session_state:
    st.session_state.tour = 1  # 1 = joueur 1, 2 = IA
if 'max_soldats_j1' not in st.session_state:
    st.session_state.max_soldats_j1 = 3
if 'max_soldats_ia' not in st.session_state:
    st.session_state.max_soldats_ia = 3

st.title("Placement des soldats sur la grille 3x3")

# Affichage du nombre de soldats placés
soldats_j1 = sum(cell == 1 for row in st.session_state.grid for cell in row)
soldats_ia = sum(cell == 2 for row in st.session_state.grid for cell in row)
st.write(f"Soldats Joueur 1 (rouge) : {soldats_j1}/{st.session_state.max_soldats_j1} | Soldats IA (bleu) : {soldats_ia}/{st.session_state.max_soldats_ia}")

# Affichage de la grille avec clés uniques
grid_key_prefix = f"grid-{random.randint(0, 1000000)}"
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
        if cols[j].button(label, key=f"{grid_key_prefix}-{i}-{j}"):
            st.session_state.selected = (i, j)

st.write(f"Case sélectionnée : {st.session_state.selected}")

# Tour du joueur 1
if st.session_state.tour == 1:
    if st.button("Placer un soldat rouge (Joueur 1) sur la case sélectionnée", key=f"place-soldat-{random.randint(0,1000000)}"):
        i, j = st.session_state.selected
        if st.session_state.grid[i][j] == 0:
            if soldats_j1 < st.session_state.max_soldats_j1:
                st.session_state.grid[i][j] = 1
                st.success("Soldat rouge placé !")
                st.session_state.tour = 2
            else:
                st.warning("Nombre maximum de soldats placés !")
        else:
            st.info("Il y a déjà un soldat ici.")

# Tour de l'IA (joueur 2)
if st.session_state.tour == 2:
    empty_cells = [(i, j) for i in range(3) for j in range(3) if st.session_state.grid[i][j] == 0]
    if empty_cells and soldats_ia < st.session_state.max_soldats_ia:
        ia_choice = random.choice(empty_cells)
        st.session_state.grid[ia_choice[0]][ia_choice[1]] = 2
        st.info(f"L'IA (bleu) a placé un soldat en case {ia_choice}")
        st.session_state.tour = 1
import streamlit as st
import random

# Initialisation de la grille (0 = vide, 1 = soldat joueur 1, 2 = soldat IA)
if 'grid' not in st.session_state:
    st.session_state.grid = [[0 for _ in range(3)] for _ in range(3)]
if 'selected' not in st.session_state:
    st.session_state.selected = (0, 0)
if 'tour' not in st.session_state:
    st.session_state.tour = 1  # 1 = joueur 1, 2 = IA

st.title("Placement des soldats sur la grille 3x3")

# Affichage de la grille
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

# Tour du joueur 1
if st.session_state.tour == 1:
    if st.button("Placer un soldat rouge (Joueur 1) sur la case sélectionnée"):
        i, j = st.session_state.selected
        if st.session_state.grid[i][j] == 0:
            st.session_state.grid[i][j] = 1
            st.success("Soldat rouge placé !")
            st.session_state.tour = 2
        else:
            st.info("Il y a déjà un soldat ici.")

# Tour de l'IA (joueur 2)
if st.session_state.tour == 2:
    # IA choisit une case vide aléatoire
    empty_cells = [(i, j) for i in range(3) for j in range(3) if st.session_state.grid[i][j] == 0]
    if empty_cells:
        ia_choice = random.choice(empty_cells)
        st.session_state.grid[ia_choice[0]][ia_choice[1]] = 2
        st.info(f"L'IA (bleu) a placé un soldat en case {ia_choice}")
        st.session_state.tour = 1

# Affichage du nombre de soldats placés
soldats_j1 = sum(cell == 1 for row in st.session_state.grid for cell in row)
soldats_ia = sum(cell == 2 for row in st.session_state.grid for cell in row)
st.write(f"Soldats Joueur 1 (rouge) : {soldats_j1} | Soldats IA (bleu) : {soldats_ia}")
import streamlit as st
import time

# Initialisation des ressources et points de vie
if 'bois' not in st.session_state:
    st.session_state.bois = 0
if 'or_' not in st.session_state:
    st.session_state.or_ = 0
if 'soldat' not in st.session_state:
    st.session_state.soldat = 0
if 'base1' not in st.session_state:
    st.session_state.base1 = 100
if 'base2' not in st.session_state:
    st.session_state.base2 = 100
if 'last_action' not in st.session_state:
    st.session_state.last_action = ''
if 'last_gain' not in st.session_state:
    st.session_state.last_gain = ''
if 'attack_anim' not in st.session_state:
    st.session_state.attack_anim = False

st.title("Mini jeu de stratégie")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Joueur 1")
    st.progress(st.session_state.base1)
    st.markdown(f"Bois : {st.session_state.bois} ")
    st.markdown(f"Or : {st.session_state.or_}")
    st.markdown(f"Soldats : {st.session_state.soldat}")
    if st.session_state.last_action == 'recolter':
        st.markdown(f"<span style='color:green;font-size:24px;'>+10</span> <span style='color:gold;font-size:24px;'>+5</span>", unsafe_allow_html=True)
    if st.session_state.last_action == 'attaquer' and st.session_state.attack_anim:
        st.markdown("<span style='font-size:40px;'>⚪</span>", unsafe_allow_html=True)

with col2:
    st.subheader("Joueur 2")
    st.progress(st.session_state.base2)
    # Pour l'exemple, pas de ressources affichées pour le joueur 2

st.write("---")

# Actions
if st.button("Récolter"):
    st.session_state.bois += 10
    st.session_state.or_ += 5
    st.session_state.last_action = 'recolter'
    st.session_state.attack_anim = False
    st.session_state.last_gain = '+10 bois, +5 or'
    st.rerun()

if st.button("Attaquer"):
    if st.session_state.soldat > 0:
        st.session_state.base2 -= 10
        st.session_state.soldat -= 1
        st.session_state.last_action = 'attaquer'
        st.session_state.attack_anim = True
        st.rerun()
    else:
        st.warning("Pas de soldat pour attaquer !")

if st.button("Construire un soldat"):
    if st.session_state.bois >= 10 and st.session_state.or_ >= 5:
        st.session_state.bois -= 10
        st.session_state.or_ -= 5
        st.session_state.soldat += 1
        st.session_state.last_action = 'construire'
        st.session_state.attack_anim = False
        st.rerun()
    else:
        st.warning("Pas assez de ressources !")

if st.session_state.base2 <= 0:
    st.success("Joueur 1 a gagné !")
    st.session_state.base2 = 100
    st.session_state.bois = 0
    st.session_state.or_ = 0
    st.session_state.soldat = 0
    st.session_state.last_action = ''
    st.session_state.attack_anim = False
    st.rerun()
class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.bois = 0
        self.or_ = 0
        self.soldat = 0
        self.base = 100  # points de vie de la base

    def afficher(self):
        print(f"{self.nom} | Bois: {self.bois} | Or: {self.or_} | Soldats: {self.soldat} | Base: {self.base}")

class Action:
    def __init__(self, type_action, joueur, cible=None):
        self.type_action = type_action  # 'recolter', 'construire', 'attaquer'
        self.joueur = joueur
        self.cible = cible  # Pour attaquer, cible est l'adversaire

    def execute(self):
        if self.type_action == 'recolter':
            self.joueur.bois += 10
            self.joueur.or_ += 5
            print(f"{self.joueur.nom} récolte 10 bois et 5 or.")
        elif self.type_action == 'construire':
            if self.joueur.bois >= 10 and self.joueur.or_ >= 5:
                self.joueur.bois -= 10
                self.joueur.or_ -= 5
                self.joueur.soldat += 1
                print(f"{self.joueur.nom} construit un soldat.")
            else:
                print(f"{self.joueur.nom} n'a pas assez de ressources pour construire.")
        elif self.type_action == 'attaquer' and self.cible:
            if self.joueur.soldat > 0:
                self.cible.base -= 10
                self.joueur.soldat -= 1
                print(f"{self.joueur.nom} attaque {self.cible.nom} et inflige 10 dégâts à la base.")
            else:
                print(f"{self.joueur.nom} n'a pas de soldat pour attaquer.")

class Game :
    def __init__(self, joueur1, joueur2):
        self.joueur1 = joueur1
        self.joueur2 = joueur2

    def start(self, mode_ia=False):
        print("Début du jeu!")
        tour = 0
        while self.joueur1.base > 0 and self.joueur2.base > 0:
            tour += 1
            print(f"\n--- Tour {tour} ---")
            self.joueur1.afficher()
            self.joueur2.afficher()
            # Tour du joueur 1
            action1 = input(f"{self.joueur1.nom}, choisis une action (recolter, construire, attaquer ou q pour quitter): ")
            if action1 == 'q':
                print("Jeu interrompu.")
                return
            if action1 == 'attaquer':
                act1 = Action('attaquer', self.joueur1, self.joueur2)
            else:
                act1 = Action(action1, self.joueur1)
            act1.execute()

            # Tour du joueur 2
            if mode_ia:
                action2 = random.choice(['recolter', 'construire', 'attaquer'])
                print(f"{self.joueur2.nom} (IA) choisit : {action2}")
            else:
                action2 = input(f"{self.joueur2.nom}, choisis une action (recolter, construire, attaquer ou q pour quitter): ")
                if action2 == 'q':
                    print("Jeu interrompu.")
                    return
            if action2 == 'attaquer':
                act2 = Action('attaquer', self.joueur2, self.joueur1)
            else:
                act2 = Action(action2, self.joueur2)
            act2.execute()
        print("\nFin du jeu!")
        if self.joueur1.base > 0:
            print(f"{self.joueur1.nom} a gagné!")
        else:
            print(f"{self.joueur2.nom} a gagné!")
if __name__ == "__main__":
    import random
    mode = st.radio("Choisissez le mode de jeu :", ["Joueur vs Joueur", "Joueur vs IA"])
    nom1 = input("Nom du joueur 1: ")
    if mode == 'Joueur vs IA':
        nom2 = "IA"
        ia_mode = True
    else:
        nom2 = input("Nom du joueur 2: ")
        ia_mode = False
    j1 = Joueur(nom1)
    j2 = Joueur(nom2)
    jeu = Game(j1, j2)
    jeu.start(mode_ia=ia_mode)
