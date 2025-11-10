import random
from PIL import Image
from terrain import TILE_SIZE, TERRAINS, PRIORIDAD_TERRENO
from settings import *

ANCHO = 7
ALTO = 7

def es_parche(mascara):
    patch_masks = [
        BIT_ESTE + BIT_OESTE,
        BIT_NORTE + BIT_SUR,
        BIT_NORTE + BIT_OESTE + BIT_SURESTE,
        BIT_NORTE + BIT_ESTE + BIT_SUROESTE,
        BIT_SUR + BIT_OESTE + BIT_NORESTE,
        BIT_SUR + BIT_ESTE + BIT_NOROESTE,
    ]
    for patch_mask in patch_masks:
        if (mascara & patch_mask) == patch_mask:
            return True
    return False

# --- FUNCIÓN PRINCIPAL DE AUTOTILING ---
def calcular_mascara_borde(mapa, x, y):
    """
    Calcula una máscara de 8 bits para cada celda de 'target_terreno' 
    que bordea a 'terreno_central'.

    Retorna un nuevo mapa donde:
    - 1 significa que no requiere borde.
    - Un valor entre 1 y 255 es el código de la máscara.
    """

    # Lista de direcciones y sus desplazamientos (dy, dx) y valores de bit
    VECINOS = [
        (-1, 0, BIT_NORTE),  # Norte
        ( 0, 1, BIT_ESTE),   # Este
        ( 1, 0, BIT_SUR),    # Sur
        ( 0,-1, BIT_OESTE),   # Oeste
        (-1, -1, BIT_NOROESTE),  # Noroeste
        ( 1, -1, BIT_SUROESTE),   # Suroeste
        ( -1, 1, BIT_NORESTE),    # Noreste
        ( 1, 1, BIT_SURESTE)   # Sureste
    ]

    target_terreno = mapa[y][x]
    mascara_actual = 0
                
    # Comprobamos los 8 vecinos cardinales
    for dy, dx, bit_valor in VECINOS:
        ny, nx = y + dy, x + dx  # Coordenadas del vecino
                    
        if 0 <= ny < ALTO and 0 <= nx < ANCHO:                        
            terreno_vecino = mapa[ny][nx]
            if target_terreno == terreno_vecino:
                mascara_actual += bit_valor
        else:
            mascara_actual += bit_valor
                                
    return mascara_actual

def calcular_terrenos(mapa_terreno):
    # Reunimos los terrenos únicos que existen en el mapa (lista de listas)
    terrenos_set = set()
    for fila in mapa_terreno:
        terrenos_set.update(fila)
    terrenos_unicos = list(terrenos_set)
    
    # Ordenamos los terrenos según el valor de prioridad definido en el diccionario
    return sorted(terrenos_unicos, key=lambda t: PRIORIDAD_TERRENO.get(t, float('inf')))

def calcular_matriz_capa(mapa_terreno, terreno):
    mapa_capa = np.zeros((ALTO, ANCHO))
    for y in range(ALTO):
        for x in range(ANCHO):
            if PRIORIDAD_TERRENO[terreno] <= PRIORIDAD_TERRENO[mapa_terreno[y][x]]:
                mapa_capa[y][x] = 1
    return mapa_capa

def autotile(mapa_terreno, name):
    tileset = Image.open("tileset.png").convert("RGBA")
    map = Image.new("RGBA", (ANCHO * TILE_SIZE, ALTO * TILE_SIZE), (255, 255, 255,255))
    terrenos = calcular_terrenos(mapa_terreno)
    for terreno in terrenos:
        capa = calcular_matriz_capa(mapa_terreno, terreno)
        for y in range(len(capa)):
            for x in range(len(capa[y])):
                if capa[y][x]:
                    mascara_actual = calcular_mascara_borde(capa, x, y)
                    if mascara_actual == 255:
                        tile = random.choice(TERRAINS[terreno]["tiles"])
                    else:
                        border = "patch"
                        for borde,mascara in BORDER_MASKS.items():
                            if (mascara_actual & mascara) == mascara:
                                border = borde
                                break
                        tile = TERRAINS[terreno]["borders"][border]
                    tile_region = (tile['x']*TILE_SIZE, tile['y']*TILE_SIZE, (tile['x'] + 1) * TILE_SIZE, (tile['y'] + 1) * TILE_SIZE)
                    map.paste(
                        tileset.crop(tile_region),
                        (x*TILE_SIZE, y*TILE_SIZE),
                        mask=tileset.crop(tile_region)
                    )
    map.save(name)

mapa = [
    ['water', 'sand','sand', 'sand', 'sand','sand', 'sand'],
    ['grass', 'water','sand', 'sand', 'sand','grass', 'sand'],
    ['grass', 'grass','water', 'sand', 'sand','sand', 'sand'],
    ['grass', 'grass','grass', 'water', 'sand','sand', 'sand'],
    ['grass', 'grass','grass', 'grass', 'water','sand', 'sand'],
    ['grass', 'sand','grass', 'grass', 'grass','water', 'sand'],
    ['grass', 'grass','grass', 'grass', 'grass','grass', 'water'],
]

autotile(mapa, 'examples/test.png')