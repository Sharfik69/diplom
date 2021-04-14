def secant(f, x0, eps: float = 1e-7, kmax: int = 1e3):
    x, x_prev, i = x0, x0 + 2 * eps, 0

    while abs(x - x_prev) >= eps and i < kmax:
        x, x_prev, i = x - f(x) / (f(x) - f(x_prev)) * (x - x_prev), x, i + 1

    return x


# def f(x):
#     return x ** 2 - 9
#
# print(secant(f, -1000))