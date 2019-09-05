""" Noise for painting.

1/f noise
Olshausen noise
pink noise

"""
import numpy as np
import PIL
import torch
from torch import Tensor
import dft
import images
import whiten
import laplacian
import complex


def save_image(tensor: Tensor, filename: str):
    assert images.is_image(tensor)
    min = torch.min(tensor)
    max = torch.max(tensor)
    visual = ((tensor - min) / (max - min)).squeeze(0)
    array = (visual.numpy() * 255).astype(np.uint8)
    image = PIL.Image.fromarray(array)
    image.save(filename)


# Create complex random Gaussian field, Gaussian in both real and imaginary.
size = 2048
noise = np.random.normal(size=(size, size))
real = torch.from_numpy(noise).float().unsqueeze(0)
noise = np.random.normal(size=(size, size))
imag = torch.from_numpy(noise).float().unsqueeze(0)
spectral_gaussian = complex.cast(real, imag)
save_image(real, '_noise_gaussian.png')

# Olshausen noise, approximates human visual system response
olshausen_filter = whiten.Filters.inverse(size)
product = complex.multiply(spectral_gaussian, olshausen_filter)
result = complex.real_(dft.invert2d(product))
save_image(result, '_noise_olshausen.png')

# Our base filter is the inverse Laplacian which corresponds to 1 / f noise
base_filter = laplacian.Filters.inverse(size)
product = complex.multiply(spectral_gaussian, base_filter)
result = complex.real_(dft.invert2d(product))
save_image(result, '_noise_1_over_f.png')

images.display(
    ('olshausen spectrum', complex.real_(olshausen_filter)),
    ('laplacian spectrum', complex.real_(base_filter))
)


filter = whiten.Filters.inverse(size)
#filter = laplacian.Filters.inverse(size)
'''
print('filter shape', filter.shape)
product = complex.multiply(tensor, filter)
print('product shape', product.shape)

images.display(complex.real_(tensor), result)
images.display(complex.real_(tensor), save_file='junk.png')
'''