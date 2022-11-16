import pygame
from overworld import Overworld
from level import Level
from ui import UI
from game_end import GameOver, Victory


class SelectLevel:
  def __init__(self, surface, get_status,create_main_menu) -> None:
    self.display_surface = surface
    self.status = 'overworld'

    self.create_main_menu = create_main_menu
    self.get_status = get_status

    self.ui = UI(self.display_surface)
    self.max_health = 100
    self.current_health = 100
    self.coins = 0

    self.max_level = 0
    self.overworld = Overworld(
        0, self.max_level, self.display_surface, self.create_level, self.check_game_start, self.get_status)

    self.water_collide = False
    self.game_start = False

    # self.game_over = GameOver(self.display_surface, self.coins, 'Kitton',self.change_status)

  def create_level(self, current_level) -> None:
    self.level = Level(current_level, self.display_surface,
                       self.create_overworld, self.change_coins, self.change_health, self.check_water_collision)
    self.status = 'level'

  def create_overworld(self, current_level, new_max_level) -> None:
    if new_max_level > self.max_level:
      self.max_level = new_max_level
    self.overworld = Overworld(current_level, self.max_level,
                               self.display_surface, self.create_level, self.check_game_start, self.get_status)
    self.status = 'overworld'

  def check_water_collision(self, check):
    self.water_collide = check

  def change_coins(self, amount):
    self.coins += amount

  def change_status(self, status):
    self.status = status

  def change_health(self, amount):
    self.current_health += amount
    if self.current_health > 100:
      self.current_health = 100

  def check_game_over(self):
    if self.current_health <= 0 or self.water_collide:
      self.current_health = 100
      self.game_over = GameOver(
          self.display_surface, self.coins, self.change_status, self.create_main_menu)
      self.coins = 0
      self.max_level = 0
      self.water_collide = False
      self.overworld = Overworld(
          0, self.max_level, self.display_surface, self.create_level, self.check_game_start, self.get_status)
      self.status = 'game_over'
      self.game_start = False
      # self.status = 'overworld'

  def check_game_victory(self):
    if self.level.goal_collide and self.overworld.current_level == 5:
      self.current_health = 100
      self.victory = Victory(self.display_surface,
                             self.coins, self.change_status, self.create_main_menu)
      self.max_level = 0
      self.overworld = Overworld(
          0, self.max_level, self.display_surface, self.create_level, self.check_game_start, self.get_status)
      self.status = 'victory'
      self.coins = 0


  def check_game_start(self, start):
    self.game_start = start

  def input(self) -> None:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] and not self.game_start:
      self.get_status('input_box')

  def run(self, name) -> None:

    # self.input()
    if self.status == 'overworld':
      self.overworld.run()
    elif self.status == 'game_over':
      self.game_over.run(name)
    elif self.status == 'victory':
      self.victory.run(name)
    else:
      self.level.run(name)
      self.ui.show_health(self.current_health, self.max_health)
      self.ui.show_coins(self.coins)
      self.check_game_over()
      self.check_game_victory()
