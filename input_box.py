import pygame
from support import get_font_surf
from setting import screen_width


class TextInputBox(pygame.sprite.Sprite):
  def __init__(self, pos, width, surface, current_mode, create_main_menu) -> None:
    super().__init__()
    self.display_surface = surface
    self.pos = pos
    self.width = width
    self.active = False
    self.text = ""
    self.font = pygame.font.Font("./assets/font/Evil/EvilEmpire-4BBVK.ttf", 35)
    self.backcolor = None

    self.current_mode = current_mode
    self.create_main_menu = create_main_menu

    self.render_text()

  def render_text(self) -> None:
    text_surface = self.font.render(self.text, True, 'black', self.backcolor)
    self.image = pygame.Surface((max(self.width, text_surface.get_width(
    ) + 10), text_surface.get_height() + 10), pygame.SRCALPHA)
    if self.backcolor:
      self.image.fill(self.backcolor)

    self.image.blit(text_surface, (5, 5))
    pygame.draw.rect(self.image, 'black',
                     self.image.get_rect().inflate(-2, -2), 2)
    self.rect = self.image.get_rect(center=self.pos)

  def update(self, event_list) -> None:
    for event in event_list:
      if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
        self.active = self.rect.collidepoint(event.pos)
      if event.type == pygame.KEYDOWN and self.active:
        if event.key == pygame.K_RETURN:
          self.active = False
        elif event.key == pygame.K_BACKSPACE:
          self.text = self.text[:-1]
        else:
          self.text += event.unicode
        self.render_text()


class InputName:
  def __init__(self, surface, current_mode, create_main_menu, get_status) -> None:
    self.display_surface = surface
    self.create_main_menu = create_main_menu
    self.current_mode = current_mode

    self.get_status = get_status

    self.text_input_box = TextInputBox(
        (screen_width / 2, 550), 350, self.display_surface, current_mode, self.create_main_menu)
    self.text_group = pygame.sprite.Group(self.text_input_box)

  def input(self) -> None:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
      self.create_main_menu(self.current_mode)

    elif keys[pygame.K_RETURN] and self.text_input_box.text != '':
      self.get_status("select_level", self.text_input_box.text)
      keys = pygame.key.get_pressed()

  def run(self, event_list) -> None:
    background = pygame.image.load("./assets/Background.png")
    self.display_surface.blit(background, (0, 0))

    player_image = pygame.image.load("./assets/p1_front.png")
    player_image = pygame.transform.scale(
        player_image, (player_image.get_width() * 3, player_image.get_height() * 3))
    player_image_rect = player_image.get_rect(center=(screen_width / 2, 330))
    self.display_surface.blit(player_image, player_image_rect)

    name_text = get_font_surf('evil', 60, "Enter Your Name", 'black')
    name_text_rect = name_text.get_rect(center=(screen_width / 2, 100))
    self.display_surface.blit(name_text, name_text_rect)

    self.input()
    self.text_group.update(event_list)
    self.text_group.draw(self.display_surface)
