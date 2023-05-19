def parse(filename):
    '''
    Функция для парсинга файла расширения .vtk, на вход передается имя файла, на выходе два списка:
    ---- points: Point[]
    ---- triangles: Triangle[]
    '''
    from models import Point, Triangle
    point_number = 0
    with open(filename) as file:
        points = []
        triangles = []
        trigger = 'skip'
        for line in file:
            first_word = line.rstrip().split()[0]

            if trigger == 'points':
                try:
                    coords = list(map(float, line.rstrip().split()))
                    points.append(Point(coords[0], coords[1], coords[2], point_number))
                except ValueError:
                    pass
                point_number += 1
            elif trigger == 'cells':
                try:
                    temp = list(map(int, line.rstrip().split()))
                except ValueError:
                    pass
                try:
                    triangles.append(Triangle(points[temp[1]], points[temp[2]], points[temp[3]]))
                except IndexError:
                    pass
            elif trigger == 'skip':
                pass

            if first_word == 'POINTS':
                trigger = 'points'
            elif first_word == 'CELLS':
               trigger = 'cells'
            else:
                trigger == 'skip'
    return points, triangles

# print(parse('./cube.vtk'))