import tkinter as tk
from time import strftime
import datetime
from tkinter import font
import win32gui
import win32con

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def update_time():
    now = datetime.datetime.now()
    hour = now.strftime("%I")
    minute = now.strftime("%M")
    second = now.strftime("%S")
    ampm = now.strftime("%p")
    day = now.strftime("%A, %d %B %Y")
    
    hour_label.config(text=hour)
    minute_label.config(text=minute)
    second_label.config(text=f"SECONDS: {second}")
    ampm_label.config(text=ampm)
    date_label.config(text=day)
    
    root.after(1000, update_time)

def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

def set_as_desktop_widget(window):
    desktop_handle = win32gui.GetDesktopWindow()
    widget_handle = win32gui.GetParent(window.winfo_id())
    win32gui.SetParent(widget_handle, desktop_handle)

# Create the main window
root = tk.Tk()
root.title("Digital Clock")
root.configure(bg='black')
root.overrideredirect(True)
root.attributes('-transparentcolor', 'black')

# Set the window size
width, height = 340, 180
root.geometry(f"{width}x{height}")

# Calculate position to place it at the top right of the screen with space
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_margin = 10  # Adjust margin as needed
y_margin = 10  # Adjust margin as needed
x = screen_width - width - x_margin
y = y_margin

root.geometry(f"+{x}+{y}")

# Load custom font
custom_font = font.Font(family="coolvetica", size=60, weight="bold")
custom_font_small = font.Font(family="coolvetica", size=10)
custom_font_date = font.Font(family="coolvetica", size=12)

# Create main canvas
canvas = tk.Canvas(root, width=width, height=height, bg='black', highlightthickness=0)
canvas.pack()

# Create rounded rectangle for background
create_rounded_rectangle(canvas, 0, 0, width, height, radius=20, fill='#2c2c2c', outline='')

# Create rounded rectangles for hour and minute
create_rounded_rectangle(canvas, 20, 20, 160, 120, radius=15, fill='#1c1c1c', outline='')
create_rounded_rectangle(canvas, 180, 20, 320, 120, radius=15, fill='#1c1c1c', outline='')

# Create and configure the time labels
hour_label = tk.Label(root, font=custom_font, bg='#1c1c1c', fg='white', width=2)
hour_label.place(x=40, y=25, width=100, height=70)

minute_label = tk.Label(root, font=custom_font, bg='#1c1c1c', fg='white', width=2)
minute_label.place(x=200, y=25, width=100, height=70)

ampm_label = tk.Label(root, font=custom_font_small, bg='#1c1c1c', fg='white')
ampm_label.place(x=40, y=95, width=100, height=20)

second_label = tk.Label(root, font=custom_font_small, bg='#1c1c1c', fg='white')
second_label.place(x=200, y=95, width=100, height=20)

# Create and configure the date label
date_label = tk.Label(root, font=custom_font_date, bg='#2c2c2c', fg='white')
date_label.place(x=20, y=130, width=300, height=30)

# Bind mouse events to make the widget movable
root.bind("<ButtonPress-1>", start_move)
root.bind("<ButtonRelease-1>", stop_move)
root.bind("<B1-Motion>", do_move)

# Set the widget as a desktop child window
root.after(10, lambda: set_as_desktop_widget(root))

# Start the time update function
update_time()

# Run the application
root.mainloop()
