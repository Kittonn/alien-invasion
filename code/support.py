from csv import reader
from os import walk
import pygame
from setting import tile_size
import json
import pygame


def import_folder(path):
  surface_list = []

  for _, __, img_files in walk(path):
    for image in img_files:
      full_path = path + '/' + image
      image_surface = pygame.image.load(full_path)
      surface_list.append(image_surface)

  return surface_list


def import_csv_layout(path):
  terrain_map = []
  with open(path) as map:
    level = reader(map, delimiter=',')
    for row in level:
      terrain_map.append(list(row))

    return terrain_map


def import_cut_graphics(path):
  surface = pygame.image.load(path).convert_alpha()
  tile_num_x = int(surface.get_size()[0] / tile_size)
  tile_num_y = int(surface.get_size()[1] / tile_size)

  cut_tiles = []
  for row in range(tile_num_y):
    for col in range(tile_num_x):
      x = col * tile_size
      y = row * tile_size
      new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
      new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
      cut_tiles.append(new_surf)

  return cut_tiles


def get_font_surf(type, size, text, color):
  path = "fonts/"
  font_path = {
      'chakra_petch': 'Chakrapetch/ChakraPetch-SemiBold.ttf',
      'hacked': 'Hacked/Hacked-KerX.ttf',
      'evil': "Evil/EvilEmpire-4BBVK.ttf"
  }
  return pygame.font.Font(path + font_path[type], size).render(text, True, color)


def import_score_leaderboard(path):
  return sorted(json.load(open(path)), key=lambda k: k['score'], reverse=True)[:5]


def write_score_leaderboard(new_data, path):
  json_file = json.load(open(path))
  json_file.append(new_data)
  with open(path, 'w') as file:
    file.write(json.dumps(json_file, indent=2))
