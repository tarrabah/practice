import tkinter as tk
from tkinter import scrolledtext
import matrix


class interface_error(BaseException):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class app_interface(tk.Tk):

    def __init__(self):

        super().__init__()
        self.title("Решить СЛАУ")
        self.geometry("520x550")


        self.label_matrix = tk.Label(master=self, text='Матрица системы (числа через пробел):')
        self.label_matrix.grid(row = 0, column = 0, sticky=tk.W, padx = 2, pady = 2, columnspan = 2)


        self.chosen_option = tk.StringVar()
        self.chosen_option.set("2x2")
        self.options = [
            "2x2",
            "3x3",
            "4x4",
            "5x5",
            "6x6",
            "7x7"
        ]

        self.menu = tk.OptionMenu(self, self.chosen_option, *self.options)
        self.menu.grid(row = 1, column = 0, sticky=tk.W, padx = 2, pady = 2)

        self.label_column = tk.Label(master=self, text='Столбец (каждое \nчисло в новой строке):', justify = 'left')
        self.label_column.grid(row = 0, column = 2, sticky=tk.W, padx = 20, pady = 2, rowspan = 2)

        self.text_matrix = tk.Text(master = self, bg='white', width = 40, height = 10)
        self.text_matrix.grid(row = 2, column = 0, sticky=tk.E, padx = 2, pady = 2, columnspan = 2)

        self.text_column = tk.Text(master = self, bg='white', width = 20, height = 10)
        self.text_column.grid(row = 2, column = 2, sticky=tk.EW, padx = 20, pady = 2)

        self.label_solution = tk.Label(master = self, text='Ход решения:')
        self.label_solution.grid(row = 4, column = 0, sticky=tk.W, padx = 2, pady = 2)

        self.button_cramer = tk.Button(master= self, text='Метод Крамера', command=self.cramer)
        self.button_cramer.grid(row=3, column = 0, sticky=tk.W, padx = 2, pady = 2)

        self.button_gauss = tk.Button(master= self, text='Метод Гаусса', command=self.gauss)
        self.button_gauss.grid(row=3, column = 1, sticky=tk.W, padx = 2, pady = 2)

        self.button_invert = tk.Button(master= self, text = "Обратная матрица", command = self.invert)
        self.button_invert.grid(row=3, column = 2, sticky=tk.W, padx = 2, pady = 2)

        self.sc_text_solution = scrolledtext.ScrolledText(
            master = self,
            width = 62,
            height = 14,
            bg = "white"
        )
        self.sc_text_solution.grid(row = 5, column = 0, columnspan = 3, sticky=tk.W, padx = 2, pady = 2)

    #starts programm
    def start(self):
        self.mainloop()


    #closes program
    def close(self):
        exit()


    def parse_matrix(self):
        size = int(self.chosen_option.get()[0])
        #print(size)
        text = self.text_matrix.get('1.0', tk.END).strip().split('\n')
        try:
            text = list(
                map(
                    lambda x: list(
                        map(
                            lambda x: float(x.strip()),
                            x.strip().split(' ')
                        )
                    ),
                    text
                )
            )
        except BaseException as e:
            raise interface_error("Слишком много пробелов")

        for i in range(1, len(text)):
            if len(text[0]) != len(text[i]):
                raise interface_error("Размеры строк не совпадают")
        if len(text) != len(text[0]):
            raise interface_error("Размер строк не совпадает с количеством столбцов")
        elif len(text) != size:
            raise interface_error("Выбрана не та опция размера")

        return matrix.SquareMatrix(text)


    def parse_column(self):
        text = self.text_column.get('1.0', tk.END).strip().split('\n')
        if len(text) == 0 or text[0] == '':
            raise interface_error("Столбец не введён")

        try:
            text = list(map(float, text))
            return text
        except BaseException as e:
            raise interface_error("Слишком много переводов строки")


    def error_out(self, error):
        self.sc_text_solution.delete(1.0, tk.END)
        self.sc_text_solution.insert(1.0, error.__str__())


    def cramer(self):
        self.sc_text_solution.delete(1.0, tk.END)
        try:
            matrix_A = self.parse_matrix()
            column_B = self.parse_column()
            if not matrix.column_len_check(matrix_A, column_B):
                raise interface_error('Размер столбца и матрицы не совпадают')

            result = matrix_A.cramers_rule(column_B)
            self.sc_text_solution.insert(1.0, result[1])

        except BaseException as e:
            self.error_out(e)


    def gauss(self):
        self.sc_text_solution.delete(1.0, tk.END)
        try:
            matrix_A = self.parse_matrix()
            column_B = self.parse_column()
            if not matrix.column_len_check(matrix_A, column_B):
                raise interface_error('Размер столбца и матрицы не совпадают')

            result = matrix_A.gauss_solve(column_B)
            self.sc_text_solution.insert(1.0, result[1])

        except BaseException as e:
            self.error_out(e)


    def invert(self):
        self.sc_text_solution.delete(1.0, tk.END)
        try:
            matrix_A = self.parse_matrix()
            column_B = self.parse_column()
            if not matrix.column_len_check(matrix_A, column_B):
                raise interface_error('Размер столбца и матрицы не совпадают')

            result = matrix_A.invertible_matrix_solve(column_B)
            self.sc_text_solution.insert(1.0, result[1])

        except BaseException as e:
            self.error_out(e)


app = app_interface()
app.start()