import pygame
import sys
from pygame.locals import*

pygame.init()

clock = pygame.time.Clock()
pygame.display.set_caption("This is not a GAME")
ecran = pygame.display.set_mode((600, 300))
background = pygame.image.load('fond.jpg')
bg = pygame.transform.scale(background, (600, 300))
continuer = True

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, velocity_x, velocity_y):
    super().__init__()
    self.position = (x, y)
    self.velocity = (velocity_x, velocity_x)

  def update(self):
    self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

  def draw(self, surface):
    pygame.draw.circle(surface, (255, 0, 0), self.position, 10)
  def move_left(self):
    self.velocity[0] = -1
    3
  def move_right(self):
      self.velocity[0] = 1

player = Player(320, 240, 0, 0)

while continuer:
  clock.tick(60)
  ecran.blit(bg,(0, 0))

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
      continuer = False

    elif event.type == pygame.QUIT:
      continuer = False

    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
        Player.move_right
    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
        Player.move_left

  player.update()
  player.draw(ecran)
  pygame.display.update()

player = Player(320, 240, 0, 0)

pygame.quit()

