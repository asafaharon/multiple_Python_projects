import math
import tkinter as tk
import tkinter.filedialog as filedialog

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.configure(background='light green')

        # Styling buttons for a better appearance
        self.button_style = {'font': ('Arial', 14),
                             'bg': 'light yellow',
                             'activebackground': 'yellow',
                             'padx': 20,
                             'pady': 10}

        # Entry widget for input and result display
        self.entry = tk.Entry(root, width=50, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=4)

        # Button configurations
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("+/-", 4, 2), ("+", 4, 3)
        ]

        # Creating and placing buttons on the grid
        for text, row, column in buttons:
            button = tk.Button(root, text=text, **self.button_style,
                               command=lambda t=text: self.button_click(t))
            button.grid(row=row, column=column)

        # Additional functional buttons
        self.button_equals = tk.Button(root, text="=", **self.button_style,
                                       command=self.equals_click)
        self.button_equals.grid(row=5, column=3)
        self.button_clear = tk.Button(root, text="CE", **self.button_style,
                                      command=self.clear_entry)
        self.button_clear.grid(row=4, column=0)
        self.button_sqrt = tk.Button(root, text="√", **self.button_style,
                                     command=self.square_root)
        self.button_sqrt.grid(row=1, column=4)
        self.button_power_of_2 = tk.Button(root, text="x^2", **self.button_style,
                                           command=self.power_of_2)
        self.button_power_of_2.grid(row=2, column=4)
        self.button_sin = tk.Button(root, text="sin", **self.button_style,
                                    command=self.sin_click)
        self.button_sin.grid(row=5, column=1)
        self.button_cos = tk.Button(root, text="cos", **self.button_style,
                                    command=self.cos_click)
        self.button_cos.grid(row=5, column=4)
        self.button_save_history = tk.Button(root, text="Save History", **self.button_style,
                                             command=self.save_history)
        self.button_save_history.grid(row=6, column=4)

    def button_click(self, number):
        """Appends the pressed number or operator to the entry field."""
        current_number = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current_number + number)

    def clear_entry(self):
        """Clears the entry field."""
        self.entry.delete(0, tk.END)

    def equals_click(self):
        """Calculates the expression in the entry field and shows the result."""
        expression = self.entry.get()
        try:
            result = eval(expression)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        except Exception:
            self.entry.insert(0, "Error")

    def square_root(self):
        """Calculates the square root of the number in the entry field."""
        try:
            current_number = self.entry.get()
            result = math.sqrt(float(current_number))
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        except ValueError:
            self.entry.insert(0, "Invalid input for square root")

    def switch_sign(self):
        """Switches the sign of the current number in the entry field."""
        current_number = self.entry.get()
        if current_number.startswith('-'):
            self.entry.delete(0)
        else:
            self.entry.insert(0, '-')

    def delete_last_digit(self):
        """Deletes the last digit or character in the entry field."""
        current_number = self.entry.get()
        self.entry.delete(len(current_number) - 1)

    def power_of_2(self):
        """Calculates the square of the number in the entry field."""
        try:
            current_number = self.entry.get()
            result = float(current_number) ** 2
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        except ValueError:
            self.entry.insert(0, "Invalid input for power of 2")

    def sin_click(self):
        """Calculates the sine of the number in the entry field."""
        current_number = self.entry.get()
        try:
            result = math.sin(math.radians(float(current_number)))
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        except ValueError:
            self.entry.insert(0, "Invalid input for sin")

    def cos_click(self):
        """Calculates the cosine of the number in the entry field."""
        current_number = self.entry.get()
        try:
            result = math.cos(math.radians(float(current_number)))
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        except ValueError:
            self.entry.insert(0, "Invalid input for cos")

    def save_history(self):
        """Saves the current entry field content to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.entry.get())

root = tk.Tk()
Calculator(root)
root.mainloop()
