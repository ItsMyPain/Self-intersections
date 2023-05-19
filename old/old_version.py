def intersectEdges(a, b, c, d):
    M = [[b[0] - a[0], b[1] - a[1], b[2] - a[2]],
         [c[0] - a[0], c[1] - a[1], c[2] - a[2]],
         [d[0] - a[0], d[1] - a[1], d[2] - a[2]]]

    return np.linalg.det(M)


def findUV(a, b, c, d):
    LT = [[d[0] - b[0], d[0] - b[0]],
          [d[1] - b[1], d[1] - b[1]]]

    RT = [[a[0] - b[0], d[0] - b[0]],
          [a[1] - b[1], d[1] - b[1]]]

    B = [[a[0] - b[0], d[0] - c[0]],
         [a[1] - b[1], d[1] - c[1]]]

    return np.linalg.det(LT) / np.linalg.det(B), np.linalg.det(RT) / np.linalg.det(B)


def line_insertion(a, b, c, d, eps=1e-3):
    det = intersectEdges(a, b, c, d)
    if -eps < det < eps:
        u, v = findUV(a, b, c, d)
        if (0 + eps < u < 1 - eps) and (0 + eps < v < 1 - eps):
            return u, v
    return False, False


def area(a, b, c):
    a = abs(a - b)
    b = abs(b - c)
    c = abs(c - a)
    p = (a + b + c) / 2
    return np.sqrt(p * (p - a) * (p - b) * (p - c))


def hehehe(string):
    a = list(map(int, string.split()[1:]))
    return (a[0], a[1]), (a[0], a[2]), (a[1], a[2])
