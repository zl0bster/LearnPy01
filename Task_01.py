import matplotlib.pyplot as plt
import numpy as np

x1 = -100
x2 = 100
y1 = -50
y2 = 50
plt.axis([x1, x2, y1, y2])
plt.axis('on')
plt.grid(True, color='b')
plt.title('title string')
plt.xlabel('axis X')
plt.ylabel('axis Y')
# for x in np.arange(1, 100, 1):
#     r = x / 100
#     g = 0
#     b = x / 100
#     plt.plot([x, x], [0, 50], linewidth=5, color=(r, g, b))
#     plt.plot([x, x], [0, -50], linewidth=5, color=(r, b, g))

dx = 5
dy = 5
for x in np.arange(x1, x2, dx):
    for y in np.arange(y1, y2, dy):
        plt.scatter(x, y, s=5, color='g')
plt.plot([-40, 40], [-40, -40], linewidth=2, color='r', linestyle=':')
plt.plot([40, 40], [-40, 40], linewidth=2, color='r')
plt.plot([40, -40], [40, 40], linewidth=2, color='r', linestyle='-.')
plt.plot([-40, -40], [40, -40], linewidth=2, color='r')
plt.axes().set_aspect('equal')

plt.arrow(0, 0, 20, 0, head_length=4, head_width=3, color='r')
plt.arrow(0, 0, 0, 20, head_length=4, head_width=3, color='r')

plt.show()
