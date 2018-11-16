""" Fourier approach to generating Perlin / Simplex noise for use as
a universal texture. The base code is from:
https://www.reddit.com/r/proceduralgeneration/comments/5rood4/
cubic_noise_a_simple_alternative_to_perlin_noise/

"""
import numpy as np
import matplotlib.pyplot as plt
import math
import imageio
from PIL import Image
from numpy.fft import fft2, ifft2, ifftshift, fftshift

def noise(size: int, power=-1.0) -> np.ndarray:
    """ Generate 1 / f^power noise. """
    offsets = np.fft.fftshift(np.arange(size, dtype='complex128') - size / 2)
    [xvals, yvals] = np.meshgrid(offsets, offsets)
    dist_sq = xvals * xvals + yvals * yvals
    f = lambda r: 0j if r == 0.0 else np.power(r, 0.5 * power)
    noise = np.real(np.fft.ifft2(
        np.exp(2j * math.pi * np.random.rand(size, size)) *
        np.vectorize(f)(dist_sq)))
    return noise


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


def gaussian2d(size: int, sigma=1.0, mu=0.0) -> np.ndarray:
    x, y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
    d = np.sqrt(x * x + y * y)
    g = np.exp(-((d - mu) ** 2 / (2.0 * sigma ** 2)))
    return g


def gaussian_spectral_noise(size: int, sigma=1.0, mu=0.0) -> np.ndarray:
    raw_spectrum = gaussian2d(size, sigma, mu)
    spectrum = ifftshift(raw_spectrum)
    spectrum[0, 0] = 0
    noise = np.real(ifft2(spectrum))
    return np.real(raw_spectrum)



size = 1024


plt.title('gaussian spectral noise')
plt.imshow(gaussian_spectral_noise(size, sigma=size/2), cmap='gray')
plt.show()

plt.title('1 / f noise')
plt.imshow(noise(size, power=-0.5), cmap='gray')  # 1/f noise
plt.show()

plt.title('white noise')
plt.imshow(noise(size, power=-1.0), cmap='gray')  # white noise
plt.show()

plt.title('pink noise')
plt.imshow(noise(size, power=-1.5), cmap='gray')  # pink noise
plt.show()

plt.title('brown noise')
plt.imshow(noise(1024, power=-2.0), cmap='gray')  # brown noise
plt.show()

