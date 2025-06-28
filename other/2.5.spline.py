import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Точки кривої ABCDEF (заміни на свої координати)
points = np.array([
    [0.0, 0.0],     # A
    [0.2, 0.8],     # B
    [0.3, 1.5],     # C
    [1.0, 2.0],     # D
    [2.0, 1.5],     # E
    [2.5, 0.8],     # F
])

# Розділяємо на x та y
x = points[:, 0]
y = points[:, 1]

# Параметризація за довжиною (spline по аркдовжині)
t = np.linspace(0, 1, len(x))
t_new = np.linspace(0, 1, 200)  # Більше точок для гладкості

# Інтерполяція
spl_x = make_interp_spline(t, x, k=3)
spl_y = make_interp_spline(t, y, k=3)

x_smooth = spl_x(t_new)
y_smooth = spl_y(t_new)

# Побудова графіка
plt.plot(x, y, 'o-', label='Оригінальна ламана')
plt.plot(x_smooth, y_smooth, '-', label='Гладка крива')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()
