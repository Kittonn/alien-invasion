import pygame
from support import get_font_surf
from setting import screen_width


class HowToPlay:
  def __init__(self, surface,current_mode, create_main_menu) -> None:
    self.display_surface = surface
    self.current_mode = current_mode
    self.create_main_menu = create_main_menu
    
  def input(self) -> None:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
      self.create_main_menu(self.current_mode)

  def run(self) -> None:
    self.input()
    
    background = pygame.image.load("graphics/Background.png")
    self.display_surface.blit(background, (0, 0))
    
    howtoplay_text = get_font_surf(
        'evil', 60, "How To Play", 'black')
    howtoplay_rect = howtoplay_text.get_rect(
        center=(screen_width / 2, 100))
    self.display_surface.blit(howtoplay_text, howtoplay_rect)