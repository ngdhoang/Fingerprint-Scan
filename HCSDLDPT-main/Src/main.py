import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import os
import feature_extraction as fe
import search_image as si

path = 'Changes Images/'
n = 8
si.read_data(n)

def open_image():
    filepath = filedialog.askopenfilename()
    if filepath:
        clear_images()
        display_selected_image(filepath)

def display_selected_image(filepath):
    img = Image.open(filepath)
    filename = os.path.basename(filepath)
    feature_current = fe.crop_images(img, filename, n, hasInput=True)
    image_list = si.search_image(feature_current, n)
    display_image_sequence(image_list, 0)
    img = img.resize((180, 190), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    fixed_panel.config(image=img)
    fixed_panel.image = img
    fixed_label.config(text=filename)

def display_image_sequence(image_list, index):
    if index < len(image_list):
        img_path = path + image_list[index][1]
        img = Image.open(img_path)
        img = img.resize((180, 190), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(image_frame, image=img, bg='yellow')
        panel.image = img
        panel.grid(row=0, column=index, padx=10, pady=10)
        label = tk.Label(image_frame, text=f"{os.path.basename(img_path)}\nSimilarity : {abs(image_list[index][0])}", bg='yellow', font=('Helvetica', 12, 'bold'))
        label.grid(row=1, column=index, padx=10, pady=5)
        image_labels.append((panel, label))
        root.after(200, display_image_sequence, image_list, index + 1)

def drop(event):
    filepath = event.data
    filepath = filepath.replace('{', '').replace('}', '')  # Clean up filepath
    clear_images()
    display_selected_image(filepath)

def clear_images():
    for panel, label in image_labels:
        panel.destroy()
        label.destroy()
    image_labels.clear()

def read_data():
    si.read_data(n)

def update_n(value):
    global n
    n = int(value)

root = TkinterDnD.Tk()  # Corrected to use TkinterDnD.Tk()
root.title("Fingerprint Ranking")
root.geometry('888x666')
root.configure(bg='yellow')

image_labels = []

button_frame = tk.Frame(root, bg='yellow')
button_frame.pack(side='bottom', fill='x', padx=20, pady=10)

image_frame = tk.Frame(root, bg='yellow')
image_frame.pack(side='top', fill='x', padx=20, pady=10)

open_button = tk.Button(button_frame, text="Open Image", command=open_image, bg='green', fg='white',
                        width=20, height=2, font=('Helvetica', 14, 'bold'), relief='raised', bd=4)
open_button.pack(side='left', padx=20, pady=10)

# Fixed image display next to the button
fixed_frame = tk.Frame(button_frame, bg='yellow')
fixed_frame.pack(side='left', padx=60)
fixed_panel = tk.Label(fixed_frame, bg='yellow')
fixed_panel.pack(side='top')
fixed_label = tk.Label(fixed_frame, text='', bg='yellow', font=('Helvetica', 12, 'bold'))
fixed_label.pack(side='top')

# Add a slider to change the value of n
slider_frame = tk.Frame(button_frame, bg='yellow')
slider_frame.pack(side='right', padx=30)
slider_button = tk.Button(slider_frame, text='Adjust n:', command=read_data, bg='green', font=('Helvetica', 14, 'bold'), fg = 'white')
slider_button.pack(side='top', pady=5)
n_slider = tk.Scale(slider_frame, from_=1, to=15, orient='horizontal', command=update_n, bg='green', font=('Helvetica', 12), fg = 'white')
n_slider.set(n)
n_slider.pack(side='top', pady=5)

# Drag and Drop functionality
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

root.mainloop()
