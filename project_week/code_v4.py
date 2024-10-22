import pygame
import sys
from pygame.locals import*

pygame.init()

clock = pygame.time.Clock()
pygame.display.set_caption("This is not a GAME")
ecran = pygame.display.set_mode((900, 400))
background = pygame.image.load('fond.jpg')
bg = pygame.transform.scale(background, (900, 400))
continuer = True


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
        self.rect = self.image.get_rect(center=(x + 30, y + 20))
        self.velocity = 5

    def update(self):
        self.rect.x += self.velocity
        if self.rect.x > 900:
            self.kill()

class Player(pygame.sprite.Sprite):
    player = pygame.image.load('tank_sprite.jpg')
    player.set_colorkey((255, 255, 255))
    pl = pygame.transform.scale(player, (80, 60))

    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__()
        self.position = [x, y]
        self.velocity = [velocity_x, velocity_y]
        self.image = Player.pl
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] + self.rect.width > 900:
            self.position[0] = 900 - self.rect.width
        elif self.position[1] + self.rect.height < 320:
            self.position[1] = 320 - self.rect.height
        elif self.position[1] + self.rect.height > 400:
            self.position[1] = 400 - self.rect.height
        
        self.rect.topleft = self.position

    def draw(self, surface):
       surface.blit(self.image, self.rect.topleft)

    def move_left(self):
        self.velocity[0] = -1
        self.velocity[1] = 0
    def move_right(self):
        self.velocity[0] = 1
        self.velocity[1] = 0
    def move_up(self):
        self.velocity[1] = -1
        self.velocity[0] = 0
    def move_down(self):
        self.velocity[1] = 1.
        self.velocity[0] = 0
    def stop(self):
        self.velocity[0] = 0
        self.velocity[1] = 0
    
    def tirer(self, projectiles):
        projectile = Projectiles(self.rect.centerx, self.rect.top)
        projectiles.add(projectile)

player = Player(0, 320, 0, 0)
projectiles = pygame.sprite.Group()
keys_pressed = set()

while continuer:
    clock.tick(60)
    ecran.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            continuer = False

        elif event.type == pygame.QUIT:
            continuer = False

        if event.type == pygame.KEYDOWN:
            keys_pressed.add(event.key)
            if event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_DOWN:
                player.move_down()
            elif event.key == pygame.K_UP:
                player.move_up()
            elif event.key == pygame.K_SPACE:
                player.tirer(projectiles)
        if event.type == pygame.KEYUP:
            keys_pressed.discard(event.key)
            if not keys_pressed.intersection({pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP}):
                player.stop()

    player.update()
    projectiles.update()
    player.draw(ecran)
    projectiles.draw(ecran)
    pygame.display.update()

pygame.quit()

