""" Basic skin palettes for Caucasian, Asian, and Black skin.

The local hue of skin, regardless of ethnicity, is ~5YR. The chroma curve for
a given person peaks at one value larger than the value of the local hue. See
the youtube video by Paul Foxton: https://www.youtube.com/watch?v=B4ziC_3icKw
and also see his web site: http://www.learning-to-see.co.uk/

Following is the approximate chroma curve for a Caucasian of average
complexion from Foxton's video. Note that Munsell uses 11 values, 0 through 10,
but we use only 1 through 9 for painting.

    value   chroma     use
      9       1
      8       3     reflected light
      7       5     brightest, full light (center light)
      6       4     local color
      5       3     half tone (this is in the light)
      4       2     reflected light
      3       1     core shadow
      2       1
      1       1

Asian skin has a similar value/chroma scale.

Foxton says that Jamaican black skin is two values lower, so it would have
the following curve:

    value   chroma     use
      9       1
      8       1
      7       2
      6       3     reflected light
      5       5     brightest, full light (center light)
      4       4     local color
      3       3     half tone
      2       2     reflected light
      1       1     core shadow

To account for hue variability, hues on either side of 5YR are also generated.
This yields a palette of three hues and nine values, with chromas as listed
above. Two palettes are generated, one for dark skin, one for light skin.
Darker or lighter palettes could also be generated

"""
from typing import Tuple
from tkinter import Tk, Canvas, PhotoImage, mainloop
import munsell

# Chroma scales, indexed by Munsell value (0 through 10)
pale_chroma = [0, 1, 1, 1, 2, 3, 4, 5, 3, 1, 0]
dark_chroma = [0, 1, 2, 3, 4, 5, 3, 2, 1, 1, 0]

# Hue variation: reddish, orangish, yellowish, grayscale (dummy hue)
hues = ('10R', '5YR', '10YR', '2.5YR')

# Palette size. Top row used for reddish skin, middle row for orangish skin,
# bottom row for yellowish skin, last row for grayscale.
PALETTE_ROWS = 4
PALETTE_COLUMNS = 9
SWATCH_SIZE = 25
PALETTE_WIDTH = PALETTE_COLUMNS * SWATCH_SIZE
PALETTE_HEIGHT = PALETTE_ROWS * SWATCH_SIZE

# Skin palette files.
PALE_FILE = 'pale_skin_palette.jpg'
DARK_FILE = 'dark_skin_palette.jpg'


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
window.title('Skin & Hair Palette')
canvas = Canvas(window, width=PALETTE_WIDTH, height=PALETTE_HEIGHT, bg='#000000')
canvas.pack()
img = PhotoImage(width=PALETTE_WIDTH, height=PALETTE_HEIGHT)
canvas.create_image((PALETTE_WIDTH // 2, PALETTE_HEIGHT // 2), image=img, state='normal')
canvas.image = img  # To prevent garbage collection

for scale in (pale_chroma, dark_chroma):
    file = PALE_FILE if scale == pale_chroma else DARK_FILE
    for row in range(len(hues)):
        hue = hues[row]
        for value in range(1, 10):
            if row != PALETTE_ROWS - 1:
                chroma = scale[value]
            else:
                chroma = 0
            column = value - 1
            rgb_color = munsell.to_rgb(hue, value, chroma)
            paint_swatch(img, row, column, rgb_color)
    canvas.image.write(file)

mainloop()
