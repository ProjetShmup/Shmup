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
"""remplacement de la souris de l'OS par un sprite personalisé"""

pygame.mouse.set_visible ( False ) #on rend le curseur original invisible
souris = pygame.image.load("Images/Souris/souris.png").convert_alpha() #et on associe à une variable le nouveau sprite


###########################################################################################################################################################################
"""Chargement des pistes audio du jeu"""

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

#On charge les sprites des tirs dans deux variables, la première pour ceux du joueur et la seconde pour ceux des ennemis
sprite_tir = pygame.image.load("Images/Tirs_1.png").convert_alpha()
sprite_tir2 = pygame.image.load("Images/Tirs_2.png").convert_alpha()


sprite_ennemie = pygame.image.load("Images/Ennemis.png").convert_alpha()
pos_ennemie = sprite_ennemie.get_rect()

listEnnemie = []
listTir = [] #Variable globale définie par une liste vide qui contiendra chaque objet de classe TirsJoueur
listTirEnnemie = [] #Variable globale définie par une liste vide qui contiendra chaque objet de classe TirsEnnemie


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
une position (là où apparaîtra l'objet à sa création)"""


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
une position (là où apparaîtra l'objet à sa création)"""

    def __init__ (self, puissance, pos):

        self.vitesse = 2 #vitesse d'un projectile (en pixels par frame)
        #self.puissance = puissance
        self.image = sprite_tir #on défini le sprite du tir
        self.rect = self.image.get_rect() #on défini un objet Rect avec le sprite du tir
        self.rect.topleft = pos # on défini la position de l'objet par son coin supperieur gauche

    def afficher (self) : #Methode affichant le tir sur la fenêtre
        fenetre.blit(self.image,self.rect.topleft)

    def move (self) : #Methode déplacant le tir selon sa vitesse
        self.rect.top-=self.vitesse

    def delete (self) : #Methode supprimant le tir de la fenêtre
        listTir.remove(tir)


###########################################################################################################################################################################
"""Chargement de l'arrière-plan :"""

fond = pygame.image.load("Images/fond.png").convert()  #Chargement de l'image de fond
position = fond.get_rect() #on définit un objet Rect à partir de l'image précédement chargée
position.topleft = (0,0) #on place ce rectangle sur l'écran en prenant comme point d'ancrage son coin supperieur gauche
positionbis = position.copy() #on définit une copie de l'objet Rect précédent qui va permettre un défilement illimité
positionbis.bottomleft = (0,0) #on place cette copie au même endroit mais avec comme point d'ancrage son coin infèrieur gauche, ainsi elle se trouve au dessus du premier Rect

#on répète la même opération pour chaque image composant l'arrière-plan
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

credits = pygame.image.load("Images/credits.png").convert_alpha() #On charge l'image des crédits dès l'allumage, elle est constamment chargée mais n'apparaît pas sur la fenêtre
pos_credits = credits.get_rect() #on définit un objet Rect à partir de l'image des crédits
pos_credits.bottom = 0 #on place la bas du Rect à y=0, de cette façon il est dissimulé au delà des bordures de la fenêtre


###########################################################################################################################################################################
"""Création du Menu du jeu"""

    #Titre du jeu
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
"""Création du GAMEOVER"""

    #Image du gameover
gameover = pygame.image.load("Images/gameover.png").convert_alpha()
pos_gameover = gameover.get_rect()
pos_gameover.bottomleft = (0,0)

    #Bouton "Rejouer"
bouton_rejouer = pygame.image.load("Images/bouton_rejouer.png").convert_alpha()
pos_bouton_rejouer = bouton_rejouer.get_rect()
pos_bouton_rejouer.bottomleft = (0,0)

    #Bouton "Menu"
bouton_menu = pygame.image.load("Images/bouton_menu.png").convert_alpha()
pos_bouton_menu = bouton_menu.get_rect()
pos_bouton_menu.bottomleft = (0,0)


###########################################################################################################################################################################
"""Création de l'HUD en jeu"""

vie = 3 #Variable associée à la vie du joueur, par défaut à 3 (maximum)
score = 0 #Variable associée au score du joueur, par défaut à 0 (minimum)
vague = 1 #variable associée à la vague d'ennemis actuelle, par défaut à 1

HUD = pygame.image.load("Images\HUD.png").convert_alpha()
pos_hud = HUD.get_rect()
pos_hud.topleft = (0,768)

police = 'Polices/ARCADECLASSIC.TTF' # On définit la police d'écriture utilisée par le score et les vagues par cette variable
scorePolice = pygame.font.Font(police,12 ) #On définit le style de police du score et des vagues (type de police d'écriture et taille)
vaguePolice = pygame.font.Font(police,18 )
scoreTexte = scorePolice.render('{}'.format(score),1,(255, 255, 255)) #On crée un objet texte suivant le style de "scorePolice" dont le contenu changera selon la variable Score
vagueTexte = vaguePolice.render('{}'.format(vague),1,(255, 255, 255)) #Idem avec la variable vague

def Blit_hud () : #Fonction affichant chaque élément de l'HUD
    fenetre.blit(HUD, (pos_hud.left,pos_hud.top))
    fenetre.blit(scoreTexte, (pos_hud.left + 50, pos_hud.top + 76))#on affiche l'image non-pas par rapport à la fenètre mais par rapport à la position de l'HUD
    fenetre.blit(vagueTexte, (pos_hud.left + 74, pos_hud.top + 37))
    if vie == 3: #condition permetant d'afficher selon la vie restante du joueur, son état de santé.
        fenetre.blit(imagevie3,(pos_hud))#vie pleine (trois points de vie)
    elif vie == 2 :
        fenetre.blit(imagevie2,(pos_hud))#deux points de vie
    elif vie == 1 :
        fenetre.blit(imagevie,(pos_hud))#un seul point de vie

def score_incrementation (): # fonction augmentant le score du joueur
    global score
    global scoreTexte
    score = score + 1000
    scoreTexte = scorePolice.render('{}'.format(score),1,(255, 255, 255))

def vague_incrementation (): # fonction augmentant la vague actuelle
    global vague
    global vagueTexte
    vague = vague + 1
    vagueTexte = vaguePolice.render('{}'.format(vague),1,(255, 255, 255))

imagevie3 = pygame.image.load("Images/ViePleine.png")
pos_imagevie3 = imagevie3.get_rect()
pos_imagevie3.topleft = (0,(pos_hud.top))#on positionne l'image non-pas par rapport à la fenètre mais par rapport à la position de l'HUD

imagevie2= pygame.image.load("Images/Vie2.png")
pos_imagevie2 = imagevie2.get_rect()
pos_imagevie2.topleft = (0,(pos_hud.top))

imagevie = pygame.image.load("Images/Vie1.png")
pos_imagevie = imagevie.get_rect()
pos_imagevie.topleft = (0,(pos_hud.top))


###########################################################################################################################################################################

""" définition des fonctions qui permettrons de rendre le défilement de l'arrière-plan illimité """

#Ces fonctions sont appellées lorce qu'un clone atteint le haut de l'écran

def boucle_defilement_fond () : #Fonction permettant de boucler le défilement de l'image de fond
    global position
    global positionbis
    positionbis = position #on remplace le clone par le Rect original
    position.topleft = (0,0) #que l'on replace aussitot à sa position d'origine
    positionbis = position.copy() #on recrée un clone
    positionbis.bottomleft = (0,0) #et on le met lui-aussi à sa position d'origine
#on répète la même opération pour chacune des fonctions


def boucle_defilement_etoiles1 () : #Fonction permettant de boucler le défilement d'une des images d'étoiles
    global position_etoiles1
    global position_etoiles1bis
    position_etoiles1bis = position_etoiles1
    position_etoiles1.topleft = (0,0)
    position_etoiles1bis = position_etoiles1.copy()
    position_etoiles1bis.bottomleft = (0,0)

def boucle_defilement_etoiles2 () : #Fonction permettant de boucler le défilement d'une des images d'étoiles
    global position_etoiles2
    global position_etoiles2bis
    position_etoiles2bis = position_etoiles2
    position_etoiles2.topleft = (0,0)
    position_etoiles2bis = position_etoiles2.copy()
    position_etoiles2bis.bottomleft = (0,0)

def boucle_defilement_etoiles3 () : #Fonction permettant de boucler le défilement d'une des images d'étoiles
    global position_etoiles3
    global position_etoiles3bis
    position_etoiles3bis = position_etoiles3
    position_etoiles3.topleft = (0,0)
    position_etoiles3bis = position_etoiles3.copy()
    position_etoiles3bis.bottomleft = (0,0)
        
###########################################################################################################################################################################
""" définition des fonctions affichant chaque élément à l'écran """

def blit_fond() : #fonction affichant chaque éléments du fond
    fenetre.blit(fond, (position))
    fenetre.blit(fond, (positionbis))
    fenetre.blit(etoiles1, (position_etoiles1))
    fenetre.blit(etoiles1, (position_etoiles1bis))
    fenetre.blit(etoiles2, (position_etoiles2))
    fenetre.blit(etoiles2, (position_etoiles2bis))
    fenetre.blit(etoiles3, (position_etoiles3))
    fenetre.blit(etoiles3, (position_etoiles3bis))

def blit_menu() : #fonction affichant chaque éléments des différents menus
    #on affiche chaque élément, même si il n'apparaît pas sur la fenêtre de jeu
    fenetre.blit(bouton_credit, (pos_bouton_credit))
    fenetre.blit(bouton_jeu, (pos_bouton_jeu))
    fenetre.blit(bouton_quitter, (pos_bouton_quitter))
    fenetre.blit(titre, (pos_titre))
    fenetre.blit(credits,(pos_credits))
    fenetre.blit(bouton_rejouer, (pos_bouton_rejouer))
    fenetre.blit(bouton_menu, (pos_bouton_menu))
    fenetre.blit(gameover, (pos_gameover))

def aff_plein_ecran(): #fonction passant le jeu de mode fenêtré à plein-écran
    fenetre = pygame.display.set_mode((768, 768), pygame.FULLSCREEN) #on bascule l'affichage en plein-écran
    global fullscreen
    fullscreen = 1 # et on met la variable fullscreen à 1

def aff_fenetre (): #fonction passant le jeu de mode plein-écran à fenêtré
    global fullscreen
    fullscreen = 0 #on met la variable fullscreen à 0
    fenetre = pygame.display.set_mode((768, 768)) # et on bascule l'affichage en fenêtré

###########################################################################################################################################################################
""" Définition des évenements personnalisés"""

scroll = USEREVENT #on associe la variable scroll à l'id d'évenement : USEREVENT
pygame.time.set_timer(scroll, 2000) # fonction appelle l'évenement d'id "scroll" toute les 2000 ms

scroll2 = USEREVENT+1 #on associe la variable à l'id d'évenement : USEREVENT + 1 car nous ne souhaitons pas le même id que l'évenement précédement défini
pygame.time.set_timer(scroll2, 750)

#on répète la même opération pour chaque évenement personnalisé

scroll3 = USEREVENT+2
pygame.time.set_timer(scroll3, 500)

scroll4 = USEREVENT+3
pygame.time.set_timer(scroll4, 300)

scroll_menu = USEREVENT+4
scroll_menu_credits = USEREVENT+5
scroll_hud = USEREVENT+6
scroll_joueur = USEREVENT + 7

spawn_ennemie = USEREVENT
pygame.time.set_timer(spawn_ennemie, 2000)

###########################################################################################################################################################################

"""Boucle infinie parcourant chaque évennements """

def repetition (delai, interval) : #fonction activant la répétition d'une action lorce qu'une touche reste appuyée
    pygame.key.set_repeat(delai, interval)

repetition(10,10)

jeu = 0
"""la variable jeu va définir sur quelle "fenêtre" nous nous trouvons, ainsi :
 si jeu == 0 : nous sommes sur le menu
 si jeu == 1 : nous sommes sur la fenêtre de jeu
 si jeu == 2 : nous sommes sur la fenêtre des crédits
 si jeu == 3 : nous sommes sur la fenêtre de gameover"""

while True: # on commence une boucle infinie

    for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
        
        if event.type == QUIT: #si on fèrme la fenètre
            pygame.quit()
            sys.exit()

#  Défillement de l'arrière-plan :
        elif event.type == scroll : #défilement de l'image de fond
            position = position.move(0,+1) #on remplace l'objet Rect par son clone mais à des coordonnées différentes, ce qui revient à déplacer le rectangle
            positionbis = positionbis.move(0,+1)

        elif event.type == scroll2 : #défilement d'une des images d'étoiles
            position_etoiles1 = position_etoiles1.move(0,+1)
            position_etoiles1bis = position_etoiles1bis.move(0,+1)

        elif event.type == scroll3 : #défilement d'une des images d'étoiles
            position_etoiles2 = position_etoiles2.move(0,+1)
            position_etoiles2bis = position_etoiles2bis.move(0,+1)

        elif event.type == scroll4 : #défilement d'une des images d'étoiles
            position_etoiles3 = position_etoiles3.move(0,+1)
            position_etoiles3bis = position_etoiles3bis.move(0,+1)

#  Défillement du menu / transition
        elif event.type == scroll_menu : #transition du menu vers la fenêtre de jeu (le menu défile jusqu'à ne plus apparaître à l'écran)
            if jeu == 1: #si on est dans la fenêtre de jeu
                if 0<=pos_titre.top<=800  :
                    pos_bouton_jeu = pos_bouton_jeu.move(0,+2)
                    pos_bouton_credit = pos_bouton_credit.move(0,+2)
                    pos_bouton_quitter = pos_bouton_quitter.move(0,+2)
                    pos_titre = pos_titre.move(0,+2)

        elif event.type == scroll_menu_credits : #transition du menu vers la fenêtre de crédits (le menu défile et les crédits apparaissent)
            if 0<=pos_titre.top<=800  :
                pos_bouton_jeu = pos_bouton_jeu.move(0,+3)
                pos_bouton_credit = pos_bouton_credit.move(0,+3)
                pos_bouton_quitter = pos_bouton_quitter.move(0,+3)
                pos_titre = pos_titre.move(0,+2)
            pos_credits = pos_credits.move(0,+1)

        if event.type == KEYDOWN :
            if event.key == K_F4 and fullscreen == 0: #si on appuis sur F4 et que l'on se trouve en mode fenêtré, le jeu passe en plein-écran
                aff_plein_ecran()
            elif fullscreen == 1 and event.key == K_ESCAPE or event.key == K_F4 : #si on appuis sur echap ou F4 en mode pleine écran, on bascule en mode fenêtré
                aff_fenetre()


#Defilement du HUD et du joueur / transition :
        if event.type == scroll_hud : #apparition du HUD au lancement de la partie
            if 900>=pos_hud.top>=673:
                pos_hud = pos_hud.move(0,-1)

        if event.type == scroll_joueur: #apparition du joueur au lancement de la partie
            if 1076>=pos_joueur.bottom>=692:
                pos_joueur = pos_joueur.move(0,-1)


#Lorsqu'on est sur le menu
        if jeu == 0 : 

##  Actions des boutons sur le menu : Quitter ; Jouer ; Aller aux crédits
            if event.type == MOUSEBUTTONDOWN: #lorsque la touche est enfoncée

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


            elif event.type == MOUSEBUTTONUP: #lorsqu'on relache la touche

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
                    pygame.time.set_timer(scroll_menu_credits, 50) #transition du menu vers les crédits
                    jeu = 2


#lorsque l'on est sur la fenêtre de jeu
        elif jeu == 1 : 

            pygame.time.set_timer(scroll_menu, 10) #transition du menu vers la fenêtre de jeu

            if event.type == spawn_ennemie and pos_hud.top <= 674: #apparition aléatoire des ennemis
                pos = randint(0, 735)
                listEnnemie.append(Ennemie(1,(pos,0)))

            if pos_titre.top == 700 : #lorsque le menu sort de la fenêtre
                pygame.mixer.music.fadeout(300)
                pygame.mixer.Sound.play(son_spawn)

                pos_joueur.bottomleft = (370,692+96) #on place le sprite du joueur juste sous la fenêtre
                pygame.time.set_timer(scroll_hud, 40) #apparition du HUD sous la fenêtre
                pygame.time.set_timer (scroll_joueur, 80) #apparition du joueur sous la fenêtre

                pygame.mixer.music.load("Musiques/loop_jeu.ogg")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)
    
            #vagues prédéterminées
            if score == 10000 : #pour toute tranche de 10000 points, la vague augmente
                global vague
                vague = 2 #on augmente la variable vague 
                vagueTexte = vaguePolice.render('{}'.format(vague),1,(255, 255, 255)) #et on actualise le texte 

            elif score == 20000 :
                global vague
                vague = 3
                vagueTexte = vaguePolice.render('{}'.format(vague),1,(255, 255, 255))

            elif score == 30000 :
                global vague
                vague = 4
                vagueTexte = vaguePolice.render('{}'.format(vague),1,(255, 255, 255))

            elif score == 40000 :
                global vague
                vague = 5
                vagueTexte = vaguePolice.render('{}'.format(vague),1,(255, 255, 255))

            elif score == 50000 :
                global vague
                vague = "BOSS" #note : aucun boss n'a été implémenté, c'est un futur ajout au jeu.
                vagueTexte = vaguePolice.render('{}'.format(vague),1,(255, 255, 255))

#Actions du joueur en jeu
            if event.type == KEYDOWN : #lorce que l'on appuis sur la touche

                if event.key == K_LEFT and pos_joueur.left >= 0: #si le joueur ne sort pas de la fenêtre et que l'on appuis sur la fleche gauche, le sprite se déplace
                    pos_joueur = pos_joueur.move(-4,0)

                if event.key == K_RIGHT and pos_joueur.right <= 768: #si l'on appuis sur la fleche droite, le sprite se déplace
                    pos_joueur = pos_joueur.move(4,0)

                if event.key == K_SPACE : #lorce qu'on appuis sur la barre d'espace, le joueur tire
                    repetition(0,0) #on désactive la répétition des actions 
                    listTir.append(TirsJoueur(1,(pos_joueur.left + 10,pos_joueur.top - 20))) #on ajoute à la liste listTir un objet TirsJoueur qui a por position celle du sprite du joueur
                    pygame.mixer.Sound.play(son_tirjoueur)

            for ennemie in listEnnemie : # l'action se répète pour chaque éléments de la liste listEnnemie
                if event.type == scroll2 and pos_hud.top <= 674: #à interval régulier et lorce que la partie à commencée, les ennemis tirent
                    listTirEnnemie.append(TirsEnnemie(1,(ennemie.rect.left + 17,ennemie.rect.bottom - 25))) #on ajoute à la liste TirsEnnemie un objet TirsEnnemie qui a pour position celle du sprite de l'ennemi
                    pygame.mixer.Sound.play(son_tirennemi)

            if event.type == KEYUP : #lorsque l'on relache la touche

                if event.key == K_SPACE : #lorsque l'on relache la touche de tir
                    repetition(10,10) #on réactive la répétition des actions

            if vie == 0: #lorce que le joueur perd toutes ses vies
                jeu = 3 #on passe de la fenêtre de jeu à la fenêtre de gameover
                pos_bouton_rejouer.topleft = (231,260) #on place les éléments de la fenêtre de gameover 
                pos_bouton_menu.topleft = (231,380)
                pos_bouton_quitter.topleft = (406,480)
                pos_gameover.topleft = (0,0)
                pos_hud.bottomleft = (0,0) #et on retire le joueur et le HUD de la fenêtre
                pos_joueur.bottomleft = (0,0)
                pygame.mixer.music.stop()


#lorsque l'on est sur la fenêtre de gameover
        if jeu == 3:
            ##  Actions des boutons sur le menu : Quitter ; Jouer ; Aller aux crédits
            if event.type == MOUSEBUTTONDOWN: #lorsque la touche est enfoncée

                #bouton quitter
                    if event.type == MOUSEBUTTONDOWN and event.button == 1 and pos_bouton_quitter.top < event.pos[1] < pos_bouton_quitter.bottom and pos_bouton_quitter.left < event.pos[0] < pos_bouton_quitter.right:
                        pygame.mixer.Sound.play(son_quitter)
                        pygame.time.wait(500)

                #bouton rejouer
                    elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pos_bouton_rejouer.top < event.pos[1] < pos_bouton_rejouer.bottom and pos_bouton_rejouer.left < event.pos [0] < pos_bouton_rejouer.right:
                        pygame.mixer.Sound.play(son_bouton)

                #bouton menu
                    elif event.type == MOUSEBUTTONDOWN and event.button == 1 and pos_bouton_menu.top < event.pos[1] < pos_bouton_menu.bottom and pos_bouton_menu.left < event.pos [0] < pos_bouton_menu.right:
                        pygame.mixer.Sound.play(son_bouton)


            elif event.type == MOUSEBUTTONUP: #lorsque l'on relache la touche

                #bouton rejouer
                    if event.type == MOUSEBUTTONUP and event.button == 1 and pos_bouton_rejouer.top < event.pos[1] < pos_bouton_rejouer.bottom and pos_bouton_rejouer.left < event.pos [0] < pos_bouton_rejouer.right:
                        vie = 3 #on remet chaque image à sa place d'origine et chaque variables à leurs valeurs d'origine (remise à zero)
                        pos_gameover.bottomleft = (0,0)
                        pos_bouton_rejouer.bottomleft = (0,0)
                        pos_bouton_menu.bottomleft = (0,0)
                        pos_bouton_quitter.bottomleft = (0,0)
                        pos_hud.topleft = (0,768)
                        pos_joueur.bottomleft = (370,692+96)
                        pygame.mixer.Sound.play(son_spawn)
                        score = 0
                        vague = 1
                        listEnnemie = []
                        listTir = []
                        listTirEnnemie = []
                        jeu = 1 #et le jeu lance la partie
                        pygame.mixer.music.load("Musiques/loop_jeu.ogg")
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.2)

                #bouton quitter
                    if event.type == MOUSEBUTTONUP and event.button == 1 and pos_bouton_quitter.top < event.pos[1] < pos_bouton_quitter.bottom and pos_bouton_quitter.left < event.pos[0] < pos_bouton_quitter.right:
                        pygame.quit()
                        sys.exit()

                #bouton menu
                    elif event.type == MOUSEBUTTONUP and event.button == 1 and pos_bouton_menu.top < event.pos[1] < pos_bouton_menu.bottom and pos_bouton_menu.left < event.pos [0] < pos_bouton_menu.right:
                        vie =3 #on remet chaque image à sa place d'origine et chaque variables à leurs valeurs d'origine (remise à zero)
                        jeu = 0 #et le jeu se remet au menu
                        pos_bouton_credit.topleft = (231,380)
                        pos_bouton_jeu.topleft =  (231,260)
                        pos_titre.topleft = (0,0)
                        pos_gameover.bottomleft = (0,0)
                        pos_bouton_rejouer.bottomleft = (0,0)
                        pos_bouton_menu.bottomleft = (0,0)
                        pos_hud.topleft = (0,900)
                        pos_joueur.bottomleft = (0,0)
                        score = 0
                        vague = 1
                        listEnnemie = []
                        listTir = []
                        listTirEnnemie = []

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

#on sort de la boucle "for event in pygame.event.get()"

    if jeu == 2: #"effet spéciaux" à l'apparition des noms dans la fenêtre des crédits 
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

# Mise à jour de l'affichage : (la fonction blit() "colle" les éléments du jeu les un aux dessus des autres et ce à chaque fois que la fenêtre se rafraîchit)

    blit_fond() #affichage du fond
    blit_menu() #affichage des éléments de chaque menu

#ceci est un compteur qui permet de connaître le nombre d'actions effectuées en moyenne par seconde, nous l'utilisons comme outil d'optimisation
    end_t = time()
    time_taken = end_t - start_t
    start_t = end_t
    frame_times.append(time_taken)
    frame_times = frame_times[-20:]
    fps = len(frame_times) // sum(frame_times)
    fpsPolice = pygame.font.Font('Polices/calibril.ttf',24 )
    fpsTexte = fpsPolice.render('{}'.format(fps),1,(255, 255, 255))
    fenetre.blit(fpsTexte,(0,0))

    if jeu == 1 : #lorce que l'on est sur la fenêtre de jeu
        Blit_hud() #affichage du HUD
        fenetre.blit(Joueur,(pos_joueur)) #affichage du joueur

#l'action se répète pour chaque éléments de la liste listTir
    for tir in listTir: 
        tir.afficher() #on affiche l'objet ( fonction blit() )
        tir.move() #on déplace l'objet

#l'action se répète pour chaque éléments de la liste listTirEnnemie
    for tir in listTirEnnemie: 
        tir.afficher() #on affiche l'objet
        tir.move() #on déplace l'objet
        
        collision3 = [pos_joueur] #on crée une liste contenant l'objet Rect du sprite du joueur

        if tir.rect.bottom > 768 :
            tir.delete() #on supprime l'objet

        elif tir.rect.collidelist(collision3) != -1 : #si un tir entre en collision avec un objet de la liste collision3 (le joueur)
            pygame.mixer.Sound.play(son_joueurtoucher)
            if vie == 3 : #on réduit la vie de 1
                vie = 2

            elif vie == 2 :
                vie = 1

            elif vie == 1 :
                vie =0
            tir.delete() # et on supprime l'objet

#l'action se répète pour chaque éléments de la liste listEnnemie
    for ennemie in listEnnemie: 
        ennemie.afficher() #on appelle la methode "afficher()"
        ennemie.move() #on appelle la methode "move()"
        collision4 = [pos_joueur] #on crée une liste contenant l'objet Rect du sprite du joueur

        if ennemie.rect.bottom > 768 : #lorsqu'un ennemi touche le bas de la fenêtre
            ennemie.delete() #on supprime l'objet

        if ennemie.rect.collidelist(collision4) != -1 : #si un ennemi entre en collision avec le joueur
            pygame.mixer.Sound.play(son_joueurtoucher)
            ennemie.delete() #on supprime l'objet

#l'action se répète pour chaque éléments de la liste listEnnemie ET de la liste listTir
    for tir in listTir:
        for ennemie in listEnnemie : 

            collision = [tir.rect] #on crée deux liste contenant les objets Rect des tirs du joueur et des ennemis
            collision2 = [ennemie.rect]

            if tir.rect.top < 0 : #lorsqu'un tir atteint le haut de la fenêtre
                tir.delete() #on supprime l'objet

            elif tir.rect.collidelist(collision2) != -1: #lorsqu'un tir entre en collision avec un ennemi
                pygame.mixer.Sound.play(son_ennemitoucher)
                tir.delete() #on supprime le tir
                score_incrementation() #le score augmente

            if ennemie.rect.bottom > 768 : #lorsqu'un ennemi touche le bas de la fenêtre
                ennemie.delete() #on supprime l'objet

            elif ennemie.rect.collidelist(collision) != -1: #lorsqu'un ennemi entre en collision avec un tir
                ennemie.delete() #on supprime l'ennemi


#  Remplacement de la souris :

    if jeu == 0 or jeu == 3: #lorsque l'on est sur le menu ou sur l'écran de gameover
        x_curseur , y_curseur = pygame.mouse.get_pos() #on associe aux variables (x_curseur,y_curseur) les coordonnées de la souris
        fenetre.blit(souris,(x_curseur,y_curseur)) #on affiche la nouvelle apparence aux coordonnées de la souris

#  Appels aux fonctions pour boucler le défilement de l'arrière-plan lorce que nécessaire
    if positionbis.bottom == 1152 :
        boucle_defilement_fond()
    elif position_etoiles1bis.bottom == 800 :
        boucle_defilement_etoiles1()
    elif position_etoiles2bis.bottom == 1300 :
        boucle_defilement_etoiles2()
    elif position_etoiles3bis.bottom == 1800 :
        boucle_defilement_etoiles3()

    pygame.display.flip() #mise à jour de l'affichage / raffraichissement.
    #la boucle infinie se termine ici et recommence et-ce jusqu'à ce que la fenêtre soit fermée.