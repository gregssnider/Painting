""" Canned Perlin noise

    Self-similar over scale (fractal) so can be used on any size figure or face
    Generated on cpetry.github.io/TextureGenerator-Online with parameters:
        Type: Perlin Noise
        Octaves: 10
        Scale: 100
        Persistence: 1
        Seed: 1

    The output file from the above website i is ../data/PerlinNoise.png
    This program merely displays that file along with its spectrum.
"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


def show_spectrum(image: np.ndarray):
    """ Display the Fourier spectrum of an image. """
    assert len(image.shape) == 2, 'image must be 2D'
    spectral = np.fft.fft2(image)
    spectral[0, 0] = 0  # Kill DC component
    spectrum = np.fft.fftshift(spectral)  # Shift DC to center
    magnitude = np.log(np.abs(spectrum))
    plt.imshow(magnitude, cmap='gray')
    plt.show()


if __name__ == '__main__':
    filename = '../data/PerlinNoise.png'
    image = rgb2gray(np.asarray(Image.open(filename))[:, :])

    plt.title('multi-scale Perlin noise')
    plt.imshow(image, cmap='gray')
    plt.show()

    plt.title('multi-scale Perline spectrum')
    show_spectrum(image)
