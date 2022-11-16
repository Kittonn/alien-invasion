import pygame
from game_data import levels
from support import get_font_surf
from setting import screen_width
from decoration import Background


class Node(pygame.sprite.Sprite):
  def __init__(self, pos, status, icon_speed):
    super().__init__()
    self.image = pygame.Surface((120, 80))
    if status == 'available':
      self.image.fill("red")
    else:
      self.image.fill("green")
    self.rect = self.image.get_rect(center=pos)

    self.detection_zone = pygame.Rect(self.rect.centerx - (
        icon_speed / 2), self.rect.centery - (icon_speed / 2), icon_speed, icon_speed)


class Icon(pygame.sprite.Sprite):
  def __init__(self, pos):
    super().__init__()
    self.pos = pos
    self.image = pygame.image.load("./assets/node/node-icon.png")
    self.rect = self.image.get_rect(center=pos)

  def update(self):
    self.rect.center = self.pos


class Overworld:
  def __init__(self, start_level, max_level, surface, create_level, check_game_start, get_status):
    self.display_surface = surface
    self.max_level = max_level
    self.current_level = start_level

    self.create_level = create_level
    self.check_game_start = check_game_start

    self.moving = False
    self.move_direction = pygame.math.Vector2(0, 0)
    self.speed = 8

    self.setup_nodes()
    self.setup_icon()

    self.background = pygame.sprite.GroupSingle(Background())

    self.get_status = get_status

  def setup_nodes(self):
    self.nodes = pygame.sprite.Group()
    for index, node_data in enumerate(levels.values()):
      if index <= self.max_level:
        node_sprite = Node(node_data['node_pos'], 'available', self.speed)
      else:
        node_sprite = Node(node_data['node_pos'], 'locked', self.speed)
      self.nodes.add(node_sprite)

  def draw_paths(self):
    if self.max_level > 0:
      points = [node['node_pos'] for index, node in enumerate(
          levels.values()) if index <= self.max_level]
      pygame.draw.lines(self.display_surface, 'red', False, points, 6)

  def setup_icon(self):
    self.icon = pygame.sprite.GroupSingle()
    icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
    self.icon.add(icon_sprite)

  def input(self):
    keys = pygame.key.get_pressed()
    if not self.moving:
      if keys[pygame.K_d] and self.current_level < self.max_level:
        self.move_direction = self.get_movement_data('next')
        self.current_level += 1
        self.moving = True
      elif keys[pygame.K_a] and self.current_level > 0:
        self.move_direction = self.get_movement_data('previous')
        self.current_level -= 1
        self.moving = True
      elif keys[pygame.K_ESCAPE]:
        print("back to text input")
        self.get_status('input_box')
        keys = pygame.key.get_pressed()
      elif keys[pygame.K_SPACE]:
        self.check_game_start(True)
        self.create_level(self.current_level)
        keys = pygame.key.get_pressed()

  def get_movement_data(self, target):
    start = pygame.math.Vector2(
        self.nodes.sprites()[self.current_level].rect.center)
    if(target == 'next'):
      end = pygame.math.Vector2(
          self.nodes.sprites()[self.current_level + 1].rect.center)
    else:
      end = pygame.math.Vector2(
          self.nodes.sprites()[self.current_level - 1].rect.center)
    return (end - start).normalize()

  def update_icon_pos(self):
    if self.moving and self.move_direction:
      self.icon.sprite.pos += self.move_direction * self.speed
      target_node = self.nodes.sprites()[self.current_level]
      if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)

  def run(self):
    self.background.draw(self.display_surface)
    name_text = get_font_surf('evil', 60, 'Select Level', 'black')
    name_text_rect = name_text.get_rect(center=(screen_width/2, 100))
    self.display_surface.blit(name_text, name_text_rect)
    self.input()
    self.update_icon_pos()
    self.icon.update()
    self.nodes.draw(self.display_surface)
    self.draw_paths()
    self.icon.draw(self.display_surface)
