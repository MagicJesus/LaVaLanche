import numpy as np
from laspy.file import File

# file = File("./out.las", mode = 'r')
# file = File("D:\\Mapy Tatr\\A\\M-34-101-A-a-1-1-2.las")
# point_records = file.points # ndarray z w wszystkimi punktami
# UWAGA! Wiersze i poszczególne rekordy są typu numpy.void (cokolwiek to narazie znaczy)

# print(type(point_records))
# print(type(point_records[0][0]))
# print("Liczba parametrów dla punktu:", len(point_records[0][0]))
# print(point_records[0][0])
#
# # Odczytujemy współrzędne
# print(type(file.x))
# print(len(file.x))
# print(file.x.shape)
# print(file.header.max)
# print(file.header.min)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# wyciągniemy co 10-ty punkt i spróbujemy nanieść na wykres 3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection = '3d')
# ax.scatter(file.x[::1000], file.y[::1000], file.z[::1000], c = file.z[::1000], cmap = 'gray')
# ax.scatter(file.x[1000000:1500000:1000], file.y[1000000:1500000:1000], file.z[1000000:1500000:1000], c = 'r')
# plt.axis('off')
# plt.show()


def extract_data(map_name):
    print(map_name)
    if '101' in map_name:
        path = "D:\\Mapy Tatr\\A\\" + map_name.rstrip()
    elif '100' in map_name:
        path = "D:\\Mapy Tatr\\B\\" + map_name.rstrip()
    open_map = File(path)

    data = [open_map.header.max, open_map.header.min]
    return data

