""" A low-chroma palette extended with high-chroma warms (red) and cools (blue).

By keeping the chroma low, color harmony is ensured. Extending this on the fly
to create a more colorful palette (e.g. by boosting the chroma of red) is easy.

Hues:
    Since 5YR is generally considered the hue of most skin, we include that as
    our base and pick up all of the "5" hues, yielding 10 of the 40 Munsell
    hues.

Values:
    9 from the Munsell scale: 1, 2, 3, 4, 5, 6, 7, 8, 9. Note that Munsell uses
    an 11 value scale, where 0 is black and 10 is white

Chroma:
    Peak chroma is assigned to value 7, declining linearly to values 1 and 9.
    This is appropriate for light colored objects, such as Caucasian skin, but
    is not appropriate for darker objects. For example, black skin has a
    peak chroma near the value of 5. Chroma can be toned down on the fly by
    blending in the appropriate value of gray.

    Here's an approximate map for a peak chroma value of 4. This map is
    sometimes called the "chroma curve" for an object with a local color of
    chroma 4 at value 7:

         value     chroma
         -----     ------
           9          1
           8          2.5
           7          4
           6          3.5
           5          3
           4          2.5
           3          2
           2          1.5
           1          1

The swatches are broken into 2 rows of low chroma colors, and one row of
grayscale + high chroma colors. The high chroma colors are centered on red,
mimicking the Zorn palette.

Palette layout:

      +-------------+-------------+-------------+-------------+-------------+
      |     5RP     |     5R      |     5YR     |     5Y      |     5GY     |
      +-------------+-------------+-------------+-------------+-------------+
      |     5G      |     5GB     |     5B      |     5PB     |     5P      |
      +-------------+-------------+-------------+-------------+-------------+
      |  grayscale  |             |   hot 5RP   |   hot 5R    |   hot 5YR   |
      +-------------+-------------+-------------+-------------+-------------+

Within each color, values are arranged from 1 to 9:

         1    2    3    4    5    6    7    8    9    <-- value
      +----+----+----+----+----+----+----+----+----+
      |           5G  (example color)              |
      +----+----+----+----+----+----+----+----+----+


"""
from typing import Tuple
from tkinter import Tk, Canvas, PhotoImage, mainloop
from color import munsell
import sys


# Output palette file
file = '../palettes/general_palette.png'

# Hues, ordered from top to bottom by row.
gray = '10R'   # Dummy hue for grayscale.
hues = (
    ('5RP', '5R', '5YR', '5Y', '5GY'),  # row 1: warm colors
    ('5G', '5BG', '5B', '5PB', '5P'),   # row 2: cool colors
    (gray, '5RP', '5R', '5YR', '5Y')    # row 3: grayscale + hot colors
)

# Peak chromas, ordered from top to bottom by row.
peak_chromas = (
    (3, 3, 3, 3, 3),      # row 1
    (3, 3, 3, 3, 3),      # row 2
    (0, 16, 16, 16, 16)   # row 3
)

# Values for each color where chroma peaks. We peak the soft warm and cool
# colors at value 7, and the hot colors at value 5.
peak_values = (
    (7, 7, 7, 7, 7),      # row 1
    (7, 7, 7, 7, 7),      # row 2
    (9, 5, 5, 5, 5)       # row 3
)

# Values, ordered left to right by column.
values = (1, 2, 3, 4, 5, 6, 7, 8, 9)


def adjust_chroma(value: int, peak_chroma: int, peak_value) -> float:
    """ Adjust the chroma to match the chroma curve.

    We linearly interpolate down from peak chroma at value 7 to a chroma of 0
    at values -1.5 and 11.5. This gives a tiny bit of extra chroma on the bottom
    and top which looks nicer, even though it may not be quite accurate
    physiologically. Hey, this is art.
    """
    assert 1 <= value <= 9
    if value == peak_value:
        return peak_chroma
    elif value < peak_value:
        slope = peak_chroma / (peak_value + 1.0)
        return peak_chroma - slope * (peak_value - value)
    else:
        slope = peak_chroma / (peak_value - 10.0)
        return peak_chroma - slope * (peak_value - value)


# Palette size
# Organized
COLOR_ROWS = 3
COLOR_COLUMNS = 5
PALETTE_ROWS = COLOR_ROWS
PALETTE_COLUMNS = COLOR_COLUMNS * len(values)
SWATCH_SIZE = 50
#GAP = 3  # Column gap between darks and lights
#GAP_COLUMN = 5
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
    #if column >= GAP_COLUMN:
    #    x_start += GAP
    y_start = row * SWATCH_SIZE
    for x in range(x_start, x_start + SWATCH_SIZE - 1):
        for y in range(y_start, y_start + SWATCH_SIZE - 1):
            image.put("#%02x%02x%02x" % color, (x, y))


window = Tk()
window.title('General Palette')
canvas = Canvas(window, width=PALETTE_WIDTH, height=PALETTE_HEIGHT, bg='#000000')
canvas.pack()

print('creating', file)
img = PhotoImage(width=PALETTE_WIDTH, height=PALETTE_HEIGHT)
canvas.create_image((PALETTE_WIDTH // 2, PALETTE_HEIGHT // 2), image=img,
                    state='normal')
canvas.image = img  # To prevent garbage collection

# Paint palette background black
img.put("{black}", (0, 0, PALETTE_WIDTH, PALETTE_HEIGHT))

for color_row in range(COLOR_ROWS):
    for color_col in range(COLOR_COLUMNS):
        hue = hues[color_row][color_col]
        peak_value = peak_values[color_row][color_col]
        peak_chroma = peak_chromas[color_row][color_col]
        for index, value in enumerate(values):
            chroma = adjust_chroma(value, peak_chroma, peak_value)
            print('hue', hue, 'value', value, 'chroma', chroma,
                  'peak value', peak_value)
            rgb_color = munsell.to_rgb(hue, value, chroma)
            palette_col = color_col * len(values) + index
            if rgb_color is not None:
                paint_swatch(img, color_row, palette_col, rgb_color)
            else:
                print('missing rgb_color!!!')
canvas.image.write(file, format='png')
print('done.')
sys.exit(0)

mainloop()
