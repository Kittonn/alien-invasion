vertical_tile_number = 11
tile_size = 64

screen_width = 1200
screen_height = vertical_tile_number * tile_size

main_menu_data = {
    0: {
        "name": "Play Game",
        "node_pos": (screen_width / 2, 260)
    },
    1: {
        "name": "Leaderboard",
        "node_pos": (screen_width / 2, 410)
    },
    2: {
        "name": "Quit",
        "node_pos": (screen_width / 2, 560)
    },

}


game_pause = False