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
        #BIT_NOROESTE + BIT_SURESTE,
        #BIT_NORESTE + BIT_SUROESTE,
    ]
    for patch_mask in patch_masks:
        if (mascara & patch_mask) == patch_mask:
            return True
    return False

# --- FUNCIÓN PRINCIPAL DE AUTOTILING ---
def calcular_mascara_borde(mapa, x, y, recursive=True):
    """
    Calcula una máscara de 4 bits para cada celda de 'target_terreno' 
    que bordea a 'terreno_central'.

    Retorna un nuevo mapa donde:
    - 0 significa que no requiere borde.
    - Un valor entre 1 y 15 es el código de la máscara (0001 a 1111 binario).
    """

    # if recursive:
    #     mascara_actual = calcular_mascara_borde(mapa, x, y, False)
    #     if es_parche(mascara_actual):
    #         return mascara_actual
    
    # Lista de direcciones y sus desplazamientos (dy, dx) y valores de bit
    VECINOS = [
        (-1, 0, BIT_NORTE),  # Norte
        ( 0, 1, BIT_ESTE),   # Este
        ( 1, 0, BIT_SUR),    # Sur
        ( 0,-1, BIT_OESTE),   # Oeste
        (-1, -1, BIT_NOROESTE),  # Norte
        ( 1, -1, BIT_SUROESTE),   # Este
        ( -1, 1, BIT_NORESTE),    # Sur
        ( 1, 1, BIT_SURESTE)   # Oeste
    ]

    target_terreno = mapa[y][x]
    mascara_actual = 0
                
    # Comprobamos los 8 vecinos cardinales
    for dy, dx, bit_valor in VECINOS:
        ny, nx = y + dy, x + dx  # Coordenadas del vecino
                    
        if 0 <= ny < ALTO and 0 <= nx < ANCHO:                        
            terreno_vecino = mapa[ny][nx]
                            
            # if recursive:
            #     mascara_vecino = calcular_mascara_borde(mapa, nx, ny, False)
            #     if es_parche(mascara_vecino):
            #         terreno_vecino = calcular_terreno_base(mapa, nx, ny)

            if target_terreno != terreno_vecino and PRIORIDAD_TERRENO[
                terreno_vecino] < PRIORIDAD_TERRENO[target_terreno]:
                mascara_actual += bit_valor
                                
    return mascara_actual

def calcular_terreno_base(mapa, x, y):
    terreno_actual = mapa[y][x]
    candidato = terreno_actual
    mascara_actual = calcular_mascara_borde(mapa, x, y, False)
    if es_parche(mascara_actual):
        candidato = None
    VECINOS = [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
        (1, 1),
    ]
    for dx,dy in VECINOS:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < ANCHO and 0 <= ny < ALTO:
            mascara_vecino = calcular_mascara_borde(mapa, nx, ny, False) & 15
            if es_parche(mascara_vecino):
                for dx2,dy2 in VECINOS:
                    nx2 = nx + dx2
                    ny2 = ny + dy2
                    if 0 <= nx2 < ANCHO and 0 <= ny2 < ALTO:
                        if not candidato or PRIORIDAD_TERRENO[
                            mapa[ny2][nx2]] < PRIORIDAD_TERRENO[candidato]:
                            candidato = mapa[ny2][nx2]
            elif not candidato or PRIORIDAD_TERRENO[mapa[ny][nx]] < PRIORIDAD_TERRENO[candidato]:
                    candidato = mapa[ny][nx]
    return candidato

def autotile(mapa_terreno, name):
    tileset = Image.open("tileset.png").convert("RGBA")
    map = Image.new("RGBA", (ANCHO * TILE_SIZE, ALTO * TILE_SIZE), (255, 255, 255,255))
    for y in range(len(mapa_terreno)):
        for x in range(len(mapa_terreno[y])):
            mascara = calcular_mascara_borde(mapa_terreno, x, y)
            mascara_simple = mascara & 15
            terreno_base = calcular_terreno_base(mapa_terreno, x, y)
            if mascara == 0 or (
                mascara_simple != 15 and PRIORIDAD_TERRENO[
                    mapa_terreno[y][x]] < PRIORIDAD_TERRENO[terreno_base]
            ) or terreno_base == mapa_terreno[y][x]:
                tile = random.choice(TERRAINS[mapa_terreno[y][x]]["tiles"])
            else:
                border = "patch"
                # if (x == 2 and y == 3):
                #     print(mascara)
                if es_parche(mascara):
                    border = "patch"
                elif mascara_simple == 9 or \
                    (mascara & 40) == 40 or \
                    (mascara & 65) == 65:
                    border = "top_left"
                elif mascara_simple == 3 or \
                    (mascara & 18) == 18 or\
                    (mascara & 129) == 129:
                    border = "top_right"
                elif mascara_simple == 12 or \
                    (mascara & 136) == 136 or\
                    (mascara & 20) == 20:
                    border = "bottom_left"
                elif mascara_simple == 6 or \
                    (mascara & 66) == 66 or\
                    (mascara & 36) == 36:
                    border = "bottom_right"
                elif mascara_simple == 1:
                    border = "top"
                elif mascara_simple == 8:
                    border = "left"
                elif mascara_simple == 2:
                    border = "right"
                elif mascara_simple == 4:
                    border = "bottom"
                elif mascara == 16:
                    border = "upper_left_diagonal"
                elif mascara == 32:
                    border = "upper_right_diagonal"
                elif mascara == 64:
                    border = "lower_left_diagonal"
                elif mascara == 128:
                    border = "lower_right_diagonal"
                tile = random.choice(TERRAINS[terreno_base]["tiles"])
                tile_region = (tile['x']*TILE_SIZE, tile['y']*TILE_SIZE, (tile['x'] + 1) * TILE_SIZE, (tile['y'] + 1) * TILE_SIZE)
                map.paste(
                    tileset.crop(tile_region),
                    (x*TILE_SIZE, y*TILE_SIZE)
                )
                tile = TERRAINS[mapa_terreno[y][x]]["borders"][border]
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
    ['grass', 'sand','grass', 'grass', 'water','sand', 'sand'],
    ['grass', 'sand','grass', 'grass', 'grass','water', 'sand'],
    ['grass', 'grass','grass', 'grass', 'grass','grass', 'water'],
]

autotile(mapa, 'examples/test.png')