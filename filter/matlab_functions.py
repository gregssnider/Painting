"""
Emulated Matlab functions, making it easier to port Matlab code to Python.

Ported from the Cognitive Computing Toolkit, HPE.

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
from typing import Tuple


def index_range(first: int, step: int, last: int) -> np.ndarray:
    if last <= first or step <= 0:
        raise ValueError('illegal arguments')

    result = []
    for i in range(first, last, step):
        result.append(i)
    return np.array(result)


def meshgrid(x_domain: np.ndarray, y_domain: np.ndarray) -> Tuple[np.ndarray]:
    if len(x_domain.shape) != 1 or len(y_domain.shape) != 1:
        raise ValueError('inputs must be 1D arrays')

    columns = x_domain.shape[0]
    rows = y_domain.shape[0]
    x = np.zeros((rows, columns))
    for row in range(rows):
        for col in range(columns):
            x[row, col] = x_domain[col]

    y = np.zeros((rows, columns))
    for row in range(rows):
        for col in range(columns):
            y[row, col] = y_domain[row]
    return x, y


def cart2pol(fx: np.ndarray, fy: np.ndarray) -> Tuple[np.ndarray]:
    if len(fx.shape) != 2 or len(fy.shape) != 2:
        raise ValueError('inputs must be 2D arrays')
    if fx.shape != fy.shape:
        raise ValueError('inputs must have the same shape')
    theta = np.zeros(fx.shape)
    rho = np.zeros(fx.shape)
    for row in range(fx.shape[0]):
        for col in range(fx.shape[1]):
            x = fx[row, col]
            y = fy[row, col]
            theta[row, col] = math.atan2(-y, x)
            rho[row, col] = math.sqrt(x * x + y * y)
    return theta, rho


if __name__ == '__main__':
    x_range = index_range(1, 3, 15)
    y_range = index_range(1, 1, 5)
    x, y = meshgrid(x_range, y_range)
    theta, rho = cart2pol(x, y)
    print(x)
    print()
    print(y)
    print()
    print(theta)
    print()
    print(rho)




