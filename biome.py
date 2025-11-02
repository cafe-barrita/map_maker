import numpy as np
from settings import ANCHO, ALTO

BIOMES = {
    "default": {
        "ELEVACION": {
            "water": 0.25,
            "sand": 0.4,
            "grass": 0.7,
            "rock": 1.0
        },
        "HUMEDAD": {
            "sand": 0.15,
            "ground": 0.25,
            "grass": 0.7,
            "dark_grass": 1.0
        },
        "TEMPERATURA": {
            "dark_ground": 0.25,
            "rock": 0.5,
            "dark_rock": 0.7,
            "lava": 1.0
        }
    },
    "sea": {
        "ELEVACION": {
            "water": 0.6,
            "sand": 0.8,
            "grass": 0.9,
            "rock": 1.0
        },
        "HUMEDAD": {
            "sand": 0.1,
            "ground": 0.2,
            "grass": 0.6,
            "dark_grass": 1.0
        },
        "TEMPERATURA": {
            "dark_ground": 0.4,
            "rock": 0.8,
            "dark_rock": 0.9,
            "lava": 1.0
        }
    },
    "beach": {
        "ELEVACION": {
            "water": 0.47,
            "sand": 0.65,
            "grass": 0.9,
            "rock": 1.0
        },
        "HUMEDAD": {
            "sand": 0.1,
            "ground": 0.2,
            "grass": 0.6,
            "dark_grass": 1.0
        },
        "TEMPERATURA": {
            "dark_ground": 0.4,
            "rock": 0.8,
            "dark_rock": 0.9,
            "lava": 1.0
        }
    },
    "highlands": {
        "ELEVACION": {
            "water": 0.44,
            "sand": 0.44,
            "grass": 0.55,
            "rock": 1.0
        },
        "HUMEDAD": {
            "sand": 0.1,
            "ground": 0.4,
            "grass": 0.55,
            "dark_grass": 1.0
        },
        "TEMPERATURA": {
            "dark_ground": 0.4,
            "rock": 0.8,
            "dark_rock": 0.9,
            "lava": 1.0
        }
    },
    "grassland": {
        "ELEVACION": {
            "water": 0.15,
            "sand": 0.35,
            "grass": 0.6,
            "rock": 1.0
        },
        "HUMEDAD": {
            "sand": 0.1,
            "ground": 0.2,
            "grass": 0.6,
            "dark_grass": 1.0
        },
        "TEMPERATURA": {
            "dark_ground": 0.4,
            "rock": 0.8,
            "dark_rock": 0.9,
            "lava": 1.0
        }
    },
    "desert": {
        "ELEVACION": {
            "water": 0.3,
            "sand": 0.3,
            "grass": 0.57,
            "rock": 1.0
        },
        "HUMEDAD": {
            "sand": 0.5,
            "ground": 0.62,
            "grass": 0.9,
            "dark_grass": 1.0
        },
        "TEMPERATURA": {
            "dark_ground": 0.4,
            "rock": 0.75,
            "dark_rock": 0.9,
            "lava": 1.0
        }
    },
    "steppe": {
        "ELEVACION": {
            "water": 0.15,
            "sand": 0.35,
            "grass": 0.6,
            "rock": 1.0
        },
        "HUMEDAD": {
            "sand": 0.25,
            "ground": 0.55,
            "grass": 0.8,
            "dark_grass": 1.0
        },
        "TEMPERATURA": {
            "dark_ground": 0.4,
            "rock": 0.8,
            "dark_rock": 0.9,
            "lava": 1.0
        }
    },
    "mountain": {
        "ELEVACION": {
            "water": 0.15,
            "sand": 0.25,
            "grass": 0.45,
            "rock": 1.0
        },
        "HUMEDAD": {
            "sand": 0.1,
            "ground": 0.35,
            "grass": 0.5,
            "dark_grass": 1.0
        },
        "TEMPERATURA": {
            "dark_ground": 0.45,
            "rock": 0.8,
            "dark_rock": 0.9,
            "lava": 1.0
        }
    },
    "volcano": {
        "ELEVACION": {
            "water": 0.1,
            "sand": 0.2,
            "grass": 0.4,
            "rock": 1.0
        },
        "HUMEDAD": {
            "sand": 0.3,
            "ground": 0.52,
            "grass": 0.75,
            "dark_grass": 1.0
        },
        "TEMPERATURA": {
            "dark_ground": 0.25,
            "rock": 0.45,
            "dark_rock": 0.54,
            "lava": 1.0
        }
    },
    "hotspring": {
        "ELEVACION": {
            "water": 0.42,
            "sand": 0.42,
            "grass": 0.45,
            "rock": 1.0
        },
        "HUMEDAD": {
            "sand": 0.25,
            "ground": 0.35,
            "grass": 0.55,
            "dark_grass": 1.0
        },
        "TEMPERATURA": {
            "dark_ground": 0.25,
            "rock": 0.5,
            "dark_rock": 0.55,
            "lava": 1.0
        }
    },
}

def asignar_terrenos(mapa_elevacion, mapa_humedad, mapa_temperatura,
                     umbrales_elevacion, umbrales_humedad, umbrales_temp):
    """Asigna un tipo de terreno (string) a cada celda basado en el umbral de elevación."""
    mapa_terrenos = np.empty_like(mapa_elevacion, dtype=object)
    
    for y in range(ALTO):
        for x in range(ANCHO):
            elevacion = mapa_elevacion[y][x]
            humedad = mapa_humedad[y][x]
            temp = mapa_temperatura[y][x]
            
            # Buscamos el terreno asociado al rango de elevación
            if elevacion < umbrales_elevacion["water"]:
                mapa_terrenos[y][x] = "water"
            # Zona de transición: Playa
            elif elevacion < umbrales_elevacion["sand"]:
                mapa_terrenos[y][x] = "sand"
            elif elevacion < umbrales_elevacion["grass"]:
                if humedad < umbrales_humedad["sand"]:
                    mapa_terrenos[y][x] = "sand"
                elif humedad < umbrales_humedad["ground"]:
                    mapa_terrenos[y][x] = "ground"
                elif humedad < umbrales_humedad["grass"]:
                    mapa_terrenos[y][x] = "grass"
                else:
                    mapa_terrenos[y][x] = "dark_grass"
            else:
                if temp < umbrales_temp["dark_ground"]:
                    mapa_terrenos[y][x] = "dark_ground"
                elif temp < umbrales_temp["rock"]:
                    mapa_terrenos[y][x] = "rock"
                elif temp < umbrales_temp["dark_rock"]:
                    mapa_terrenos[y][x] = "dark_rock"
                else:
                    mapa_terrenos[y][x] = "lava"
                
    return mapa_terrenos