""" Fourier implementation of Wavelet Noise.

Based on the paper "Wavelet Noise" by R. Cook and T. DeRose, Pixar Animation
Studios.

My interpretation of the paper is, perhaps, unorthodox. Here's how I read it:

    1. The function Downsample in Appendix 1 appears to be a truncated
    sinc function, used as a high-quality low-pass filter.

    2. The function Upsample in Appendix 1 appears to be bilinear
    interpolation.

    3. Figure 10a shows a Gaussian spectrum of noise over 12 bands.

These assumptions suggest that perhaps Wavelet / Perlin noise is mimicking the
spectral response of the human visual system. Figure 10a is qualitatively
similar to the "whitening" operation performed by retina / LGN / visual cortex.

So this is a simple experiment to test my hypothesis:
    1. Generate Gaussian noise (spatial domain).
    2. Take its Fourier transform.
    3. Multiply that by Bruno Olshausen's spectral whitening filter.
    4. Take inverse Fourier transform of that product.

We'll see how that compares to Perlin noise.

"""
import numpy as np
import matplotlib.pyplot as plt
import math
import imageio
from PIL import Image
from numpy.fft import fft2, ifft2, ifftshift, fftshift
from filter.whiten import whiten


if __name__ == '__main__':
    # Generate Gaussian noise and display it.
    shape = (2048, 2048)
    noise = np.random.normal(size=shape)
    plt.title('Gaussian noise')
    plt.imshow(noise, cmap='gray')
    plt.show()

    # Whiten it
    whitened_noise = whiten(noise)

    # Display it.
    plt.title('whitened Gaussian noise')
    plt.imshow(whitened_noise, cmap='gray')
    plt.show()
