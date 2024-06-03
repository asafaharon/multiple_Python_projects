from tkinter import Tk, Label, Canvas
import random
import math


def show_resume():
    root = Tk()
    root.title("Resume")

    # Generate random grades for various subjects
    grades_text = "Computer Science Student - Year 3\n\nGrades:\n\nPython: {}\nJava: {}\nC++: {}\nAlgorithms: {}\nData Structures: {}\nOperating Systems: {}\n".format(
        random.randint(80, 85),
        random.randint(80, 85),
        random.randint(80, 85),
        random.randint(80, 85),
        random.randint(80, 85),
        random.randint(80, 85)
    )

    # Create a label to display the grades
    marks_label = Label(root, text=grades_text, font=("Arial", 14))
    marks_label.pack()

    # Create a canvas for animation
    canvas = Canvas(root, width=500, height=500, bg='white')
    canvas.pack()

    shapes = []  # List to store shape information
    num_shapes = 200

    def random_color():
        # Generate a random color
        color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return color

    def create_shape():
        # Create a random shape (either oval, rectangle, or ellipse) with random position and color
        x = random.randint(50, 450)
        y = random.randint(50, 450)
        size_x = random.randint(10, 30)
        size_y = random.randint(10, 30)
        shape_type = random.choice(['oval', 'rectangle'])

        if shape_type == 'oval':
            shape = canvas.create_oval(x, y, x + size_x, y + size_y, fill=random_color())
        elif shape_type == 'rectangle':
            shape = canvas.create_rectangle(x, y, x + size_x, y + size_y, fill=random_color())

        angle = random.randint(10, 30)  # Generates a random integer between 10 and 30
        shapes.append((shape, math.cos(angle), math.sin(angle)))

    def move_shapes():
        # Move the shapes in their current direction
        new_directions = []
        for shape, dx, dy in shapes:
            x1, y1, x2, y2 = canvas.coords(shape)
            if x1 <= 0 or x2 >= 500 or y1 <= 0 or y2 >= 500:
                dx, dy = change_direction(dx, dy)
            canvas.move(shape, dx * 5, dy * 5)
            new_directions.append((shape, dx, dy))

        shapes[:] = new_directions  # Update the shapes list with new directions
        root.after(1, move_shapes)

    def change_direction(dx, dy):
        # Change the direction of the shape by rotating 90 degrees clockwise
        new_dx = dy
        new_dy = -dx
        return new_dx, new_dy

    # Start creating and moving shapes
    for _ in range(num_shapes):
        create_shape()

    # Call move_shapes after 1000 ms (1 second) to start the animation
    root.after(100, move_shapes)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    show_resume()
