import numpy as np
import noise
import random
from PIL import Image
import argparse
from terrain import TILE_SIZE, TERRAINS, PRIORIDAD_TERRENO
from biome import BIOMES, asignar_terrenos
from settings import *


parser = argparse.ArgumentParser(prog='Map Maker', description='Crea mapas procedurales')
parser.add_argument('-b', '--biome', help="Bioma con umbrales de ruido a utilizar", default="default")

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
                    border = "patch"
                    mascara_actual = calcular_mascara_borde(capa, x, y)
                    if mascara_actual == 255:
                        tile = random.choice(TERRAINS[terreno]["tiles"])
                    else:
                        for borde,mascara in BORDER_MASKS.items():
                            if (mascara_actual & mascara) == mascara:
                                border = borde
                                break
                        tile = TERRAINS[terreno]["borders"][border]
                    if border in CORNERS:
                        for corner in CORNERS:
                            mascara = BORDER_MASKS[corner]
                            if (mascara_actual & mascara) == mascara:
                                tile = TERRAINS[terreno]["borders"][corner]
                                tile_region = (tile['x']*TILE_SIZE, tile['y']*TILE_SIZE, (tile['x'] + 1) * TILE_SIZE, (tile['y'] + 1) * TILE_SIZE)
                                map.paste(
                                    tileset.crop(tile_region),
                                    (x*TILE_SIZE, y*TILE_SIZE),
                                    mask=tileset.crop(tile_region)
                                )
                    else:
                        tile_region = (tile['x']*TILE_SIZE, tile['y']*TILE_SIZE, (tile['x'] + 1) * TILE_SIZE, (tile['y'] + 1) * TILE_SIZE)
                        map.paste(
                            tileset.crop(tile_region),
                            (x*TILE_SIZE, y*TILE_SIZE),
                            mask=tileset.crop(tile_region)
                        )
    map.save(name)

if __name__ == "__main__":
    args = parser.parse_args()
    mapa_elevacion = generar_mapa_ruido(ANCHO, ALTO, ESCALA_RUIDO, OCTAVAS, PERSISTENCIA, LACUNARIDAD, SEMILLA_ELEVACION)
    mapa_humedad = generar_mapa_ruido(ANCHO, ALTO, ESCALA_CLIMA, OCTAVAS, PERSISTENCIA, LACUNARIDAD, SEMILLA_HUMEDAD)
    mapa_temperatura = generar_mapa_ruido(ANCHO, ALTO, ESCALA_CLIMA, OCTAVAS, PERSISTENCIA, LACUNARIDAD, SEMILLA_TEMP)

    bioma = BIOMES[args.biome]

    mapa_terreno = asignar_terrenos(
        mapa_elevacion, mapa_humedad, mapa_temperatura,
        bioma["ELEVACION"], bioma["HUMEDAD"], bioma["TEMPERATURA"]
    )
    autotile(mapa_terreno, f'examples/{args.biome}.png')