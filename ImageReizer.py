
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
import argparse

"""
================
Prep variables
================
"""
init()
version = "1.0"

red = Fore.RED
yellow = Fore.YELLOW
cyan = Fore.CYAN
green = Fore.GREEN
reset = Style.RESET_ALL
"""
=============
Code begins
=============
"""


def init_run():
    print(f"{green}=================\n"
          f"  Image resizer\n"
          f"  version: {cyan}{version}{green}\n"
          f"================={reset}\n")

    print(f"{red}Program may be slow the more images you use. This usually happens around the prep & finishing stages"
          f"{reset}")

    InputFolder = "Input"
    if not os.path.exists(InputFolder):
        print(f"NOTE: {yellow}-Creating {InputFolder} folder{reset}")
        os.makedirs(InputFolder)

        path = os.path.realpath(InputFolder)
        os.startfile(path)
    input("PRESS ENTER TO CONTINUE")

    file_conversion()


def menu():
    # User choices
    print()


def file_conversion():
    isInt = False
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
        print(f"NOTE: {yellow}-Creating {ToDirectory} folder{reset}")
        os.makedirs(ToDirectory)

    print(f"NOTE: Copying files from {FromDirectory} to {ToDirectory}.")
    copy_tree(FromDirectory, ToDirectory)

    print("Resizing images")
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
        print(f"NOTE: {yellow}-Creating {Output} folder{reset}")
        os.makedirs(Output)

    FromTemp = ToDirectory
    print(f"NOTE: Copying files from {FromTemp} to {Output}.\nPlease wait.")
    copy_tree(FromTemp, Output)

    path = os.path.realpath(Output)
    os.startfile(path)




init_run()


def file_conversion_not_in_use():

    files = glob.glob('Prep\\*.*')
    for file in files:
        print(f"INFO: {cyan}Renaming {file}{reset}")
        parts = file.split(".")
        new_name = "{}.png".format(parts[0])
        try:
            os.rename(file, new_name)
        except:
            os.replace(file, new_name)

    print("Fixing color depth")
    path = "Prep\\"
    dirs = os.listdir("Prep")
    for item in dirs:
        if os.path.isfile(path + item):
            print(f"INFO: {cyan}Fixing color depth for {item}{reset}")
            im = Image.open(path + item).convert("RGBA")
            im.save(path + item, "PNG")

    if not os.path.exists("Finished"):
        print(f"NOTE: {yellow}-Creating Finished folder{reset}")
        os.makedirs("Finished")

    Move1 = glob.glob("Prep\\*.*")
    print("Moving files from Prep to Finished folder")
    for file in Move1:
        print(f"INFO: {cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, "Finished")
    print("Moved files from Prep to Finished")

    print(f"NOTE: {yellow}Deleting Prep folder{reset}")
    os.rmdir("Prep")

    Move2 = glob.glob("LSPTTemp\\*.*")
    print("Moving files from LSPTTemp to Finished folder")
    for file in Move2:
        print(f"INFO: {cyan}Moving {file} to Finished folder. {reset}")
        shutil.move(file, "Finished")
    print("Moved files from LSPTTemp to Finished")

    print(f"NOTE: {yellow}Deleting LSPTTemp folder{reset}")
    os.rmdir("LSPTTemp")

    sg.Popup("Done!\nYou can now move the photos to 76")
    path = "Finished"
    path = os.path.realpath(path)
    os.startfile(path)