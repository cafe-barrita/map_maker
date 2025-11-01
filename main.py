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
def calcular_mascara_borde(mapa, x, y, recursive=True):
    """
    Calcula una máscara de 4 bits para cada celda de 'target_terreno' 
    que bordea a 'terreno_central'.

    Retorna un nuevo mapa donde:
    - 0 significa que no requiere borde.
    - Un valor entre 1 y 15 es el código de la máscara (0001 a 1111 binario).
    """
    # --- BITS DE MÁSCARA (Norte, Este, Sur, Oeste) ---
    # Se utiliza un bit para cada dirección cardinal
    BIT_NORTE = 1  # 2^0
    BIT_ESTE = 2   # 2^1
    BIT_SUR = 4    # 2^2
    BIT_OESTE = 8  # 2^3
    
    # Lista de direcciones y sus desplazamientos (dy, dx) y valores de bit
    VECINOS = [
        (-1, 0, BIT_NORTE),  # Norte
        ( 0, 1, BIT_ESTE),   # Este
        ( 1, 0, BIT_SUR),    # Sur
        ( 0,-1, BIT_OESTE)   # Oeste
    ]

    target_terreno = mapa[y][x]
    mascara_actual = 0
                
    # Comprobamos los 4 vecinos cardinales
    for dy, dx, bit_valor in VECINOS:
        ny, nx = y + dy, x + dx  # Coordenadas del vecino
                    
        # 1. Comprobamos límites: ignorar si está fuera del mapa
        if 0 <= ny < ALTO and 0 <= nx < ANCHO:
                        
            terreno_vecino = mapa[ny, nx]
            igual_terreno = target_terreno == terreno_vecino
                            
            # 2. Lógica de Borde:
            # Comprobar si el vecino es un patch
            if recursive:
                mascara_vecino = calcular_mascara_borde(mapa, nx, ny, False)
                terreno_vecino = calcular_terreno_base(mapa, nx, ny)
                # Si es un patch, invertir la lógica
                # Por ejemplo, un parche de agua es como si fuese arena
                if mascara_vecino in [5,7,10,11,13,14, 15]:
                    igual_terreno = target_terreno == terreno_vecino
            # Si el vecino NO es el mismo terreno, se requiere un borde
            # *o* si el vecino es el 'terreno central' que queremos bordear.
                            
            # En este caso: si el vecino NO es hierba, necesitamos un borde.
            if not igual_terreno:
                mascara_actual += bit_valor
                                
    return mascara_actual

def calcular_terreno_base(mapa, x, y):
    terreno_actual = mapa[y][x]
    candidato = terreno_actual
    VECINOS = [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1)
    ]
    for dx,dy in VECINOS:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < ANCHO and 0 <= ny < ALTO:
            mascara_vecino = calcular_mascara_borde(mapa, nx, ny, False)
            if mascara_vecino == 15:
                candidato = None
                for dx2,dy2 in VECINOS:
                    nx2 = nx + dx2
                    ny2 = ny + dy2
                    if 0 <= nx2 < ANCHO and 0 <= ny2 < ALTO:
                        if not candidato:
                            candidato = mapa[ny2][nx2]
                        elif PRIORIDAD_TERRENO[mapa[ny2][nx2]] < PRIORIDAD_TERRENO[candidato]:
                            candidato = mapa[ny2][nx2]
            elif mascara_vecino in [5,7,10,11,13,14]:
                for dx2,dy2 in VECINOS:
                    nx2 = nx + dx2
                    ny2 = ny + dy2
                    if 0 <= nx2 < ANCHO and 0 <= ny2 < ALTO:
                        if PRIORIDAD_TERRENO[mapa[ny2][nx2]] < PRIORIDAD_TERRENO[candidato]:
                            candidato = mapa[ny2][nx2]
            elif PRIORIDAD_TERRENO[mapa[ny][nx]] < PRIORIDAD_TERRENO[candidato]:
                candidato = mapa[ny][nx]
    return candidato

def autotile(mapa_terreno, name):
    tileset = Image.open("tileset.png").convert("RGBA")
    map = Image.new("RGBA", (ANCHO * TILE_SIZE, ALTO * TILE_SIZE), (255, 255, 255,255))
    for y in range(len(mapa_terreno)):
        for x in range(len(mapa_terreno[y])):
            mascara = calcular_mascara_borde(mapa_terreno, x, y)
            terreno_base = calcular_terreno_base(mapa_terreno, x, y)
            if mascara == 0 or (
                mascara != 15 and PRIORIDAD_TERRENO[
                    mapa_terreno[y][x]] < PRIORIDAD_TERRENO[terreno_base]
            ) or terreno_base == mapa_terreno[y][x]:
                tile = random.choice(TERRAINS[mapa_terreno[y][x]]["tiles"])
            else:
                border = "patch"
                if mascara == 9:
                    border = "top_left"
                elif mascara == 1:
                    border = "top"
                elif mascara == 3:
                    border = "top_right"
                elif mascara == 8:
                    border = "left"
                elif mascara == 2:
                    border = "right"
                elif mascara == 12:
                    border = "bottom_left"
                elif mascara == 4:
                    border = "bottom"
                elif mascara == 6:
                    border = "bottom_right"
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