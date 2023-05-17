import math
import tkinter as tk
from tkinter import messagebox

class EOQ:
    def __init__(self, table_data, total_stock_area):
        self.table_data = table_data
        self.total_stock_area = total_stock_area
        self.result = {}

    def find_optimum_lambda(self):
        self.try_lambdas()
        positive = [value for value in self.result.values() if value >= 0]
        negative = [value for value in self.result.values() if value < 0]
        lower_lambda = [key for key, value in self.result.items() if value == min(positive)][0]
        upper_lambda = [key for key, value in self.result.items() if value == max(negative)][0]
        return self.linear_interpolation(lower_lambda, self.result[lower_lambda], upper_lambda, self.result[upper_lambda], 0)

    def calculate_optimum_order_quantity(self, row, lambda_val):
        return math.sqrt((2 * row['k'] * row['d']) / (row['h'] - 2 * lambda_val * row['a']))

    def unconstrained_optimum(self, lambda_val):
        sum_val = sum(
            math.sqrt((2 * row['k'] * row['d']) / (row['h'] - 2 * lambda_val * row['a'])) * row['a']
            for row in self.table_data
        )
        return round(sum_val - self.total_stock_area, 2)

    def try_lambdas(self):
        lambda_val = 0.0
        while lambda_val > -1.1:
            self.result[lambda_val] = self.unconstrained_optimum(lambda_val)
            lambda_val -= 0.1
            lambda_val = round(lambda_val, 1)

    def linear_interpolation(self, lambda_val1, y1, lambda_val2, y2, y3):
        return lambda_val1 + (y3 - y1) * (lambda_val2 - lambda_val1) / (y2 - y1)

def get_stock_data(stock_number):
    def save_data():
        nonlocal stock_data
        try:
            stock_data = {
                'stok': stock_number,
                'k': float(unit_cost_entry.get()),
                'd': float(demand_rate_entry.get()),
                'h': float(holding_cost_entry.get()),
                'a': float(storage_area_entry.get())
            }
            top.destroy()
        except ValueError:
            messagebox.showerror('Error', 'Invalid input. Please enter numeric values.')

    stock_data = None
    top = tk.Toplevel()
    top.title(f"Stok({stock_number})")

    unit_cost_label = tk.Label(top, text="k(TL) değerini girin:")
    unit_cost_label.pack()
    unit_cost_entry = tk.Entry(top)
    unit_cost_entry.pack()

    demand_rate_label = tk.Label(top, text="d(adet/gün) değerini girin:")
    demand_rate_label.pack()
    demand_rate_entry = tk.Entry(top)
    demand_rate_entry.pack()

    holding_cost_label = tk.Label(top, text="h(TL) değerini girin:")
    holding_cost_label.pack()
    holding_cost_entry = tk.Entry(top)
    holding_cost_entry.pack()

    storage_area_label = tk.Label(top, text="a(m^2) değerini girin:")
    storage_area_label.pack()
    storage_area_entry = tk.Entry(top)
    storage_area_entry.pack()

    save_button = tk.Button(top, text="Kaydet", command=save_data)
    save_button.pack()

    top.wait_window()  # Wait for the top-level window to be closed
    return stock_data

def get_table_data(row_count):
    table_data = []
    for i in range(row_count):
        stock_number = i + 1
        stock_data = get_stock_data(stock_number)
        if stock_data is not None:
            table_data.append(stock_data)
        else:
            return None
    return table_data

def handle_submit():
    try:
        row_count = int(row_count_entry.get())
        if row_count > 0:
            table_data = get_table_data(row_count)
            total_stock_area = float(total_stock_area_entry.get())

            calculator = EOQ(table_data, total_stock_area)
            result_lambda = calculator.find_optimum_lambda()

            # Calculate optimum order quantity for each row
            optimum_quantities = []
            for row in table_data:
                optimum_quantity = calculator.calculate_optimum_order_quantity(row, result_lambda)
                optimum_quantity = round(optimum_quantity, 2)  # Round to two decimal places
                optimum_quantities.append(optimum_quantity)

            result_label.config(text=f"Optimum Lambda: {result_lambda:.3f}\nOptimum Order Quantities:\n{format_optimum_quantities(optimum_quantities)}")
        else:
            messagebox.showerror('Error', 'Invalid input. Please enter a positive integer.')
    except ValueError:
        messagebox.showerror('Error', 'Invalid input. Please enter numeric values.')

def format_optimum_quantities(optimum_quantities):
    return '\n'.join(f"Y{i+1}: {optimum_quantities[i]:.2f}" for i in range(len(optimum_quantities)))

root = tk.Tk()
root.title("EOQ Calculator")

row_count_label = tk.Label(root, text="Tablo satır/stok sayısını girin:")
row_count_label.pack()
row_count_entry = tk.Entry(root)
row_count_entry.pack()

total_stock_area_label = tk.Label(root, text="Toplam stok alanını girin:")
total_stock_area_label.pack()
total_stock_area_entry = tk.Entry(root)
total_stock_area_entry.pack()

submit_button = tk.Button(root, text="Hesapla", command=handle_submit)
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
