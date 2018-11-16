"""
Whitening filter. Ported from cct from HPE.

A whitening filter for natural images that flattens the spectrum (on
average).

This uses the fact that natural images have an amplitude spectrum of 1/f,
so this is essentially a filter with the inverse spectrum. The algorithm
is from Bruno Olshausen:

    http://redwood.berkeley.edu/bruno/npb261b/lab2/lab2.html

(c) Copyright 2016 Hewlett Packard Enterprise Development LP

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import numpy as np
import math
from .matlab_functions import index_range, meshgrid, cart2pol
from numpy.fft import fft2, ifft2, fftshift, ifftshift


# Dictionary of spectral whitening filters:  shape -> filter
_spectral_filter_cache = {}


def whitening_filter(size: int) -> np.ndarray:
    # Create whitening filter in the frequency domain.
    # Frequencies run from -N/2 to N/2 - 1, inclusive
    f = index_range(-(size // 2), 1, size // 2)
    fx, fy = meshgrid(f, f)
    theta, rho = cart2pol(fx, fy)

    # Window the 1/f function with a circular Gaussian to (1) clip the
    # corners of the frequency domain; and (2) low-pass filter the highest
    # frequencies to minimize the effects of noise.
    gauss = np.zeros((size, size))

    def sq(x: float):
        return x * x

    for row in range(size):
        for col in range(size):
            gauss[row, col] = math.exp(-0.5 * sq(rho[row, col] / \
                                                 (0.7 * size // 2)))
    gauss = gauss * rho
    max_value = np.max(gauss)
    gauss /= max_value
    return fftshift(gauss)


def whiten(image: np.ndarray) -> np.ndarray:
    if image.dtype not in [np.float32, np.float64]:
        raise ValueError('image must be a "float" image')
    if len(image.shape) == 2:
        image_fft = fft2(image)
        return ifft2(whiten_spectral(image_fft)).real
    elif len(image.shape) == 3:
        red_fft = fft2(image[:, :, 0])
        green_fft = fft2(image[:, :, 1])
        blue_fft = fft2(image[:, :, 2])

        # Whitening removes DC component. Add 0.5 to approximate that for
        # color images.
        return np.stack(
            (ifft2(whiten_spectral(red_fft)).real + 0.5,
             ifft2(whiten_spectral(green_fft)).real + 0.5,
             ifft2(whiten_spectral(blue_fft)).real + 0.5
             ),
            axis=2
        )
    else:
        raise ValueError('image must be 2D, color or grayscale')




def whiten_spectral(image: np.ndarray) -> np.ndarray:
    if image.dtype not in (np.complex64, np.complex128):
        raise ValueError('Image must be in the frequency domain.')
    if len(image.shape) != 2:
        raise ValueError('Image must be 2D.')
    if image.shape[0] != image.shape[1]:
        raise ValueError('Image must be square.')
    size = image.shape[0]
    key = image.shape
    if key not in _spectral_filter_cache:
        _spectral_filter_cache[image.shape] = whitening_filter(image.shape[0])
    white_filter = _spectral_filter_cache[image.shape]
    return white_filter * image
