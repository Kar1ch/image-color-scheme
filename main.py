MAX_COLOR = 128

import sys
import os
from tkinter import *
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap
from tkinter.filedialog import askopenfilename
from materialyoucolor.utils.color_utils import rgba_from_argb
from materialyoucolor.quantize import QuantizeCelebi, StbLoadImage
from materialyoucolor.score.score import Score
from materialyoucolor.scheme.scheme import Scheme
from PIL import Image, ImageTk

rgba_to_hex = lambda rgba: "#{:02X}{:02X}{:02X}{:02X}".format(*map(round, rgba))



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("ашалеть")
        self.setStyleSheet("background-color: black;") 
        self.resize(800, 600)

        layout = QVBoxLayout()
        button = QPushButton("Выбрать картинку")
        button.setStyleSheet("background-color: gray; border-radius: 10px;" )
        button.setFixedSize(QSize(150, 60))
        button.clicked.connect(self.openFileDialog)
        layout.addWidget(button)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    
    def openFileDialog(self):
        fname_E, selFilter = QFileDialog.getOpenFileName()
        image = Image.open(fname_E)
        pixel_len = image.width * image.height


        image_data = image.getdata()
        pixel_array = [image_data[_] for _ in range(0, pixel_len)]
        pixel_array = StbLoadImage(fname_E)
        
        colors = QuantizeCelebi(pixel_array, MAX_COLOR)
        #print(colors)

        selected = Score.score(colors)
        print(selected)
        


        bgcolor = "#" + hex(selected[0])[4::]
        
        self.setStyleSheet("background-color: "+ bgcolor + ";") 

        
        #frame = Frame(root, background='white')
        layout = QVBoxLayout()
        maincolors = []
        for i in range(len(selected)):    
            color = selected[i]
            bgcolorlabel = "#" + hex(color)[4::]
            colorLabel = QLabel(self)
            colorLabel.setStyleSheet("background-color: " + bgcolorlabel + ";")
            colorLabel.setFixedSize(QSize(60, 20))
            layout.addWidget(colorLabel)
            #maincolors.append(Label(frame, background=bgcolorlabel, width=10))
            #maincolors[i].pack(padx=1, pady=1)
            #layout.addWidget()
        #frame.pack(padx=0, pady=0)
        
        '''
        test = Scheme.light(selected[0])
        schemecolors = []
        cnt = 0
        schemelabel = Label(frame, background="white", text="Scheme.light", width=10)
        schemelabel.pack(padx=1, pady=1)
        for key in test.props.keys():
            color = selected[i]
            #bgcolorlabel = "#" + hex(color)[4::]
            schemecolors.append(Label(frame, background=rgba_to_hex(test.props[key])[:-2], width=10))
            schemecolors[cnt].pack(padx=1, pady=1)
            cnt += 1
            myButton.configure(background=rgba_to_hex(test.props["primaryContainer"])[:-2])
            button_quit.configure(background=rgba_to_hex(test.props["error"])[:-2])
            print(rgba_to_hex(test.props[key]))

        '''




        lb = QLabel(self)
        pixmap = QPixmap(fname_E)
        height_label = 100
        lb.resize(int(image.width/2), int(image.height/2))
        lb.setPixmap(pixmap.scaled(lb.size()))

        
        #layout = QVBoxLayout()
        button = QPushButton("Выбрать картинку")
        color = selected[1]
        bgcolorbutton = "#" + hex(color)[4::]

        button.setStyleSheet("background-color: " + bgcolorbutton + "; border-radius: 8px;" )
        button.setFixedSize(QSize(160, 50))
        button.clicked.connect(self.openFileDialog)
        layout.addWidget(button)

        layout.addWidget(lb)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        print(pixel_len)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()





'''

if __name__ == "__main__":
    root = Tk()
    root.geometry("800x600")
    #root.configure(background="#ffffff")

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

        
        frame = Frame(root, background='white')
        frame.pack_forget()
        maincolors = []
        for i in range(len(selected)):    
            color = selected[i]
            bgcolorlabel = "#" + hex(color)[4::]
            maincolors.append(Label(frame, background=bgcolorlabel, width=10))
            maincolors[i].pack(padx=1, pady=1)
        frame.pack(padx=0, pady=0)
        

        test = Scheme.light(selected[0])
        schemecolors = []
        cnt = 0
        schemelabel = Label(frame, background="white", text="Scheme.light", width=10)
        schemelabel.pack(padx=1, pady=1)
        for key in test.props.keys():
            color = selected[i]
            #bgcolorlabel = "#" + hex(color)[4::]
            schemecolors.append(Label(frame, background=rgba_to_hex(test.props[key])[:-2], width=10))
            schemecolors[cnt].pack(padx=1, pady=1)
            cnt += 1
            myButton.configure(background=rgba_to_hex(test.props["primaryContainer"])[:-2])
            button_quit.configure(background=rgba_to_hex(test.props["error"])[:-2])
            print(rgba_to_hex(test.props[key]))
       

        #print(test.props.keys())

        #print(pixel_len)
        #print(image_data)
        my_label.configure(image=imageTk)
        my_label.image = imageTk



    myButton = Button(root, text='Scan Part Number', command=myClick,
                  bg='#ffaaaa', fg='#ffffff', borderwidth=0)
    myButton.pack()

    root.mainloop()

'''
