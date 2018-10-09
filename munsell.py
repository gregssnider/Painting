""" Munsell color space.

The data file real_sRGB.ods is from https://www.rit.edu/science/pocs/renotation.
This was converted to real_sRGB.csv for easier parsing by Python.

The colour-science library does not appear to be reliable for this type of
conversion (see https://stackoverflow.com/questions/3620663/
color-theory-how-to-convert-munsell-hvc-to-rgb-hsb-hsl) so instead I do bilinear
interpolation of the Munsell data from RIT.

"""
from typing import Tuple, Dict
import math
import numpy
import colour


def create_color_dict() -> Dict[Tuple[str, int, int], Tuple[int, int, int]]:
    """ Create the dictionary mapping (hue, value, chroma) to (r, g, b). """
    file = 'real_sRGB.csv'
    dictionary = dict()
    with open(file, 'r') as f:
        lines = f.read().splitlines()
        for i in range(1, len(lines)):
            _, hue, value, chroma, *_, r, g, b = lines[i].split(',')
            dictionary[(hue, value, chroma)] = (r, g, b)
    return dictionary


munsell_to_rgb = create_color_dict()


def to_rgb(hue: str, value: int, chroma: float) -> Tuple[int, int, int]:
    """ Convert a Munsell (hue, value, chroma) color spec to RGB using
    linear interpolation

    Args:
        hue: E.g. "7.5YR"
        value: Value from 1 (darkest) to 9 (lightest)
        chroma: Value greater than zero (in principle unbounded).

    Returns:
        RGB triple
    """
    if value < 1 or value > 9:
        raise ValueError('value must be in the interval [1, 9]')

    # Round chroma up and down to nearest multiple of 2.
    bottom_chroma = math.floor(chroma)
    if bottom_chroma % 2 == 1:
        bottom_chroma -= 1
    top_chroma = math.ceil(chroma)
    if top_chroma % 2 == 1:
        top_chroma += 1
    if top_chroma == bottom_chroma:
        return munsell_to_rgb[(hue, value, top_chroma)]

    # Linear interpolation
    assert top_chroma - bottom_chroma == 2
    bottom_rgb = munsell_to_rgb[(hue, value, bottom_chroma)]
    top_rgb = munsell_to_rgb[(hue, value, top_chroma)]

    bottom_
    diff_rgb = tuple(numpy.subtract(top_rgb, bottom_rgb))



def from_rgb(rgb: Tuple[int, int, int]) -> str:
    """ Convert standard RGB color to a Munsell string.

    Args:
        rgb: RGB channels, each in the interval [0, 255]

    Returns:
        Munsell string for color.
    """
    C = colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']
    srgb = (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    munsell = colour.xyY_to_munsell_colour(
        colour.XYZ_to_xyY(colour.sRGB_to_XYZ(srgb, C)))
    return munsell


if __name__ == '__main__':
    munsell = '7.5YR 2/2'
    rgb = to_rgb('7.5YR', 2, 2)
    recovered_munsell = from_rgb(rgb)
    print(munsell, '-->', rgb, '-->', recovered_munsell)

    '''
    hue = '5.0YR'
    for value in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0):
        for chroma in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0):
            color = hue + ' ' + str(value) + '/' + str(chroma)
            rgb = to_rgb(color)
            print(color, '==>', rgb)
    '''
