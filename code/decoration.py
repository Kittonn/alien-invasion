import pygame
from setting import screen_height, screen_width, tile_size
from tile import StaticTile


class Background(pygame.sprite.Sprite):
  def __init__(self) -> None:
    super().__init__()
    self.image = pygame.image.load(
        "graphics/background/Background.png").convert_alpha()
    self.rect = self.image.get_rect(
        center=(screen_width / 2, screen_height / 2))


class Water:
  def __init__(self) -> None:
    self.water_top = pygame.image.load("graphics/tiles/water.png")
    self.water_center = pygame.image.load("graphics/tiles/center_water.png")

    tile_x_amount = int(screen_width / self.water_center.get_width()) + 1

    self.water_sprites = pygame.sprite.Group()

    for i in range(1, 3):
      for j in range(tile_x_amount):
        x = j * tile_size
        y = screen_height - (tile_size * i)
        if i == 1:
          sprite = StaticTile(tile_size, x, y, pygame.image.load(
              "graphics/tiles/center_water.png").convert_alpha())
        elif i == 2:
          sprite = StaticTile(tile_size, x, y, pygame.image.load(
              "graphics/tiles/water.png").convert_alpha())
        self.water_sprites.add(sprite)

  def draw(self, surface):
    self.water_sprites.draw(surface)
