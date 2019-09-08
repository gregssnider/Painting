""" Palettes of soft, low-chroma colors. 10 hues, 5 values per hue, plus gray.

By keeping the chroma low, color harmony is ensured. Extending this on the fly
to create a more colorful palette (e.g. by boosting the chroma of red) is easy.

Hues:
    Since 5YR is generally considered the hue of most skin, we include that as
    our base and pick up all of the "5" hues, yielding 10 of the 40 Munsell
    hues.

Values:
    Only 5 from the Munsell scale: 1, 3, 5, 7, 9. Note that Munsell uses an
    11 value scale, from 0 to 10, so that the values 1 and 9 are not pure black
    or pure white, respectively.

Chroma:
    Peak chroma is assigned to value 7, declining linearly to values 1 and 9.
    This is appropriate for light colored objects, such as Caucasian skin, but
    is not appropriate for darker objects. For example, black skin has a
    peak chroma near the value of 5. Chroma can be toned down on the fly by
    blending in the appropriate value of gray.

    Here's the map for a peak chroma value of 4. This map is sometimes called
    the "chroma curve" for an object with a local color of chroma 4 at value 7:

         value     chroma
         -----     ------
           9          1
           7          4
           5          3
           3          2
           1          1

The swatches are broken into two palettes, a "warm" and a "cool".

Warm palette layout. Within each hue, values are {1, 3, 5, 7, 9).

      +----+----+----+----+----+----+----+----+----+----+
      |           5RP          |           5Y           |
      +----+----+----+----+----+----+----+----+----+----+
      |           5R           |           5GY          |
      +----+----+----+----+----+----+----+----+----+----+
      |           5YR          |          gray          |
      +----+----+----+----+----+----+----+----+----+----+


Cool palette layout. Within each hue, values are {1, 3, 5, 7, 9).

      +----+----+----+----+----+----+----+----+----+----+
      |           5G           |           5PB          |
      +----+----+----+----+----+----+----+----+----+----+
      |           5BG          |           5P           |
      +----+----+----+----+----+----+----+----+----+----+
      |           5B           |          gray          |
      +----+----+----+----+----+----+----+----+----+----+

The above can be conveniently laid out in two Procreate palettes. But these
are concatenated here to make it easier to use when placing this directly
on the canvas:

             warms                cools
      +---------+---------+---------+---------+
      |  5RP    |   5Y    |   5G    |  5PB    |
      +---------+---------+---------+---------+
      |  5R     |  5GY    |   5BG   |  5P     |
      +---------+---------+---------+---------+
      |  5YR    |  gray   |   5B    |  gray   |
      +---------+---------+---------+---------+


"""
from typing import Tuple
from tkinter import Tk, Canvas, PhotoImage, mainloop
from color import munsell


# Hues. "gray" is a dummy hue for grayscale with chroma 0 (gray has no hue).
gray = '10R'
hue_layout = (
    ('5RP', '5Y', '5G', '5PB'),
    ('5R', '5GY', '5BG', '5P'),
    ('5YR', gray, '5B', gray),
)

# Values
values = (1, 3, 5, 7, 9)

# Chroma curve for Munsell values 0 - 10. We linearly interpolate down from
# peak chroma at value 7 to a chroma of 0 at values -1 and 10
peak_chroma = 3.0
peak_value = 7
chroma_curve = [peak_chroma for i in range(11)]
for val in (0, 1, 2, 3, 4, 5, 6):
    chroma_curve[val] = peak_chroma * ((val + 1) / peak_value)
for val in (8, 9, 10):
    chroma_curve[val] = peak_chroma * ((11 - val) / peak_value)

# Palette size
PALETTE_ROWS = 3
PALETTE_COLUMNS = 20
SWATCH_SIZE = 50
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
window.title('Soft Palette')
canvas = Canvas(window, width=PALETTE_WIDTH, height=PALETTE_HEIGHT, bg='#000000')
canvas.pack()

file = '../palettes/soft_color_palette.png'
print('creating', file)
img = PhotoImage(width=PALETTE_WIDTH, height=PALETTE_HEIGHT)
canvas.create_image((PALETTE_WIDTH // 2, PALETTE_HEIGHT // 2), image=img,
                    state='normal')
canvas.image = img  # To prevent garbage collection

for row in range(PALETTE_ROWS):
    print('ROW --------------------------------')
    for col in range(PALETTE_COLUMNS):
        hue_column = col // 5
        hue = hue_layout[row][hue_column]
        value = 2 * (col % 5) + 1
        chroma = chroma_curve[value] if hue != gray else 0
        print('hue value chroma', hue, value, chroma)
        rgb_color = munsell.to_rgb(hue, value, chroma)
        if rgb_color is not None:
            paint_swatch(img, row, col, rgb_color)
        else:
            print('missing rgb_color!!!')
canvas.image.write(file, format='png')
print('done.')

mainloop()
