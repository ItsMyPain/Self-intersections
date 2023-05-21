from intersept import visualize, intersect
from models import Grid, Triangle

grid = Grid()
# grid.load_from_file('cube.vtk')
grid.load_from_file('intersected_sphere.vtk')

final = Grid()
stop = 1000
offset = 16
eps = 1e-6
N = 0

for first in grid.triangles:
    for second in grid.triangles:
        fs = intersect(first, second, eps)
        sf = intersect(second, first, eps)

        if fs or sf:
            N += 2
        if fs and sf:
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

        elif fs:
            f = list(fs.values())
            diff = f[0] - f[1]
            norm = diff / abs(diff)
            pr = [first.a * norm / abs(first.a), first.b * norm / abs(first.b), first.c * norm / abs(first.c)]
            idx = pr.index(max(pr, key=lambda x: abs(x)))

            M1, M2 = (f[0], f[1]) if pr[idx] < 0 else (f[1], f[0])

            if idx == 0:
                final.add_triangle(Triangle(first.C, first.A, M1))
                final.add_triangle(Triangle(first.C, first.B, M2))
                final.add_triangle(Triangle(first.C, M1, M2))
                final.add_triangle(Triangle(first.A, first.B, M1))
                final.add_triangle(Triangle(first.B, M1, M2))
            elif idx == 1:
                final.add_triangle(Triangle(first.A, first.B, M1))
                final.add_triangle(Triangle(first.A, first.C, M2))
                final.add_triangle(Triangle(first.A, M1, M2))
                final.add_triangle(Triangle(first.B, first.C, M1))
                final.add_triangle(Triangle(first.C, M1, M2))
            elif idx == 2:
                final.add_triangle(Triangle(first.B, first.C, M1))
                final.add_triangle(Triangle(first.B, first.A, M2))
                final.add_triangle(Triangle(first.B, M1, M2))
                final.add_triangle(Triangle(first.C, first.A, M1))
                final.add_triangle(Triangle(first.A, M1, M2))

            if 'a' in fs and 'b' in fs:
                final.add_triangle(Triangle(second.C, second.A, f[0]))
                final.add_triangle(Triangle(second.C, f[0], f[1]))
                final.add_triangle(Triangle(second.B, f[0], f[1]))
            elif 'b' in fs and 'c' in fs:
                final.add_triangle(Triangle(second.A, second.B, f[0]))
                final.add_triangle(Triangle(second.A, f[0], f[1]))
                final.add_triangle(Triangle(second.C, f[0], f[1]))
            elif 'c' in fs and 'a' in fs:
                final.add_triangle(Triangle(second.B, second.C, f[1]))
                final.add_triangle(Triangle(second.B, f[0], f[1]))
                final.add_triangle(Triangle(second.A, f[0], f[1]))

        elif sf:
            f = list(sf.values())
            diff = f[0] - f[1]
            norm = diff / abs(diff)
            pr = [second.a * norm / abs(second.a), second.b * norm / abs(second.b), second.c * norm / abs(second.c)]
            idx = pr.index(max(pr, key=lambda x: abs(x)))

            M1, M2 = (f[0], f[1]) if pr[idx] < 0 else (f[1], f[0])

            if idx == 0:
                final.add_triangle(Triangle(second.C, second.A, M1))
                final.add_triangle(Triangle(second.C, second.B, M2))
                final.add_triangle(Triangle(second.C, M1, M2))
                final.add_triangle(Triangle(second.A, second.B, M1))
                final.add_triangle(Triangle(second.B, M1, M2))
            elif idx == 1:
                final.add_triangle(Triangle(second.A, second.B, M1))
                final.add_triangle(Triangle(second.A, second.C, M2))
                final.add_triangle(Triangle(second.A, M1, M2))
                final.add_triangle(Triangle(second.B, second.C, M1))
                final.add_triangle(Triangle(second.C, M1, M2))
            elif idx == 2:
                final.add_triangle(Triangle(second.B, second.C, M1))
                final.add_triangle(Triangle(second.B, second.A, M2))
                final.add_triangle(Triangle(second.B, M1, M2))
                final.add_triangle(Triangle(second.C, second.A, M1))
                final.add_triangle(Triangle(second.A, M1, M2))

            if 'a' in sf and 'b' in sf:
                final.add_triangle(Triangle(first.C, first.A, f[0]))
                final.add_triangle(Triangle(first.C, f[0], f[1]))
                final.add_triangle(Triangle(first.B, f[0], f[1]))
            elif 'b' in sf and 'c' in sf:
                final.add_triangle(Triangle(first.A, first.B, f[0]))
                final.add_triangle(Triangle(first.A, f[0], f[1]))
                final.add_triangle(Triangle(first.C, f[0], f[1]))
            elif 'c' in sf and 'a' in sf:
                final.add_triangle(Triangle(first.B, first.C, f[1]))
                final.add_triangle(Triangle(first.B, f[0], f[1]))
                final.add_triangle(Triangle(first.A, f[0], f[1]))
        else:
            pass
        # final.add_triangle(first)
        # final.add_triangle(second)
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
