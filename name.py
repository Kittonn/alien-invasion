import pygame
from support import get_font_surf
from setting import screen_height, screen_width


class Name:
  def __init__(self, surface) -> None:
    self.display_surface = surface

    self.name_surf = get_font_surf(
        'chakra_petch', 18, '65010077 - Kittipod Lambangchang', 'black')
    self.name_rect = self.name_surf.get_rect(topleft=(
        screen_width - self.name_surf.get_width() - 10, screen_height - self.name_surf.get_height() - 10))

  def draw(self) -> None:
    self.display_surface.blit(self.name_surf, self.name_rect)
