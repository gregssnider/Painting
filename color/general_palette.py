""" A low-chroma palette extended with high-chroma warms (red) and cools (blue).

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

The swatches are broken into 3 sections: soft, warm, cool

Soft swatches, max chroma = 3:

         1    3    5    7    9    <-- Value
      +----+----+----+----+----+
      |           5RP          |
      +----+----+----+----+----+
      |           5R           |        ^
      +----+----+----+----+----+        |
      |           5YR          |       Hue
      +----+----+----+----+----+        |
      |           5Y           |        V
      +----+----+----+----+----+
      |           5GY          |
      +----+----+----+----+----+
      |           5G           |
      +----+----+----+----+----+
      |           5BG          |
      +----+----+----+----+----+
      |           5B           |
      +----+----+----+----+----+
      |           5PB          |
      +----+----+----+----+----+
      |           5P           |
      +----+----+----+----+----+
      |        grayscale       |
      +----+----+----+----+----+

In addition to those soft colors, you add either hot swatches or cool swatches
(but not both) to form a harmonious palette. We use red rather than orange
as the peak of the gamut for one reason: lipstick.

Hot swatches, added for a hot gamut:

         1    3    5    7    9      max chroma
      +----+----+----+----+----+
      |           5P           |        6
      +----+----+----+----+----+
      |           5RP          |        9
      +----+----+----+----+----+
      |           5R           |        6
      +----+----+----+----+----+
      |         grayscale      |        0   A spacer
      +----+----+----+----+----+

Cool swatches, added for a cool gamut:

         1    3    5    7    9      max chroma
      +----+----+----+----+----+
      |           5BG          |        6
      +----+----+----+----+----+
      |           5B           |        9
      +----+----+----+----+----+
      |           5PB          |        6
      +----+----+----+----+----+


"""
from typing import Tuple
from tkinter import Tk, Canvas, PhotoImage, mainloop
from color import munsell


# Output palette file
file = '../palettes/general_palette.png'

# Hues, ordered from top to bottom by row.
gray = '10R'   # Dummy hue for grayscale.
hues = (
    # Soft section
    '5RP', '5R', '5YR', '5Y', '5GY', '5G', '5BG', '5B', '5PB', '5P', gray,
    # Warm section, centered on red-purple (closer to red than 5R)
    '5P', '5RP', '5R', gray,
    # Cool section, centered on blue
    '5BG', '5B', '5PB'
)

# Peak chromas, ordered from top to bottom by row.
peak_chromas = (
    # Soft section
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0,
    # Warm section, centered on red
    6, 9, 6, 0,
    # Cool section, centered on blue
    6, 9, 6
)
assert len(peak_chromas) == len(hues)

# Values, ordered left to right by column.
values = (1, 2, 3, 4, 5, 6, 7, 8, 9)
#values = (1, 3, 5, 7, 9)


def adjust_chroma(value: int, peak_chroma: int) -> float:
    """ Adjust the chroma to match the chroma curve.

    We linearly interpolate down from peak chroma at value 7 to a chroma of 0
    at values -1.5 and 11.5. This gives a tiny bit of extra chroma on the bottom
    and top which looks nicer, even though it may not be quite accurate
    physiologically. Hey, this is art.
    """
    peak_value = 7
    if value == peak_value:
        return peak_chroma
    elif value < peak_value:
        return peak_chroma * ((value + 1.5) / peak_value)
    else:
        return peak_chroma * ((11.5 - value) / peak_value)


# Palette size
PALETTE_ROWS = len(hues)
PALETTE_COLUMNS = len(values)
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
window.title('General Palette')
canvas = Canvas(window, width=PALETTE_WIDTH, height=PALETTE_HEIGHT, bg='#000000')
canvas.pack()

print('creating', file)
img = PhotoImage(width=PALETTE_WIDTH, height=PALETTE_HEIGHT)
canvas.create_image((PALETTE_WIDTH // 2, PALETTE_HEIGHT // 2), image=img,
                    state='normal')
canvas.image = img  # To prevent garbage collection

for row in range(PALETTE_ROWS):
    hue = hues[row]
    for col in range(PALETTE_COLUMNS):
        value = values[col]
        chroma = adjust_chroma(value, peak_chromas[row])
        print('hue value chroma', hue, value, chroma)
        rgb_color = munsell.to_rgb(hue, value, chroma)
        if rgb_color is not None:
            paint_swatch(img, row, col, rgb_color)
        else:
            print('missing rgb_color!!!')
canvas.image.write(file, format='png')
print('done.')

mainloop()
