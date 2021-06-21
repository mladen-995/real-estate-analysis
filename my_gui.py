import tkinter as tk
import pandas as pd

from algorithms.linear_regression import LinearRegression
from algorithms.knn import KNN

class MyGui:
    def start(self):
        self.top = tk.Tk()
        self.top.title('Real estate price predictor')

        validation = self.top.register(self.validation_number)

        city_parts_list = pd.read_csv('city-part-categories.csv')['city_part'].values

        self.area_label = tk.Label(self.top, text="Kvadratura").grid(row=0)
        self.build_year_label = tk.Label(self.top, text="Godina izgradnje").grid(row=1)
        self.number_of_rooms_label = tk.Label(self.top, text="Broj soba").grid(row=2)
        self.level_label = tk.Label(self.top, text="Sprat").grid(row=3)
        self.city_part_label = tk.Label(self.top, text="Deo grada").grid(row=5)

        self.area_entry = tk.Entry(self.top, validate='key', validatecommand=(validation, '%S'))
        self.area_entry.grid(row=0, column=1)

        self.build_year_entry = tk.Entry(self.top, validate='key', validatecommand=(validation, '%S'))
        self.build_year_entry.grid(row=1, column=1)

        self.number_of_rooms_entry = tk.Entry(self.top, validate='key', validatecommand=(validation, '%S'))
        self.number_of_rooms_entry.grid(row=2, column=1)

        self.level_entry = tk.Entry(self.top, validate='key', validatecommand=(validation, '%S'))
        self.level_entry.grid(row=3, column=1)

        self.city_part_value = tk.StringVar(self.top)
        self.city_part_value.set('Izaberi...')
        self.city_part_entry = tk.OptionMenu(self.top, self.city_part_value, *city_parts_list)
        self.city_part_entry.grid(row=5, column=1)

        self.k_label = tk.Label(self.top, text='K')
        self.k_label.grid(row=6)

        self.k_entry = tk.Entry(self.top, validate='key', validatecommand=(validation, '%S'))
        self.k_entry.grid(row=6, column=1)

        self.button_linear = tk.Button(self.top, text='Izracunaj primenom linearne regresije', command=self.execute_linear_regression)
        self.button_linear.grid(row=15)

        self.linear_regression_result = tk.StringVar()
        self.linear_regression_result_label = tk.Label(self.top, textvariable=self.linear_regression_result)
        self.linear_regression_result_label.grid(row=15, column=1)

        self.button_linear = tk.Button(self.top, text='Izracunaj primenom knn', command=self.execute_knn)
        self.button_linear.grid(row=16)

        self.knn_result = tk.StringVar()
        self.knn_result_label = tk.Label(self.top, textvariable=self.knn_result)
        self.knn_result_label.grid(row=16, column=1)

        self.linear_regression = LinearRegression()
        self.linear_regression.init()

        self.knn = KNN()
        self.knn.init()

        self.top.mainloop()

    def validation_number(self, number):
        return number.isdigit()

    def execute_linear_regression(self):
        result = self.linear_regression.predict(
            self.city_part_value.get(),
            self.build_year_entry.get(),
            self.area_entry.get(),
            self.number_of_rooms_entry.get(),
            self.level_entry.get()
        )

        self.linear_regression_result.set(result)

    def execute_knn(self):
        k = None

        if self.k_entry.get() != '':
            k = int(self.k_entry.get())

        result = self.knn.predict(
            self.city_part_value.get(),
            self.build_year_entry.get(),
            self.area_entry.get(),
            self.number_of_rooms_entry.get(),
            self.level_entry.get(),
            k
        )

        self.knn_result.set(str(result) + 'e')

gui = MyGui()
gui.start()