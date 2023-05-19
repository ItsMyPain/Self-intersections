from cmath import sqrt

sgl = 1e-3


class Point:
    x: float
    y: float
    z: float
    number: int

    def __init__(self, x, y, z, number=-1):
        self.x = x
        self.y = y
        self.z = z
        self.number = number

    def __eq__(self, other):
        return abs(self.x - other.x) < sgl and abs(self.y - other.y) < sgl and abs(self.z - other.z) < sgl
        # return self.number == other.number
        # return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return f"{self.x} {self.y} {self.z}"

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


class Vector:
    x: float
    y: float
    z: float

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other, self.z * other)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


class Triangle:
    A: Point
    B: Point
    C: Point
    a: Vector
    b: Vector
    c: Vector

    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C
        self.a = B - A
        self.b = C - B
        self.c = A - C

    def __eq__(self, other):
        return self.A == other.A and self.B == other.B and self.C == other.C

    def __repr__(self):
        return f"{self.A.number} {self.B.number} {self.C.number}"

    def isNeighbour(self, other):
        return self.A == other.A or self.A == other.B or self.A == other.C or self.B == other.A or self.B == other.B or self.B == other.C or self.C == other.A or self.C == other.B or self.C == other.C

    def area(self):
        a = abs(self.a)
        b = abs(self.b)
        c = abs(self.c)
        return sqrt((a + b + c) * (- a + b + c) * (a - b + c) * (a + b - c)) / 4

    def isInTriangle(self, point: Point, eps=1e-2):
        S0 = self.area()
        S1 = Triangle(point, self.B, self.C).area()
        S2 = Triangle(self.A, point, self.C).area()
        S3 = Triangle(self.A, self.B, point).area()
        if abs(S0 - (S1 + S2 + S3)) < eps:
            return True
        return False


class Grid:
    points: list[Point] = []
    triangles: list[Triangle] = []
    n_points: int = 0
    n_triangles: int = 0

    def add_point(self, point: Point):
        self.n_points += 1
        point.number = self.n_points
        self.points.append(point)

        return point

    def add_triangle(self, triangle: Triangle):
        triangle.A = self.add_point(triangle.A)
        triangle.B = self.add_point(triangle.B)
        triangle.C = self.add_point(triangle.C)
        self.triangles.append(triangle)
        self.n_triangles += 1

        return triangle

    def load_from_file(self, filename: str):
        n = 0
        with open(filename, 'r', encoding='UTF-8') as file:
            for i in range(4):
                file.readline()
            self.n_points = int(file.readline().split()[1])
            for i in range(self.n_points):
                line = list(map(float, file.readline().split()))
                self.points.append(Point(line[0], line[1], line[2], n))
                n += 1

            print(f'Загружено {self.n_points} точек')

            self.n_triangles = int(file.readline().split()[1])
            for i in range(self.n_triangles):
                line = list(map(int, file.readline().split()[1:]))
                self.triangles.append(Triangle(self.points[line[0]], self.points[line[1]], self.points[line[2]]))

            print(f'Загружено {self.n_triangles} треугольников')

    def save_to_file(self, filename: str):
        with open(filename, 'w', encoding='UTF-8') as file:
            file.write(
                f'# vtk DataFile Version 3.0\n{filename.split(".")[0]}.stl\nASCII\nDATASET UNSTRUCTURED_GRID\nPOINTS {self.n_points} double\n')
            for i in self.points:
                file.write(f'{i.x} {i.y} {i.z}\n')

            print(f'Записано {self.n_points} точек')

            file.write(f'CELLS {self.n_triangles} {self.n_triangles * 4}\n')
            for i in self.triangles:
                file.write(f'3 {i.A.number} {i.B.number} {i.C.number}\n')

            file.write(f'CELL_TYPES {self.n_triangles} \n')
            for _ in range(self.n_triangles):
                file.write('5\n')

            print(f'Записано {self.n_triangles} треугольников')

# TR = Triangle(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0))
# P = Point(1 / 2, 1 / 1.2, 0)
# print(TR.isInTriangle(P))
# a = Grid()
# a.load_from_file('cube.vtk')
# a.save_to_file('out.vtk')
