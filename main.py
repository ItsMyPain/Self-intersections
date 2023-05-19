from models import Grid, Triangle, Point
from intersept import visualize

grid = Grid()
grid.load_from_file('cube.vtk')

TR = Triangle(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0))
grid.add_triangle(TR)

grid.save_to_file('out.vtk')

visualize('out.vtk')
