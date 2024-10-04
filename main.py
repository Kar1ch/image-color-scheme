import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

root = Tk()

button_quit = Button(root, text='Exit Program', command=root.quit)
button_quit.pack()


my_label = Label()
my_label.pack()


def myClick():
    link = askopenfilename()
    my_img = ImageTk.PhotoImage(Image.open(link))
    my_label.configure(image=my_img)
    my_label.image = my_img


myButton = Button(root, text='Scan Part Number', command=myClick,
                  bg='pink', fg='white')
myButton.pack()



root.mainloop()
