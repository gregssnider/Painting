""" Spectral noise

    Gaussian spectral noise
    1/f noise
    white noise
    pink noise
    brown noise

The base code is from:
https://www.reddit.com/r/proceduralgeneration/comments/5rood4/
cubic_noise_a_simple_alternative_to_perlin_noise/

"""
import numpy as np
import matplotlib.pyplot as plt
import math
import imageio
import PIL
from numpy.fft import fft2, ifft2, ifftshift, fftshift


def save_image(tensor: np.ndarray, filename: str):
    min = tensor.min()
    max = tensor.max()
    visual = ((tensor - min) / (max - min))
    array = (visual * 255).astype(np.uint8)
    image = PIL.Image.fromarray(array)
    image.save(filename)


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


def color_noise(size: int, power=-1.0) -> np.ndarray:
    """ Generate 1 / f^power noise, in color. """
    r = noise(size, power)
    g = noise(size, power)
    b = noise(size, power)
    image = np.ndarray((size, size, 3))
    image[:, :, 0] = r
    image[:, :, 1] = g
    image[:, :, 2] = b
    return image


def rgb2gray(rgb):
    """ Convert an RGB color image to a grayscale image. """
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


def gaussian2d(size: int, sigma=1.0, mu=0.0) -> np.ndarray:
    """ Construct a 2D Gaussian. """
    x, y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
    d = np.sqrt(x * x + y * y)
    g = np.exp(-((d - mu) ** 2 / (2.0 * sigma ** 2)))
    return g


def gaussian_spectral_noise(size: int, sigma=1.0, mu=0.0) -> np.ndarray:
    """ Generate Gaussian spectral noise. """
    raw_spectrum = gaussian2d(size, sigma, mu)
    spectrum = ifftshift(raw_spectrum)
    spectrum[0, 0] = 0
    noise = np.real(ifft2(spectrum))
    return np.real(raw_spectrum)


if __name__ == '__main__':
    size = 2048
    save_image(noise(size, power=-0.5), 'noise_1_over_f.jpg')
    save_image(noise(size, power=-0.7), 'noise_0.7.jpg')
    save_image(noise(size, power=-1.0), 'noise_white.jpg')
    save_image(noise(size, power=-1.5), 'noise_pink.jpg')
    save_image(noise(size, power=-2.0), 'noise_brown.jpg')

    save_image(color_noise(size, power=-0.5), 'noise_color_1_over_f.jpg')
    save_image(color_noise(size, power=-0.7), 'noise_color_0.7.jpg')
    save_image(color_noise(size, power=-1.0), 'noise_color_white.jpg')
    save_image(color_noise(size, power=-1.5), 'noise_color_pink.jpg')
    save_image(color_noise(size, power=-2.0), 'noise_color_brown.jpg')

    '''
    plt.title('brown noise')
    image = noise(1024, power=-2.0)
    plt.imshow(image, cmap='gray')  # brown noise
    plt.show()
    save_image(image, 'noise_brown.jpg')
    '''
