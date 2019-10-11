# ==============
# Import list
# ==============

from distutils.dir_util import copy_tree
from colorama import init, Fore, Style
import os
import sys
import glob
import shutil
from PIL import Image
# TODO: Add argparse to the program.
import argparse

"""
================
Prep variables
================
"""
init()
version = "0.4"

red = Fore.RED
yellow = Fore.YELLOW
cyan = Fore.CYAN
green = Fore.GREEN
reset = Style.RESET_ALL

DeleteInputFiles = False
CustomDimensions = "Custom"

Width = False
Height = False

"""
=============
Code begins
=============
"""


def init_run():
    print(f"{green}=================\n"
          f"  Image resizer\n"
          f"  version: {cyan}{version}{green}\n"
          f"================={reset}")

    InputFolder = "Input"
    if not os.path.exists(InputFolder):
        print(f"NOTE: {yellow}Creating {InputFolder} folder{reset}")
        os.makedirs(InputFolder)

        path = os.path.realpath(InputFolder)
        os.startfile(path)
    menu()


def menu():
    global DeleteInputFiles

    print(f"{green}Deletion after finish: {cyan}{DeleteInputFiles} {reset}")
    print(f"{green}Dimensions: {cyan}{CustomDimensions}{reset}\n")

    print(f"{green}Choose your choice{reset}")
    print(f"{green} 1.{cyan} Start program{reset}")
    print(f"{green} 2.{cyan} Choose a set of listed dimensions{reset}")
    print(f"{green} 3.{cyan} Toggle deletion of images from input folder when finished{reset}")
    print(f"{green} 4.{cyan} Close Program{reset}")
    print(f"{red}Program may be slow the more images you use. This usually happens around the prep & finishing stages"
          f"{reset}")

    i = input("Choice: ")

    if int(i) == 1:
        file_conversion()

    elif int(i) == 2:
        dimensions()

    elif int(i) == 3:
        if DeleteInputFiles is True:
            DeleteInputFiles = False
        else:
            DeleteInputFiles = True
        menu()

    elif int(i) == 4:
        sys.exit()

    elif i is not int:
        print("Only use numbers\n")
        menu()


def dimensions():
    global CustomDimensions
    global Width
    global Height

    print(f"{yellow}Choose one of the following{reset}")
    print(f" {yellow}1. {cyan}Custom dimensions{reset}")
    print(f" {yellow}2. {cyan}1920 x 1080p{reset}")
    print(f" {yellow}3. {cyan}1280 x 720p{reset}")

    i = input("Choice: ")

    if int(i) == 1:
        CustomDimensions = "Custom"
        print(f"Dimensions is now set to {CustomDimensions}!")
        menu()

    elif int(i) == 2:
        CustomDimensions = "1920 x 1080p"
        print(f"Dimensions is now set to {CustomDimensions}!")
        Width = 1920
        Height = 1080

    elif int(i) == 3:
        CustomDimensions = "1280 x 720p"
        print(f"Dimensions is now set to {CustomDimensions}!")
        Width = 1280
        Height = 720

    elif i is not int:
        print("You must choose a number")
        dimensions()

    menu()


def file_conversion():
    global DeleteInputFiles
    global Width
    global Height

    if Width is not False and Height is not False:
        pass
    else:
        try:
            Width = input("Width: ")
            Width = int(Width)
        except:
            print("Width needs to be a number and not contain any other characters")
            file_conversion()
        try:
            Height = input("Height: ")
            Height = int(Height)
        except:
            print("Height needs to be a number and not contain any other characters")
            file_conversion()

    FromDirectory = "Input"
    ToDirectory = "TempResizingFolder"

    if not os.path.exists(ToDirectory):
        print(f"NOTE: {yellow}Creating {ToDirectory} folder{reset}")
        os.makedirs(ToDirectory)

    print(f"NOTE: {yellow}Copying files from {FromDirectory} to {ToDirectory}.{reset}")
    copy_tree(FromDirectory, ToDirectory)

    # TODO: Add the option to convert images into 32 bit depth
    print(f"INFO: {yellow}Resizing images{reset}")
    path = f"{ToDirectory}\\"
    dirs = os.listdir(ToDirectory)
    for item in dirs:
        if os.path.isfile(path + item):
            print(f"INFO: {cyan}Resizing {item}{reset}")
            im = Image.open(path + item)
            imResize = im.resize((Width, Height), Image.ANTIALIAS)
            imResize.save(path + item, "PNG")

    Output = "Output"
    if not os.path.exists(Output):
        print(f"INFO: {yellow}Creating {Output} folder{reset}")
        os.makedirs(Output)

    # TODO: Add a check to override files that already exist in output or to rename files
    FromTemp = ToDirectory
    print(f"NOTE: {yellow}Moving files from {FromTemp} to {Output}.{reset}")
    Folder = glob.glob(f"{FromTemp}\\*.*")
    for file in Folder:
        print(f"INFO: {cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, Output)
    print(f"NOTE: {yellow}Moved files from {FromTemp} to {Output}{reset}")

    try:
        print(f"NOTE: {yellow}Deleting {FromTemp} folder{reset}")
        os.rmdir(FromTemp)
    except:
        print(f"WARN: Unable to delete {FromTemp}")

    if DeleteInputFiles is True:
        try:
            print(f"NOTE: {yellow}Deleting contents of {FromDirectory} folder{reset}")
            shutil.rmtree(FromDirectory)
        except:
            print(f"WARN: Unable to delete some or all of {FromDirectory}'s folder content")

    path = os.path.realpath(Output)
    os.startfile(path)


init_run()
