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

## ⚠️ Note importante concernant l'exécution en ligne
Ce projet utilise **Tkinter** pour son interface graphique et **Pygame** pour la gestion multimédia. En raison de ces dépendances graphiques et audio, **le code ne peut pas s'exécuter directement dans le navigateur via le terminal cloud de GitHub Codespaces** (qui ne dispose pas d'interface d'affichage native).

### 🚀 Comment lancer le projet sur votre machine :
Pour profiter pleinement de l'expérience et tester le jeu, il vous suffit de :
1. **[Télécharger ou cloner ce dossier](https://github.com/yohanherve1-art/foule/tree/main/HERVE_HUAN)** sur votre ordinateur (via le bouton vert *Code* > *Download ZIP*).
2. Ouvrir le dossier dans votre environnement de développement Python habituel (comme VS Code ou PyCharm).
3. Vous assurer d'avoir installé les bibliothèques requises (`pip install pygame pillow`).
4. Ouvrir et exécuter le script principal **`PROJET S5.py`** (le fichier `tkiteasy.py` devant impérativement se trouver dans le même dossier pour gérer l'affichage).
