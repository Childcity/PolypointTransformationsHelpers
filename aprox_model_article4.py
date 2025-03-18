
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Вхідні дані (потрібно вставити реальні значення)
x_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 14,15, 16,17, 18,19,  20,21, 22,23, 24])
y_data = np.array([9.5046578,
5.0958577,
3.5401821,
2.9680175,
2.5259849,
2.2899589,
2.1082424,
2.1036021,
2.0392318,
1.9209286,
1.7921972,
1.5870859,
1.6055488,
1.5564492,
1.4770171,
1.4419957,
1.4426954,
1.4471335,
1.4274322,
1.4338891,
1.3923659,
1.3311026,
1.3024705,
1.301843
])

# Обчислюємо c
c = y_data[9] - 1  # f(1) = y_data[0]. тому c = f(1) - 1

# Визначаємо апроксимаційну функцію
def approx_func(x):
    return 1.0/x + c

# Генеруємо точки для побудови графіка
x_fit = np.linspace(1, max(x_data), 100)
y_fit = approx_func(x_fit)

# Виводимо рівняння у консоль
print(f"Апроксимація: f(x) = 1/x + {c:.3f}")
# Будуємо графік
plt.scatter(x_data, y_data, label="Data", color="blue")
plt.plot(x_fit, y_fit, label=f"Апроксимація: 1/x + {c:.3f}", color="red")
plt.xlabel("Threads Count")
plt.ylabel("Seconds")
plt.xticks(np.arange(min(x_data), max(x_data) + 1, 1))  # Крок 1 по осі X
plt.yticks(np.arange(1, max(y_data) + 1, 1))  # Крок 1 по осі Y
plt.legend()
plt.grid()
#plt.savefig("images/output.png")

#######################################################

# Функція апроксимації
def model_1(x, a, b, c):
    return a / (x + b) + c
def model_2(x, a, b, c):
    return a * pow(x, -b) + c

# Підбір параметрів a, b, c
params, _ = curve_fit(model_2, x_data, y_data, p0=[1, 1, 1])  # p0 - початкові наближення

# Отримані параметри
a_fit, b_fit, c_fit = params

# Побудова апроксимації
x_fit = np.linspace(1, 24, 100)
y_fit = model_2(x_fit, a_fit, b_fit, c_fit)

# Відображення графіка
plt.figure(figsize=(10, 5))
plt.scatter(x_data, y_data, label="Data", color="blue")
plt.plot(x_fit, y_fit, label=f"f(x) = {a_fit:.3f} * x^(-{b_fit:.3f}) + {c_fit:.3f}", color="green")
plt.xlabel("Threads Count")
plt.ylabel("Seconds")
plt.xticks(np.arange(min(x_data), max(x_data) + 1, 1))  # Крок 1 по осі X
plt.yticks(np.arange(1, max(y_data) + 1, 1))  # Крок 1 по осі Y
plt.legend()
plt.grid()
#plt.savefig("images/output3.png")

# a / (x + b) + c
print(f"Підібрана апроксимаційна функція: f(x) = {a_fit:.3f} / (x + {b_fit:.3f}) + {c_fit:.3f}")
# f(x) = 7.655 / (x - 0.098) + 1.016 

# a * pow(x, -b) + c
print(f"Підібрана апроксимаційна функція: f(x) = {a_fit:.3f} * x^(-{b_fit:.3f}) + {c_fit:.3f}")
# f(x) = 8.429 * x^(-1.070) + 1.063


#################################################

from sklearn.metrics import mean_absolute_error

# Обчислення прогнозів для обох моделей
y_pred_rational = [7.655 / (x - 0.098) + 1.016 for x in x_data]
y_pred_power = [8.429 * x**(-1.070) + 1.063 for x in x_data]

# Обчислення MAE
mae_rational = mean_absolute_error(y_data, y_pred_rational)
mae_power = mean_absolute_error(y_data, y_pred_power)

print(f"MAE для f(x) = 7.655 / (x - 0.098) + 1.016: {mae_rational:.5f}") # 0.05001
print(f"MAE для f(x) = 8.429 * x^(-1.070) + 1.063: {mae_power:.5f}") # 0.04912