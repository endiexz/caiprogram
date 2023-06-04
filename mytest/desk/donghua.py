import tkinter as tk
import time

def get_pic(i):
    if(i>=42):
        i=1
    i=str(i)
    img='.\\ey\\' + i + '.png'
    return img

def move(x,y,x2,y2,canvas):
    i=1
    while True:
        t = 0
        while t <= 1:
            x_pos = x + (x2 - x) * t
            y_pos = y + (y2 - y) * t
            t += 0.01
            canvas.delete("all")
            time.sleep(0.01)
            img=get_pic(i)
            photo = tk.PhotoImage(file=img)
            canvas.create_image((x_pos, y_pos), image=photo)
            i=i+1
            if (i >= 42):
                i = 1
            canvas.update()
            print(x_pos,y_pos)
            if int(x_pos) == x2 or int(y_pos) == y2:
                canvas.delete("all")
                canvas.update()

        break

if __name__ == '__main__':
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack()
    move(200,200,100,100,canvas)
    time.sleep(5)
    move(200, 200, 100, 100, canvas)
    root.mainloop()