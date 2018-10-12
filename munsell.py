""" Munsell color space.

The data file real_sRGB.ods is from https://www.rit.edu/science/pocs/renotation.
This was converted to real_sRGB.csv for easier parsing by Python.

The colour-science library does not appear to be reliable for this type of
conversion (see https://stackoverflow.com/questions/3620663/
color-theory-how-to-convert-munsell-hvc-to-rgb-hsb-hsl) so instead I do linear
interpolation of the Munsell data from RIT.

The computed Munsell color is found by searching for the nearest RGB neighbor
of the given color in the Munsell color dictionary.

"""
from typing import Tuple, Dict
import math
import numpy


# Grayscale values in RGB. From: http://www.andrewwerth.com/color/
# Munsell uses an 11 value scale, from 0 (black) to 10 (white). For painting,
# we use only values 1 through 9.
gray_rgb_values = [
    (0, 0, 0),
    (34, 34, 34),
    (58, 58, 58),
    (82, 82, 82),
    (107, 107, 107),
    (136, 136, 136),
    (162, 162, 162),
    (181, 181, 181),
    (202, 202, 202),
    (232, 232, 232),
    (255, 255, 255)
]

def create_color_dict() -> Dict[Tuple[str, int, int], Tuple[int, int, int]]:
    """ Create the dictionary mapping (hue, value, chroma) to (r, g, b). """
    file = 'real_sRGB.csv'
    dictionary = dict()
    hues = set()
    with open(file, 'r') as f:
        lines = f.read().splitlines()
        for i in range(1, len(lines)):
            _, hue, value, chroma, *_, r, g, b = lines[i].split(',')
            value = int(value)
            chroma = int(chroma)
            r = int(r)
            g = int(g)
            b = int(b)
            dictionary[(hue, value, chroma)] = (r, g, b)
            hues.add(hue)

    # Add grayscale values for each hue.
    chroma = 0
    for hue in hues:
        for value in range(11):
            dictionary[(hue, value, chroma)] = gray_rgb_values[value]

    def average(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) \
        -> Tuple[int, int, int]:
        """ Compute the average of two rgb tuples. """
        r = int((rgb1[0] + rgb2[0] + 0.5) / 2)
        g = int((rgb1[1] + rgb2[1] + 0.5) / 2)
        b = int((rgb1[2] + rgb2[2] + 0.5) / 2)
        return r, g, b

    # Interpolate to create odd chroma values.
    for (hue, value, chroma) in tuple(dictionary.keys()):
        low_rgb = dictionary[(hue, value, chroma)]
        high_rgb = dictionary.get((hue, value, chroma + 2))
        if high_rgb is not None:
            dictionary[(hue, value, chroma + 1)] = average(low_rgb, high_rgb)
    return dictionary


munsell_to_rgb = create_color_dict()


def distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """ Compute the Euclidean distance between two rgb tuples. """
    r = rgb1[0] - rgb2[0]
    g = rgb1[1] - rgb2[1]
    b = rgb1[2] - rgb2[2]
    return math.sqrt(r**2 + g**2 + b**2)


def from_rgb(rgb: Tuple[int, int, int]) -> (str, int, int):
    """ Return the nearest munsell color for an RGB tuple. """
    min_distance = 1e50
    min_color = None
    for munsell, rgb_ in munsell_to_rgb.items():
        dist = distance(rgb, rgb_)
        if dist < min_distance:
            min_distance = dist
            min_color = munsell
    return min_color


def to_rgb(hue: str, value: int, chroma: int) -> Tuple[int, int, int]:
    """ Convert a Munsell (hue, value, chroma) color spec to RGB using
    linear interpolation

    Args:
        hue: E.g. "7.5YR"
        value: Value from 1 (darkest) to 9 (lightest)
        chroma: Value greater than zero (in principle unbounded).

    Returns:
        RGB triple
    """
    if chroma == 0:
        return gray_rgb_values[value]
    else:
        return munsell_to_rgb[(hue, value, chroma)]



if __name__ == '__main__':
    pass
    '''
    munsell = '7.5YR 2/2'
    rgb = to_rgb('7.5YR', 2, 2)
    recovered_munsell = from_rgb(rgb)
    print(munsell, '-->', rgb, '-->', recovered_munsell)


    hue = '5.0YR'
    for value in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0):
        for chroma in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0):
            color = hue + ' ' + str(value) + '/' + str(chroma)
            rgb = to_rgb(color)
            print(color, '==>', rgb)
    '''
