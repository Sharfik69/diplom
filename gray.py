from PIL import Image
import numpy as np
from polinom import secant

class ImgWorker:
    def __init__(self, img_name):
        self.img = Image.open(img_name)

        if self.img.mode != 'RGB':
            self.img = self.img.convert('RGB')

        self.img = self.img.convert('L')

        self.P = np.array(self.img)

        self.K = np.array([
            [-1/16, 1/8, 1/4, -1/2],
            [9/16, -11/8, -1/4, 3/2],
            [9/16, 11/8, -1/4, -3/2],
            [-1/16, -1/8, 1/4, 1/2]
        ])

        self.B = {}
        self.C = {}
        self.h = {}

        self.zero = 0
        self.coord = []

    def save_grey_scale(self, name):
        self.img.save(name)


    def create_B_matrix(self):
        f = open('list_1.txt', 'w')
        for i in range(len(self.P) - 3):
            for j in range(len(self.P[0]) - 3):
                p = self.P[i:i+4, j:j+4]
                f.write(str(p[0][0]) + ' ')
                self.B[i, j] = np.transpose(self.K) * p * self.K
            f.write('\n')

    def work_with_b(self):

        def h_kink(l, h):
            h_2 = [koef * my_h for koef, my_h in zip([2, 6, 12, 20, 30], h[2:])]
            ans = 0
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

            h = []

            for i in range(4):
                a = 0
                x, y = i, 0

                while x != -1:
                    a += c[x][y]
                    x -= 1
                    y += 1
                h.append(a)

            for j in range(1, 4):
                a = 0
                x, y = 3, j

                while y != 4:
                    a += c[x][y]
                    x -= 1
                    y += 1
                h.append(a)

            self.H = h



                # for j in range(i + 1):
                #     x, y = j, j - i
                #     a += c[j][i - j]
                #     h.append(a)

            l_max = 0.5 / max(g_y, g_x)

            a, b = h_kink(l_max, h), h_kink(-l_max, h)

            if a * b < 0:
                self.zero += 1
                h_2 = h[2:]
                def f(x):
                    return 2 * h_2[0] + 6 * h_2[1] * x + 12 * h_2[2] * x ** 2 + 20 * h_2[3] * x ** 3 + 30 * h_2[4] * x ** 4

                x = secant(f, -100000)

                if abs(f(x) - 0) <= 0.00000009:
                    self.coord.append(q)

        print(self.zero)
        for i in self.coord:
            print(i)

    def test(self):
        img2 = self.img
        img2 = img2.convert('RGB')
        for i in self.coord:
            img2.putpixel((i[1], i[0]), (155, 155, 55))
        img2.save('img/test test.png')
