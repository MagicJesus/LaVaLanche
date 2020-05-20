"""
Przykład użycia biblioteki pyvista:
- teselacja;
- obliczenie nachyleń.
"""

import numpy as np
import pyvista as pv

points = np.array([[1, 0, 0], [-1, 0, 0], [-1, 0, 1], [0, 1, 0]])

cloud = pv.PolyData(points)
# cloud.plot(point_size = 15)

surf = cloud.delaunay_2d()
# 0, 1, 2, 3      4, 5, 6, 7,          8, 9, 10, 11
print(surf.faces) # [cell0_nverts, cell0_v0, cell0_v1, cell0_v2, cell1_nverts, ...]
print(surf.points) # wszystkie punkty
print(surf.face_normals) # wektory normalne

surf.plot(show_edges = True)

# obliczymy nachylenie
xy_normal = np.array([0, 0, 1])

normal_1 = surf.face_normals[0]
nach_1 = np.degrees(np.arccos(np.dot(xy_normal, normal_1)))
print(f"Nachylenie 1. (powinno wynosić 90 stopni): {nach_1} stopni")

normal_2 = surf.face_normals[1]
nach_2 = np.degrees(np.arccos(np.dot(xy_normal, normal_2)))
print(f"Nachylenie 2. (powinno wynosić 180 stopni): {nach_2} stopni")
