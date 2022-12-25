import numpy as np
import matplotlib.pyplot as plt

mu0 = 4 * np.pi * 10 ** -7
eps = 0.000000000000001
scaler = 0.8 * 10e2


class Point:
    def __init__(self, coords):
        self.value = 0
        self.vector = np.array([0, 0, 0])
        self.coords = coords

    def draw(self, ax):
        ax.arrow(self.coords[0], self.coords[2], (self.vector[0] * self.value * scaler) / 2,
                 (self.vector[2] * self.value * scaler) / 2, width=0.05,
                 length_includes_head=True, color="red")


class Line:
    def __init__(self, x, amperage):
        self.amperage = amperage
        self.x = x

    def calculate_B(self, point):
        x = point.coords[0]
        z = point.coords[2]
        distance = ((self.x - x) ** 2 + z ** 2) ** 0.5
        bAbs = np.abs(mu0 * self.amperage / (2 * np.pi * distance + eps))
        bVec = -np.array([self.amperage * z, 0, self.amperage * (self.x - x)])
        bVec = bVec / (np.linalg.norm(bVec) + eps)
        return bAbs, bVec

    def draw(self, ax):
        ax.scatter(self.x, 0, c="blue")


class BField:
    def __init__(self, bAbs, bVector):
        self.bAbs = bAbs
        self.bVector = self.norm(np.array(bVector))

    def norm(self, bVector):
        return bVector/(np.linalg.norm(bVector) + eps)


#ЗАДАЕМ РАЗМЕР РИСУНКА
gridSize = 19 #нечетное
offset = (gridSize - 1) / 2

# ЗАДАЕМ ВНЕШНЕЕ ПОЛЕ
field = BField(5*10e-5, [1.0, 0, 0.0])


# ЗАДАЕМ ПРОВОДНИКИ
pr1 = Line(6.0, 10000)
pr1Coords = [pr1.x, 0]
pr2 = Line(-6.0, -10000)
pr2Coords = [pr2.x, 0]


# ЗАДАЕМ ТОЧКИ
points = np.array([])

for i in range(gridSize):
    for j in range(gridSize):
        if pr1Coords[0] == -offset + j and pr1Coords[1] == offset - i:
            continue
        if pr2Coords[0] == -offset + j and pr2Coords[1] == offset - i:
            continue

        points = np.append(points, Point([-offset + j, 0, offset - i]))


for i in range(len(points)):
    B1 = pr1.calculate_B(points[i])
    B2 = pr2.calculate_B(points[i])
    points[i].value = np.linalg.norm(B1[1] * B1[0] + B2[1] * B2[0] + field.bVector * field.bAbs)
    points[i].vector = (B1[1] * B1[0] + B2[1] * B2[0] + field.bVector * field.bAbs) / (points[i].value + eps)


fig, ax = plt.subplots()
fig.set_figwidth(12)
fig.set_figheight(12)

for i in range(len(points)):
    points[i].draw(ax)

pr1.draw(ax)
pr2.draw(ax)

ax.set_xticks([-offset + i - 1 for i in range(gridSize + 2)])
ax.set_yticks([-offset + i - 1 for i in range(gridSize + 2)])

plt.savefig(str(2) + ".png", dpi=500)
