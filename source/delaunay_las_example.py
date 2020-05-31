"""
Próba użycia pyvista na rzeczywistej chmurze punktów.

UWAGA!
Informację, czy na danym terenie jest żleb wyciągniemy prosto ze strony z obszarem
"""

# 1. Załadowanie pliku .las
import numpy as np
from laspy.file import File
import os
from pathlib import Path

path = str(Path(os.getcwd()).parent.parent) + "/maps"
# path to np. "/home/ditto/Repos/maps"

file = File(path + "/A/M-34-101-A-c-3-2-2.las", mode = 'r')
# file = File("D:\\maps\\A\\M-34-101-A-c-4-3-2.las", mode = 'r')
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

"""
print(surf.faces) # [cell0_nverts, cell0_v0, cell0_v1, cell0_v2, cell1_nverts, ...]
print(surf.points) # wszystkie punkty
print(surf.face_normals) # wektory normalne

surf.plot(show_edges = True)
"""

p = pv.Plotter()
p.add_mesh(surf, color = "white", show_edges = True)

# --- OBLICZANIE NACHYLENIA ---
# Uwaga! Nie wiemy, czy wektor normalny jest skierowany wgłąb góry czy na powierzchnię (tak, jak byśmy chieli),
# dlatego sprawdziwmy wartość i ewentualnie weźmiemy tę dopełniającą do 180 stopni.

xy_normal = np.array([0, 0, 1])

for i in range(surf.face_normals.shape[0]):
    face_normal = surf.face_normals[i]
    face_slope = np.degrees(np.arccos(np.dot(xy_normal, face_normal)))
    face_slope = face_slope if face_slope < 90 else 180 - face_slope

    """
    # Teraz chcemy zaznaczyć na wykresie trójkąty o nachyleniu 25 - 45 stopni
    v1 = surf.points[surf.faces[i * 4 + 1]]
    v2 = surf.points[surf.faces[i * 4 + 2]]
    v3 = surf.points[surf.faces[i * 4 + 3]]

    vertices = np.array([v1, v2, v3])
    polygon = pv.PolyData(vertices, np.array([3, 0, 1, 2]))

    if face_slope >= 25 and face_slope <= 45:
        c = "red"
    elif face_slope > 45:
        c = "brown"
    else:
        c = "green"

    p.add_mesh(polygon, color = c, opacity = 0.7, lighting = False)
    """

# --- OBLICZANIE EKSPOZYCJI ---
# Teraz obliczmy ekspozycję i zobaczmy, czy wszystko się zgadza (dobrze byłoby wyświelić w danym kolorze
# wszystkie stoki o tym samym nachyleniu).
compass = {}
compass["N"] = np.array([0, 1, 0])
compass["NE"] = np.array([1, 1, 0]) / np.linalg.norm(np.array([1, 1, 0]))
compass["E"] = np.array([1, 0, 0])
compass["SE"] = np.array([1, -1, 0]) / np.linalg.norm(np.array([1, -1, 0]))
compass["S"] = -compass["N"]
compass["SW"] = -compass["NE"]
compass["W"] = -compass["E"]
compass["NW"] = -compass["SE"]

for i in range(surf.face_normals.shape[0]):
    face_normal = surf.face_normals[i]
    face_normal = face_normal if face_normal[2] >= 0 else -face_normal

    flattened_normal = np.array([face_normal[0], face_normal[1], 0])
    flattened_normal = flattened_normal / np.linalg.norm(flattened_normal)

    for dir in compass:
        c = None
        angle = np.degrees(np.arccos(np.dot(compass[dir], flattened_normal)))
        if angle < 15 and dir == "E":
            c = "yellow"
            break
        elif angle < 15 and dir == "NE":
            c = "blue"
            break
        elif angle < 15 and dir == "W":
            c = "brown"
            break

    if c:
        # Teraz zaznaczymy na wykresie stoki o odpowiedniej ekspozycji
        v1 = surf.points[surf.faces[i * 4 + 1]]
        v2 = surf.points[surf.faces[i * 4 + 2]]
        v3 = surf.points[surf.faces[i * 4 + 3]]

        vertices = np.array([v1, v2, v3])
        polygon = pv.PolyData(vertices, np.array([3, 0, 1, 2]))

        p.add_mesh(polygon, color = c, opacity = 0.7)

# Finalizujemy rysowanie wykresu
p.add_axes(xlabel = "East", ylabel = "North", zlabel = "Height")
# compass = "    N   \nW    E\n    S "
# p.add_text(compass, font_size = 8, shadow = True)
p.show(cpos = "xz")
