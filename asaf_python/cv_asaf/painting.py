import paintprev
import tkinter as tk
from tkinter.colorchooser import askcolor

# Create a Tkinter root window
root = tk.Tk()

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

class DrawingApp:
    def __init__(self, root):
        # Initialize the DrawingApp class
        self.root = root
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        self.canvas.bind("<ButtonRelease-2>", self.zoom_in)
        self.canvas.bind("<ButtonRelease-4>", self.zoom_out)
        self.canvas.bind("<ButtonRelease-3>", self.delete_point)
        self.canvas.bind("<Button-2>", self.delete_continuous)
        self.root.bind("B", self.choose_background_color)
        self.zoom_scale = 1.2
        self.call_choose_background_color = "white"
        self.drawing = False
        self.last_x = 0
        self.last_y = 0
        self.color = "black"
        self.brush_size = 2
        self.zoom_scale = 1.0
        self.is_zooming = False
        self.undo_list = []
        self.rundo_list = []

    # Function to draw a rectangle on the canvas
    def draw_rectangle(self, event):
        """
        Draws a rectangle on the canvas.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.drawing:
            self.canvas.create_rectangle(
                self.last_x, self.last_y, event.x, event.y,
                outline=self.color, width=self.brush_size
            )
            self.undo_list.append(self.canvas.find_all()[-1])  # Add the shape to the undo list

    # Function to draw a circle on the canvas
    def draw_circle(self, event):
        """
        Draws a circle on the canvas.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.drawing:
            self.canvas.create_oval(
                self.last_x, self.last_y, event.x, event.y,
                outline=self.color, width=self.brush_size
            )
            self.undo_list.append(self.canvas.find_all()[-1])  # Add the shape to the undo list

    # Function to draw a line on the canvas
    def draw_line(self, event):
        """
        Draws a line on the canvas.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.drawing:
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.color, width=self.brush_size
            )
            self.undo_list.append(self.canvas.find_all()[-1])  # Add the shape to the undo list

    # Function to draw a square on the canvas
    def draw_square(self, event):
        """
        Draws a square on the canvas.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.drawing:
            x0, y0 = self.last_x, self.last_y
            x1, y1 = event.x, event.y
            side_length = min(abs(x1 - x0), abs(y1 - y0))
            if x1 < x0:
                x1 = x0 - side_length
            else:
                x1 = x0 + side_length
            if y1 < y0:
                y1 = y0 - side_length
            else:
                y1 = y0 + side_length

            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline=self.color, width=self.brush_size
            )
            self.undo_list.append(self.canvas.find_all()[-1])  # Add the shape to the undo list

    # Function to draw an ellipse on the canvas
    def draw_ellipse(self, event):
        """
        Draws an ellipse on the canvas.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.drawing:
            self.canvas.create_oval(
                self.last_x, self.last_y, event.x, event.y,
                outline=self.color, width=self.brush_size
            )
            self.undo_list.append(self.canvas.find_all()[-1])  # Add the shape to the undo list

    # Function to draw a triangle on the canvas
    def draw_triangle(self, event):
        """
        Draws a triangle on the canvas.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.drawing:
            x0, y0 = self.last_x, self.last_y
            x1, y1 = event.x, event.y
            x2, y2 = x0 + (x1 - x0) / 2, y0  # Calculate the middle point of the top side
            self.canvas.create_polygon(
                x0, y0, x1, y1, x2, y2,
                outline=self.color, width=self.brush_size
            )
            self.undo_list.append(self.canvas.find_all()[-1])  # Add the shape to the undo list

    # Function to draw a hexagon on the canvas
    def draw_hexagon(self, event):
        """
        Draws a hexagon on the canvas.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.drawing:
            x0, y0 = self.last_x, self.last_y
            x1, y1 = event.x, event.y
            x2, y2 = x0 + (x1 - x0) / 2, y0  # Calculate the middle point of the top side
            x3, y3 = x0 + (x1 - x0) / 2, y1  # Calculate the middle point of the bottom side
            x4, y4 = x0, y0 + (y1 - y0) / 3  # Calculate the leftmost point of the left side
            x5, y5 = x1, y0 + (y1 - y0) / 3  # Calculate the rightmost point of the right side
            self.canvas.create_polygon(
                x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5,
                outline=self.color, width=self.brush_size
            )
            self.undo_list.append(self.canvas.find_all()[-1])  # Add the shape to the undo list

    # Function to choose the background color
    def choose_background_color(self):
        """
        Opens a color chooser dialog to choose the background color of the canvas.
        """
        color = askcolor(title="Tkinter Color Chooser")[1]
        if color is not None:
            self.background_color = color
            self.canvas.config(bg=self.background_color)

    # Function to start drawing
    def start_drawing(self, event):
        """
        Starts the drawing process.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        self.current_line = self.canvas.create_line(
            self.last_x, self.last_y, event.x, event.y,
            fill=self.color, width=self.brush_size
        )
        self.undo_list.append(self.current_line)

    # Function to stop drawing
    def stop_drawing(self, event):
        """
        Stops the drawing process.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        self.drawing = False

    # Function to draw on the canvas
    def draw(self, event):
        """
        Draws on the canvas.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.drawing:
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.color, width=self.brush_size
            )
            self.last_x = event.x
            self.last_y = event.y
            self.undo_list.append(self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.color, width=self.brush_size
            ))

    # Function to undo the last action
    def undo(self):
        """
        Undo the last action performed on the canvas.
        """
        if self.undo_list:
            item = self.undo_list.pop()
            self.rundo_list.append(item)
            self.canvas.delete(item)

    # Function to redo the last undone action
    def rundo(self):
        """
        Redo the last undone action performed on the canvas.
        """
        if self.rundo_list:
            item = self.rundo_list.pop()
            if item:
                self.undo_list.append(item)
                self.canvas.delete(item)

    # Function to choose the drawing color
    def choose_color(self):
        """
        Opens a color chooser dialog to choose the drawing color.
        """
        color = askcolor(title="Tkinter Color Chooser")[1]
        if color is not None:
            self.color = color

    # Function to change the brush size
    def change_brush_size(self):
        """
        Opens a window to change the brush size.
        """
        top = tk.Toplevel(self.root)
        top.title("Brush Size")
        top.geometry("300x100")

        label = tk.Label(top, text="Choose brush size (1-100):")
        label.pack()

        scale = tk.Scale(top, from_=1, to=100, orient=tk.HORIZONTAL)
        scale.set(self.brush_size)
        scale.pack()

        button = tk.Button(top, text="OK", command=lambda: self.change_brush_size_value(scale.get(), top))
        button.pack()

    # Function to set the brush size to the selected value
    def change_brush_size_value(self, size, top):
        """
        Sets the brush size to the selected value.

        Parameters:
            size (int): The selected brush size.
            top (tk.Toplevel): The top-level window.
        """
        self.brush_size = size
        top.destroy()

    # Function to clear the canvas
    def clear_canvas(self):
        """
        Clears the canvas.
        """
        self.canvas.delete("all")

    # Function to delete a point on the canvas
    def delete_point(self, event):
        """
        Deletes a point on the canvas.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        item = self.canvas.find_closest(event.x, event.y)[0]
        self.canvas.delete(item)

    # Function to delete all objects on the canvas
    def delete_continuous(self, event):
        """
        Deletes all objects on the canvas continuously.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if event.num == 3:
            self.canvas.delete(tk.ALL)

    # Function to choose a specific background color
    def background_specific(self):
        """
        Opens a color chooser dialog to choose a specific background color.
        """
        color = askcolor(title="Tkinter Color Chooser")[1]
        if color is None:
            return

        self.call_choose_background_color = color
        self.is_filling_area = True
        self.canvas.bind("<Button-1>", self.select_area)
        self.canvas.bind("<B1-Motion>", self.update_area)
        self.canvas.bind("<ButtonRelease-1>", self.change_background_color)

    # Function to select an area for changing the background color
    def select_area(self, event):
        """
        Selects an area on the canvas for changing the background color.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.is_filling_area:
            self.rect = {"x": event.x, "y": event.y, "width": 0, "height": 0}

    # Function to update the selected area for changing the background color
    def update_area(self, event):
        """
        Updates the selected area on the canvas for changing the background color.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.is_filling_area and self.rect:
            self.rect["width"] = event.x - self.rect["x"]
            self.rect["height"] = event.y - self.rect["y"]
            self.draw_area()

    # Function to draw the selected area for changing the background color
    def draw_area(self):
        """
        Draws the selected area on the canvas for changing the background color.
        """
        self.canvas.delete("area")
        self.canvas.create_rectangle(
            self.rect["x"], self.rect["y"],
            self.rect["x"] + self.rect["width"], self.rect["y"] + self.rect["height"],
            outline="red", tag="area"
        )

    # Function to change the background color of the selected area
    def change_background_color(self, event):
        """
        Changes the background color of the selected area on the canvas.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        if self.is_filling_area:
            selected_area = (
                self.rect["x"], self.rect["y"],
                self.rect["x"] + self.rect["width"], self.rect["y"] + self.rect["height"]
            )
            self.canvas.create_rectangle(selected_area, fill=self.call_choose_background_color, outline="")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.is_filling_area = False
        self.background_specific()

    # Function to toggle the zoom mode
    def toggle_zoom_mode(self, event):
        """
        Toggles the zoom mode.

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        self.is_zooming = False

    # Function to zoom in on the canvas
    def zoom_in(self):
        """
        Zooms in on the canvas.
        """
        self.is_zooming = True
        root.bind("z", app.toggle_zoom_mode)
        self.canvas.bind("<Button-1>", self.zoom_in2)

    # Function to zoom out on the canvas
    def zoom_out(self):
        """
        Zooms out on the canvas.
        """
        root.bind("z", app.toggle_zoom_mode)
        self.canvas.bind("<Button-1>", self.zoom_out2)

    # Function to zoom in on the canvas (part 2)
    def zoom_in2(self, event):
        """
        Zooms in on the canvas (part 2).

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        root.bind("z", app.toggle_zoom_mode)
        self.zoom_scale *= 1.2
        if self.is_zooming:
            self.canvas.scale(tk.ALL, event.x, event.y, self.zoom_scale, self.zoom_scale)
        else:
            self.canvas.unbind("<Button-1>")

    # Function to zoom out on the canvas (part 2)
    def zoom_out2(self, event):
        """
        Zooms out on the canvas (part 2).

        Parameters:
            event (tk.Event): The event containing information about the mouse click.
        """
        root.bind("z", app.toggle_zoom_mode)
        self.zoom_scale /= 1.2
        if self.is_zooming:
            self.canvas.scale(tk.ALL, event.x, event.y, self.zoom_scale, self.zoom_scale)
        else:
            self.canvas.unbind("<Button-1>")

    # Function to return to drawing mode
    def draw1(self):
        """
        Returns to drawing mode.
        """
        self.is_zooming = False
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.start_drawing)
        root.unbind("u")
        root.unbind("r")
        root.bind("u", self.undo)
        root.bind("r", self.rundo)

# Create an instance of the DrawingApp class
app = DrawingApp(root)

# Create the menu bar
menu_bar = tk.Menu(root)

# Create the file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save Image", command=paintprev.save_image)
file_menu.add_command(label="Load Image", command=paintprev.load_image)
file_menu.add_command(label="Send Email", command=paintprev.send_email)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create the color menu
color_menu = tk.Menu(menu_bar, tearoff=0)
color_menu.add_command(label="Choose Color", command=app.choose_color)
menu_bar.add_cascade(label="Colors", menu=color_menu)

# Create the background specific menu
background_specific_menu = tk.Menu(menu_bar, tearoff=0)
background_specific_menu.add_command(label="Choose Color", command=app.background_specific)
background_specific_menu.add_command(label="back to draw", command=app.draw1)
menu_bar.add_cascade(label="Background Specific", menu=background_specific_menu)

# Create the brush size menu
size_menu = tk.Menu(menu_bar, tearoff=0)
size_menu.add_command(label="Change Brush Size", command=app.change_brush_size)
menu_bar.add_cascade(label="Brush Size", menu=size_menu)

# Create the background color menu
colors_submenu = tk.Menu(menu_bar, tearoff=0)
colors_submenu.add_command(label="Choose Background Color", command=app.choose_background_color)
menu_bar.add_cascade(label="background color", menu=colors_submenu)

# Create the undo and redo menu
undo_rundo = tk.Menu(menu_bar, tearoff=0)
undo_rundo.add_command(label="undo", command=app.undo)
undo_rundo.add_command(label="rundo", command=app.rundo)
menu_bar.add_cascade(label="undo_rundo", menu=undo_rundo)

# Create the clear menu
clear_menu = tk.Menu(menu_bar, tearoff=0)
clear_menu.add_command(label="Clear Canvas", command=app.clear_canvas)
menu_bar.add_cascade(label="Clear", menu=clear_menu)

# Create the zoom menu
zoom_menu = tk.Menu(menu_bar, tearoff=0)
zoom_menu.add_command(label="Zoom In", command=app.zoom_in)
zoom_menu.add_command(label="Zoom Out", command=app.zoom_out)
zoom_menu.add_command(label="back to draw", command=app.draw1)
menu_bar.add_cascade(label="Zoom", menu=zoom_menu)

# Create the shapes menu
shape_menu = tk.Menu(menu_bar, tearoff=0)
shape_menu.add_command(label="Rectangle", command=lambda: app.canvas.bind("<B1-Motion>", app.draw_rectangle))
shape_menu.add_command(label="Circle", command=lambda: app.canvas.bind("<B1-Motion>", app.draw_circle))
shape_menu.add_command(label="Line", command=lambda: app.canvas.bind("<B1-Motion>", app.draw_line))
shape_menu.add_command(label="Square", command=lambda: app.canvas.bind("<B1-Motion>", app.draw_square))
shape_menu.add_command(label="Ellipse", command=lambda: app.canvas.bind("<B1-Motion>", app.draw_ellipse))
shape_menu.add_command(label="Triangle", command=lambda: app.canvas.bind("<B1-Motion>", app.draw_triangle))
shape_menu.add_command(label="Hexagon", command=lambda: app.canvas.bind("<B1-Motion>", app.draw_hexagon))
menu_bar.add_cascade(label="Shapes", menu=shape_menu)

# Configure the root window with the menu bar
root.config(menu=menu_bar)

# Run the Tkinter event loop
root.mainloop()
