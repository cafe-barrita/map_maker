import numpy as np

ANCHO = 48
ALTO = 48

MAX_ATTEMPTS = 10

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

BORDER_MASKS = {
    "upper_left_diagonal": BIT_NORTE + BIT_NORESTE + BIT_ESTE+ BIT_SURESTE +BIT_SUR + BIT_SUROESTE + BIT_OESTE,
    "upper_right_diagonal": BIT_NORTE + BIT_NOROESTE + BIT_ESTE+ BIT_SURESTE +BIT_SUR + BIT_SUROESTE + BIT_OESTE,
    "lower_left_diagonal": BIT_NORTE + BIT_NORESTE + BIT_ESTE+ BIT_SURESTE +BIT_SUR + BIT_NOROESTE + BIT_OESTE,
    "lower_right_diagonal": BIT_NORTE + BIT_NORESTE + BIT_ESTE+ BIT_NOROESTE +BIT_SUR + BIT_SUROESTE + BIT_OESTE,
    "top": BIT_OESTE + BIT_SUROESTE + BIT_SUR + BIT_SURESTE + BIT_ESTE,
    "left": BIT_NORTE + BIT_NORESTE + BIT_ESTE + BIT_SURESTE + BIT_SUR,
    "right": BIT_NORTE + BIT_NOROESTE + BIT_OESTE + BIT_SUROESTE + BIT_SUR,
    "bottom": BIT_ESTE + BIT_NORESTE + BIT_NORTE + BIT_NOROESTE + BIT_OESTE,
    "top_left": BIT_ESTE + BIT_SURESTE + BIT_SUR,
    "top_right": BIT_OESTE + BIT_SUROESTE + BIT_SUR,
    "bottom_left": BIT_NORTE + BIT_NORESTE + BIT_ESTE,
    "bottom_right": BIT_NORTE + BIT_NOROESTE + BIT_OESTE
}

CORNERS = ["top_left", "top_right", "bottom_left", "bottom_right"]
