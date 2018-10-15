""" Generate half of the Munsell hue palettes (every other one), the '5' and
'10' variants.

Intermediate hues can be mixed on canvas as needed.

"""
from typing import Tuple
from tkinter import Tk, Canvas, PhotoImage, mainloop
import munsell

# Supported Munsell hues (half of the total), ordered clockwise.
hues = ('5R', '10R', '5YR', '10YR', '5Y', '10Y', '5GY', '10GY', '5G', '10G',
        '5BG', '10BG', '5B', '10B', '5PB', '10PB', '5P', '10P', '5RP', '10RP')

# Supported Munsell values.
values = (9, 8, 7, 6, 5, 4, 3, 2, 1)

# Supported Munsell chromas, all even (not all of them exist for every hue).
CHROMAS = 13
chromas = range(2, 26, 2)

# Palette size.
PALETTE_ROWS = len(values)
PALETTE_COLUMNS = CHROMAS
SWATCH_SIZE = 25
PALETTE_WIDTH = PALETTE_COLUMNS * SWATCH_SIZE
PALETTE_HEIGHT = PALETTE_ROWS * SWATCH_SIZE


def paint_swatch(image: PhotoImage, row: int, column: int,
                 color: Tuple[int, int, int]):
    """ Paint a color swatch on the palette in (row, column). """
    if column < 0 or column >= PALETTE_COLUMNS:
        raise ValueError('bad column')
    if row < 0 or row >= PALETTE_ROWS:
        raise ValueError('bad row')
    x_start = column * SWATCH_SIZE
    y_start = row * SWATCH_SIZE
    for x in range(x_start, x_start + SWATCH_SIZE - 1):
        for y in range(y_start, y_start + SWATCH_SIZE - 1):
            image.put("#%02x%02x%02x" % color, (x, y))


window = Tk()
window.title('Color Palette')
canvas = Canvas(window, width=PALETTE_WIDTH, height=PALETTE_HEIGHT, bg='#000000')
canvas.pack()

for hue in hues:
    file = 'palettes/' + hue + '.png'
    print('creating', file)
    img = PhotoImage(width=PALETTE_WIDTH, height=PALETTE_HEIGHT)
    canvas.create_image((PALETTE_WIDTH // 2, PALETTE_HEIGHT // 2), image=img,
                        state='normal')
    canvas.image = img  # To prevent garbage collection
    for column, chroma in enumerate(chromas):
        for row, value in enumerate(values):
            rgb_color = munsell.to_rgb(hue, value, chroma)
            if rgb_color is not None:
                paint_swatch(img, row, column, rgb_color)
    canvas.image.write(file, format='png')

mainloop()
