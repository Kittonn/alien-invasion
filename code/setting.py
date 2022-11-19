vertical_tile_number = 11
tile_size = 64

screen_width = 1200
screen_height = vertical_tile_number * tile_size

main_menu_data = {
    0: {
        "name": "Play Game",
        "node_pos": (screen_width / 2, 230)
    },
    1: {
        "name": "Leaderboard",
        "node_pos": (screen_width / 2, 350)
    },
    2: {
        "name": "How to play",
        "node_pos": (screen_width / 2, 470)
    },
    3: {
        "name": "Quit",
        "node_pos": (screen_width / 2, 590)
    },

}


game_pause = False