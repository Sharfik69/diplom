import numpy as np
from PIL import Image

from polinom import secant, bisect, bisect_numpy


class ImgWorker:
    def __init__(self, img_name):
        self.img_name = img_name
        self.img = Image.open(img_name)

        if self.img.mode != 'RGB':
            self.img = self.img.convert('RGB')

        self.img = self.img.convert('L')
        self.P = np.array(self.img)

        self.K = np.array([
            [-1 / 16, 1 / 8, 1 / 4, -1 / 2],
            [9 / 16, -11 / 8, -1 / 4, 3 / 2],
            [9 / 16, 11 / 8, -1 / 4, -3 / 2],
            [-1 / 16, -1 / 8, 1 / 4, 1 / 2]
        ])
        self.K_t = self.K.transpose()

        self.B = {}
        self.C = {}
        self.h = {}
        self.l_max_f = {}

        self.zero = 0
        self.coord = []

    def save_grey_scale(self, name):
        self.img.save(name)

    def create_B_matrix(self):
        for i in range(len(self.P) - 3):
            for j in range(len(self.P[0]) - 3):
                p = self.P[i:i + 4, j:j + 4]
                self.B[i, j] = np.matmul(np.matmul(self.K_t, p), self.K)

    def work_with_b(self):

        def h_kink(l, h):
            ans = 0
            h_2 = [koef * my_h for koef, my_h in zip([2, 6, 12, 20, 30], h[2:])]
            for i, val in enumerate(h_2):
                ans += l ** i * val
            return ans

        for q, val in self.B.items():
            g_x = val[0][1]
            g_y = val[1][0]

            if g_x == 0 and g_y == 0:
                continue

            c = np.zeros(shape=(4, 4))

            pow_g_x = {i: g_x ** i for i in range(4)}
            pow_g_y = {i: g_y ** i for i in range(4)}

            for i in range(4):
                for j in range(4):
                    c[i][j] = pow_g_y[i] * pow_g_x[j] * val[i][j]

            self.C[q[0], q[1]] = c

            h = [c[0][0], c[1][0] + c[0][1], c[2][0] + c[1][1] + c[0][2], c[3][0] + c[2][1] + c[1][2] + c[0][3],
                 c[3][1] + c[2][2] + c[1][3], c[3][2] + c[2][3], c[3][3]]

            self.h[q[0], q[1]] = h

            if g_y == 0:
                l_max = 0.5 / g_x
            elif g_x == 0:
                l_max = 0.5 / g_y
            else:
                l_max = 0.5 / max(g_y, g_x)

            self.l_max_f[q[0], q[1]] = l_max

            def f(x_):
                return 2 * h[2] + x_ * (6 * h[3] + x_ * (12 * h[4] + x_ * (20 * h[5] + x_ * 30 * h[6])))

            def h_first_(x_):
                res = h[1] + 2 * h[2] * x_ + 3 * h[3] * (x_ ** 2) + 4 * h[4] * (x_ ** 3) + 5 * h[5] * (x_ ** 4) + 6 * h[
                    6] * (x_ ** 5)
                return res

            a, b = f(l_max), f(-l_max)

            # if a * b < 0:
            if (a > 0 and b < 0) or (a < 0 and b > 0):
                self.zero += 1
                # x = secant(f, -10000)
                # x = bisect(f, -l_max, l_max)

                # if abs(f(x)) <= 0.00000009 and l_max > x > -l_max:
                #     print(f(x))
                #     self.coord.append(q)
                roots = list(np.roots([30 * h[6], 20 * h[5], 12 * h[4], 6 * h[3], 2 * h[2]]))
                h_first_max, dot_ = -1, 0
                for root in roots:
                    if type(root) is type(np.complex128()):
                        continue
                    if -l_max < root < l_max:
                        h_first = h_first_(root)
                        if abs(h_first) > h_first_max:
                            h_first_max = h_first
                            dot_ = root

                if h_first_max != -1:
                    self.coord.append(q)

        # print(self.zero)
        # for i in self.coord:
        #     print(i)

    def test(self):
        img2 = self.img
        img2 = img2.convert('RGB')
        for i in self.coord:
            img2.putpixel((i[1] + 1, i[0] + 1), (155, 155, 55))
            img2.putpixel((i[1] + 2, i[0] + 1), (155, 155, 55))
            img2.putpixel((i[1] + 1, i[0] + 2), (155, 155, 55))
            img2.putpixel((i[1] + 2, i[0] + 2), (155, 155, 55))

        file_name = '{}_response.png'.format(self.img_name.split('/')[-1].split('.')[0])

        img2.save('static/img/{}'.format(file_name))

        return file_name
