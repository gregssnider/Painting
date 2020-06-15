""" Analyze pixels in a color image.

Prompts the user for an image file name then displays it. Shows the RGB
and Munsell color for the pixel pointed at by the mouse.

"""
import os
from tkinter import Label, Tk, StringVar
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from color import munsell

if __name__ == '__main__':
    # Create Window for color analysis
    window = Tk()
    window.configure(background='grey')

    # Get image file to display
    filename = askopenfilename(title='Select file')
    window.title(os.path.basename(filename))

    # Display image and color information of pixel pointed at by mouse
    MAX_WIDTH = 1200
    MAX_HEIGHT = 700
    raw_image = Image.open(filename)
    raw_image.thumbnail((MAX_WIDTH, MAX_HEIGHT))
    img = ImageTk.PhotoImage(raw_image)
    panel = Label(window, image = img)
    location = StringVar()
    location.set('hue value chroma:')
    position = Label(window, textvar=location)
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    position.pack(side = 'top', fill='both', expand='yes')

    def clamp(n, smallest, largest):
        return max(smallest, min(n, largest))

    def motion(event):
        # Get mouse position clamped to borders of displayed image.
        width = img.width()
        height = img.height()
        x, y = clamp(event.x, 0, width - 1), clamp(event.y, 0, height - 1)

        # Display color info.
        rgb = raw_image.getpixel((x, y))
        hue, value, chroma = munsell.from_rgb(rgb)
        location.set('hue value chroma:  ' +
                     hue + '  ' + str(value) + '  ' + str(chroma) +
                     '   rgb:  ' +
                     str(rgb[0]) + ' ' + str(rgb[1]) + ' ' + str(rgb[2])
                     )

    window.bind('<Motion>', motion)
    window.mainloop()
