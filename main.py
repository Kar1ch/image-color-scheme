MAX_COLOR = 128

import sys
import os
from pathlib import Path
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap
from materialyoucolor.utils.color_utils import rgba_from_argb
from materialyoucolor.quantize import QuantizeCelebi
from materialyoucolor.score.score import Score
from materialyoucolor.scheme.scheme import Scheme
from PIL import Image
import subprocess

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
        #for key in scheme.props.keys():
        #    print(key, scheme.props[key])
        return(scheme)
    

    def setWaybarColors(self, _color_int):
        home = Path.home()
        path_to_waybar_style = home / ".config/waybar/style.css"

        scheme = self.createColorScheme(_color_int)
        print(scheme.props["primary"])

        with open(path_to_waybar_style) as file:
            lines = file.readlines()

        is_button_color = False
        is_button_background_color = False
        is_active_button_color = False
        is_active_button_background_color = False
        is_clock_color = False
        is_clock_background_color = False
        for i, line in enumerate(lines):
            if "#workspaces button{" in line or "#workspaces button " in line:
                is_button_color = True
                is_button_background_color = True

            if "#workspaces button.active{" in line or "#workspaces button.active " in line:
                is_active_button_color = True
                is_active_button_background_color = True
            
            if "#clock" in line:
                is_clock_color = True
                is_clock_background_color = True


            if is_button_color and " color" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    parts[-1] = rgba_to_hex(scheme.props["primary"])[:-2] + ";"
                    lines[i] = ": ".join(parts) + "\n"
                is_button_color = False

            if is_button_background_color and " background-color" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    parts[-1] = rgba_to_hex(scheme.props["background"])[:-2] + ";"
                    lines[i] = ": ".join(parts) + "\n"
                is_button_background_color = False 


            if is_active_button_color and " color" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    parts[-1] = rgba_to_hex(scheme.props["onPrimary"])[:-2] + ";"
                    lines[i] = ": ".join(parts) + "\n"
                is_active_button_color = False

            if is_active_button_background_color and " background-color" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    parts[-1] = rgba_to_hex(scheme.props["primary"])[:-2] + ";"
                    lines[i] = ": ".join(parts) + "\n"
                is_active_button_background_color = False 


            if is_clock_color and " color" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    parts[-1] = rgba_to_hex(scheme.props["primary"])[:-2] + ";"
                    lines[i] = ": ".join(parts) + "\n"
                is_clock_color = False

            if is_clock_background_color and " background-color" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    parts[-1] = rgba_to_hex(scheme.props["background"])[:-2] + ";"
                    lines[i] = ": ".join(parts) + "\n"
                is_clock_background_color = False 


        with open(path_to_waybar_style, "w") as file:
            file.writelines(lines)


        subprocess.run(['bash', 'waybar_restart.sh'])
        


    def setHyprlandColors(self, _color_int):
        home = Path.home()
        scheme = self.createColorScheme(_color_int)
        new_border_color = (rgba_to_hex(scheme.props["primary"])[:-2])[1:]
        print("border", new_border_color)
        path_to_hyprland = home / ".config/hypr/hyprland.conf" 
        with open(path_to_hyprland) as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if "col.active_border" in line:
                parts = line.split('=')
                if len(parts) > 1:
                    parts[-1] = "rgba(" + new_border_color + "ff)"
                    lines[i] = '= '.join(parts) + "\n" 
        with open(path_to_hyprland, 'w') as file:
            file.writelines(lines)


    def openFileDialog(self):
        fname_E, selFilter = QFileDialog.getOpenFileName()
        image = Image.open(fname_E)
        pixel_len = image.width * image.height

        image_data = image.getdata()
        pixel_array = [image_data[_] for _ in range(0, pixel_len)]
        
        colors = QuantizeCelebi(pixel_array, MAX_COLOR)
        most_popular_color = max(colors, key=colors.get)

        
        print("Left accents:", self.getAccentColorsFromLeftSide(pixel_array, image.width, 0.5, MAX_COLOR))
        print("Left most common color:", self.getMostCommonColorFromLeftSide(pixel_array, image.width, 0.01, MAX_COLOR))
        accent_colors =  self.getAccentColorsFromImage(pixel_array, 64)
        print("Full image accents:", accent_colors)
        print("Most common color:", self.getMostCommonColorFromImage(pixel_array, 32))
        print(self.getMostCommonAccentColor(pixel_array, MAX_COLOR))

        self.createColorScheme(accent_colors[0])
        
        selected = Score.score(colors)

        for color in accent_colors:
            color_in_hex = hex(color)[4::]
            if (color_in_hex[0] != "f") and (color_in_hex[2] != "f") and (color_in_hex[4] != "f"):
                #self.setWaybarColors(color)
                self.setHyprlandColors(color)
                break


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




