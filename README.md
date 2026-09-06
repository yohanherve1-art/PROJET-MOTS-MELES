# 🦁 MotMêlé - Projet Savane (HERVE_HUAN)

Bienvenue sur le dépôt de notre projet de **MotMêlé** développé en Python ! Ce projet a été pensé pour allier la logique algorithmique du Scrabble à une expérience visuelle immersive et ludique.

---

## ✨ Fonctionnalités principales

* **Génération intelligente :** Création de grilles de mots mêlés basée sur la distribution officielle des lettres du jeu du **Scrabble**.
* **Immersion visuelle :** Une interface graphique travaillée avec des décors inspirés de la **savane** pour rendre l'expérience plus vivante.
* **Modes de jeu multiples :** 
  * 👤 **Mode Solo :** Jouez à votre rythme pour trouver les mots cachés.
  * 👥 **Mode Duo :** Affrontez un(e) ami(e) sur la même grille.
* **Résolution automatique par arbre :** À la fin de la partie, un algorithme basé sur la théorie des arbres parcourt la grille pour retrouver et afficher l'intégralité des mots possibles.

---

## 📂 Structure du projet

Le projet est organisé de la manière suivante pour garantir une portabilité totale (chemins relatifs) :
* Code source principal en Python.
* Fichiers de ressources graphiques et sonores (dans un dossier dédié).
* Dictionnaire de mots (`dico.txt`).

---

## 📦 Installation et dépendances

Ce projet nécessite quelques bibliothèques Python pour fonctionner (notamment pour l'affichage graphique et la gestion du jeu).

1. Clonez ou téléchargez le projet sur votre machine.
2. Installez les dépendances requises en tapant la commande suivante dans votre terminal :
   ```bash
   pip install pygame pillow
