"""
Próba użycia pyvista na rzeczywistej chmurze punktów.
"""

# 1. Załadowanie pliku .las

import numpy as np
from laspy.file import File
from pathlib import Path
home = str(Path.home()) # '/home/twoja_nazwa_użytkownika'

file = File(home + "/Sym/M-34-101-A-c-3-2-2.las", mode = 'r')
point_records = file.points # ndarray z w wszystkimi punktami

x = file.x[::100000]
y = file.y[::100000]
z = file.z[::100000]

points = [list(point) for point in zip(x, y, z)]
points = np.array(points)

# 2. Triangulacja
import pyvista as pv

cloud = pv.PolyData(points)
# cloud.plot(point_size = 15)

surf = cloud.delaunay_2d()

print(surf.faces) # [cell0_nverts, cell0_v0, cell0_v1, cell0_v2, cell1_nverts, ...]
print(surf.points) # wszystkie punkty
print(surf.face_normals) # wektory normalne

surf.plot(show_edges = True)
