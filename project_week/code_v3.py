import pygame
import sys
from pygame.locals import*

pygame.init()

clock = pygame.time.Clock()
pygame.display.set_caption("This is not a GAME")
ecran = pygame.display.set_mode((800, 400))
background = pygame.image.load('fond.jpg')
bg = pygame.transform.scale(background, (800, 400))
continuer = True

class Player(pygame.sprite.Sprite):
    player = pygame.image.load('tank_sprite.jpg')
    player.set_colorkey((213, 213, 213))
    pl = pygame.transform.scale(player, (60, 60))

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
        self.rect.topleft = self.position

    def draw(self, surface):
       surface.blit(self.image, self.rect.topleft)

    def move_left(self):
        self.velocity[0] = -1

    def move_right(self):
        self.velocity[0] = 1

    def move_up(self):
        self.velocity[1] = -1

    def move_down(self):
        self.velocity[1] = 1.

    def stop(self):
        self.velocity[0] = 0
        self.velocity[1] = 0

player = Player(320, 240, 0, 0)

while continuer:
    clock.tick(60)
    ecran.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            continuer = False

        elif event.type == pygame.QUIT:
            continuer = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_DOWN:
                player.move_down()
            elif event.key == pygame.K_UP:
                player.move_up()
        if event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or 
                                           event.key == pygame.K_DOWN or event.key == pygame.K_UP):
            player.stop()

    player.update()
    player.draw(ecran)
    pygame.display.update()

pygame.quit()

