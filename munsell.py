""" Munsell color space. """
from typing import Tuple
import colour


def to_rgb(munsell: str) -> Tuple[int, int, int]:
    """ Convert a Munsell color string to RGB. From:
    https://stackoverflow.com/questions/3620663/
    color-theory-how-to-convert-munsell-hvc-to-rgb-hsb-hsl

    Args:
        munsell: Color definition, e.g. '4.2YR 8.1/5.3'

    Returns:
        RGB components, each an integer in the interval [0, 255]
    """
    # The first step is to convert the *MRS* colour to *CIE xyY*
    # colourspace.
    xyY = colour.munsell_colour_to_xyY(munsell)

    # We then perform conversion to *CIE xyY* tristimulus values.
    XYZ = colour.xyY_to_XYZ(xyY)

    # The last step will involve using the *Munsell Renotation System*
    # illuminant which is *CIE Illuminant C*:
    #     http://nbviewer.ipython.org/github/colour-science/
    #     colour-ipython/blob/master/notebooks/colorimetry/
    #     illuminants.ipynb#CIE-Illuminant-C
    # It is necessary in order to ensure white stays white when
    # converting to *sRGB* colourspace and its different whitepoint
    # (*CIE Standard Illuminant D65*) by performing chromatic
    # adaptation between the two different illuminant.
    C = colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['C']
    srgb = colour.XYZ_to_sRGB(XYZ, C)
    rgb = (int(round(255 * srgb[0])),
           int(round(255 * srgb[1])),
           int(round(255 * srgb[2])))
    return rgb


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
    munsell = '4.2YR 8.1/5.3'
    rgb = to_rgb(munsell)
    recovered_munsell = from_rgb(rgb)
    print(munsell, '-->', rgb, '-->', recovered_munsell)
