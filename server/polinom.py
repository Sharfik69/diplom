import numpy as np


def secant(f, x0, eps: float = 1e-7, kmax: int = 1e3):
    x, x_prev, i = x0, x0 + 2 * eps, 0

    while abs(x - x_prev) >= eps and i < kmax:
        x, x_prev, i = x - f(x) / (f(x) - f(x_prev)) * (x - x_prev), x, i + 1

    return x


def bisect_numpy(f, a, b, eps: float = 1e-7):
    n = 1
    p = 0
    while True:
        p = a + (b - a) / 2
        if np.isclose(f(p), 0) or np.abs(a - b) < eps:
            return p
        if f(a) * f(p) < 0:
            b = p
        else:
            a = p
        n += 1


def bisect(f, x0, x1, eps: float = 1e-7):
    f0 = f(x0)
    f1 = f(x1)
    while True:
        xc = (x0 + x1) * 0.5
        fc = f(xc)
        if abs(fc) < eps:
            return xc
        if (f0 < 0) == (fc > 0):
            x1 = xc
            f1 = fc
        else:
            x0 = xc
            f0 = fc


# def f(x):
#     return x ** 2 + 9
#
#
# print(bisect_numpy(f, -10, 10))
