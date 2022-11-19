import pygame
import sys
from setting import *
from main_menu import Menu
from leaderboard import Leaderboard
from select_level import SelectLevel
from input_box import InputName
from how_to_play import HowToPlay


class Game:
  def __init__(self) -> None:
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    self.display_surface = screen
    pygame.display.set_caption("Alien Invasion")
    pygame.display.set_icon(pygame.image.load('graphics/icon.png'))
    self.clock = pygame.time.Clock()

    self.status = 'main_menu'
    self.current_mode = 0
    
    self.main_menu = Menu(self.display_surface, self.current_mode,
                          self.create_input_box, self.create_leaderboard, self.create_how_to_play)

    self.select_level = SelectLevel(
        self.display_surface, self.get_status,self.create_main_menu)

    self.how_to_play = HowToPlay(
        self.display_surface, self.current_mode, self.create_main_menu)

  def get_status(self, new_status, name_text="") -> None:
    self.status = new_status
    self.name = name_text

  def create_input_box(self, current_mode) -> None:
    self.status = 'input_box'
    self.current_mode = current_mode
    self.input_box = InputName(
        self.display_surface, self.current_mode, self.create_main_menu, self.get_status)

  def create_main_menu(self, current_mode) -> None:
    self.status = 'main_menu'
    self.current_mode = current_mode
    self.main_menu = Menu(self.display_surface, self.current_mode,
                          self.create_input_box, self.create_leaderboard, self.create_how_to_play)

  def create_leaderboard(self, current_mode) -> None:
    self.status = 'leaderboard'
    self.leaderboard = Leaderboard(
        self.display_surface, current_mode, self.create_main_menu)

  def create_how_to_play(self, current_mode) -> None:
    self.status = 'how_to_play'
    self.how_to_play = HowToPlay(
        self.display_surface, current_mode, self.create_main_menu)

  def run(self) -> None:
    while True:
      event_list = pygame.event.get()
      for event in event_list:
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      self.display_surface.fill('black')

      if self.status == 'main_menu':
        self.main_menu.run()
      elif self.status == 'leaderboard':
        self.leaderboard.run()
      elif self.status == 'input_box':
        self.input_box.run(event_list)
      elif self.status == 'select_level':
        self.select_level.run(self.name)
      elif self.status == 'how_to_play':
        self.how_to_play.run()  

      pygame.display.update()
      self.clock.tick(60)
