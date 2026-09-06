from tkiteasy import *
import random
import pygame
pygame.mixer.init()



with open(r"./dico.txt", "r", encoding="utf-8") as fichier:
    mots = fichier.read().splitlines()
with open(r"./meilleurscore.txt", "r", encoding="utf-8") as fichier2:
    meilleurscore = int(fichier2.read())
dictionnaire_fr = {mot: True for mot in mots}

g = ouvrirFenetre(1000, 1000)

points=0
points1 = 0
points2 = 0

class Noeud:
    def __init__(self, caractere):
        self.caractere = caractere  # Lettre stockée dans le noeud
        self.enfants = {}  # Dictionnaire des noeuds enfants
        self.finmot = False  # Indique si c'est la fin d'un mot valide


class ArbreMots:
    def __init__(self):
        self.racine = Noeud("")
    def ajoutermot(self, mot):
        noeud = self.racine
        for lettre in mot:
            if lettre not in noeud.enfants:
                noeud.enfants[lettre] = Noeud(lettre)  # Ajoute la lettre si absente
            noeud = noeud.enfants[lettre]  # Avance au noeud suivant
        noeud.finmot = True  # Marque la fin d'un mot valide

    def chargerdictionnaire(self, fichier):
        with open(fichier, "r", encoding="utf-8") as f:  # Ouvre le fichier
            for ligne in f:
                mot = ligne.strip()
                self.ajoutermot(mot)  # Ajoute chaque mot à l'arbre

    def recherchermot(self, mot):
        noeud = self.racine
        for lettre in mot:
            if lettre not in noeud.enfants:
                return False  # Mot absent si une lettre est manquante
            noeud = noeud.enfants[lettre]  # Passe au noeud suivant
        return noeud.finmot  # Retourne True si c'est un mot complet

    def afficherarbre(self, noeud=None, prefixe=""):
        if noeud is None:
            noeud = self.racine  # Départ à la racine

        if noeud.finmot:
            print(prefixe)  # Affiche le mot complet

        for lettre, enfant in noeud.enfants.items():
            self.afficherarbre(enfant, prefixe + lettre)

    def trouvermots(self, grille):
        motstrouves = set()  # Stocke les mots trouvés pour les afficher plus tard
        taille = len(grille)  # Adaptation en fonction de la taille de la grille

        def explorermot(x, y, noeud, prefixe, visite):
            if (x, y) in visite or not (0 <= x < taille and 0 <= y < taille):
                return
            lettre = grille[x][y]
            if lettre not in noeud.enfants:
                return  # Arrête si la lettre n'existe pas dans l'arbre

            visite.add((x, y))  # On enregistre la case visitéde pour ne pas retourner dessuer
            noeud = noeud.enfants[lettre]
            prefixe += lettre  # Ajoute la lettre au mot en cours de compositon

            if noeud.finmot:
                motstrouves.add(prefixe)  # Enregistre le mot si valide

            for i in range(-1, 2):  # Explore toutes les directions possibles même les diagonales
                for j in range(-1, 2):
                    if i != 0 or j != 0:
                        explorermot(x + i, y + j, noeud, prefixe, visite)

            visite.remove((x, y))  # Nettoie la visite après exploration

        for i in range(taille):  # Parcourt la grille en entier
            for j in range(taille):
                explorermot(i, j, self.racine, "", set())

        return motstrouves
arbre = ArbreMots()
arbre.chargerdictionnaire("./dico.txt")

son2 = pygame.mixer.Sound("son4.mp3")
son2.play()

class Jeu1v1():
    def __init__(self, nbcase):
        self.nbcase = nbcase    # Adaptation du jeu en fonction du nombre de cases voulues
        self.motdejavalide = [] # Stockage commun des mots déjà validés pour le mode JcJ pour pas remettre le mot de son adversaire
        self.lettres = {
            'A': 0.081, 'B': 0.009, 'C': 0.033, 'D': 0.037, 'E': 0.171, 'F': 0.011, 'G': 0.009, 'H': 0.009,
            'I': 0.075, 'J': 0.002, 'K': 0.001, 'L': 0.054, 'M': 0.030, 'N': 0.071, 'O': 0.058, 'P': 0.025,
            'Q': 0.014, 'R': 0.067, 'S': 0.081, 'T': 0.070, 'U': 0.057, 'V': 0.013, 'W': 0.001, 'X': 0.004,
            'Y': 0.003, 'Z': 0.001 }
        self.damier = [[random.choices(list(self.lettres.keys()), weights=self.lettres.values(), k=1)[0]
                        for _ in range(self.nbcase)] for _ in range(self.nbcase)]
    def menu(self):
        pygame.mixer.music.load("musique.mp3")
        pygame.mixer.music.play(-1)
        g.afficherImage(0, 0, "./fond.webp", 1000, 1000)
        g.afficherImage(955, 745, "./feuille1.png", 70, 70)
        g.afficherImage(915, 770, "./feuille2.png", 70, 70)
        g.afficherImage(935, 760, "./coco.png", 70, 70)
        g.afficherImage(360, 160, "./singe.png", 300, 300)
        bouton1 = g.afficherImage(220, 420, "./modesolo.png", 550, 170)
        bouton2 = g.afficherImage(220, 570, "./modejcj.png", 550, 170)
        son1 = pygame.mixer.Sound("yea.mp3")
        cont = True
        while cont:
            p = g.attendreClic()
            pos = (p.x, p.y)
            if 260 < pos[0] < 730 and 450 < pos[1] < 550:
                cont = False

                g.supprimer(bouton1)   # Animation du bouton : on le rend plus petit pendant un petit lapse de temps pour avoir une impression de bouton enfoncé
                bouton1 = g.afficherImage(245, 428, "./modesolo.png", 500, 153)
                g.actualiser()
                g.pause(0.01)
                g.supprimer(bouton1)
                bouton1 = g.afficherImage(220, 420, "./modesolo.png", 550, 170)
                g.actualiser()

                g.supprimerTout()
                pygame.mixer.music.stop()
                son1.play()
                self.modesolo()
            if 260 < pos[0] < 730 and 600 < pos[1] < 700:
                cont = False

                g.supprimer(bouton2)    # Animation du bouton
                bouton1 = g.afficherImage(245, 578, "./modejcj.png", 500, 153)
                g.actualiser()
                g.pause(0.01)
                g.supprimer(bouton1)
                bouton1 = g.afficherImage(220, 570, "./modejcj.png", 550, 170)
                g.actualiser()

                g.supprimerTout()
                pygame.mixer.music.stop()
                son1.play()
                self.modeduo()
            if 935 < pos[0] < 1000 and 760 < pos[1] < 830:   # Easter Egg secret
                b = g.afficherImage(0, 200, "./yoha.jpg", 1000, 600)
                pygame.mixer.music.load("son3.mp3")
                pygame.mixer.music.play()
                g.actualiser()
                g.pause(0.5)
                g.supprimer(b)
                g.actualiser()
                pygame.mixer.music.stop()
                pygame.mixer.music.load("musique.mp3")
                pygame.mixer.music.play(-1)

    def modesolo(self):
        bouton1, bouton2, affichagescore, affichagemeilleurscore = self.affichagesolo()
        self.selectionmotsolo(bouton1, bouton2, affichagescore, affichagemeilleurscore)

    def modeduo(self):
        bouton1, bouton2, affichagescore1, affichagescore2 = self.affichageduo()
        self.selectionmotduo(bouton1, bouton2, affichagescore1, affichagescore2,1)


    def matrice(self):
        return self.damier

    def affichagesolo(self):
        g.afficherImage(0,0, "./fond2.webp", 1000, 1000)

        g.afficherImage(955, 745, "./feuille1.png", 70, 70)
        g.afficherImage(915, 770, "./feuille2.png", 70, 70)
        g.afficherImage(935, 760, "./coco.png", 70, 70)

        for i in range(self.nbcase):
            for j in range(self.nbcase):
                g.afficherImage(5 + (650/self.nbcase)*j,5 + (650/self.nbcase)*i, "./case.png", 650 // self.nbcase , 650 // self.nbcase)   # On affiche chaque cases

        for i in range(self.nbcase):
            for j in range(self.nbcase):
                x_case = 10 + (650 / self.nbcase) * j
                y_case = 10 + (650 / self.nbcase) * i
                taille_case = (650 / self.nbcase) - 10
                g.afficherTexte(self.damier[i][j], x_case + taille_case / 2, y_case + taille_case / 2, "green",650 // (4 * self.nbcase))  # On affiche les lettres dans les cases

        bouton2 = g.afficherImage(0,670,"./valider.png" , 360, 150)
        bouton1 = g.afficherImage(350,670,"./terminer.png" , 380, 150)     # On associe les boutons a des objets pour les modifier et rendre possible l'animation du clic

        g.afficherImage(900, 200, "./case2.png", 80, 80)
        g.afficherImage(885, 190, "./score.png", 110, 40)
        affichagescore = g.afficherTexte(f"{points}", 940, 240, "#FFD900", 30)
        g.afficherImage(900, 50, "./case2.png", 80, 80)
        g.afficherImage(885, 40, "./meilleur.png", 110, 40)
        affichagemeilleurscore = g.afficherTexte(f"{meilleurscore}", 940, 90, "#FFD900", 30) # De meme pour les scores pour pouvoir les modifier

        g.actualiser()
        return bouton1,bouton2,affichagescore,affichagemeilleurscore

    def affichageduo(self):
        g.afficherImage(0, 0, "./fond1.webp", 1000, 1000)

        g.afficherImage(955, 745, "./feuille1.png", 70, 70)
        g.afficherImage(915, 770, "./feuille2.png", 70, 70)
        g.afficherImage(935, 760, "./coco.png", 70, 70)

        for i in range(self.nbcase):
            for j in range(self.nbcase):
                g.afficherImage(5 + (650 / self.nbcase) * j, 5 + (650 / self.nbcase) * i, "./case.png",650 // self.nbcase, 650 // self.nbcase)

        for i in range(self.nbcase):
            for j in range(self.nbcase):
                x_case = 10 + (650 / self.nbcase) * j
                y_case = 10 + (650 / self.nbcase) * i
                taille_case = (650 / self.nbcase) - 10
                g.afficherTexte(self.damier[i][j], x_case + taille_case / 2, y_case + taille_case / 2, "green",650 // (4 * self.nbcase))

        bouton2 = g.afficherImage(0, 670, "./valider.png", 360, 150)
        bouton1 = g.afficherImage(350, 670, "./terminer.png", 380, 150)

        g.afficherImage(900, 200, "./case2.png", 80, 80)
        g.afficherImage(885, 190, "./scorej1.png", 110, 40)
        affichagescore1 = g.afficherTexte(f"{points1}", 940, 240, "#FFD900", 30)
        g.afficherImage(900, 50, "./case2.png", 80, 80)
        g.afficherImage(885, 40, "./scorej2.png", 110, 40)
        affichagescore2 = g.afficherTexte(f"{points2}", 940, 90, "#FFD900", 30)

        g.actualiser()
        return bouton1, bouton2, affichagescore1, affichagescore2

    def selectionmotsolo(self,bouton1,bouton2,affichagescore,affichagemeilleurscore):
        liste = []   # Lettres stockées actuellement pour la composition de ce mot
        liste2 = []  # Mots déjà validés
        liste3 = []  # Stockage de la coordonnées de la lettre précédente pour le voisinage
        liste4 = []  # Lettres déjà utilisées pour composer ce mot
        surbrillance = []  # Stocke les coordonnées des lettres utilisés pour enlever la surbrillance jaune des lettres
        cont = True
        while cont:
            clic = g.attendreClic()
            pos = (clic.x, clic.y)
            if 28 < pos[0] < 328 and 700 < pos[1] < 790:
                pygame.mixer.music.load("clic.mp3")
                pygame.mixer.music.play()

                g.supprimer(bouton2)   # Animation du bouton
                bouton2 = g.afficherImage(18, 678, "./valider.png", 324, 135)
                g.actualiser()
                g.pause(0.01)
                g.supprimer(bouton2)
                bouton2 = g.afficherImage(0,670,"./valider.png" , 360, 150)
                g.actualiser()

                affichagescore, affichagemeilleurscore = self.verificationsolo(liste, liste2, affichagescore, affichagemeilleurscore)
                liste = []
                liste3 = []
                liste4 = []    # Une fois qu'on valide le mot on remet tout à zéro sauf la liste des mots déjà validés

                for i in range(0,len(surbrillance)-1,2):
                    x_case = 10 + (650 / self.nbcase) * surbrillance[i+1]
                    y_case = 10 + (650 / self.nbcase) * surbrillance[i]
                    taille_case = (650 / self.nbcase) - 10
                    g.afficherTexte(self.damier[surbrillance[i]][surbrillance[1+i]], x_case + taille_case / 2, y_case + taille_case / 2,"green", 650 // (4 * self.nbcase))

                surbrillance = []   # Une fois qu'on a redessiné plus besoin de stocker les anciennes lettres pour la prochaine fois

            if 380 < pos[0] < 700 and 700 < pos[1] < 790:
                pygame.mixer.music.load("clic.mp3")
                pygame.mixer.music.play()

                g.supprimer(bouton1)  # Animation du bouton
                bouton1 = g.afficherImage(369, 678, "./terminer.png", 342, 135)
                g.actualiser()
                g.pause(0.01)
                g.supprimer(bouton1)
                bouton1 = g.afficherImage(350,670,"./terminer.png" , 380, 150)
                g.actualiser()

                cont = False

                self.trouvemaxi()  # Si on appuie sur le bouton terminé on lance la recherche de mots

            if 935 < pos[0] < 1000 and 760 < pos[1] < 830:
                g.supprimerTout()
                self.menu()    # Le bouton noix de coco permet de revenir au menu

            for i in range(self.nbcase):
                for j in range(self.nbcase):
                    x_case = 10 + (650 / self.nbcase) * j
                    y_case = 10 + (650 / self.nbcase) * i
                    taille_case = (650 / self.nbcase) - 10
                    if x_case < pos[0] < x_case + taille_case and y_case < pos[1] < y_case + taille_case and (int(f"{i}{j}") not in liste4):
                        if liste3 != []:
                            if ( i-1 <= liste3[0] <= i+1 and j-1 <= liste3[1] <= j+1) and (liste3[0] != i or liste3[1] != j) :   # Si c'est pas la première lettre on vérifie le voisinage tout en regardant que ça soit pas la même case
                                liste3[0] = i
                                liste3[1] = j    # Les coordonnées de la nouvelle case remplace les anciennes, et ne sont pas ajoutés : très important
                                liste.append(self.damier[i][j])
                                g.afficherTexte(self.damier[i][j], x_case + taille_case / 2, y_case + taille_case / 2,
                                                "#FFD900", 650 // (4 * self.nbcase))

                                surbrillance.append(i)
                                surbrillance.append(j)
                                liste4.append(int(f"{i}{j}"))

                        elif  liste3 == []:   # Si c'est la première lettre du mot qu'on essaye de composer alors pas besoin de vérification de voisinage
                            liste3.append(i)
                            liste3.append(j)
                            liste.append(self.damier[i][j])
                            g.afficherTexte(self.damier[i][j], x_case + taille_case / 2, y_case + taille_case / 2,
                                            "#FFD900", 650 // (4 * self.nbcase))

                            surbrillance.append(i)
                            surbrillance.append(j)
                            liste4.append(int(f"{i}{j}"))


    def selectionmotduo(self,bouton1,bouton2,affichagescore1,affichagescore2,jo):
        liste = []  # Lettres stockées actuellement pour la composition de ce mot
        liste3 = []  # Stockage de la coordonnées de la lettre précédente pour le voisinage
        liste4 = []  # Lettres déjà utilisées pour composer ce mot
        surbrillance = []  # Stocke les coordonnées des lettres utilisés pour enlever la surbrillance jaune des lettres
        cont = True
        while cont:
            p = g.attendreClic()
            pos = (p.x, p.y)
            if 28 < pos[0] < 328 and 700 < pos[1] < 790:
                pygame.mixer.music.load("clic.mp3")
                pygame.mixer.music.play()

                g.supprimer(bouton2)   # Animation du bouton
                bouton2 = g.afficherImage(18, 678, "./valider.png", 324, 135)
                g.actualiser()
                g.pause(0.01)
                g.supprimer(bouton2)
                bouton2 = g.afficherImage(0, 670, "./valider.png", 360, 150)
                g.actualiser()

                affichagescore1, affichagescore2 = self.verificationduo(liste, affichagescore1,affichagescore2,jo)
                liste = []
                liste3 = []
                liste4 = []     # Une fois qu'on valide le mot on remet tout à zéro sauf la liste des mots déjà validés

                for i in range(0, len(surbrillance) - 1, 2):
                    x_case = 10 + (650 / self.nbcase) * surbrillance[i + 1]
                    y_case = 10 + (650 / self.nbcase) * surbrillance[i]
                    taille_case = (650 / self.nbcase) - 10
                    g.afficherTexte(self.damier[surbrillance[i]][surbrillance[1 + i]], x_case + taille_case / 2,
                                    y_case + taille_case / 2, "green", 650 // (4 * self.nbcase))

                if jo ==1:
                    cont = False
                    self.selectionmotduo(bouton1, bouton2, affichagescore1, affichagescore2, 2)
                if jo ==2:
                    cont = False
                    self.selectionmotduo(bouton1, bouton2, affichagescore1, affichagescore2, 1)

                # En fonction de qui à joué avant, on lance le tour de l'autre joueur
            if 380 < pos[0] < 700 and 700 < pos[1] < 790:
                pygame.mixer.music.load("clic.mp3")
                pygame.mixer.music.play()

                g.supprimer(bouton1)   # Animation du bouton
                bouton1 = g.afficherImage(369, 678, "./terminer.png", 342, 135)
                g.actualiser()
                g.pause(0.01)
                g.supprimer(bouton1)
                bouton1 = g.afficherImage(350, 670, "./terminer.png", 380, 150)
                g.actualiser()

                cont = False

                self.trouvemaxi()

                g.supprimerTout()

            if 935 < pos[0] < 1000 and 760 < pos[1] < 830:
                g.supprimerTout()
                self.menu()

            for i in range(self.nbcase):
                for j in range(self.nbcase):
                    x_case = 10 + (650 / self.nbcase) * j
                    y_case = 10 + (650 / self.nbcase) * i
                    taille_case = (650 / self.nbcase) - 10
                    if x_case < pos[0] < x_case + taille_case and y_case < pos[1] < y_case + taille_case and (int(f"{i}{j}") not in liste4):     # Si c'est pas la première lettre on vérifie le voisinage tout en regardant que ça soit pas la même case
                        if liste3 != []:
                            if (i - 1 <= liste3[0] <= i + 1 and j - 1 <= liste3[1] <= j + 1) and (
                                    liste3[0] != i or liste3[1] != j):
                                liste3[0] = i
                                liste3[1] = j      # Les coordonnées de la nouvelle case remplace les anciennes, et ne sont pas ajoutés : très important
                                liste.append(self.damier[i][j])
                                g.afficherTexte(self.damier[i][j], x_case + taille_case / 2, y_case + taille_case / 2,
                                                "#FFD900", 650 // (4 * self.nbcase))

                                surbrillance.append(i)
                                surbrillance.append(j)
                                liste4.append(int(f"{i}{j}"))

                        elif liste3 == []:     # Si c'est la première lettre du mot qu'on essaye de composer alors pas besoin de vérification de voisinage
                            liste3.append(i)
                            liste3.append(j)
                            liste.append(self.damier[i][j])
                            g.afficherTexte(self.damier[i][j], x_case + taille_case / 2, y_case + taille_case / 2,
                                            "#FFD900", 650 // (4 * self.nbcase))

                            surbrillance.append(i)
                            surbrillance.append(j)
                            liste4.append(int(f"{i}{j}"))



    def verificationsolo(self,liste,liste2,affichagescore,affichagemeilleurscore):
        global points
        global meilleurscore
        sortie = "".join(liste).lower()
        if sortie in liste2:   # Vérification si le mot à déjà été validé
            pygame.mixer.music.load("bientente.mp3")
            pygame.mixer.music.play()
        elif sortie in dictionnaire_fr and sortie not in liste2:
            points += len(sortie)
            if len(sortie) > 5:
                pygame.mixer.music.load("son3.mp3")
                pygame.mixer.music.play()
            elif len(sortie) > 3:
                pygame.mixer.music.load("son2.mp3")
                pygame.mixer.music.play()
            else :
                pygame.mixer.music.load("son1.mp3")
                pygame.mixer.music.play()   # On lance une musique différente en fonction de la taille du mot
            liste2.append(sortie)
            if points > meilleurscore:
                with open(r"/Users/louishuan/Downloads/meilleurscore.txt", "w", encoding="utf-8") as fichier2:
                    fichier2.write(str(points))  # On tient à jour le meilleur score si on le dépasse
                meilleurscore = points
        else:
            pygame.mixer.music.load("faux.mp3")
            pygame.mixer.music.play()

        g.supprimer(affichagescore)
        g.supprimer(affichagemeilleurscore)
        affichagescore = g.afficherTexte(f"{points}", 940, 240, "#FFD900", 30)
        affichagemeilleurscore = g.afficherTexte(f"{meilleurscore}", 940, 90, "#FFD900", 30)
        g.actualiser()   # On met à jour le score et le meilleur score à chaque tour

        return affichagescore, affichagemeilleurscore


    def verificationduo(self,liste,affichagescore1,affichagescore2,jo):
        global points1
        global points2


        sortie = "".join(liste).lower()
        if sortie in self.motdejavalide:    # Vérification si le mot à déjà été validé
            pygame.mixer.music.load("bientente.mp3")
            pygame.mixer.music.play()
        elif sortie in dictionnaire_fr and sortie not in self.motdejavalide:
            if jo == 1:
                points1 += len(sortie)
            if jo == 2:
                points2 += len(sortie)
            if len(sortie) > 5:
                pygame.mixer.music.load("son3.mp3")
                pygame.mixer.music.play()
            elif len(sortie) > 3:
                pygame.mixer.music.load("son2.mp3")
                pygame.mixer.music.play()
            else :
                pygame.mixer.music.load("son1.mp3")
                pygame.mixer.music.play()
            self.motdejavalide.append(sortie)
        else:
            pygame.mixer.music.load("faux.mp3")
            pygame.mixer.music.play()

        if (points2 - points1) > 9 or (points1 - points2 ) > 9 :
            pygame.mixer.music.load("sontriste.mp3")
            pygame.mixer.music.play()   # Musique triste qui se lance si un joueur a trop d'avance sur son adversaire

        g.supprimer(affichagescore1)
        g.supprimer(affichagescore2)
        affichagescore1 = g.afficherTexte(f"{points1}", 940, 240, "#FFD900", 30)
        affichagescore2 = g.afficherTexte(f"{points2}", 940, 90, "#FFD900", 30)
        g.actualiser()

        return affichagescore1, affichagescore2
    def trouvemaxi(self):
        damier = [[lettre.lower() for lettre in ligne] for ligne in self.damier]  # On met les lettres en minuscules pour la recherche avec l'arbre
        motstrouves = arbre.trouvermots(damier)
        motstrouves = [mot.upper() for mot in motstrouves]  # On veut afficher les mots en majuscules à la fin du jeu
        self.affichagemotfinal(motstrouves)

    def affichagemotfinal(self,set):
        boucle = True
        a = 0
        b = -1
        g.supprimerTout()
        g.afficherImage(0, 0, "./fond.webp", 1000, 1000)
        g.afficherImage(0,0, "./case3.png", 1020, 820)
        listetriee = sorted(set) # On affiche par odres aphabétiques les solutions
        for i in range(0,min(len(listetriee),128)):
            b += 1
            g.afficherTexte(listetriee[i], 150 + 100*(b//16) , 100 + 40*i - 640*(b//16), "green", 18)
        while boucle:
            touche = g.attendreTouche()
            if touche == "Return":
                boucle = False
                g.fermerFenetre()
            if len(listetriee) > 128 + 128*a:
                if touche == "z":
                    b=-1
                    a +=1
                    g.supprimerTout()
                    g.afficherImage(0, 0, "./fond.webp", 1000, 1000)
                    g.afficherImage(0, 0, "./case3.png", 1020, 820)
                    for i in range(128*a, min(len(listetriee), 128 + 128*a)):
                        b += 1
                        g.afficherTexte(listetriee[i], 150 + 100 * (b // 16), 100 + 40 * b - 640 * (b // 16), "green", 18)
                    g.actualiser()
            if len(listetriee) > 128 + 128*(a-1) and a != 0:
                if touche == "a":
                    b=-1
                    a += -1
                    g.supprimerTout()
                    g.afficherImage(0, 0, "./fond.webp", 1000, 1000)
                    g.afficherImage(0, 0, "./case3.png", 1020, 820)
                    for i in range(128*a, min(len(listetriee), 128 + 128*a)):
                        b += 1
                        g.afficherTexte(listetriee[i], 150 + 100 * (b // 16), 100 + 40 * b - 640 * (b // 16), "green", 18)
                    g.actualiser()

jeu = Jeu1v1(4)
print(jeu.matrice)
jeu.menu()
