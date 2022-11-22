import pygame
from tile import Tile, StaticTile, Crate, Coin, French, Item, Block
from decoration import Background, Water
from setting import tile_size, screen_width, screen_height
from player import Player
from support import import_csv_layout, import_cut_graphics, get_font_surf
from enemy import Enemy
from game_data import levels, graphic_tiles, items, times
from random import randint


class Level:
  def __init__(self, current_level, surface, create_overworld, change_coins, change_health, check_water_collision):
    self.display_surface = surface
    self.world_shift = 0
    self.current_x = None

    self.create_overworld = create_overworld
    self.current_level = current_level

    self.collect_coin_sound = pygame.mixer.Sound("./audio/collect_coin.wav")
    self.collect_item_sound = pygame.mixer.Sound("./audio/collect_item.wav")
    self.player_hit_sound = pygame.mixer.Sound("./audio/player_hit.wav")
    self.enemy_hit_sound = pygame.mixer.Sound("./audio/enemy_hit.wav")

    self.collect_coin_sound.set_volume(0.5)
    self.collect_item_sound.set_volume(0.5)
    self.player_hit_sound.set_volume(0.5)
    self.enemy_hit_sound.set_volume(0.5)

    self.time_enemy_hit_play = 0

    level_data = levels[self.current_level]

    self.new_max_level = level_data['unlock']

    player_layout = import_csv_layout(level_data['player'])
    self.player = pygame.sprite.GroupSingle()
    self.goal = pygame.sprite.GroupSingle()
    self.player_setup(player_layout, change_health)

    self.check_water_collision = check_water_collision
    self.change_coins = change_coins
    self.goal_collide = False

    terrain_layout = import_csv_layout(level_data['tile'])
    self.terrain_sprites = self.create_tile_group(terrain_layout, 'tile')

    crate_layout = import_csv_layout(level_data['crate'])
    self.crate_sprites = self.create_tile_group(crate_layout, 'crate')

    coin_layout = import_csv_layout(level_data['coin'])
    self.coin_sprites = self.create_tile_group(coin_layout, 'coin')

    enemy_layout = import_csv_layout(level_data['enemy'])
    self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')

    constant_layout = import_csv_layout(level_data['constant'])
    self.constant_sprites = self.create_tile_group(constant_layout, 'constant')

    french_layout = import_csv_layout(level_data['french'])
    self.french_sprites = self.create_tile_group(french_layout, 'french')

    block_layout = import_csv_layout(level_data['block'])
    self.block_sprites = self.create_tile_group(block_layout, 'block')

    self.item_sprites = pygame.sprite.Group()

    self.background = pygame.sprite.GroupSingle(Background())

    self.enemy_collide_time = 0

    self.water = Water()
    
    self.countdown_time = times[self.current_level]
    
    
    
  def count_down_time(self):
    if self.countdown_time > 0:
      self.countdown_time -= 1/60
    else:
      self.countdown_time = 60
      self.check_water_collision(True)
    
    self.time_text = get_font_surf('evil',40, str(int(self.countdown_time)), 'black')
    self.time_text_rect = self.time_text.get_rect(center=(screen_width/2, 50))
    self.display_surface.blit(self.time_text, self.time_text_rect)

  def check_win(self):
    if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
      if self.current_level == 5:
        self.goal_collide = True
      else:
        self.goal_collide = False
      self.create_overworld(self.current_level, self.new_max_level)

  def check_death(self):
    if self.player.sprite.rect.top > screen_height:
      self.check_water_collision(True)

  def check_coin_collision(self):
    collied_coins = pygame.sprite.spritecollide(
        self.player.sprite, self.coin_sprites, True)
    if collied_coins:
      self.collect_coin_sound.play()
      for coin in collied_coins:
        self.change_coins(coin.value)

  def check_enemy_collision(self):
    enemy_collisions = pygame.sprite.spritecollide(
        self.player.sprite, self.enemy_sprites, False)

    if enemy_collisions:
      for enemy in enemy_collisions:
        enemy_center = enemy.rect.centery
        enemy_top = enemy.rect.top
        player_bottom = self.player.sprite.rect.bottom
        if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 1:
          self.player_hit_sound.play()
          self.player.sprite.direction.y = -15
          random_item = randint(0, 4)
          random_create = randint(0, 1)
          if random_create == 1:
            self.item_sprites.add(Item(tile_size, enemy.rect.x, enemy.rect.y,
                                       pygame.image.load(items[random_item]['path']).convert_alpha(), items[random_item]['id']))
          enemy.kill()
        else:
          if pygame.time.get_ticks() - self.time_enemy_hit_play > 2000:
            self.enemy_hit_sound.play()
            self.time_enemy_hit_play = pygame.time.get_ticks()
          self.player.sprite.get_damage()
          self.enemy_collide_time = pygame.time.get_ticks()

  def check_item_collision(self):
    item_collisions = pygame.sprite.spritecollide(
        self.player.sprite, self.item_sprites, True)

    if item_collisions:
      self.collect_item_sound.play()
      for item in item_collisions:
        if item.id != 1:
          self.change_coins(2+item.id)
        else:
          self.player.sprite.change_health(20)

  def create_tile_group(self, layout, type):
    sprite_group = pygame.sprite.Group()
    for row_index, row in enumerate(layout):
      for col_index, val in enumerate(row):
        if val != '-1':
          x = col_index * tile_size
          y = row_index * tile_size

          if type == 'tile':

            terrain_tile_list = import_cut_graphics(
                graphic_tiles[self.current_level])

            tile_surface = terrain_tile_list[int(val)]
            sprite = StaticTile(tile_size, x, y, tile_surface)

          if type == 'crate':
            sprite = Crate(tile_size, x, y)

          if type == 'coin':
            terrain_tile_list = import_cut_graphics(
                "graphics/tiles/coin_tiles.png")
            coin_random = randint(0, 2)
            coin_surface = terrain_tile_list[coin_random]
            sprite = Coin(tile_size, x, y, coin_surface, coin_random + 1)

          if type == 'enemy':
            random_id = randint(1, 2)
            sprite = Enemy(tile_size, x, y, random_id,self.current_level)

          if type == 'constant':
            sprite = Tile(tile_size, x, y)

          if type == 'french':
            terrain_tile_list = import_cut_graphics(
                "graphics/tiles/french_tiles.png")
            french_surface = terrain_tile_list[int(val)]
            sprite = French(tile_size, x, y, french_surface)

          if type == 'block':
            sprite = Block(tile_size, x, y)

          sprite_group.add(sprite)
    return sprite_group

  def player_setup(self, layout, change_health):
    for row_index, row in enumerate(layout):
      for col_index, val in enumerate(row):
        x = col_index * tile_size
        y = row_index * tile_size
        if val == '0':
          sprite = Player((x, y), change_health)
          self.player.add(sprite)
        if val == '1':
          goal_surface = pygame.image.load(
              "graphics/tiles/goal.png").convert_alpha()
          sprite = StaticTile(tile_size, x, y, goal_surface)
          self.goal.add(sprite)

  def block_movement_collision(self):
    block_collisions = pygame.sprite.spritecollide(
        self.player.sprite, self.block_sprites, False)
    if block_collisions:
      for block in block_collisions:
        if block.rect.colliderect(self.player.sprite.rect):
          if self.player.sprite.direction.x < 0:
            self.player.sprite.rect.left = block.rect.right

          elif self.player.sprite.direction.x > 0:
            self.player.sprite.rect.right = block.rect.left

  def horizontal_movement_collision(self):
    player = self.player.sprite
    player.rect.x += player.direction.x * player.speed
    collidable_sprite = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

    for sprite in collidable_sprite:
      if sprite.rect.colliderect(player.rect):
        if player.direction.x < 0:
          player.rect.left = sprite.rect.right
          player.on_left = True
          self.current_x = player.rect.left
        elif player.direction.x > 0:
          player.rect.right = sprite.rect.left
          player.on_right = True
          self.current_x = player.rect.right

    if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
      player.on_left = False

    if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
      player.on_right = False

  def vertical_movement_collision(self):
    player = self.player.sprite
    player.apply_gravity()
    collidable_sprite = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

    for sprite in collidable_sprite:
      if sprite.rect.colliderect(player.rect):
        if player.direction.y > 0:
          player.rect.bottom = sprite.rect.top
          player.direction.y = 0
          player.on_ground = True
        elif player.direction.y < 0:
          player.rect.top = sprite.rect.bottom
          player.direction.y = 0
          player.on_ceiling = True

    if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
      player.on_ground = False
    if player.on_ceiling and player.direction.y > 0:
      player.on_ceiling = False

  def scroll_x(self):
    player = self.player.sprite
    player_x = player.rect.centerx
    direction_x = player.direction.x

    if player_x < screen_width / 4 and direction_x < 0:
      self.world_shift = 8
      player.speed = 0
    elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
      self.world_shift = -8
      player.speed = 0
    else:
      self.world_shift = 0
      player.speed = 8

  def input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
      self.create_overworld(self.current_level, self.current_level)

  def enemy_collision_reverse(self):
    for enemy in self.enemy_sprites.sprites():
      if pygame.sprite.spritecollide(enemy, self.constant_sprites, False):
        enemy.reverse()

  def run(self, name):
    self.input()
    self.background.draw(self.display_surface)

    self.water.draw(self.display_surface)
    self.terrain_sprites.update(self.world_shift)
    self.terrain_sprites.draw(self.display_surface)

    self.crate_sprites.update(self.world_shift)
    self.crate_sprites.draw(self.display_surface)

    self.french_sprites.update(self.world_shift)
    self.french_sprites.draw(self.display_surface)

    self.coin_sprites.update(self.world_shift)
    self.coin_sprites.draw(self.display_surface)

    self.enemy_collision_reverse()
    self.enemy_sprites.update(self.world_shift)
    self.enemy_sprites.draw(self.display_surface)

    self.constant_sprites.update(self.world_shift)

    name_text = get_font_surf('evil', 30, name, 'black')
    name_text_rect = name_text.get_rect(
        midleft=(screen_width - name_text.get_width() - 10, name_text.get_height() - 5))
    self.display_surface.blit(name_text, name_text_rect)

    self.player.update()
    self.horizontal_movement_collision()
    self.vertical_movement_collision()
    self.scroll_x()

    self.goal.update(self.world_shift)
    self.goal.draw(self.display_surface)

    self.check_death()
    self.check_win()
    self.check_coin_collision()
    self.check_enemy_collision()
    self.check_item_collision()
    self.block_movement_collision()

    self.item_sprites.update(self.world_shift)
    self.item_sprites.draw(self.display_surface)

    self.player.draw(self.display_surface)
    self.block_sprites.update(self.world_shift)
    self.block_sprites.draw(self.display_surface)
    
    self.count_down_time()
