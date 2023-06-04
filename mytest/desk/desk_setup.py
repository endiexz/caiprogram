import multiprocessing
import donghua
import tkinter as tk
import clock_tk
def run_clock():
    clock_tk.clock_main()
def run_move(x,y,x2,y2,canvas):
    donghua.move(x,y,x2,y2,canvas)


if __name__ == '__main__':
    # Create a process pool with two processes
    pool = multiprocessing.Pool(processes=2)
    pool.apply_async(run_clock)
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1800, height=1200)
    canvas.pack()


    while True:
        choice = input("Enter 1 to run notepad component, 2 to run animation component, or any other key to exit:\n ")
        if choice == '1':
            pool.apply_async(run_move(150,150,1500,1000,canvas))
        elif choice == '2':
            pool.apply_async(run_move(150,150,100,200,canvas))

        else:
            pass

    # Wait for all processes to complete
    root.mainloop()
    pool.close()
    pool.join()