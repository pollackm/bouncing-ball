import tkinter as tk

root = tk.Tk()
root.title("Bouncing Ball")

WIDTH = 600
HEIGHT = 400
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

canvas.create_rectangle(2, 2, WIDTH - 2, HEIGHT - 2, outline="white", width=3)

radius = 20
x, y = 300, 200
dx, dy = 4, 3

ball = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red")


def animate():
    global x, y, dx, dy
    x += dx
    y += dy

    if x - radius <= 0 or x + radius >= WIDTH:
        dx = -dx
    if y - radius <= 0 or y + radius >= HEIGHT:
        dy = -dy

    canvas.coords(ball, x - radius, y - radius, x + radius, y + radius)
    root.after(16, animate)


animate()
root.mainloop()
