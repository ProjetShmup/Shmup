import pygame
from pygame.locals import *
import sys
from random import randint
from time import sleep, time

pygame.mixer.pre_init(buffer=1024)
pygame.mixer.init()
pygame.init()

#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((768, 768))
pygame.display.set_caption("SHMUP")


Clock = pygame.time.Clock()
frame_times = []
start_t = time()

fullscreen = 0
###########################################################################################################################################################################


#Remplacement de la souris par une nouvelle personnalisée :

pygame.mouse.set_visible ( False ) #on rend le curseur original invisible
souris = pygame.image.load("Images/Souris/souris.png").convert_alpha() #et on ajoute la nouvelle apparence en tant que variable


###########################################################################################################################################################################
#Chargement des pistes audio du jeu

son_bouton = pygame.mixer.Sound("sfx/sfx_bouton.ogg")
son_quitter = pygame.mixer.Sound("sfx/sfx_bouton_quitter.ogg")
son_spawn = pygame.mixer.Sound("sfx/Spawn.ogg")

son_tirennemi = pygame.mixer.Sound("sfx/tir_ennemi.ogg")
son_tirjoueur = pygame.mixer.Sound("sfx/tir_joueur.ogg")

son_joueurtoucher = pygame.mixer.Sound("sfx/explosion_joueur.ogg")
son_ennemitoucher = pygame.mixer.Sound("sfx/explosion_ennemi.ogg")

son_credit = pygame.mixer.Sound("sfx/credit_ooh1.ogg")
son_credit2 = pygame.mixer.Sound("sfx/credit_ooh2.ogg")
son_credit3 = pygame.mixer.Sound("sfx/credit_ooh3.ogg")
son_credit4 = pygame.mixer.Sound("sfx/credit_ooh4.ogg")
son_credit5 = pygame.mixer.Sound("sfx/credit_ooh5.ogg")
son_credit6 = pygame.mixer.Sound("sfx/credit_ooh6.ogg")
son_credit7 = pygame.mixer.Sound("sfx/credit_ooh7.ogg")
son_credit8 = pygame.mixer.Sound("sfx/credit_ooh8.ogg")

Musique = randint(1,3)
if Musique == 1:
    Musique_menu = pygame.mixer.music.load("Musiques/loop_menu.ogg")
    pygame.mixer.music.play(-1)

if Musique == 2:
    Musique_menu = pygame.mixer.music.load("Musiques/loop_menu_2.ogg")
    pygame.mixer.music.play(-1)

if Musique == 3:
    Musique_menu = pygame.mixer.music.load("Musiques/loop_menu_3.ogg")
    pygame.mixer.music.play(-1)


###########################################################################################################################################################################


Joueur = pygame.image.load("Images/Joueur.png").convert_alpha()
pos_joueur = Joueur.get_rect()
pos_joueur.bottomleft = (0,0)

sprite_tir = pygame.image.load("Images/Tirs_1.png").convert_alpha()
sprite_tir2 = pygame.image.load("Images/Tirs_2.png").convert_alpha()
pos_tir = sprite_tir.get_rect()

sprite_ennemie = pygame.image.load("Images/Ennemis.png").convert_alpha()
pos_ennemie = sprite_ennemie.get_rect()

listEnnemie = []
listTir = []
listTirEnnemie = []


#_________________________________________________________#

class Ennemie :
    """classe définissant les entitées adverses du joueur avec :
une vie (le nombre de dégats que devra subir l'objet avant de se faire éliminer)
"""
    def __init__ (self, vie, pos):
        self.image = sprite_ennemie
        self.rect = self.image.get_rect()
        self.vie = 3
        self.vitesse = 1
        self.rect.topleft = pos

    def afficher (self):
        fenetre.blit(self.image,self.rect.topleft)

    def move (self) :
        self.rect.bottom+=self.vitesse

    def delete (self) :
        listEnnemie.remove(ennemie)


#_________________________________________________________#

class TirsEnnemie :

    """classe définissant un projectile lancé par le sprite du joueur avec :
une puissance (le nombre de dégats qu'il infligerai),
une position (là où se trouve le sprite du joueur)"""


    def __init__ (self, puissance, pos):

        self.vitesse = 2 #vitesse d'un projectile (en pixels par frame)
        #self.puissance = puissance
        self.image = sprite_tir2
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def afficher (self) :
        fenetre.blit(self.image,self.rect.topleft)

    def move (self) :
        self.rect.top+=self.vitesse

    def delete (self) :
        listTirEnnemie.remove(tir)

#_________________________________________________________#

class TirsJoueur :

    """classe définissant un projectile lancé par le sprite du joueur avec :
une puissance (le nombre de dégats qu'il infligerai),
une position (là où se trouve le sprite du joueur)"""

    def __init__ (self, puissance, pos):

        self.vitesse = 2 #vitesse d'un projectile (en pixels par frame)
        #self.puissance = puissance
        self.image = sprite_tir
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def afficher (self) :
        fenetre.blit(self.image,self.rect.topleft)

    def move (self) :
        self.rect.top-=self.vitesse

    def delete (self) :
        listTir.remove(tir)


###########################################################################################################################################################################

#Chargement et collage du fond et image des différents défillements :

fond = pygame.image.load("Images/fond.png").convert()
position = fond.get_rect()
position.topleft = (0,0)
positionbis = position.copy()
positionbis.bottomleft = (0,0)

etoiles1 = pygame.image.load("Images/etoiles1.png").convert_alpha()
position_etoiles1 = etoiles1.get_rect()
position_etoiles1.topleft = (0,0)
position_etoiles1bis = position_etoiles1.copy()
position_etoiles1bis.bottomleft = (0,0)

etoiles2 = pygame.image.load("Images/etoiles2.png").convert_alpha()
position_etoiles2 = etoiles2.get_rect()
position_etoiles2.topleft = (0,0)
position_etoiles2bis = position_etoiles2.copy()
position_etoiles2bis.bottomleft = (0,0)

etoiles3 = pygame.image.load("Images/etoiles3.png").convert_alpha()
position_etoiles3 = etoiles3.get_rect()
position_etoiles3.topleft = (0,0)
position_etoiles3bis = position_etoiles3.copy()
position_etoiles3bis.bottomleft = (0,0)

credits = pygame.image.load("Images/credits.png").convert_alpha()
pos_credits = credits.get_rect()
pos_credits.bottom = 0


###########################################################################################################################################################################


"""Création du Menu du jeu"""

    #Titre du jeu affiché dans le menu
titre = pygame.image.load("Images/Titre_tutoriel.png").convert_alpha()
pos_titre = titre.get_rect()

    #Bouton "Jeu"
bouton_jeu = pygame.image.load("Images/bouton_jeu.png").convert_alpha()
pos_bouton_jeu = bouton_jeu.get_rect()
pos_bouton_jeu.topleft = (231,260)

    #Bouton "Crédits"
bouton_credit = pygame.image.load("Images/bouton_credits.png").convert_alpha()
pos_bouton_credit = bouton_credit.get_rect()
pos_bouton_credit.topleft =(231,380)

    #Bouton "Quitter"
bouton_quitter = pygame.image.load("Images/bouton_quitter.png").convert_alpha()
pos_bouton_quitter = bouton_quitter.get_rect()
pos_bouton_quitter.topleft = (406,480)

###########################################################################################################################################################################

"""Création du HUD en jeu"""
vie = 3
score = 0
vague = 1

HUD = pygame.image.load("Images\HUD.png").convert_alpha()
pos_hud = HUD.get_rect()
pos_hud.topleft = (0,768)

police = 'Polices/ARCADECLASSIC.TTF'
scorePolice = pygame.font.Font(police,12 )
vaguePolice = pygame.font.Font(police,18 )
scoreTexte = scorePolice.render('{}'.format(score),1,(255, 255, 255))
vagueTexte = vaguePolice.render('{}'.format(vague),1,(255, 255, 255))

def Blit_hud () :
    fenetre.blit(HUD, (pos_hud.left,pos_hud.top))
    fenetre.blit(scoreTexte, (pos_hud.left + 50, pos_hud.top + 76))
    fenetre.blit(vagueTexte, (pos_hud.left + 74, pos_hud.top + 37))
    if vie == 3:
        fenetre.blit(imagevie3,(pos_hud))
    elif vie == 2 :
        fenetre.blit(imagevie2,(pos_hud))
    elif vie == 1 :
        fenetre.blit(imagevie,(pos_hud))


imagevie3 = pygame.image.load("Images/ViePleine.png")
pos_imagevie3 = imagevie3.get_rect()
pos_imagevie3.topleft = (0,(pos_hud.top))

imagevie2= pygame.image.load("Images/Vie2.png")
pos_imagevie2 = imagevie2.get_rect()
pos_imagevie2.topleft = (0,(pos_hud.top))

imagevie = pygame.image.load("Images/Vie1.png")
pos_imagevie = imagevie.get_rect()
pos_imagevie.topleft = (0,(pos_hud.top))


###########################################################################################################################################################################


def boucle_defilement_etoiles1 () :
    global position
    global positionbis
    positionbis = position
    position.topleft = (0,0)
    positionbis = position.copy()
    positionbis.bottomleft = (0,0)

def boucle_defilement_etoiles1 () :
    global position_etoiles1
    global position_etoiles1bis
    position_etoiles1bis = position_etoiles1
    position_etoiles1.topleft = (0,0)
    position_etoiles1bis = position_etoiles1.copy()
    position_etoiles1bis.bottomleft = (0,0)

def boucle_defilement_etoiles2 () :
    global position_etoiles2
    global position_etoiles2bis
    position_etoiles2bis = position_etoiles2
    position_etoiles2.topleft = (0,0)
    position_etoiles2bis = position_etoiles2.copy()
    position_etoiles2bis.bottomleft = (0,0)

def boucle_defilement_etoiles2 () :
    global position_etoiles3
    global position_etoiles3bis
    position_etoiles3bis = position_etoiles3
    position_etoiles3.topleft = (0,0)
    position_etoiles3bis = position_etoiles3.copy()
    position_etoiles3bis.bottomleft = (0,0)

def defilement_fond () :
    if positionbis.bottom == 1152 :
        boucle_defilement_etoiles1()
    elif position_etoiles1bis.bottom == 800 :
        boucle_defilement_etoiles1()
    elif position_etoiles2bis.bottom == 1300 :
        boucle_defilement_etoiles1()
    elif position_etoiles3bis.bottom == 1800 :
        boucle_defilement_etoiles3()

def blit_fond() :
    fenetre.blit(fond, (position))
    fenetre.blit(fond, (positionbis))
    fenetre.blit(etoiles1, (position_etoiles1))
    fenetre.blit(etoiles1, (position_etoiles1bis))
    fenetre.blit(etoiles2, (position_etoiles2))
    fenetre.blit(etoiles2, (position_etoiles2bis))
    fenetre.blit(etoiles3, (position_etoiles3))
    fenetre.blit(etoiles3, (position_etoiles3bis))

def blit_menu() :
    fenetre.blit(bouton_credit, (pos_bouton_credit))
    fenetre.blit(bouton_jeu, (pos_bouton_jeu))
    fenetre.blit(bouton_quitter, (pos_bouton_quitter))
    fenetre.blit(titre, (pos_titre))
    fenetre.blit(credits,(pos_credits))

def aff_plein_ecran():
    fenetre = pygame.display.set_mode((768, 768), pygame.FULLSCREEN)
    global fullscreen
    fullscreen = 1

def aff_fenetre ():
    global fullscreen
    fullscreen = 0
    fenetre = pygame.display.set_mode((768, 768))

###########################################################################################################################################################################

#Rafraîchissement de l'écran
pygame.display.flip()

#Vitesse du défillement de l'arrière-plan / définition de la parallaxe :
## Ex : toutes les 1.5 secondes l'évennement "scroll", correspondant au défillement de l'image de fond, sera appellé.
scroll = USEREVENT
pygame.time.set_timer(scroll, 2000)

scroll2 = USEREVENT+1
pygame.time.set_timer(scroll2, 750)

scroll3 = USEREVENT+2
pygame.time.set_timer(scroll3, 500)

scroll4 = USEREVENT+3
pygame.time.set_timer(scroll4, 300)

#défilement du menu quand l'utilisateur clique sur un bouton
scroll_menu = USEREVENT+4
scroll_menu_credits = USEREVENT+5
scroll_hud = USEREVENT+6
scroll_joueur = USEREVENT + 7

spawn_ennemie = USEREVENT
pygame.time.set_timer(spawn_ennemie, 2000)
###########################################################################################################################################################################


def repetition (delai, interval) :
    pygame.key.set_repeat(delai, interval)

repetition(10,10)
jeu = 0

"""Boucle infinie parcourant chaque évennements """
while True:
    entraindetirer = 0
    for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

##  Défillement de l'arrière-plan :
        elif event.type == scroll :
            position = position.move(0,+1)
            positionbis = positionbis.move(0,+1)

        elif event.type == scroll2 :
            position_etoiles1 = position_etoiles1.move(0,+1)
            position_etoiles1bis = position_etoiles1bis.move(0,+1)

        elif event.type == scroll3 :
            position_etoiles2 = position_etoiles2.move(0,+1)
            position_etoiles2bis = position_etoiles2bis.move(0,+1)

        elif event.type == scroll4 :
            position_etoiles3 = position_etoiles3.move(0,+1)
            position_etoiles3bis = position_etoiles3bis.move(0,+1)

##  Défillement du menu / transition
        elif event.type == scroll_menu :
            if 0<=pos_titre.top<=800  :
                pos_bouton_jeu = pos_bouton_jeu.move(0,+2)
                pos_bouton_credit = pos_bouton_credit.move(0,+2)
                pos_bouton_quitter = pos_bouton_quitter.move(0,+2)
                pos_titre = pos_titre.move(0,+2)

        elif event.type == scroll_menu_credits :
            if 0<=pos_titre.top<=800  :
                pos_bouton_jeu = pos_bouton_jeu.move(0,+3)
                pos_bouton_credit = pos_bouton_credit.move(0,+3)
                pos_bouton_quitter = pos_bouton_quitter.move(0,+3)
                pos_titre = pos_titre.move(0,+2)
            pos_credits = pos_credits.move(0,+1)

        if event.type == KEYDOWN :
            if event.key == K_F4 and fullscreen == 0:
                aff_plein_ecran()
            elif fullscreen == 1 and event.key == K_ESCAPE or event.key == K_F4 :
                aff_fenetre()


        #Defilement du HUD et du joueur / transition :
        if event.type == scroll_hud :
            if 769>=pos_hud.top>=673:
                pos_hud = pos_hud.move(0,-1)

        if event.type == spawn_ennemie and pos_hud.top <= 674:
            pos = randint(0, 735)
            listEnnemie.append(Ennemie(1,(pos,0)))

        if event.type == scroll_joueur:
            if 1076>=pos_joueur.bottom>=692:
                pos_joueur = pos_joueur.move(0,-1)

        if jeu == 0 : #Lorsqu'on est sur le menu

##  Actions des boutons sur le menu : Quitter ; Jouer ; Aller aux crédits
            if event.type == MOUSEBUTTONDOWN:

            #bouton quitter
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and pos_bouton_quitter.top < event.pos[1] < pos_bouton_quitter.bottom and pos_bouton_quitter.left < event.pos[0] < pos_bouton_quitter.right:
                    pygame.mixer.Sound.play(son_quitter)
                    pygame.time.wait(500)

            #bouton jeu
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pos_bouton_jeu.top < event.pos[1] < pos_bouton_jeu.bottom and pos_bouton_jeu.left < event.pos [0] < pos_bouton_jeu.right:
                    pygame.mixer.Sound.play(son_bouton)

            #bouton credits
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pos_bouton_credit.top < event.pos[1] < pos_bouton_credit.bottom and pos_bouton_credit.left < event.pos [0] < pos_bouton_credit.right:
                    pygame.mixer.Sound.play(son_bouton)


            elif event.type == MOUSEBUTTONUP:

            #bouton quitter
                if event.type == MOUSEBUTTONUP and event.button == 1 and pos_bouton_quitter.top < event.pos[1] < pos_bouton_quitter.bottom and pos_bouton_quitter.left < event.pos[0] < pos_bouton_quitter.right:
                    pygame.quit()
                    sys.exit()

            #bouton jeu
                elif event.type == MOUSEBUTTONUP and event.button == 1 and pos_bouton_jeu.top < event.pos[1] < pos_bouton_jeu.bottom and pos_bouton_jeu.left < event.pos [0] < pos_bouton_jeu.right:
                    jeu = 1


            #bouton credits
                elif event.type == MOUSEBUTTONUP and event.button == 1 and pos_bouton_credit.top < event.pos[1] < pos_bouton_credit.bottom and pos_bouton_credit.left < event.pos [0] < pos_bouton_credit.right:
                    pygame.mixer.music.fadeout(300)
                    pygame.mixer.music.load("Musiques/Credits.ogg")
                    pygame.mixer.music.play(2)
                    pygame.mixer.music.set_volume(1)
                    pygame.time.set_timer(scroll_menu_credits, 50)
                    jeu = 2



        elif jeu == 1 : #lorsqu'on est sur la fenètre de jeu
            pygame.time.set_timer(scroll_menu, 10)
            if pos_titre.top == 700 :
                pygame.mixer.music.fadeout(300)
                pygame.mixer.Sound.play(son_spawn)

                pos_joueur.bottomleft = (370,692+96)
                pygame.time.set_timer(scroll_hud, 40)
                pygame.time.set_timer (scroll_joueur, 80)

                pygame.mixer.music.load("Musiques/loop_jeu.ogg")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)



            if event.type == KEYDOWN :

                if event.key == K_LEFT and pos_joueur.left >= 0:
                    pos_joueur = pos_joueur.move(-4,0)

                if event.key == K_RIGHT and pos_joueur.right <= 768:
                    pos_joueur = pos_joueur.move(4,0)

                if event.key == K_SPACE :
                    repetition(0,0)
                    listTir.append(TirsJoueur(1,(pos_joueur.left + 10,pos_joueur.top - 20)))
                    pygame.mixer.Sound.play(son_tirjoueur)

            for ennemie in listEnnemie :
                if event.type == scroll2 and pos_hud.top <= 674:
                    listTirEnnemie.append(TirsEnnemie(1,(ennemie.rect.left + 17,ennemie.rect.bottom - 25)))
                    pygame.mixer.Sound.play(son_tirennemi)

            if event.type == KEYUP :

                if event.key == K_SPACE :
                    repetition(10,10)

    if jeu == 2:
        if pos_credits.bottomleft == (0,75):
            pygame.mixer.Sound.play(son_credit)

        if pos_credits.bottomleft == (0,200):
            pygame.mixer.Sound.play(son_credit2)

        if pos_credits.bottomleft == (0,330):
            pygame.mixer.Sound.play(son_credit3)

        if pos_credits.bottomleft == (0,460):
            pygame.mixer.Sound.play(son_credit4)

        if pos_credits.bottomleft == (0,510):
            pygame.mixer.Sound.play(son_credit5)

        if pos_credits.bottomleft == (0,590):
            pygame.mixer.Sound.play(son_credit6)

        if pos_credits.bottomleft == (0,705):
            pygame.mixer.Sound.play(son_credit7)

        if pos_credits.bottomleft == (0,883):
            pygame.mixer.Sound.play(son_credit8)
            
##Mise à jour de l'affichage :
    blit_fond()
    blit_menu()
    fenetre.blit(Joueur,(pos_joueur))

    end_t = time()
    time_taken = end_t - start_t
    start_t = end_t
    frame_times.append(time_taken)
    frame_times = frame_times[-20:]
    fps = len(frame_times) // sum(frame_times)
    fpsPolice = pygame.font.Font('Polices/calibril.ttf',24 )
    fpsTexte = fpsPolice.render('{}'.format(fps),1,(255, 255, 255))
    fenetre.blit(fpsTexte,(0,0))

    if jeu == 1 :
        Blit_hud()


    for tir in listTir:
        tir.afficher()
        tir.move()

    for tir in listTirEnnemie:
        tir.afficher()
        tir.move()
        collision3 = [pos_joueur]

        if tir.rect.bottom > 768 :
            tir.delete()

        elif tir.rect.collidelist(collision3) != -1 :
            pygame.mixer.Sound.play(son_joueurtoucher)
            if vie == 3 :
                vie = 2

            elif vie == 2 :
                vie = 1

            elif vie == 1 :
                vie =0
            tir.delete()

    for ennemie in listEnnemie:
        ennemie.afficher()
        ennemie.move()
        collision4 = [pos_joueur]

        if ennemie.rect.bottom > 768 :
            ennemie.delete()

        elif ennemie.rect.collidelist(collision4) != -1 :
            pygame.mixer.Sound.play(son_joueurtoucher)
            ennemie.delete()

    for tir in listTir:
        for ennemie in listEnnemie :

            collision = [tir.rect]
            collision2 = [ennemie.rect]

            if tir.rect.top < 0 :
                tir.delete()

            elif tir.rect.collidelist(collision2) != -1:
                pygame.mixer.Sound.play(son_ennemitoucher)
                tir.delete()
                

            if ennemie.rect.bottom > 768 :
                ennemie.delete()

            elif ennemie.rect.collidelist(collision) != -1:
                ennemie.delete()


##  Remplacement de la souris :
    if jeu == 0:
        x_curseur , y_curseur = pygame.mouse.get_pos()
        fenetre.blit(souris,(x_curseur,y_curseur))

##  Appels aux fonctions pour boucler les défilements des différents fonds :
    defilement_fond()
    if positionbis.bottom == 1152 :
        boucle_defilement_etoiles1()
    elif position_etoiles1bis.bottom == 800 :
        boucle_defilement_etoiles1()
    elif position_etoiles2bis.bottom == 1300 :
        boucle_defilement_etoiles1()
    elif position_etoiles3bis.bottom == 1800 :
        boucle_defilement_etoiles3()

    pygame.display.flip()