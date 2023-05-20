from intersept import visualize, intersect
from models import Grid, Triangle

grid = Grid()
# grid.load_from_file('cube.vtk')
grid.load_from_file('intersected_sphere.vtk')

final = Grid()
stop = 2

for first in grid.triangles:
    for second in grid.triangles:
        bl = intersect(first, second, 1e-7)
        if bl:
            print(bl)
            # final.add_triangle(Triangle(bl[0], first.B, first.C))
            # final.add_triangle(Triangle(first.A, bl[0], first.C))
            final.add_triangle(first)
            final.add_triangle(second)
            # print('Найден')
        if final.n_triangles >= stop:
            break
    if final.n_triangles >= stop:
        break

final.save_to_file('out.vtk')

visualize('out.vtk')
# visualize('intersected_sphere.vtk')

# for first in grid.triangles:
#     final.add_triangle(first)

# TR = Triangle(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0))
# grid.add_triangle(TR)
