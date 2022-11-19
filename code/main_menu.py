import pygame
from setting import main_menu_data
import sys
from support import get_font_surf
from name import Name


class Node(pygame.sprite.Sprite):
  def __init__(self, pos, icon_speed) -> None:
    super().__init__()
    self.image = pygame.Surface((100, 80))
    self.image.fill('blue')
    self.rect = self.image.get_rect(center=pos)

    self.detection_zone = pygame.Rect(self.rect.centerx - (
        icon_speed / 2), self.rect.centery - (icon_speed / 2), icon_speed, icon_speed)


class Icon(pygame.sprite.Sprite):
  def __init__(self, pos) -> None:
    super().__init__()
    self.pos = pos
    self.image = pygame.Surface((20, 20))
    self.image.fill('green')
    self.rect = self.image.get_rect(center=pos)

  def update(self) -> None:
    self.rect.center = self.pos


class Menu:
  def __init__(self, surface, current_mode, create_input_box, create_leaderboard, create_how_to_play) -> None:
    self.display_surface = surface

    self.create_input_box = create_input_box
    self.create_leaderboard = create_leaderboard
    self.create_how_to_play = create_how_to_play

    self.current_mode = current_mode
    self.max_mode = len(main_menu_data.keys())

    self.moving = False
    self.move_direction = pygame.math.Vector2(0, 0)
    self.speed = 20

    self.name = Name(self.display_surface)

    self.setup_node()
    self.setup_icon()

  def setup_node(self) -> None:
    self.nodes = pygame.sprite.Group()
    for node_data in main_menu_data.values():
      node_sprite = Node(node_data['node_pos'], self.speed)
      self.nodes.add(node_sprite)

  def draw_paths(self) -> None:
    points = [node_data['node_pos'] for node_data in main_menu_data.values()]
    pygame.draw.lines(self.display_surface, 'red', False, points, 6)

  def setup_icon(self) -> None:
    self.icon = pygame.sprite.GroupSingle()
    icon_sprite = Icon(
        main_menu_data[self.current_mode]['node_pos'])
    self.icon.add(icon_sprite)

  def input(self) -> None:
    keys = pygame.key.get_pressed()
    if not self.moving:
      if(keys[pygame.K_w]) and self.current_mode > 0:
        self.move_direction = self.get_movement_data('previous')
        self.current_mode -= 1
        self.moving = True
      elif(keys[pygame.K_s]) and self.current_mode < self.max_mode - 1:
        self.move_direction = self.get_movement_data('next')
        self.current_mode += 1
        self.moving = True
      elif(keys[pygame.K_SPACE]):
        if self.current_mode == 0:
          self.create_input_box(self.current_mode)
          keys = pygame.key.get_pressed()
        elif self.current_mode == 1:
          self.create_leaderboard(self.current_mode)
        elif self.current_mode == 2:
          self.create_how_to_play(self.current_mode)
        elif self.current_mode == 3:
          pygame.quit()
          sys.exit()

  def get_movement_data(self, target) -> None:
    start = pygame.math.Vector2(
        self.nodes.sprites()[self.current_mode].rect.center)
    if target == 'next':
      end = pygame.math.Vector2(
          self.nodes.sprites()[self.current_mode + 1].rect.center)
    else:
      end = pygame.math.Vector2(
          self.nodes.sprites()[self.current_mode - 1].rect.center)
    return (end - start).normalize()

  def update_icon_pos(self) -> None:
    if self.moving and self.move_direction:
      self.icon.sprite.pos += self.move_direction * self.speed
      target_node = self.nodes.sprites()[self.current_mode]
      if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)

  def run(self) -> None:
    background = pygame.image.load("graphics/Background.png")
    self.display_surface.blit(background, (0, 0))

    name_text = get_font_surf('evil', 90, 'Alien Invasion', 'black')
    name_rect = name_text.get_rect(
        center=(self.display_surface.get_width()/2, 100))
    self.display_surface.blit(name_text, name_rect)

    self.name.draw()

    self.input()
    self.update_icon_pos()
    self.icon.update()
    # self.nodes.draw(self.display_surface)
    # self.draw_paths()
    # self.icon.draw(self.display_surface)

    for data in main_menu_data:
      if(data == self.current_mode):
        name_text = get_font_surf(
            'evil', 50, main_menu_data[data]['name'], '#6a040f')
      else:
        name_text = get_font_surf(
            'evil', 50, main_menu_data[data]['name'], '#03071e')

      name_rect = name_text.get_rect(center=main_menu_data[data]['node_pos'])
      self.display_surface.blit(name_text, name_rect)
