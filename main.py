MAX_COLOR = 128

import sys
import os
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap
from materialyoucolor.utils.color_utils import rgba_from_argb
from materialyoucolor.quantize import QuantizeCelebi, StbLoadImage
from materialyoucolor.score.score import Score
from materialyoucolor.scheme.scheme import Scheme
from PIL import Image

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
        self.resize(320, 400)

        layout = QVBoxLayout()
        button = QPushButton("Выбрать картинку")
        button.setStyleSheet("background-color: gray; border-radius: 10px;" )
        button.setFixedSize(QSize(150, 60))
        button.clicked.connect(self.openFileDialog)
        layout.addWidget(button)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    
    def getPixelsFromLeftSide(self, _pixel_array, _image_width, _percent_of_image):
        pixels_of_left_side                 = []
        for i in range(1, len(_pixel_array), _image_width):
            for j in range(int(_image_width * _percent_of_image)):
                pixels_of_left_side.append(_pixel_array[i+j])
        return pixels_of_left_side


    def getAccentColorsFromLeftSide(self, _pixel_array, _image_width, _percent_of_image, _max_color):
        pixels_of_left_side                 = self.getPixelsFromLeftSide(_pixel_array, _image_width, _percent_of_image)
        colors_of_left_side                 = QuantizeCelebi(pixels_of_left_side, _max_color)
        selected_colors_of_left_side        = Score.score(colors_of_left_side)
        selected_colors_of_left_side_in_hex = [hex(color)[4::] for color in selected_colors_of_left_side]
        return selected_colors_of_left_side_in_hex
        
    
    def getMostCommonColorFromLeftSide(self, _pixel_array, _image_width, _percent_of_image, _max_color):
        pixels_of_left_side                 = self.getPixelsFromLeftSide(_pixel_array, _image_width, _percent_of_image)
        colors_of_left_side                 = QuantizeCelebi(pixels_of_left_side, _max_color)
        most_popular_color                  = max(colors_of_left_side, key=colors_of_left_side.get)
        most_popular_color_in_hex           = hex(most_popular_color)[4::]
        return most_popular_color_in_hex


    def getAccentColorsFromImage(self, _pixel_array, _max_color):
        colors                              = QuantizeCelebi(_pixel_array, _max_color)
        accent_colors                       = Score.score(colors)
        selected_in_hex                     = [hex(color)[4::] for color in accent_colors]
        #return selected_in_hex
        return accent_colors
    
    def getMostCommonColorFromImage(self, _pixel_array, _max_color):
        colors                              = QuantizeCelebi(_pixel_array, _max_color)
        most_popular_color                  = max(colors, key=colors.get)
        most_popular_color_in_hex           = hex(most_popular_color)[4::]
        return most_popular_color_in_hex 

    
    def getMostCommonAccentColor(self, _pixel_array, _max_color):
        colors                              = QuantizeCelebi(_pixel_array, _max_color)
        accent_colors                       = Score.score(colors)
        most_popular_accent_color           = 0
        max_occurance                       = 0
        for color in accent_colors:
            if max_occurance < colors[color]:
                max_occurance               = colors[color]
                most_popular_accent_color   = color
            #print(color, colors[color])
        most_popular_accent_color_in_hex    = hex(most_popular_accent_color)[4::]
        return most_popular_accent_color_in_hex


    def createColorScheme(self, _primary_color):
        scheme = Scheme.dark(_primary_color)
        scheme_colors = []
        for key in scheme.props.keys():
            print(key, scheme.props[key])


    def openFileDialog(self):
        fname_E, selFilter = QFileDialog.getOpenFileName()
        image = Image.open(fname_E)
        pixel_len = image.width * image.height

        image_data = image.getdata()
        pixel_array = [image_data[_] for _ in range(0, pixel_len)]
        pixel_array = StbLoadImage(fname_E)
        
        colors = QuantizeCelebi(pixel_array, MAX_COLOR)
        most_popular_color = max(colors, key=colors.get)

        
        print("Left accents:", self.getAccentColorsFromLeftSide(pixel_array, image.width, 0.5, MAX_COLOR))
        print("Left most common color:", self.getMostCommonColorFromLeftSide(pixel_array, image.width, 0.01, MAX_COLOR))
        accent_colors =  self.getAccentColorsFromImage(pixel_array, MAX_COLOR)
        print("Full image accents:", accent_colors)
        print("Most common color:", self.getMostCommonColorFromImage(pixel_array, 32))
        print(self.getMostCommonAccentColor(pixel_array, MAX_COLOR))

        self.createColorScheme(accent_colors[0])
        



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
        #bgcolor = "#" + hex(most_popular_color)[4::]

        #bgcolor = "#" + combine_hex_values(allcolors_and_occurance)

        bgcolor = "#" + self.getMostCommonColorFromImage(pixel_array, MAX_COLOR)
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




