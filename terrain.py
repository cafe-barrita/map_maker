TILE_SIZE = 32

TERRAINS = {
    "grass": {
        "tiles": [
            {"x": 0, "y": 11},
            {"x": 1, "y": 11},
            {"x": 2, "y": 11},
            {"x": 3, "y": 11},
            {"x": 4, "y": 11},
            {"x": 5, "y": 11},
        ],
        "borders": {
            "patch": {"x": 0, "y": 6},
            "top_left": {"x": 0, "y": 8},
            "top": {"x": 1, "y": 8},
            "top_right": {"x": 2, "y": 8},
            "left": {"x": 0, "y": 9},
            "right": {"x": 2, "y": 9},
            "bottom_left": {"x": 0, "y": 10},
            "bottom": {"x": 1, "y": 10},
            "bottom_right": {"x": 2, "y": 10},
        }
    },
    "water": {
        "tiles": [
            {"x": 18, "y": 5},
            {"x": 19, "y": 5},
            {"x": 20, "y": 5},
        ],
        "borders": {
            "patch": {"x": 18, "y": 0},
            "top_left": {"x": 18, "y": 2},
            "top": {"x": 19, "y": 2},
            "top_right": {"x": 20, "y": 2},
            "left": {"x": 18, "y": 3},
            "right": {"x": 20, "y": 3},
            "bottom_left": {"x": 18, "y": 4},
            "bottom": {"x": 19, "y": 4},
            "bottom_right": {"x": 20, "y": 4},
        }
    },
    "sand": {
        "tiles": [
            {"x": 0, "y": 17},
            {"x": 1, "y": 17},
            {"x": 2, "y": 17},
        ],
        "borders": {
            "patch": {"x": 0, "y": 13},
            "top_left": {"x": 0, "y": 14},
            "top": {"x": 1, "y": 14},
            "top_right": {"x": 2, "y": 14},
            "left": {"x": 0, "y": 15},
            "right": {"x": 2, "y": 15},
            "bottom_left": {"x": 0, "y": 16},
            "bottom": {"x": 1, "y": 16},
            "bottom_right": {"x": 2, "y": 16},
        }
    },
    "ground": {
        "tiles": [
            {"x": 1, "y": 5},
            {"x": 2, "y": 5},
        ],
        "borders": {
            "patch": {"x": 0, "y": 0},
            "top_left": {"x": 0, "y": 2},
            "top": {"x": 1, "y": 2},
            "top_right": {"x": 2, "y": 2},
            "left": {"x": 0, "y": 3},
            "right": {"x": 2, "y": 3},
            "bottom_left": {"x": 0, "y": 4},
            "bottom": {"x": 1, "y": 4},
            "bottom_right": {"x": 2, "y": 4},
        }
    },
    "dark_grass": {
        "tiles": [
            {"x": 6, "y": 11},
            {"x": 7, "y": 11},
            {"x": 8, "y": 11},
        ],
        "borders": {
            "patch": {"x": 6, "y": 6},
            "top_left": {"x": 6, "y": 8},
            "top": {"x": 7, "y": 8},
            "top_right": {"x": 8, "y": 8},
            "left": {"x": 6, "y": 9},
            "right": {"x": 8, "y": 9},
            "bottom_left": {"x": 6, "y": 10},
            "bottom": {"x": 7, "y": 10},
            "bottom_right": {"x": 8, "y": 10},
        }
    },
    "dark_ground": {
        "tiles": [
            {"x": 4, "y": 5},
            {"x": 5, "y": 5},
        ],
        "borders": {
            "patch": {"x": 3, "y": 0},
            "top_left": {"x": 3, "y": 2},
            "top": {"x": 4, "y": 2},
            "top_right": {"x": 5, "y": 2},
            "left": {"x": 3, "y": 3},
            "right": {"x": 5, "y": 3},
            "bottom_left": {"x": 3, "y": 4},
            "bottom": {"x": 4, "y": 4},
            "bottom_right": {"x": 5, "y": 4},
        }
    },
    "rock": {
        "tiles": [
            {"x": 7, "y": 5},
            {"x": 8, "y": 5},
        ],
        "borders": {
            "patch": {"x": 6, "y": 0},
            "top_left": {"x": 6, "y": 2},
            "top": {"x": 7, "y": 2},
            "top_right": {"x": 8, "y": 2},
            "left": {"x": 6, "y": 3},
            "right": {"x": 8, "y": 3},
            "bottom_left": {"x": 6, "y": 4},
            "bottom": {"x": 7, "y": 4},
            "bottom_right": {"x": 8, "y": 4},
        }
    },
    "dark_rock": {
        "tiles": [
            {"x": 13, "y": 17},
            {"x": 14, "y": 17},
        ],
        "borders": {
            "patch": {"x": 12, "y": 12},
            "top_left": {"x": 12, "y": 14},
            "top": {"x": 13, "y": 14},
            "top_right": {"x": 14, "y": 14},
            "left": {"x": 12, "y": 15},
            "right": {"x": 14, "y": 15},
            "bottom_left": {"x": 12, "y": 16},
            "bottom": {"x": 13, "y": 16},
            "bottom_right": {"x": 14, "y": 16},
        }
    },
    "lava": {
        "tiles": [
            {"x": 9, "y": 17},
            {"x": 10, "y": 17},
            {"x": 11, "y": 17},
        ],
        "borders": {
            "patch": {"x": 9, "y": 12},
            "top_left": {"x": 9, "y": 14},
            "top": {"x": 10, "y": 14},
            "top_right": {"x": 11, "y": 14},
            "left": {"x": 9, "y": 15},
            "right": {"x": 11, "y": 15},
            "bottom_left": {"x": 9, "y": 16},
            "bottom": {"x": 10, "y": 16},
            "bottom_right": {"x": 11, "y": 16},
        }
    },
}

PRIORIDAD_TERRENO = {
    "water": 0,
    "sand": 1,
    "ground": 2,
    "grass": 3,
    "dark_grass": 4,
    "dark_ground": 5,
    "rock": 6,
    "dark_rock": 7,
    "lava": 8
}
