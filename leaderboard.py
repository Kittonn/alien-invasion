from support import import_score_leaderboard
import pygame
from setting import screen_width
from support import get_font_surf


class Leaderboard:
  def __init__(self, surface, current_mode, create_main_menu) -> None:
    self.display_surface = surface
    self.data = import_score_leaderboard("./score.json")

    self.current_mode = current_mode

    self.create_main_menu = create_main_menu

  def input(self) -> None:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
      self.create_main_menu(self.current_mode)

  def run(self) -> None:
    background = pygame.image.load("./assets/Background.png")
    self.display_surface.blit(background, (0, 0))

    self.input()

    leaderboard_text = get_font_surf(
        'evil', 60, "Leaderboard", 'black')
    leaderboard_rect = leaderboard_text.get_rect(
        center=(screen_width / 2, 100))
    self.display_surface.blit(leaderboard_text, leaderboard_rect)

    for index, data in enumerate(self.data):
      name_text = get_font_surf('evil', 32, f"{data['name']}", 'black')
      name_text_rect = name_text.get_rect(
          midleft=(screen_width / 2 - 300, 200 + (index * 70)))
      self.display_surface.blit(name_text, name_text_rect)

      score_text = get_font_surf('evil', 32, f"{data['score']}", 'black')
      score_text_rect = score_text.get_rect(
          midleft=(screen_width / 2 + 150, 200 + (index * 70)))
      self.display_surface.blit(score_text, score_text_rect)
