import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

class SimplexMethod:
    def __init__(self, c, A, b):
        self.c = np.array(c)
        self.A = np.array(A)
        self.b = np.array(b)
        self.num_constraints, self.num_variables = self.A.shape
        self.tableau = self._create_tableau()

    def _create_tableau(self):
        tableau = np.zeros((self.num_constraints + 1, self.num_variables + self.num_constraints + 1))
        tableau[:-1, :self.num_variables] = self.A
        tableau[:-1, self.num_variables:self.num_variables + self.num_constraints] = np.eye(self.num_constraints)
        tableau[:-1, -1] = self.b
        tableau[-1, :self.num_variables] = -self.c
        return tableau

    def _pivot(self, row, col):
        self.tableau[row, :] /= self.tableau[row, col]
        for r in range(self.tableau.shape[0]):
            if r != row:
                self.tableau[r, :] -= self.tableau[r, col] * self.tableau[row, :]

    def solve(self):
        while True:
            col = np.argmin(self.tableau[-1, :-1])
            if self.tableau[-1, col] >= 0:
                break

            row = np.argmin(np.where(self.tableau[:-1, col] > 0,
                                     self.tableau[:-1, -1] / self.tableau[:-1, col], np.inf))
            if self.tableau[row, col] <= 0:
                raise ValueError("Неограниченная задача")

            self._pivot(row, col)

        solution = np.zeros(self.num_variables)
        for i in range(self.num_constraints):
            basic_var = np.where(self.tableau[i, :self.num_variables] == 1)[0]
            if len(basic_var) == 1:
                solution[basic_var[0]] = self.tableau[i, -1]
        return solution, self.tableau

def solve_simplex():
    try:
        # Получение коэффициентов целевой функции
        c = []
        for i in range(num_vars):
            value = c_entries[i].get()
            if value == "" or not value.replace('.', '', 1).replace('-', '', 1).isdigit():
                raise ValueError("Все коэффициенты целевой функции должны быть числовыми.")
            c.append(float(value))

        # Получение коэффициентов ограничений и правой части
        A = []
        for i in range(num_constraints):
            row = []
            for j in range(num_vars):
                value = a_entries[i][j].get()
                if value == "" or not value.replace('.', '', 1).replace('-', '', 1).isdigit():
                    raise ValueError("Все коэффициенты ограничений должны быть числовыми.")
                row.append(float(value))
            A.append(row)

        b = []
        for i in range(num_constraints):
            value = b_entries[i].get()
            if value == "" or not value.replace('.', '', 1).replace('-', '', 1).isdigit():
                raise ValueError("Все правые части ограничений должны быть числовыми.")
            b.append(float(value))

        simplex = SimplexMethod(c, A, b)
        solution, tableau = simplex.solve()

        # Очистка текстового поля
        result_text.delete(1.0, tk.END)

        # Форматирование вывода
        result_text.insert(tk.END, "Симплекс-таблица:\n\n")
        for i, row in enumerate(tableau):
            result_text.insert(tk.END, '\t'.join(f"{val:.2f}" for val in row) + '\n')

        # Вычисление максимального значения целевой функции
        max_value = tableau[-1, -1]  # Максимальное значение функции Z
        result_text.insert(tk.END, "\nОптимальное решение:\n")
        result_text.insert(tk.END, f"{solution}\n")
        result_text.insert(tk.END, f"Максимальное значение Z: {max_value:.2f}\n")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")

def setup_entries():
    global c_entries, a_entries, b_entries
    # Очистка старых виджетов
    for widget in frame_inputs.winfo_children():
        widget.destroy()

    # Заголовок для коэффициентов целевой функции
    ttk.Label(frame_inputs, text="Коэффициенты целевой функции:").grid(row=0, column=0, columnspan=num_vars)

    c_entries = []
    for j in range(num_vars):
        entry = ttk.Entry(frame_inputs, width=5)
        entry.grid(row=1, column=j)
        c_entries.append(entry)

    # Заголовок для коэффициентов ограничений
    ttk.Label(frame_inputs, text="Коэффициенты ограничений:").grid(row=2, column=0, columnspan=num_vars + 1)

    a_entries = []
    b_entries = []
    for i in range(num_constraints):
        row_entries = []
        for j in range(num_vars):
            entry = ttk.Entry(frame_inputs, width=5)
            entry.grid(row=3 + i, column=j)
            row_entries.append(entry)
        a_entries.append(row_entries)

        # Ввод правой части (b)
        b_entry = ttk.Entry(frame_inputs, width=5)
        b_entry.grid(row=3 + i, column=num_vars)
        b_entries.append(b_entry)

    ttk.Label(frame_inputs, text="Правые части (b):").grid(row=2, column=num_vars)

def apply_settings():
    try:
        global num_vars, num_constraints
        num_vars = int(entry_vars.get())
        num_constraints = int(entry_constraints.get())
        setup_entries()
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения для количества переменных и ограничений.")

def exit_program():
    root.quit()

# Настройка интерфейса
root = tk.Tk()
root.title("Симплекс Метод")

# Ввод количества переменных и ограничений
frame_settings = ttk.Frame(root)
frame_settings.pack(pady=10)

ttk.Label(frame_settings, text="Количество переменных:").grid(row=0, column=0)
entry_vars = ttk.Entry(frame_settings, width=5)
entry_vars.grid(row=0, column=1)

ttk.Label(frame_settings, text="Количество ограничений:").grid(row=0, column=2)
entry_constraints = ttk.Entry(frame_settings, width=5)
entry_constraints.grid(row=0, column=3)

ttk.Button(frame_settings, text="Применить", command=apply_settings).grid(row=0, column=4, padx=10)

# Поля для ввода коэффициентов
frame_inputs = ttk.Frame(root)
frame_inputs.pack(pady=10)

# Кнопка для запуска решения
ttk.Button(root, text="Решить", command=solve_simplex).pack(pady=10)

# Поле для вывода результатов
result_text = tk.Text(root, height=15, width=80)
result_text.pack(pady=10)

# Кнопка для выхода из программы
ttk.Button(root, text="Выход", command=exit_program).pack(pady=10)

# Инициализация начальных значений
num_vars = 2
num_constraints = 2
c_entries = []
a_entries = []
b_entries = []
setup_entries()

root.mainloop()
