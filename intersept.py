import vtkmodules.all as vtk

from models import Triangle


def visualize(filename: str):
    colors = vtk.vtkNamedColors()

    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    output = reader.GetOutput()

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(output)
    mapper.ScalarVisibilityOn()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().SetLineWidth(2.0)
    actor.GetProperty().VertexVisibilityOn()
    actor.GetProperty().SetMetallic(1)
    actor.GetProperty().RenderPointsAsSpheresOn()
    actor.GetProperty().SetColor(colors.GetColor3d("MistyRose"))

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('Wheat'))

    renderer_window = vtk.vtkRenderWindow()
    renderer_window.SetSize(640, 480)
    renderer_window.AddRenderer(renderer)
    renderer_window.SetWindowName('ReadUnstructuredGrid')

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderer_window)
    interactor.Initialize()
    interactor.Start()


def intersect(first: Triangle, second: Triangle, eps=1e-4):
    if first.isNeighbour(second):
        return False

    Q1 = ((first.B.y - first.A.y) * (first.C.z - first.A.z) - (first.B.z - first.A.z) * (first.C.y - first.A.y))
    Q2 = ((first.B.x - first.A.x) * (first.C.z - first.A.z) - (first.B.z - first.A.z) * (first.C.x - first.A.x))
    Q3 = ((first.B.x - first.A.x) * (first.C.y - first.A.y) - (first.B.y - first.A.y) * (first.C.x - first.A.x))

    T1 = ((second.A.x - first.A.x) * Q1 - (second.A.y - first.A.y) * Q2 + (second.A.z - first.A.z) * Q3) / (
            (second.A.x - second.B.x) * Q1 - (second.A.y - second.B.y) * Q2 + (second.A.z - second.B.z) * Q3 + eps / 100
    )

    M1 = second.A + second.a * T1

    T2 = ((second.B.x - first.A.x) * Q1 - (second.B.y - first.A.y) * Q2 + (second.B.z - first.A.z) * Q3) / (
            (second.B.x - second.C.x) * Q1 - (second.B.y - second.C.y) * Q2 + (second.B.z - second.C.z) * Q3 + eps / 100
    )

    M2 = second.B + second.b * T2

    T3 = ((second.C.x - first.A.x) * Q1 - (second.C.y - first.A.y) * Q2 + (second.C.z - first.A.z) * Q3) / (
            (second.C.x - second.A.x) * Q1 - (second.C.y - second.A.y) * Q2 + (second.C.z - second.A.z) * Q3 + eps / 100
    )

    M3 = second.C + second.c * T3

    res = {}
    if -eps < T1 < 1 + eps and first.isInTriangle(M1, eps):
        res['a'] = M1
    if -eps < T2 < 1 + eps and first.isInTriangle(M2, eps):
        res['b'] = M2
    if -eps < T3 < 1 + eps and first.isInTriangle(M3, eps):
        res['c'] = M3

    return res or False


