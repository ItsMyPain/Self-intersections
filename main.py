from intersept import visualize, intersect
from models import Grid, Triangle

grid = Grid()
# grid.load_from_file('cube.vtk')
grid.load_from_file('intersected_sphere.vtk')

final = Grid()
stop = 200
offset = 0
eps = 1e-7
N = 0

for first in grid.triangles:
    for second in grid.triangles:
        fs = intersect(first, second, eps)
        sf = intersect(second, first, eps)

        if fs and sf:
            if offset == 0:

                N += 2
                # print(fs)
                # print(sf)
                f = list(fs.values())
                s = list(sf.values())

                if 'a' in sf:
                    final.add_triangle(Triangle(first.C, f[0], first.B))
                    final.add_triangle(Triangle(first.C, f[0], first.A))
                    final.add_triangle(Triangle(first.B, f[0], sf['a']))
                    final.add_triangle(Triangle(first.A, f[0], sf['a']))
                elif 'b' in sf:
                    final.add_triangle(Triangle(first.A, f[0], first.C))
                    final.add_triangle(Triangle(first.A, f[0], first.B))
                    final.add_triangle(Triangle(first.C, f[0], sf['b']))
                    final.add_triangle(Triangle(first.B, f[0], sf['b']))
                elif 'c' in sf:
                    final.add_triangle(Triangle(first.B, f[0], first.A))
                    final.add_triangle(Triangle(first.B, f[0], first.C))
                    final.add_triangle(Triangle(first.A, f[0], sf['c']))
                    final.add_triangle(Triangle(first.C, f[0], sf['c']))

                if 'a' in fs:
                    final.add_triangle(Triangle(second.C, s[0], second.B))
                    final.add_triangle(Triangle(second.C, s[0], second.A))
                    final.add_triangle(Triangle(second.B, s[0], fs['a']))
                    final.add_triangle(Triangle(second.A, s[0], fs['a']))
                elif 'b' in fs:
                    final.add_triangle(Triangle(second.A, s[0], second.C))
                    final.add_triangle(Triangle(second.A, s[0], second.B))
                    final.add_triangle(Triangle(second.C, s[0], fs['b']))
                    final.add_triangle(Triangle(second.B, s[0], fs['b']))
                elif 'c' in fs:
                    final.add_triangle(Triangle(second.B, s[0], second.A))
                    final.add_triangle(Triangle(second.B, s[0], second.C))
                    final.add_triangle(Triangle(second.A, s[0], fs['c']))
                    final.add_triangle(Triangle(second.C, s[0], fs['c']))

            else:
                offset -= 2

            # final.add_triangle(Triangle(fs[0], sf[0], second.B))
            # final.add_triangle(Triangle(fs[0], sf[0], second.C))
            #
            # final.add_triangle(Triangle(sf[0], second.B, second.A))
            # final.add_triangle(Triangle(second.A, sf[0], second.C))

            # final.add_triangle(first)
            # final.add_triangle(second)
            # print('Найден')
        if N >= stop:
            break
    if N >= stop:
        break

final.save_to_file('out.vtk')

visualize('out.vtk')
# visualize('intersected_sphere.vtk')

# for first in grid.triangles:
#     final.add_triangle(first)

# TR = Triangle(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0))
# grid.add_triangle(TR)
