import pygame
from tile import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
  def __init__(self, size, x, y,id) -> None:
    super().__init__(size, x, y, f"./assets/enemy/run/{id}")
    self.rect.y += size - self.image.get_size()[1]
    self.speed = randint(3, 5)

  def move(self) -> None:
    self.rect.x += self.speed

  def reverse_image(self) -> None:
    if self.speed > 0:
      self.image = pygame.transform.flip(self.image, True, False)

  def reverse(self) -> None:
    self.speed *= -1

  def update(self, shift) -> None:
    self.rect.x += shift
    self.animate()
    self.move()
    self.reverse_image()
