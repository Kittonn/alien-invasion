import pygame
from support import get_font_surf


class UI:
  def __init__(self, surface) -> None:
    self.display_surface = surface

    self.health_bar = pygame.Surface((152, 20))
    self.health_bar.fill('blue')

    self.bar_max_width = 152
    self.bar_height = 20

    self.coin = pygame.image.load("./assets/tiles/coin_gold.png")
    self.coin_rect = self.coin.get_rect(topleft=(5, 20))

  def show_health(self, current, full):
    self.display_surface.blit(self.health_bar, (10, 10))
    current_health_ratio = current / full
    current_bar_width = self.bar_max_width * current_health_ratio
    health_bar_rect = pygame.Rect(
        (10, 10), (current_bar_width, self.bar_height))
    pygame.draw.rect(self.display_surface, 'red', health_bar_rect)

  def show_coins(self, amount):
    self.display_surface.blit(self.coin, self.coin_rect)
    coin_amount_surf = get_font_surf('evil', 30, str(amount), 'black')
    coin_amount_rect = coin_amount_surf.get_rect(
        midleft=(self.coin_rect.right + 10, self.coin_rect.centery))
    self.display_surface.blit(coin_amount_surf, coin_amount_rect)
