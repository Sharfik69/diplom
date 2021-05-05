def secant(f, x0, eps: float = 1e-7, kmax: int = 1e3):
    x, x_prev, i = x0, x0 + 2 * eps, 0

    while abs(x - x_prev) >= eps and i < kmax:
        x, x_prev, i = x - f(x) / (f(x) - f(x_prev)) * (x - x_prev), x, i + 1

    return x

def bisect(f, x0,x1, eps: float = 1e-7):
    f0 = f(x0)
    f1 = f(x1)
    while True:
        xc = (x0+x1)*0.5
        fc = f(xc)
        if abs(fc)<eps:
            return xc
        if (f0<0)==(fc>0):
            x1=xc
            f1=fc
        else:
            x0=xc
            f0=fc
# def f(x):
#     return x ** 2 - 9
#
# print(secant(f, -1000))
