import sys
from tkinter import Label, Toplevel, Tk, StringVar
from tkinter.filedialog import askopenfilename

from PIL import ImageTk, Image, ImageDraw
import munsell



# Display it.
window = Tk()  #Toplevel()
window.title('Color Analyzer')
window.configure(background='grey')

# Get image file to display
print("Color Analyzer")
filename = askopenfilename(title='Select file')
print('file', filename)


#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
print(filename)
raw_image = Image.open(filename)
img = ImageTk.PhotoImage(raw_image)
print(img)
panel = Label(window, image = img)
location = StringVar()
location.set('hello there')
position = Label(window, textvar=location)
#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "bottom", fill = "both", expand = "yes")
position.pack(side = 'top', fill='both', expand='yes')
def motion(event):
    x, y = event.x, event.y
    rgb = raw_image.getpixel((x, y))
    #color = munsell.from_rgb(rgb)
    print(rgb)
    location.set(str((x, y)) + str(rgb))

window.bind('<Motion>', motion)
window.mainloop()

