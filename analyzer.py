""" Analyze pixels in a color image.

Prompts the user for an image file name then displays it. Shows the RGB
and Munsell color for the pixel pointed at by the mouse.

"""
import os
from tkinter import Label, Tk, StringVar
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image, ImageDraw
import munsell


# Create Window for color analysis
window = Tk()
window.configure(background='grey')

# Get image file to display
filename = askopenfilename(title='Select file')
window.title(os.path.basename(filename))

# Display image and color information of pixel pointed at by mouse
raw_image = Image.open(filename)
img = ImageTk.PhotoImage(raw_image)
panel = Label(window, image = img)
location = StringVar()
location.set('hello there')
position = Label(window, textvar=location)
panel.pack(side = "bottom", fill = "both", expand = "yes")
position.pack(side = 'top', fill='both', expand='yes')

def motion(event):
    x, y = event.x, event.y
    rgb = raw_image.getpixel((x, y))
    #color = munsell.from_rgb(rgb)
    location.set(str((x, y)) + str(rgb))

window.bind('<Motion>', motion)
window.mainloop()

