import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

x = np.array([100, 200, 300])
y = np.array([1, 2, 3])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Axes3D.plot(x, y, 1)