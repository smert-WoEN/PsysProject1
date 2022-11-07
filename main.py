import matplotlib.pyplot as plt
import numpy as np

import electrostatics as el

xMin, xMax = -200, 200
yMin, yMax = -150, 150
zoom = 30
xOffset = 0

el.init(xMin, xMax, yMin, yMax, zoom, xOffset)

charges = [el.PointCharge(2, [1.732, 1]),
           el.PointCharge(-2, [0, 2]),
           el.PointCharge(2, [-1.732, 1]),
           el.PointCharge(-2, [-1.732, -1]),
           el.PointCharge(2, [0, -2]),
           el.PointCharge(-2, [1.732, -1]),
           ]

field = el.ElectricField(charges)
potential = el.Potential(charges)

g = [el.GaussianCircle(charge.x, 0.1) for charge in charges]
g[2].a0 = np.radians(90)
g[3].a0 = np.radians(-90)

fieldLines = []

for g_ in g:
    for x in g_.fluxpoints(field, 12):
        fieldLines.append(field.line(x))

plt.figure(figsize=(6, 4.5))
field.plot()
potential.plot()
for fieldLine in fieldLines:
    fieldLine.plot()

for charge in charges:
    charge.plot()

el.finalize_plot()
#plt.show()
plt.savefig(str(3) + ".png", dpi=500)

