"""
Poor man's color simplex noise generator.

Takes a grayscale simplex noise image file and creates a color version.
Algorithm:
  red: take input simplex image and apply to R channel
  green: rotate input image 90 degrees and apply to G channel
  blue: rotate input image 180 degress and apply to B channel

"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


if __name__ == '__main__':
    filename = '../data/simplex_noise_16_octaves.jpg'
    outfile =  '../data/color_simplex_noise_16_octaves.jpg'
    image = np.asarray(Image.open(filename))  # [:, :]

    # Create red, green, and blue channels from grayscale by rotation.
    red = image[:, :, 0]
    green = np.rot90(red)
    blue = np.rot90(green)

    # Combine into a color image file and write it out.
    color_simplex = np.stack((red, green, blue), axis=2)
    plt.imsave(outfile, color_simplex)
    print(image.shape, color_simplex.shape)
