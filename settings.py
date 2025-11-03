import numpy as np

TILE_SIZE = 32
ANCHO = 48
ALTO = 48

# --- CONFIGURACIÓN DEL MAPA ---
ESCALA_RUIDO = 0.03  # Frecuencia: Cuanto menor, más grandes los "parches" (biomas)
OCTAVAS = 4         # Número de capas de ruido superpuestas
PERSISTENCIA = 0.5  # Amplitud de cada octava sucesiva
LACUNARIDAD = 2.0   # Frecuencia de cada octava sucesiva
SEMILLA_ELEVACION = np.random.randint(0, 2000) # Semilla para resultados reproducibles
# Mapeo de Ruido Perlin para Humedad y Temperatura
SEMILLA_HUMEDAD = np.random.randint(1000, 2000)
SEMILLA_TEMP = np.random.randint(2000, 3000)
ESCALA_CLIMA = 0.03 # Frecuencia un poco más baja para patrones más grandes

# --- BITS DE MÁSCARA (Norte, Este, Sur, Oeste) ---
# Se utiliza un bit para cada dirección cardinal
BIT_NORTE = 1  # 2^0
BIT_ESTE = 2   # 2^1
BIT_SUR = 4    # 2^2
BIT_OESTE = 8  # 2^3
BIT_NOROESTE = 16  # 2^4
BIT_NORESTE = 32   # 2^5
BIT_SUROESTE = 64    # 2^6
BIT_SURESTE = 128  # 2^7