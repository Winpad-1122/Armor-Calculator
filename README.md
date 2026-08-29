# Leather Armor Color Calculator

A tool for automatically calculating and rendering dye mixing results for leather armor, leather horse armor, and wolf armor in *Minecraft*.

## Features

- **Real-time Preview**: View armor color changes instantly as you select dyes.
- **Version Support**: Supports the latest versions of both JE and BE.
- **Body Type Support**: Supports adult and baby body types (BE only).
- **Intelligent Sequence Calculation**: Enter a target color, and the program automatically calculates the optimal dye sequence using a genetic algorithm.
- **Batch Rendering**: Render all valid dye sequences within a specified length range at once. Sequence validity follows the latest proposal (Diff/1465560) and its amendment (Diff/1465565) regarding dyed armor render naming conventions on the zh.minecraft.wiki forum.
- **Image Export**: Export the current state as a PNG image. Image naming follows the latest proposal (Diff/1465560) and its amendment (Diff/1465565) regarding dyed armor render naming conventions on the zh.minecraft.wiki forum.
- **Multi-language Support**: Simplified Chinese, Traditional Chinese, English, and Japanese.

## Usage

### Manual Rendering

1. Select the game version
2. Select the armor type
3. Select the body type (armor only) / damage level (wolf armor only)
4. Click dye buttons to add them to the sequence
5. Observe color changes in real time
6. Export the current state as an image

### Batch Rendering

Configure the following in the "Batch Render" dialog:
- Sequence length range
- Target version
- Target armor type and other options

The program will automatically generate all valid combinations and export them as images.

## Texture Copyright Notice

The texture files used in this program (the `textures/` directory) are copyrighted by **Mojang Studios / Microsoft** and are used for non-commercial purposes only, in accordance with the [Minecraft End User License Agreement](https://www.minecraft.net/terms).

This program is a third-party tool and is **not affiliated with Mojang Studios or Microsoft**.

## Dependencies

- Python 3.13.5
- Pillow
- NumPy
- Tkinter (included with Python)

## Run

python ArmorCalculator.py

## Acknowledgments

- Mojang Studios for creating *Minecraft*
- All players and Wiki members who provided feedback and suggestions
