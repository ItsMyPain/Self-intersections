from tqdm import tqdm

from intersept import visualize, intersect
from models import Grid, Triangle

eps = 1e-7


def find_problems(filenameIn: str, filenameOut: str):
    grid1 = Grid()
    grid1.load_from_file(filenameIn)
    grid2 = Grid()
    for i1 in tqdm(grid1.triangles):
        for i2 in grid1.triangles:
            if intersect(i1, i2, eps) or intersect(i2, i1, eps):
                grid2.copy_triangle(i1)
                grid2.copy_triangle(i2)

    grid2.save_to_file(filenameOut)


Input = 'intersected_sphere.vtk'
Medium = 'suzanne_problems.vtk'
Output = 'fixed_suzanne.vtk'

# find_problems(Input, Medium)
visualize(Medium)

final = Grid()
final.load_from_file(Medium)

for i in tqdm(range(20000)):

    for first in final.triangles:
        for second in final.triangles:
            fs = intersect(first, second, eps)
            sf = intersect(second, first, eps)

            if fs or sf:

                try:
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
                        pr = [first.a * norm / abs(first.a), first.b * norm / abs(first.b),
                              first.c * norm / abs(first.c)]
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
                        pr = [second.a * norm / abs(second.a), second.b * norm / abs(second.b),
                              second.c * norm / abs(second.c)]
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

                    final.dell_triangle(first)
                    final.dell_triangle(second)

                except Exception:
                    break

                break

        if fs or sf:
            break

final.save_to_file(Output)
visualize(Output)
