from tkinter import Tk, Canvas, PhotoImage, mainloop
import math

WIDTH, HEIGHT = 256, 256
window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg='#808080')
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH // 2, HEIGHT // 2), image=img, state='normal')
canvas.image = img  # To prevent garbage collection

for y in range(HEIGHT // 2):
    for x in range(WIDTH):
        img.put('#804000', (x, y))

canvas.image.write('dummy.jpg')

mainloop()
