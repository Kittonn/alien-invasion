import pygame
from support import get_font_surf, write_score_leaderboard
from setting import screen_width


class GameOver:
  def __init__(self, surface, score, change_status, create_main_menu) -> None:
    self.display_surface = surface
    self.score = score
    self.change_status = change_status
    self.create_main_menu = create_main_menu

  def input(self) -> None:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
      self.change_status('overworld')

    elif keys[pygame.K_q]:
      self.create_main_menu(0)
      self.change_status('overworld')

  def run(self, name) -> None:
    self.name = name
    background = pygame.image.load("graphics/Background.png")
    self.display_surface.blit(background, (0, 0))

    self.input()

    gameover_text = get_font_surf(
        'evil', 60, "Gameover", 'black')
    gameover_text_rect = gameover_text.get_rect(
        center=(screen_width / 2, 100))

    score_text = get_font_surf('evil', 180, str(self.score), 'black')
    name_text = get_font_surf('evil', 50, self.name, 'black')

    score_text_rect = score_text.get_rect(center=(screen_width / 2, 280))
    name_text_rect = name_text.get_rect(center=(screen_width / 2, 440))
    self.display_surface.blit(score_text, score_text_rect)
    self.display_surface.blit(name_text, name_text_rect)
    self.display_surface.blit(gameover_text, gameover_text_rect)

    press_r_text = get_font_surf('evil', 30, "Press R to restart", 'black')
    press_q_text = get_font_surf('evil', 30, "Press Q to quit", 'black')
    press_r_text_rect = press_r_text.get_rect(center=(screen_width / 2 - 300, 540))
    press_q_text_rect = press_q_text.get_rect(center=(screen_width / 2 + 300, 540))
    self.display_surface.blit(press_r_text, press_r_text_rect)
    self.display_surface.blit(press_q_text, press_q_text_rect)


class Victory:
  def __init__(self, surface, score, change_status, create_main_menu) -> None:
    self.display_surface = surface
    self.score = score
    self.change_status = change_status
    self.create_main_menu = create_main_menu

  def input(self) -> None:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
      write_score_leaderboard(
          {"name": self.name, "score": self.score}, "data/score.json")
      self.change_status('overworld')
    elif keys[pygame.K_q]:
      write_score_leaderboard(
          {"name": self.name, "score": self.score}, "data/score.json")
      self.create_main_menu(0)
      self.change_status('overworld')

  def run(self, name):
    self.input()
    self.name = name
    background = pygame.image.load("graphics/Background.png")
    self.display_surface.blit(background, (0, 0))

    victory_text = get_font_surf(
        'evil', 60, "Victory", 'black')
    victory_text_rect = victory_text.get_rect(
        center=(screen_width / 2, 100))

    score_text = get_font_surf('evil', 180, str(self.score), 'black')
    name_text = get_font_surf('evil', 50, self.name, 'black')

    score_text_rect = score_text.get_rect(center=(screen_width / 2, 280))
    name_text_rect = name_text.get_rect(center=(screen_width / 2, 440))
    self.display_surface.blit(score_text, score_text_rect)
    self.display_surface.blit(name_text, name_text_rect)

    self.display_surface.blit(victory_text, victory_text_rect)
    
    press_r_text = get_font_surf('evil', 30, "Press R to restart", 'black')
    press_q_text = get_font_surf('evil', 30, "Press Q to quit", 'black')
    press_r_text_rect = press_r_text.get_rect(center=(screen_width / 2 - 300, 540))
    press_q_text_rect = press_q_text.get_rect(center=(screen_width / 2 + 300, 540))
    self.display_surface.blit(press_r_text, press_r_text_rect)
    self.display_surface.blit(press_q_text, press_q_text_rect)
