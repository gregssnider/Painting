from tkinter import Label, Toplevel
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
import munsell


# Get image file to display
print("Color Analyzer")
filename = askopenfilename()
print('file', filename)

# Display it.
window = Toplevel()
window.title('Color Analyzer')
window.configure(background='grey')

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
print(filename)
raw_image = Image.open(filename)
img = ImageTk.PhotoImage(raw_image)
print(img)
panel = Label(window, image = img)

#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "bottom", fill = "both", expand = "yes")
def motion(event):
    x, y = event.x, event.y
    rgb = raw_image.getpixel((x, y))
    color = munsell.from_rgb(rgb)
    print(rgb, color)

window.bind('<Motion>', motion)
window.mainloop()

