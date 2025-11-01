# Map Maker

## Description

This project is a python procedural RPG map generator based on Perlin noise generation and predefined tilesets.

### Noise maps

First we generate three Perlin noise maps with a number of values of tiles, associated to elevation, humidity and temperature.

The characteristics of these noise maps can be configured through the settings.py file. The bigger the size of the map, the more variation in terrain there can be, and the lower the frequency the larger the biomes of the same terrain will be.

### Biome thresholds

Once we have our three noise maps, we need to translate the values of elevation, humidity and temperature to an actual terrain type.

We use biomes with a predisposition to certain types of terrain (water and sand for beach biome and so forth). To achieve this, each predefined biome maps the three random variables to terrain maps through predefined thresholds. Both the thresholds and the logic to apply them need to match the tileset that we will later used, but can also be adjusted independently through the biome.py file.

### Autotiling

After applying the thresholds, we have a matrix of terrains but we need the actual tiles to generate a png map image.

In order to generate the image we use tileset.png and terrain.py to map tilecrops to terrain tiles.

This information, alongside with a terrain priority is later used to determine which tiled needs to be applied given the selected terrain and its adjacencies, and the outcome image is saved on the examples file with name of the specified biome.

## Installation

We previously need Python3, pip and a C++ compiler (g++ for linux or visual studio for windows) to install the Perlin noise library. Then we can run:

```
python -m pip install -r requirements.txt
```

## Usage

After the installation we can run the script with:

```
python main.py
```

Or if you want to specify a particular biome instead of using the default one:

```
python main.py -b <biome_name>
```