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

def combine_hex_values(d):
  d_items = sorted(d.items())
  tot_weight = sum(d.values())
  red = int(sum([int(k[:2], 16)*v for k, v in d_items])/tot_weight)
  green = int(sum([int(k[2:4], 16)*v for k, v in d_items])/tot_weight)
  blue = int(sum([int(k[4:6], 16)*v for k, v in d_items])/tot_weight)
  zpad = lambda x: x if len(x)==2 else '0' + x
  return zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:])




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
        

        left_pixels = []
        for i in range(1, len(pixel_array), image.width):
            for j in range(int(image.width * 0.5)):
                left_pixels.append(pixel_array[i+j])

            #print(i, pixel_array[i])

        left_colors = QuantizeCelebi(left_pixels, MAX_COLOR)
        #print(left_colors)
        
        colors = QuantizeCelebi(pixel_array, MAX_COLOR)
        most_popular_color = max(colors, key=colors.get)


        left_selected = Score.score(left_colors)
        left_selected_hex = [hex(color)[4::] for color in left_selected]
        #print(left_selected_hex)


        selected = Score.score(colors)
        #print(selected)
        

        allcolors_in_hex = [hex(color)[4::] for color in colors]
        
        allcolorstotaloccurance = 0
        for color in colors:
            allcolorstotaloccurance += colors[color]
            #print(colors[i])

        allcolors_and_occurance = {}
        cnt = 0
        for color in colors:
            allcolors_and_occurance[allcolors_in_hex[cnt]] = (colors[color] ) / allcolorstotaloccurance
            cnt += 1
            #print((colors[selected[i]] * 100) / totaloccurance)

        #print(allcolors_and_occurance)


        left_colors_in_hex = [hex(left_color)[4::] for left_color in left_colors]
        
        leftcolorstotaloccurance = 0
        for left_color in left_colors:
            leftcolorstotaloccurance += left_colors[left_color]
            #print(colors[i])

        left_colors_and_occurance = {}
        cnt = 0
        for left_color in left_colors:
            left_colors_and_occurance[left_colors_in_hex[cnt]] = (left_colors[left_color] ) / leftcolorstotaloccurance
            cnt += 1





        selected_in_hex = [hex(color)[4::] for color in selected]
        
        
        totaloccurance = 0
        for i in range(len(selected)):
            totaloccurance += colors[selected[i]]
            #print(colors[selected[i]])

        colors_and_occurance = {}
        for i in range(len(selected)):
            colors_and_occurance[selected_in_hex[i]] = (colors[selected[i]] ) / totaloccurance
            #print((colors[selected[i]] * 100) / totaloccurance)

        #print(colors_and_occurance)
        


        #bgcolor = "#" + hex(selected[0])[4::]
        #print(colors[selected[0]])
        #bgcolor = "#" + combine_hex_values(colors_and_occurance)
        #bgcolor = "#" + combine_hex_values(left_colors_and_occurance)
        bgcolor = "#" + hex(most_popular_color)[4::]

        #bgcolor = "#" + combine_hex_values(allcolors_and_occurance)
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
        lb.resize(300, int((image.height * 300) / image.width))
        lb.setPixmap(pixmap.scaled(lb.size()))

        
        #layout = QVBoxLayout()
        button = QPushButton("Выбрать картинку")
        color = selected[0]
        bgcolorbutton = "#" + hex(color)[4::]

        button.setStyleSheet("background-color: " + bgcolorbutton + "; border-radius: 8px;" )
        button.setFixedSize(QSize(160, 50))
        button.clicked.connect(self.openFileDialog)
        layout.addWidget(button)

        layout.addWidget(lb)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        #print(pixel_len)




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
