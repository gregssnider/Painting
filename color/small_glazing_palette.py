""" A small palette of Munsell colors: 10 hues, chromas 2, 4, and 6.

This small palette fits within a single Procreate palette (which can hold 30
colors) and is therefore more convenient to use. These are meant to be used
on an "overlay" layer and therefore all swatches have value 5

If higher chromas are required, a second overlay layer can be used, extending
the chroma range to 12.

Intermediate hues can be mixed on canvas as needed.

Since 5YR is generally considered the hue of most skin, we include that as
our base and pick up all of the "5" hues, yielding 10 of the 40 Munsell hues.

Palette layout:

                5R   5YR  5Y   5GY  5G   5GB  5B   5PB  5P   5RP
              +----+----+----+----+----+----+----+----+----+----+
    chroma 2  |    |    |    |    |    |    |    |    |    |    |
              +----+----+----+----+----+----+----+----+----+----+
    chroma 4  |    |    |    |    |    |    |    |    |    |    |
              +----+----+----+----+----+----+----+----+----+----+
    chroma 6  |    |    |    |    |    |    |    |    |    |    |
              +----+----+----+----+----+----+----+----+----+----+

"""
from typing import Tuple
from tkinter import Tk, Canvas, PhotoImage, mainloop
from color import munsell


# Supported Munsell hues (a quarter of the total), ordered clockwise.
hues = ('5R', '5YR', '5Y', '5GY', '5G', '5BG', '5B', '5PB', '5P', '5RP')

# We pick the mid value of 5 so that the overlay layer does not change the value
# of the layer beneath, only its hue and chroma.
value = 5

# Supported Munsell chromas in the palette.
chromas = (2, 4, 6)

# Palette size.
PALETTE_ROWS = len(chromas)
PALETTE_COLUMNS = len(hues)
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

# Include chromas in file name for documentation.
file = '../palettes/munsell_chromas'
for chroma in chromas:
    file += '_' + str(chroma)
file += '.png'
print('creating', file)
img = PhotoImage(width=PALETTE_WIDTH, height=PALETTE_HEIGHT)
canvas.create_image((PALETTE_WIDTH // 2, PALETTE_HEIGHT // 2), image=img,
                    state='normal')
canvas.image = img  # To prevent garbage collection
for column, hue in enumerate(hues):
    for row, chroma in enumerate(chromas):
        rgb_color = munsell.to_rgb(hue, value, chroma)
        if rgb_color is not None:
            paint_swatch(img, row, column, rgb_color)
canvas.image.write(file, format='png')
print('done.')

mainloop()
