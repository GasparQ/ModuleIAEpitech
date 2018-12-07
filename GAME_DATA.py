BEFORE, AFTER, ALWAYS = 1, 2, 4

RED, PINK, BLUE, GRAY, BLACK, WHITE, PURPLE, BROWN, PHANTOM = 0, 1, 2, 3, 4, 5, 6, 7, 8

PHANTOM_PLAYER, INSPECTOR_PLAYER = 0, 1

BASE_PATHES = [[1, 4], [0, 2], [1, 3], [2, 7], [0, 5, 8], [4, 6], [5, 7], [3, 6, 9], [4, 9], [7, 8]]
PINK_PATHES = [[1, 4], [0, 2, 5, 7], [1, 3, 6], [2, 7], [0, 5, 8, 9], [4, 6, 1, 8], [5, 7, 2, 9], [3, 6, 9, 1],
               [4, 9, 5], [7, 8, 4, 6]]

TILE_NAMES = {
    RED: 'red',
    PINK: 'pink',
    BLUE: 'blue',
    GRAY: 'gray',
    BLACK: 'black',
    WHITE: 'white',
    PURPLE: 'purple',
    BROWN: 'brown'
}

TILES = {
    'red': RED,
    'pink': PINK,
    'blue': BLUE,
    'gray': GRAY,
    'black': BLACK,
    'white': WHITE,
    'purple': PURPLE,
    'brown': BROWN
}

FRENCH_TILES = {
    'rouge': RED,
    'rose': PINK,
    'bleu': BLUE,
    'gris': GRAY,
    'noir': BLACK,
    'blanc': WHITE,
    'violet': PURPLE,
    'marron': BROWN
}

FRENCH_TILES_NAMES = {
    RED: 'rouge',
    PINK: 'rose',
    BLUE: 'bleu',
    GRAY: 'gris',
    BLACK: 'noir',
    WHITE: 'blanc',
    PURPLE: 'violet',
    BROWN: 'marron'
}

PLAYER_NAMES = {
    PHANTOM_PLAYER: 'Phantom',
    INSPECTOR_PLAYER: 'Inspector'
}


TILE_CONVERTER = [
    PINK,
    RED,
    GRAY,
    BLUE,
    PURPLE,
    BROWN,
    BLACK,
    WHITE
]
