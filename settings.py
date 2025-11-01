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