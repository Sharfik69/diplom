from PIL import Image
import numpy as np


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

    def save_grey_scale(self, name):
        self.img.save(name)


    def create_B_matrix(self):
        for i in range(1, len(self.P) - 3):
            for j in range(1, len(self.P[0]) - 3):
                p = self.P[i:i+4, j:j+4]
                self.B[i, j] = np.transpose(self.K) * p * self.K

    def work_with_b(self):
        for q, val in self.B.items():
            g_x = val[0][1]
            g_y = val[1][0]

            c = np.zeros(shape=(4, 4))

            for i in range(4):
                for j in range(4):
                    c[i][j] = g_y ** i * g_x ** j * val[i][j]

            self.C[q[0], q[1]] = c

            self.h = []

            for i in range(7):
                a = 0



    def test(self):
        print(self.P)