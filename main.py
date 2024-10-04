MAX_COLOR = 128

import sys
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from materialyoucolor.quantize import QuantizeCelebi, StbLoadImage
from materialyoucolor.score.score import Score
from PIL import Image, ImageTk


if __name__ == "__main__":
    root = Tk()

    button_quit = Button(root, text='Exit Program', command=root.quit, borderwidth=0)
    button_quit.pack()


    my_label = Label(borderwidth = 0)
    my_label.pack()


    def myClick():
        link = askopenfilename()
        imageTk = ImageTk.PhotoImage(Image.open(link))
        image = Image.open(link)
        pixel_len = image.width * image.height
        image_data = image.getdata()
        pixel_array = [image_data[_] for _ in range(0, pixel_len)]
        pixel_array = StbLoadImage(link)
        
        colors = QuantizeCelebi(pixel_array, MAX_COLOR)
        #print(colors)

        selected = Score.score(colors)
        print(selected)
        
        bgcolor = "#" + hex(selected[0])[4::]
        root.configure(background = bgcolor)

        #print(pixel_len)
        #print(image_data)
        my_label.configure(image=imageTk)
        my_label.image = imageTk


    myButton = Button(root, text='Scan Part Number', command=myClick,
                  bg='#ffaaaa', fg='#ffffff', borderwidth=0)
    myButton.pack()

    root.mainloop()
