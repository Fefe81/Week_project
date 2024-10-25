import pygame
import sys
from pygame.locals import*
from random import randint
pygame.init() # initialisation de pygame

clock = pygame.time.Clock() 
pygame.display.set_caption("This is not a GAME")
ecran = pygame.display.set_mode((900, 400))     
background = pygame.image.load('fond.jpg')
bg = pygame.transform.scale(background, (900, 400)) # Elements qui gères la taille de la page et le fond
programIcon = pygame.image.load('icon.jpg')
pygame.display.set_icon(programIcon)
continuer = True
font = pygame.font.Font(None, 36)
score = 0
vie = 3
spawn = 1

class Projectiles(pygame.sprite.Sprite): # Classe qui gère les projectiles
    def __init__(self, x, y): # Fonction qui initialise la classe Projectiles
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
        self.rect = self.image.get_rect(center=(x + 30, y + 20))
        self.velocity = 7

    def update(self): # Fonction qui update les projectiles et qui les supprimes si ils sortent de l'écran
        self.rect.x += self.velocity
        if self.rect.x > 900:
            self.kill()

class mega_Projectiles(pygame.sprite.Sprite): # Classe qui gère les mégas projectiles
    def __init__(self, x, y): # Fonction qui initialise la classe mega_Projectiles
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 0), (10, 10), 10)
        self.rect = self.image.get_rect(center=(x + 30, y + 20))
        self.velocity = 7

    def update(self): # Fonction qui update les mégas projectiles et qui les supprimes si ils sortent de l'écran
        self.rect.x += self.velocity
        if self.rect.x > 900:
            self.kill()
        
class Ennemis(pygame.sprite.Sprite): # Classe qui gère les ennemies
    def __init__(self, x, y): # Fonction qui initialise la classe Ennemies 
        super().__init__()        
        self.velocity = player.mob_velocity
        self.image = pygame.image.load('zombie.jpg')
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.image.set_colorkey((253, 253, 253))
        self.rect = self.image.get_rect(center=(x , y))

    def update(self): # Fonction qui update les ennemies et qui les supprimes si ils sortent de l'écran
        self.rect.x += self.velocity
        if self.rect.x  < 0:
            self.kill()

class Base(pygame.sprite.Sprite): # Classe qui gère la base
    def __init__(self, x, y): # Fonction qui initialise la classe Base
        super().__init__()
        self.image = pygame.image.load('tower.png')
        self.image = pygame.transform.scale(self.image, (70, 130))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))

class HP(pygame.sprite.Sprite): # Classe qui gère les HP
    def __init__(self, x, y): # Fonction qui initialise la classe HP
        super().__init__()
        self.image = pygame.image.load('coeur.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.image.set_colorkey((253, 253, 253))
        self.rect = self.image.get_rect(center=(x, y))

class powerUp(pygame.sprite.Sprite): # Classe qui gère les powerups
    def __init__(self, x, y): # Fonction qui initialise la classe powerUP
        super().__init__()
        self.image = pygame.image.load('powerup.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))

class powerLife(pygame.sprite.Sprite): # Classe qui gère les gain de vie
    def __init__(self, x, y): # Fonction qui initialise la classe powerLife
        super().__init__()
        self.image = pygame.image.load('coeur.png')
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect(center=(x, y))

class Player(pygame.sprite.Sprite): # Classe qui gère le joueur et l'ensemble du jeu
    player = pygame.image.load('tank_sprite.jpg')
    player.set_colorkey((255, 255, 255))
    pl = pygame.transform.scale(player, (80, 60))
    power = 0
    cadence = 2000

    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.position = [x, y] # Initialise la position du joueur avec les coordonnées x et y
        self.velocity = [velocity_x, velocity_y] # Initialise la vélocité du joueur avec velocity_x et velocity_y 
        self.image = Player.pl # Charge l'image du joueur
        self.rect = self.image.get_rect()  # Obtient le rectangle englobant de l'image pour la gestion des collisions
        self.rect.topleft = self.position # Place le coin supérieur gauche du rectangle à la position initiale
        self.last_shot_time = 0
        self.last_spawn_time = 0
        self.last_spawn1_time = 0
        self.last_spawn2_time = 0
        self.mob_velocity = -4.000

    def update(self):
        # Met à jour la position en ajoutant la vélocité actuelle
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        if self.position[0] < 0: # Vérifie si la position x est en dehors des limites à gauche
            self.position[0] = 0
        elif self.position[0] + self.rect.width > 900: # Vérifie si la position x est en dehors des limites à droite
            self.position[0] = 900 - self.rect.width
        elif self.position[1] + self.rect.height < 320: # Vérifie si la position y est en dehors des limites en haut
            self.position[1] = 320 - self.rect.height
        elif self.position[1] + self.rect.height > 410: # Vérifie si la position y est en dehors des limites en bas
            self.position[1] = 410 - self.rect.height
        
        self.rect.topleft = self.position # Met à jour la position du rectangle englobant

    def draw(self, surface): # Dessine l'image du joueur sur la surface donnée à la position actuelle du rectangle englobant
       surface.blit(self.image, self.rect.topleft)

    def move_left(self): # Déplace le joueur vers la gauche en définissant la vélocité x à -1 et y à 0
        self.velocity[0] = -1
        self.velocity[1] = 0
    def move_right(self): # Déplace le joueur vers la droite en définissant la vélocité x à 1 et y à 0
        self.velocity[0] = 1
        self.velocity[1] = 0
    def move_up(self): # Déplace le joueur vers le haut en définissant la vélocité y à -1 et x à 0
        self.velocity[1] = -1
        self.velocity[0] = 0
    def move_down(self): # Déplace le joueur vers le bas en définissant la vélocité y à 1 et x à 0
        self.velocity[1] = 1
        self.velocity[0] = 0
    def stop(self): # Arrête le mouvement du joueur en définissant les vélocités x et y à 0
        self.velocity[0] = 0
        self.velocity[1] = 0
    
    def tirer(self, projectiles):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 500:
            projectile = Projectiles(self.rect.centerx, self.rect.top) # Crée un nouveau projectile à la position actuelle du joueur
            projectiles.add(projectile)
            self.last_shot_time = current_time

    def mega_tirer(self, mega_projectiles):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 500:
            mega_projectile = mega_Projectiles(self.rect.centerx, self.rect.top) # Crée un nouveau méga projectile à la position actuelle du joueur
            mega_projectiles.add(mega_projectile)
            self.last_shot_time = current_time

    def spawn_mob(self, ennemies):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > player.cadence:
            ennemie = Ennemis(900, randint(290, 390)) # Crée un nouvel ennemi à une position aléatoire en y
            ennemies.add(ennemie) 
            self.last_spawn_time = current_time
            player.mob_velocity -= 0.01
            if player.cadence > 0:
                player.cadence -= 10 # Augmente la cadence de spawn des mobs au fur est à mesure pour augmenter la difficulté
    def spawn_base(self, bases):
        base = Base(self.rect.centerx - 20, self.rect.top + 15) # Crée une base
        base.add(bases)

    def vie(self, vies):
        vie = HP(self.rect.centerx, self.rect.top) # Gère l'affichage de vie 
        vie.add(vies)

    def amelioration(self, powerups):
        current_time = pygame.time.get_ticks()
        if len(powerups) == 0 and current_time - self.last_spawn1_time >= 5000:
            powerup = powerUp(randint(400, 700), randint(300, 390))
            powerups.add(powerup)
            self.last_spawn1_time = current_time
            player.power = 0

    def up_vie(self, up_vies):
        current_time = pygame.time.get_ticks()
        if len(up_vies) == 0 and current_time - self.last_spawn2_time >= 12000 and vie < 3:
            up_vie = powerLife(800, randint(300, 390))
            up_vies.add(up_vie)
            self.last_spawn2_time = current_time
    
def afficher_game_over(ecran, score): #Bloque le jeu affiche l'ecran de fin et se ferme après 10sec
    ecran.fill((0, 0, 0)) 
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    ecran.blit(game_over_text, (900 / 3, 300 / 2))
    ecran.blit(score_text, (1000 / 3, 250))
    pygame.display.update()
    pygame.time.wait(10000)
    pygame.quit()
    sys.exit()

# Création de groupes de sprites pour différents types d'objets
player = Player(0, 320, 0, 0)
projectiles = pygame.sprite.Group()
mega_projectiles = pygame.sprite.Group()
ennemies = pygame.sprite.Group()
bases = pygame.sprite.Group()
vies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
up_vies = pygame.sprite.Group()
keys_pressed = set()

for i in range(vie):
    coeur = HP(100 + i * 30, 30) # Ajout des coeurs au groupe vies en fonction du nombre de vies initial
    vies.add(coeur)

def initialiser_vies(vie, vies):
    vies.empty()
    for i in range(vie):
        coeur = HP(920 - (i + 1) * 60, 30)
        vies.add(coeur)

initialiser_vies(vie, vies)

while continuer: # Boucle principale du jeu
    clock.tick(60)
    ecran.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x: # Ferme le jeu quand on appuie sur la croix ou sur la touche x en mettant la variable continuer à False
            continuer = False

        elif event.type == pygame.QUIT:
            continuer = False

        if event.type == pygame.KEYDOWN:
            keys_pressed.add(event.key)
            if event.key == pygame.K_RIGHT:
                player.move_right()
            if event.key == pygame.K_LEFT:
                player.move_left()              # Gère touts les déplacements du joueurs en fonction de quelle flèche est pressée
            if event.key == pygame.K_DOWN:
                player.move_down()
            if event.key == pygame.K_UP:
                player.move_up()
            elif event.key == pygame.K_SPACE:
                if player.power == 1:
                    player.mega_tirer(mega_projectiles) # Gère les tirs du joueur(touche espace)
                else:
                    player.tirer(projectiles)
        if event.type == pygame.KEYUP:
            keys_pressed.discard(event.key) # Retire la touche relâchée de l'ensemble des touches pressées
            if not keys_pressed.intersection({pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP}):
                player.stop() # Arrête le mouvement du joueur si aucune touche de direction n'est pressée

    player.spawn_mob(ennemies)
    player.amelioration(powerups)
    player.up_vie(up_vies)
    if spawn == 1:
        player.spawn_base(bases)
        spawn += 1

    player.update()
    projectiles.update()
    mega_projectiles.update()
    ennemies.update()
    bases.update()
    powerups.update()
    up_vies.update()

    for projectile in projectiles:
        hits = pygame.sprite.spritecollide(projectile, ennemies, True)
        if hits:
            score += 1
            projectile.kill()

    for mega_projectile in mega_projectiles:
        hits = pygame.sprite.spritecollide(mega_projectile, ennemies, True)
        if hits:
            score +=1
            mega_projectile.kill()

    for powerup in powerups:
        hits = pygame.sprite.spritecollide(player, powerups, True)       
        if hits:
            player.power = 1
            powerup.kill()
            player.last_spawn1_time = pygame.time.get_ticks()
            
    for up_vie in up_vies:
        hits = pygame.sprite.spritecollide(player, up_vies, True)
        if hits:
            vie += 1
            up_vie.kill()
            initialiser_vies(vie, vies)
            player.last_spawn2_time = pygame.time.get_ticks()

    if vie > 0:
        for base in bases:
            if pygame.sprite.spritecollideany(base, ennemies):
                vie -= 1
                vies.empty()
                for i in range(vie):
                    coeur = HP(920 - (i + 1) * 60, 30)
                    vies.add(coeur)
                for ennemi in ennemies:
                    if pygame.sprite.collide_rect(base, ennemi):
                        ennemi.kill()

    if vie <= 0:
        afficher_game_over(ecran, score)

    player.draw(ecran)
    projectiles.draw(ecran)
    mega_projectiles.draw(ecran)
    ennemies.draw(ecran)
    bases.draw(ecran)
    vies.draw(ecran)
    powerups.draw(ecran)
    up_vies.draw(ecran)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    ecran.blit(score_text, (10, 10))


    pygame.display.update()

pygame.quit()

