################################################ PROJET ######################################################


################################################ IMPORTS #####################################################

import heapq
from collections import defaultdict
import tkinter as tk
import re

############################################## CLASSES #######################################################

import heapq

class Noeud:
    def __init__(self, freq, char=None):
        # Initialisation d'un nœud avec une fréquence et un caractère
        self.freq = freq
        self.char = char
        # Initialisation des fils gauche et droit à None
        self.gauche = None
        self.droite = None

    def __lt__(self, autre):
        # Surcharge de l'opérateur "<" pour pouvoir comparer deux nœuds en fonction de leur fréquence
        return self.freq < autre.freq
    
    def __eq__(self, autre):
        # Surcharge de l'opérateur "==" pour pouvoir comparer deux nœuds en fonction de leur fréquence et leur caractère
        return self.freq == autre.freq and self.char == autre.char

    def ajouter_gauche(self, fils_gauche):
        # Ajout d'un fils gauche à ce nœud
        self.gauche = fils_gauche

    def ajouter_droite(self, fils_droit):
        # Ajout d'un fils droit à ce nœud
        self.droite = fils_droit

    def modifier_etiquette(self, freq=None, char=None):
        # Modification de la fréquence et/ou du caractère de ce nœud, si les nouvelles valeurs sont non nulles
        if freq is not None:
            self.freq = freq
        if char is not None:
            self.char = char

    def rechercher(self, char):
        # Recherche d'un nœud dans l'arbre ayant un caractère donné
        if self.char == char:
            return self
        if self.gauche is not None:
            resultat_gauche = self.gauche.rechercher(char)
            if resultat_gauche is not None:
                return resultat_gauche
        if self.droite is not None:
            resultat_droit = self.droite.rechercher(char)
            if resultat_droit is not None:
                return resultat_droit
        return None

    def supprimer(self, char):
        # Suppression d'un nœud de l'arbre ayant un caractère donné
        if self.char == char:
            return None
        if self.gauche is not None:
            self.gauche = self.gauche.supprimer(char)
        if self.droite is not None:
            self.droite = self.droite.supprimer(char)
        return self

    def fusionner(self, autre):
        # Fusion de ce nœud avec un autre nœud pour former un nouveau nœud interne
        somme_freq = self.freq + autre.freq
        nouveau_noeud = Noeud(somme_freq)
        nouveau_noeud.gauche = self
        nouveau_noeud.droite = autre
        return nouveau_noeud

    def decomposer(self):
        # Décomposition de l'arbre en une liste de nœuds feuilles
        noeuds_feuilles = []
        def parcourir(noeud):
            if noeud.gauche is None and noeud.droite is None:
                noeuds_feuilles.append(noeud)
            else:
                parcourir(noeud.gauche)
                parcourir(noeud.droite)
        parcourir(self)
        return noeuds_feuilles
    
def construire_arbre_huffman(dictionnaire_freq):
        # Construction de l'abre d'Huffman
        tas = [Noeud(freq, char) for char, freq in dictionnaire_freq.items()]
        heapq.heapify(tas)
        while len(tas) > 1:
            fils_gauche = heapq.heappop(tas)
            fils_droit = heapq.heappop(tas)
            noeud_interne = Noeud(fils_gauche.freq + fils_droit.freq)
            noeud_interne.gauche = fils_gauche
            noeud_interne.droite = fils_droit
            heapq.heappush(tas, noeud_interne)
        return tas[0]

    
# Création d'un arbre binaire
racine = Noeud(20)
gauche = Noeud(10, "a")
droite = Noeud(10, "b")
racine.ajouter_gauche(gauche)
racine.ajouter_droite(droite)

# Test de la modification d'une étiquette
print("Étiquette avant modification :", gauche.char)
gauche.modifier_etiquette(char="c")
print("Étiquette après modification :", gauche.char)

# Test de la recherche d'un élément dans l'arbre
recherche = racine.rechercher("b")
print("Élément recherché :", recherche.char)

# Test de la suppression d'un élément de l'arbre
racine.supprimer("b")
print("Arbre après suppression de 'b':")
print(racine.gauche.char)  # 'c'
print(racine.droite)  # None

# Test de la fusion de deux arbres
autre_arbre = Noeud(15)
fusion = racine.fusionner(autre_arbre)
print("Arbre après fusion avec un autre arbre :")
print(fusion.freq)  # 35

# Test de la décomposition de l'arbre en une liste de noeuds feuilles

################################################ FONCTIONS #####################################################

# Définition de la fonction récursive pour générer les codes de Huffman
def generer_codes_aide(noeud, code_courant, dictionnaire_codes):
    if noeud.char is not None:
        # Si le noeud actuel correspond à un caractère, on ajoute son code au dictionnaire des codes de Huffman
        dictionnaire_codes[noeud.char] = code_courant
    else:
        # Sinon, on continue la descente récursive dans l'arbre
        # On ajoute un "0" si on descend à gauche, un "1" si on descend à droite
        generer_codes_aide(noeud.gauche, code_courant + "0", dictionnaire_codes)
        generer_codes_aide(noeud.droite, code_courant + "1", dictionnaire_codes)

# Définition de la fonction principale pour générer les codes de Huffman
def generer_codes_huffman(arbre_huffman):
    dictionnaire_codes = {}
    # On appelle la fonction récursive pour générer les codes
    generer_codes_aide(arbre_huffman, "", dictionnaire_codes)
    # On renvoie le dictionnaire des codes de Huffman généré
    return dictionnaire_codes

# Définition de la fonction d'encodage de Huffman
def huffman_encoder(texte):
    dictionnaire_freq = defaultdict(int)
    # On calcule la fréquence d'apparition de chaque caractère dans le texte à encoder
    for char in texte:
        dictionnaire_freq[char] += 1
    # On construit l'arbre de Huffman correspondant aux fréquences calculées
    arbre_huffman = construire_arbre_huffman(dictionnaire_freq)
    # On génère les codes de Huffman à partir de l'arbre construit
    dictionnaire_codes = generer_codes_huffman(arbre_huffman)
    # On encode le texte à partir des codes de Huffman générés
    texte_encodé = "".join(dictionnaire_codes[char] for char in texte)
    # On renvoie le texte encodé, l'arbre de Huffman correspondant et le dictionnaire des codes de Huffman générés
    return texte_encodé, arbre_huffman, dictionnaire_codes

# Définition de la fonction de décodage de Huffman
def huffman_decoder(texte_encodé, arbre_huffman):
    texte_decodé = ""
    noeud_courant = arbre_huffman

    # On parcourt le texte encodé bit par bit
    for bit in texte_encodé:
        if bit == "0":
            # Si le bit est un "0", on descend dans l'arbre à gauche
            noeud_courant = noeud_courant.gauche
        else:
            # Sinon, on descend à droite
            noeud_courant = noeud_courant.droite

        if noeud_courant.char is not None:
            # Si on atteint un noeud correspondant à un caractère, on ajoute le caractère décodé au texte décodé
            texte_decodé += noeud_courant.char
            # On repart du haut de l'arbre pour décoder le caractère suivant
            noeud_courant = arbre_huffman

    # On renvoie le texte décodé
    return texte_decodé

def dessiner_arbre_huffman(noeud, dictionnaire_codes, canvas, x=300, y=50, x_offset=100, y_offset=25):
    # Si le noeud est une feuille, afficher le caractère et son code associé.
    if noeud.char is not None:
        canvas.create_text(x, y, text=f"{noeud.char}:{dictionnaire_codes[noeud.char]}")
        return

    # Si le noeud n'est pas une feuille, afficher la fréquence.
    canvas.create_text(x, y, text=str(noeud.freq))
    # Récupérer les fils gauche et droit.
    fils_gauche = noeud.gauche
    fils_droit = noeud.droite

    # Si le fils gauche existe, dessiner une ligne vers lui et dessiner l'arbre à partir de ce noeud.
    if fils_gauche is not None:
        canvas.create_line(x, y, x - x_offset, y + y_offset)
        dessiner_arbre_huffman(fils_gauche, dictionnaire_codes, canvas, x - x_offset, y + y_offset, x_offset // 2, y_offset)
    
    # Si le fils droit existe, dessiner une ligne vers lui et dessiner l'arbre à partir de ce noeud.
    if fils_droit is not None:
        canvas.create_line(x, y, x + x_offset, y + y_offset)
        dessiner_arbre_huffman(fils_droit, dictionnaire_codes, canvas, x + x_offset, y + y_offset, x_offset // 2, y_offset)



# Fonction pour encoder le texte
def encode_text():
    canvas.delete("all")
    res_text.delete('1.0', 'end')
    texte = input_text.get("1.0", 'end')
    global texte_encodé, arbre_huffman, dictionnaire_codes
    texte_encodé, arbre_huffman, dictionnaire_codes = huffman_encoder(texte)
    res_text.insert('1.0', texte_encodé)
    dessiner_arbre_huffman(arbre_huffman, dictionnaire_codes, canvas)
    maj_interface()
    

# Fonction pour décoder le texte
def decode_text():
    res_text.delete('1.0', 'end')
    texte = input_text.get("1.0", 'end')
    if re.match('^[01]+$', texte) is not None :
        decoded_text = huffman_decoder(texte_encodé, arbre_huffman)
        res_text.insert('1.0', decoded_text)
    else :
        res_text.insert('1.0', 'le texte a entré dois etre en binaire')
    maj_interface()
    

# Fonction pour mettre à jour l'interface en fonction du choix de l'utilisateur
def maj_interface():
    # Modification du texte du bouton en fonction du choix de l'utilisateur
    if var.get() == "Encoder":
        action_button.config(text="Encoder le texte")
        output_label.config(text="Texte encodé :") 
    else:
        action_button.config(text="Décoder le texte")
        output_label.config(text="Texte décodé :")
        
################################################ INTERFACE GRAPHIQUE #####################################################

# Création de la fenêtre
window = tk.Tk()
window.title("Codage Huffman")
window.geometry("800x600")
window.config(bg="#2c3e50")

# Ajout de widgets
title_label = tk.Label(text="Codage Huffman", font=("Arial", 30), bg="#2c3e50", fg="white")
title_label.pack(pady=30)

canvas = tk.Canvas(window, width=600, height=400, bg="white")
canvas.pack(side='left', padx=50, pady=150)


# Menu déroulant pour choisir entre l'encodage et le décodage
menu_frame = tk.Frame(window, bg="#2c3e50")
menu_frame.pack(pady=10)

choice_label = tk.Label(menu_frame, text="Choisissez une option :", font=("Arial", 16), bg="#2c3e50", fg="white")
choice_label.pack(side=tk.LEFT, padx=10)

var = tk.StringVar()
var.set("Encoder")

option_menu = tk.OptionMenu(menu_frame, var, "Encoder", "Decoder")
option_menu.pack(side=tk.LEFT)

# Widget pour entrer le texte à coder/décoder
input_label = tk.Label(text="Entrez votre texte :", font=("Arial", 16), bg="#2c3e50", fg="white")
input_label.pack(pady=10)

input_text = tk.Text(window, width=50, height=10, font=("Arial", 14), bg="#ecf0f1")
input_text.pack(pady=10)

# Bouton pour encoder ou décoder le texte en fonction du choix de l'utilisateur
action_button = tk.Button(text="Encoder le texte", font=("Arial", 16), bg="#3498db", fg="white", command=lambda: encode_text() if var.get() == "Encoder" else decode_text())
action_button.pack(pady=10)

# Widget pour afficher le texte encodé/décodé
output_label = tk.Label(text="Texte encodé :", font=("Arial", 16), bg="#2c3e50", fg="white")
output_label.pack(pady=10)

res_text = tk.Text(window, width=50, height=10, font=("Arial", 14), bg="#ecf0f1" )
res_text.pack(pady=10)

# Lancement de la fenêtre
window.mainloop()




