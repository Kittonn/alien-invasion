import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
  def __init__(self, pos, change_health) -> None:
    super().__init__()
    self.import_character_assets()
    self.frame_index = 0
    self.animation_speed = 0.15
    self.image = self.animations['idle'][self.frame_index]
    self.rect = self.image.get_rect(topleft=pos)

    self.change_health = change_health
    self.invincible = False
    self.invincibility_duration = 2000
    self.hurt_time = 0

    self.direction = pygame.math.Vector2(0, 0)
    self.speed = 8
    self.gravity = 0.8
    self.jump_speed = -16

    self.status = 'idle'
    self.facing_right = True
    self.on_ground = False
    self.on_ceiling = False
    self.on_left = False
    self.on_right = False

  def import_character_assets(self) -> None:
    character_path = "graphics/character/"
    self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

    for animation in self.animations.keys():
      full_path = character_path + animation
      self.animations[animation] = import_folder(full_path)

  def animate(self) -> None:
    animation = self.animations[self.status]

    self.frame_index += self.animation_speed
    if self.frame_index >= len(animation):
      self.frame_index = 0

    image = animation[int(self.frame_index)]
    if self.facing_right:
      self.image = image
    else:
      flipped_image = pygame.transform.flip(image, True, False)
      self.image = flipped_image

    if self.on_ground and self.on_right:
      self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
    elif self.on_ground and self.on_left:
      self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
    elif self.on_ground:
      self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
    elif self.on_ceiling and self.on_right:
      self.rect = self.image.get_rect(topright=self.rect.topright)
    elif self.on_ceiling and self.on_left:
      self.rect = self.image.get_rect(topleft=self.rect.topleft)
    elif self.on_ceiling:
      self.rect = self.image.get_rect(midtop=self.rect.midtop)

  def get_input(self) -> None:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
      self.direction.x = 1
      self.facing_right = True
    elif keys[pygame.K_a]:
      self.direction.x = -1
      self.facing_right = False
    else:
      self.direction.x = 0

    if keys[pygame.K_SPACE] and self.on_ground:
      self.jump()

  def get_status(self) -> None:
    if self.direction.y < 0:
      self.status = 'jump'
    elif self.direction.y > 1:
      self.status = 'fall'
    else:
      if self.direction.x != 0 and self.direction.y == 0:
        self.status = 'run'
      elif self.direction.y == 0 and self.direction.x == 0:
        self.status = 'idle'

  def apply_gravity(self) -> None:
    self.direction.y += self.gravity
    self.rect.y += self.direction.y

  def jump(self) -> None:
    self.direction.y = self.jump_speed

  def get_damage(self):
    if not self.invincible:
      self.change_health(-10)
      self.invincible = True
      self.hurt_time = pygame.time.get_ticks()
    
  def invincibility_timer(self):
    if self.invincible:
      current_time = pygame.time.get_ticks()
      if current_time - self.hurt_time >= self.invincibility_duration:
        self.invincible = False

  def update(self) -> None:
    self.get_input()
    self.get_status()
    self.animate()
    self.invincibility_timer()
