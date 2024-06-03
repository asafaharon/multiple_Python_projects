import os
import shutil
import smtplib
import tkinter as tk
import tkinter.simpledialog as simpledialog
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import filedialog, messagebox
from tkinter.colorchooser import askcolor


def save_image():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=(("PNG Files", "*.png"), ("All Files", "*.*"))
    )
    if file_path:
        try:
            self.canvas.postscript(file="temp.ps", colormode='color')
            os.system(f'convert temp.ps "{file_path}"')
            messagebox.showinfo("Image Saved", "The image has been saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the image:\n{str(e)}")

def load_image(self):
    file_path = filedialog.askopenfilename(
        filetypes=(("PNG Files", "*.png"), ("All Files", "*.*"))
    )
    if file_path:
        try:
            shutil.copyfile(file_path, "temp.png")
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk.PhotoImage(file="temp.png"))
            messagebox.showinfo("Image Loaded", "The image has been loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the image:\n{str(e)}")


def send_email():
    sender_email = None
    sender_password = None
    receiver_email = None

    # בקשת פרטי המייל והסיסמה מהמשתמש
    sender_email = simpledialog.askstring("Sender Email", "Enter your email:")
    if not sender_email:
        return

    sender_password = simpledialog.askstring("Sender Password", "Enter your email password:", show="*")
    if not sender_password:
        return

    receiver_email = simpledialog.askstring("Receiver Email", "Enter the recipient's email:")
    if not receiver_email:
        return

    # יצירת הודעה מרובת חלקים
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "My Drawing"

    # הוספת גוף ההודעה כטקסט
    text = MIMEText("Check out my drawing!")
    message.attach(text)

    # הוספת התמונה לגוף ההודעה כקובץ מוטבע
    with open("temp.png", "rb") as image_file:
        image_data = image_file.read()
        image = MIMEImage(image_data, name=os.path.basename("temp.png"))
        image.add_header("Content-ID", "<image1>")
        message.attach(image)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        messagebox.showinfo("Email Sent", "The drawing has been sent successfully.")
    except smtplib.SMTPAuthenticationError:
        messagebox.showerror("Error", "Failed to authenticate. Please check your email and password.")
    except smtplib.SMTPException as e:
        messagebox.showerror("Error", f"An error occurred while sending the email:\n{str(e)}")


    def change_brush_size(self):
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