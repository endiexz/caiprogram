import tkinter as tk

# Initialize an instance of tkinter window
root=tk.Tk()
# Set the width and height of the tkinter window
root.geometry("600x300")
# Create a canvas widget
canvas=tk.Canvas(root, width=500, height=300)
canvas.pack()
# Create a line in canvas widget
canvas.create_line(10, 25, 200, 200, width=5)
# Create a dashed line
canvas.create_line(210, 25,410 , 200,fill='red', dash=(10,5), width=2)
root.mainloop()