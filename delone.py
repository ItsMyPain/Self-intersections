import matplotlib.pyplot as plt
import numpy as np

import plotly.graph_objects as go

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

def parsePoints(filename):
    '''
    Функция для парсинга файла расширения .vtk, на вход передается имя файла, на выходе два списка:
    ---- points: Point[]
    ---- triangles: Triangle[]
    '''
    point_number = 0
    with open(filename) as file:
        points_x = []
        points_y = []
        points_z = []
        trigger = 'skip'
        for line in file:
            first_word = line.rstrip().split()[0]

            if trigger == 'points':
                try:
                    coords = list(map(float, line.rstrip().split()))
                    points_x.append(coords[0])
                    points_y.append(coords[1])
                    points_z.append(coords[2])
                except ValueError:
                    pass
                point_number += 1
            elif trigger == 'cells':
                pass
            elif trigger == 'skip':
                pass

            if first_word == 'POINTS':
                trigger = 'points'
            elif first_word == 'CELLS':
               trigger = 'cells'
            else:
                trigger == 'skip'
    return points_x, points_y, points_z

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

coords = parsePoints('./intersected_sphere.vtk')

ax.scatter(coords[0], coords[1], coords[2])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()

пщ_fig = go.Figure(data=[go.Mesh3d(x=coords[0], y=coords[1], z=coords[2], color='green',
                                opacity=0.20, alphahull=3)])
  
пщ_fig.show()