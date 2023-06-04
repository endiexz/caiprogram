import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Simple Notebook")

text = tk.Text(root, wrap='word')
text.pack(expand='yes', fill='both')

def open_file():
    file = filedialog.askopenfile(mode='r', defaultextension=".txt")
    if file is None:
        return
    content = file.read()
    text.delete("1.0", "end")
    text.insert("1.0", content)

def save_file():
    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if file is None:
        return
    content = text.get("1.0", "end")
    file.write(content)
    file.close()

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

root.mainloop()