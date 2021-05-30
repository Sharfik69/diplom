import time

import gray

start_time = time.time()

img = gray.ImgWorker('img/Lena.jpg')

# img.save_grey_scale('img/letter_gray.png')

img.create_B_matrix()

img.work_with_b()

img.test()
# x = np.array([[1, 2, 3, 4, 23, 13, 15],
#               [5, 6, 7, 8, 24, 23, 5],
#               [9, 10, 11, 12, 25, 11, 12],
#               [13, 14, 15, 16, 26, 432, 234],
#               [17, 18, 19, 20, 27, 232, 222]])
#
# print(x[0:4, 1:5])
print("--- %s seconds ---" % (time.time() - start_time))
