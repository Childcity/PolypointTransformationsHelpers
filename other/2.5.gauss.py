import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from numpy.linalg import solve
from matplotlib.widgets import Slider

def make_interp_gauss(t, y, alpha):
    """
    Створює функцію інтерполяції Гаусса на основі вузлів t та значень y.
    """
    n = len(t)
    G = np.zeros((n, n))

    # Створення матриці Гауса
    for i in range(n):
        for j in range(n):
            diff = t[i] - t[j]
            G[i, j] = np.exp(-alpha * diff ** 2)

    # Розв'язання G * b = y
    b = solve(G, y)

    # Повертаємо функцію-інтерполятор
    def interpolator(t_new):
        t_new = np.asarray(t_new)
        result = np.zeros_like(t_new, dtype=float)
        for i in range(n):
            diff = t_new - t[i]
            result += b[i] * np.exp(-alpha * diff ** 2)
        return result

    return interpolator


# Точки кривої ABCDEFA
points = np.array([
    [0.0, 0.0],     # A
    [0.2, 0.8],     # B
    [0.3, 1.5],     # C
    [1.0, 2.0],     # D
    [2.0, 1.5],     # E
    [2.5, 0.8],     # F
    [0.0, 0.0],     # A
])
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'A']
# points = np.array([
#     [8.631945e-19, 2.071667e-17],
#     [1.638150e-01, 3.367418e-01],
#     [1.996515e-01, 7.086736e-01],
#     [2.046337e-01, 1.087841e+00],
#     [2.758857e-01, 1.446289e+00],
#     [4.015709e-01, 1.704133e+00],
#     [5.662726e-01, 1.872237e+00],
#     [7.545739e-01, 1.960467e+00],
#     [9.510581e-01, 1.978687e+00],
#     [1.144314e+00, 1.936763e+00],
#     [1.322448e+00, 1.844560e+00],
#     [1.473329e+00, 1.711944e+00],
#     [1.585118e+00, 1.548779e+00],
#     [1.646010e+00, 1.364932e+00],
#     [1.744255e+00, 1.115550e+00],
#     [1.936443e+00, 9.011315e-01],
#     [2.216145e+00, 7.493204e-01],
#     [2.576931e+00, 6.867929e-01],
#     [2.880259e+00, 5.426964e-01],
#     [3.076923e+00, 3.698885e-01],
#     [8.631945e-19, 2.071667e-17],
# ])

# Розділяємо на x та y
x = points[:, 0]
y = points[:, 1]

# Параметризація за довжиною 
t = np.linspace(0, 1, len(x))
t_count_init = 7
t_count_min = 1
t_count_max = 50

t_new = np.linspace(0, 1, t_count_init)  # Більше точок для гладкості

# Обчислюємо alpha за формулою
Xmax = np.max(x)
Xmin = np.min(x)
alpha_init = (np.pi * (len(x) - 1)) / ((Xmax - Xmin) ** 2)
print(f"Обчислений alpha: {alpha_init}")

# Інтерполяція (початкове значення)
interp_gauss_x = make_interp_gauss(t, x, alpha_init)
interp_gauss_y = make_interp_gauss(t, y, alpha_init)

x_smooth = interp_gauss_x(t_new)
y_smooth = interp_gauss_y(t_new)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
orig_line, = ax.plot(x, y, 'o-')
smooth_line, = ax.plot(x_smooth, y_smooth, '-', color='orange', linewidth=2)
ax.legend()
ax.axis('equal')
ax.grid(True)

for i, label in enumerate(labels):
    x_offset = -7 if label in ['A', 'B', 'C', 'D'] else 7
    ax.annotate(label, (x[i], y[i]), textcoords="offset points", xytext=(x_offset,5), ha='center')

# Додаємо слайдер для alpha
ax_alpha = plt.axes([0.2, 0.15, 0.65, 0.03])
slider_alpha = Slider(ax_alpha, 'alpha', 0.001, alpha_init * 3, valinit=alpha_init, valstep=0.001)

# Додаємо слайдер для t_count
ax_t_count = plt.axes([0.2, 0.08, 0.65, 0.03])
slider_t_count = Slider(ax_t_count, 't_count', t_count_min, t_count_max, valinit=t_count_init, valstep=1)


def update(val):
    alpha = slider_alpha.val
    t_count = int(slider_t_count.val)
    
    t_new = np.linspace(0, 1, t_count)
    spl_x = make_interp_gauss(t, x, alpha)
    spl_y = make_interp_gauss(t, y, alpha)
    x_smooth = spl_x(t_new)
    y_smooth = spl_y(t_new)
    
    smooth_line.set_data(x_smooth, y_smooth)
    fig.canvas.draw_idle()

slider_alpha.on_changed(update)
slider_t_count.on_changed(update)

plt.show()
