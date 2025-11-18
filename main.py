import numpy as np
import noise
import random
import json
from PIL import Image
import argparse
from terrain import asignar_terrenos
from settings import *


parser = argparse.ArgumentParser(prog='Map Maker', description='Crea mapas procedurales')
parser.add_argument('-t', '--tileset', help="Tileset a utilizar", default="tileset")
parser.add_argument('-b', '--biome', help="Bioma con umbrales de ruido a utilizar", default="beach")

def generar_mapa_ruido(ancho, alto, escala, octavas, persistencia, lacunaridad, semilla):
    """Genera una matriz 2D de ruido Perlin, escalada a [0, 1]."""
    mapa_ruido = np.zeros((alto, ancho))
    
    for y in range(alto):
        for x in range(ancho):
            # Normalizamos las coordenadas (x, y) por la escala para calcular el ruido
            valor_ruido = noise.pnoise2(
                x * escala,
                y * escala,
                octaves=octavas,
                persistence=persistencia,
                lacunarity=lacunaridad,
                repeatx=1024, # Permite un mapa "tileable" (sin costuras)
                repeaty=1024,
                base=semilla
            )
            # El pnoise2 devuelve un valor de [-1, 1], lo escalamos a [0, 1]
            mapa_ruido[y][x] = (valor_ruido + 1) / 2
            
    return mapa_ruido

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

def calcular_matriz_capa(mapa_terreno, terreno, prioridad_terreno):
    mapa_capa = np.zeros((ALTO, ANCHO))
    for y in range(ALTO):
        for x in range(ANCHO):
            if prioridad_terreno[terreno] <= prioridad_terreno[mapa_terreno[y][x]]:
                mapa_capa[y][x] = 1
    return mapa_capa

# def buscar_posicion_valida(mapa_terreno, terreno, obj_x, obj_y, margen=1):
#     for i in range(MAX_ATTEMPTS):
#         nx = random.randint(margen, ANCHO - (obj_x + margen))
#         ny = random.randint(margen, ALTO - (obj_y + margen))
#         valid = True
#         for y in range(ny - margen, ny + obj_y + margen):
#             for x in range(nx - margen, nx + obj_x + margen):
#                 if mapa_terreno[y][x] != terreno:
#                     valid = False
#                     break
#             if not valid:
#                 break
#         if valid:
#             return (nx,ny)
#     return None

def autotile(mapa_terreno, tileset, bioma):
    prioridad_terreno = bioma["terrain_priority"]
    terrains = sorted(prioridad_terreno, key=lambda k: prioridad_terreno[k])
    tilemap = {
        "layers": []
    }
    id = 1
    for terrain in terrains:
        layer = []
        capa = calcular_matriz_capa(mapa_terreno, terrain, prioridad_terreno)
        for y in range(len(capa)):
            for x in range(len(capa[y])):
                if capa[y][x]:
                    border = "patch"
                    mascara_actual = calcular_mascara_borde(capa, x, y)
                    if mascara_actual == 255:
                        tile = random.choice(tileset["terrains"][terrain]["tiles"])
                    else:
                        for borde,mascara in BORDER_MASKS.items():
                            if (mascara_actual & mascara) == mascara:
                                border = borde
                                break
                        tile = tileset["terrains"][terrain]["borders"][border]
                    layer.append(tile)
                else:
                    layer.append(0)
        tilemap["layers"].append(
            {
                "id": id,
                "height": ALTO,
                "width": ANCHO,
                "name": terrain,
                "visible": True,
                "opacity": 1,
                "type": "tilelayer",
                "x": 0,
                "y": 0,
                "data": layer
            }
        )
        id += 1
    # TODO cosas
    return tilemap

if __name__ == "__main__":
    args = parser.parse_args()

    mapa_elevacion = generar_mapa_ruido(ANCHO, ALTO, ESCALA_RUIDO, OCTAVAS, PERSISTENCIA, LACUNARIDAD, SEMILLA_ELEVACION)
    mapa_humedad = generar_mapa_ruido(ANCHO, ALTO, ESCALA_CLIMA, OCTAVAS, PERSISTENCIA, LACUNARIDAD, SEMILLA_HUMEDAD)
    mapa_temperatura = generar_mapa_ruido(ANCHO, ALTO, ESCALA_CLIMA, OCTAVAS, PERSISTENCIA, LACUNARIDAD, SEMILLA_TEMP)

    bioma = json.load(open(f'config/{args.tileset}/{args.biome}.json', 'r'))
    tileset = json.load(open(f'config/{args.tileset}/tileset.json', 'r'))

    mapa_terreno = asignar_terrenos(
        mapa_elevacion, mapa_humedad, mapa_temperatura, bioma
    )

    json.dump(autotile(mapa_terreno, tileset, bioma), open(f'assets/{args.tileset}_{args.biome}.json', 'w'), indent=2)
