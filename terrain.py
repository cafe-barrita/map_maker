import numpy as np
from settings import ALTO, ANCHO

def asignar_terrenos(mapa_elevacion, mapa_humedad, mapa_temperatura, bioma):
    """Asigna un tipo de terreno (string) a cada celda basado en el umbral de elevación."""
    mapa_terrenos = np.empty_like(mapa_elevacion, dtype=object)
    
    for y in range(ALTO):
        for x in range(ANCHO):
            elevacion = mapa_elevacion[y][x]
            humedad = mapa_humedad[y][x]
            temp = mapa_temperatura[y][x]
            
            for terreno in bioma["terrains"]:
                if elevacion <= terreno["height"] \
                    and humedad <= terreno["humidity"] \
                    and temp <= terreno["temperature"]:
                    mapa_terrenos[y][x] = terreno["name"]
                    break
                
    return mapa_terrenos

# def autotile(mapa_terreno, tileset, bioma):
#     #tileset = Image.open("tileset.png").convert("RGBA")
#     tile_size = tileset["tile_size"]
#     map = Image.new("RGBA", (ANCHO * TILE_SIZE, ALTO * TILE_SIZE), (255, 255, 255,255))
#     terrenos = bioma["terrain_priority"].keys()
#     for terreno in terrenos:
#         capa = calcular_matriz_capa(mapa_terreno, terreno)
#         for y in range(len(capa)):
#             for x in range(len(capa[y])):
#                 if capa[y][x]:
#                     border = "patch"
#                     mascara_actual = calcular_mascara_borde(capa, x, y)
#                     if mascara_actual == 255:
#                         tile = random.choice(TERRAINS[terreno]["tiles"])
#                     else:
#                         for borde,mascara in BORDER_MASKS.items():
#                             if (mascara_actual & mascara) == mascara:
#                                 border = borde
#                                 break
#                         tile = TERRAINS[terreno]["borders"][border]
#                     if border in CORNERS:
#                         for corner in CORNERS:
#                             mascara = BORDER_MASKS[corner]
#                             if (mascara_actual & mascara) == mascara:
#                                 tile = TERRAINS[terreno]["borders"][corner]
#                                 tile_region = (tile['x']*TILE_SIZE, tile['y']*TILE_SIZE, (tile['x'] + 1) * TILE_SIZE, (tile['y'] + 1) * TILE_SIZE)
#                                 map.paste(
#                                     tileset.crop(tile_region),
#                                     (x*TILE_SIZE, y*TILE_SIZE),
#                                     mask=tileset.crop(tile_region)
#                                 )
#                     else:
#                         tile_region = (tile['x']*TILE_SIZE, tile['y']*TILE_SIZE, (tile['x'] + 1) * TILE_SIZE, (tile['y'] + 1) * TILE_SIZE)
#                         map.paste(
#                             tileset.crop(tile_region),
#                             (x*TILE_SIZE, y*TILE_SIZE),
#                             mask=tileset.crop(tile_region)
#                         )
#     if bioma.get("MAX_OBJECTS"):
#         for i in range(random.randint(0, bioma["MAX_OBJECTS"])):
#             terreno,objeto = random.choice(bioma["OBJECTS"])
#             tiles = OBJETOS[objeto]
#             posicion = buscar_posicion_valida(mapa_terreno, terreno, len(tiles[0]), len(tiles))
#             if posicion:
#                 y = posicion[1]
#                 for row in tiles:
#                     x = posicion[0]
#                     for tile in row:
#                         tile_region = (
#                             tile['x']*TILE_SIZE,
#                             tile['y']*TILE_SIZE,
#                             (tile['x'] + 1) * TILE_SIZE,
#                             (tile['y'] + 1) * TILE_SIZE
#                         )
#                         map.paste(
#                             tileset.crop(tile_region),
#                             (x*TILE_SIZE, y*TILE_SIZE),
#                             mask=tileset.crop(tile_region)
#                         )
#                         x += 1
#                     y += 1
#     map.save(name)
