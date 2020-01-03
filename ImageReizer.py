#
# This file is only intended to work on Windows.
#
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
import time
import concurrent.futures
# TODO: Add argparse to the program.
import argparse

"""
================
Prep variables
================
"""
init()
version = "0.6"

red = Fore.RED
yellow = Fore.YELLOW
cyan = Fore.CYAN
green = Fore.GREEN
reset = Style.RESET_ALL

DeleteInputFiles = False
BitConversion = False
CustomDimensions = "Custom"

Width = False
Height = False

"""
=============
Code begins
=============
"""


def init_run():
    print()
    global DeleteInputFiles
    global BitConversion
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

    print(f"{green}Deletion after finish: {cyan}{DeleteInputFiles} {reset}")
    print(f"{green}Dimensions: {cyan}{CustomDimensions}{reset}")
    print(f"{green}32 color depth: {cyan}{BitConversion}{reset}\n")

    print(f"{green}Choose your choice{reset}")
    print(f"{green} 1.{cyan} Start program{reset}")
    print(f"{green} 2.{cyan} Choose a set of listed dimensions{reset}")
    print(f"{green} 3.{cyan} Toggle deletion of images from input folder when finished{reset}")
    print(f"{green} 4.{cyan} Toggle color 32 color depth conversion{reset}")
    print(f"{green} 5.{cyan} Close Program{reset}")
    print(f"{red}Program may be slow the more images you use. This usually happens around the prep & finishing stages"
          f"{reset}")


def menu():
    init_run()
    global DeleteInputFiles
    global BitConversion
    i = input("Choice: ")

    if int(i) == 1:
        return

    elif int(i) == 2:
        dimensions()

    elif int(i) == 3:
        if DeleteInputFiles is True:
            DeleteInputFiles = False
        else:
            DeleteInputFiles = True
        menu()

    elif int(i) == 4:
        if BitConversion is True:
            BitConversion = False
        else:
            BitConversion = True
        menu()

    elif int(i) == 5:
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
    print(f" {yellow}2. {cyan}4K - 3840 x 2160p{reset}")
    print(f" {yellow}3. {cyan}1920 x 1080p{reset}")
    print(f" {yellow}4. {cyan}1280 x 720p{reset}")

    i = input("Choice: ")

    if int(i) == 1:
        CustomDimensions = "Custom"
        print(f"Dimensions is now set to {CustomDimensions}!")
        menu()

    elif int(i) == 2:
        CustomDimensions = "4K - 3840 x 2160p"
        print(f"Dimensions is now set to {CustomDimensions}!")
        Width = 3840
        Height = 2160

    elif int(i) == 3:
        CustomDimensions = "1920 x 1080p"
        print(f"Dimensions is now set to {CustomDimensions}!")
        Width = 1920
        Height = 1080

    elif int(i) == 4:
        CustomDimensions = "1280 x 720p"
        print(f"Dimensions is now set to {CustomDimensions}!")
        Width = 1280
        Height = 720

    elif i is not int:
        print("You must choose a number")
        dimensions()

    menu()


def file_conversion_prep():
    global DeleteInputFiles
    global BitConversion
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
            file_conversion_prep()
        try:
            Height = input("Height: ")
            Height = int(Height)
        except:
            print("Height needs to be a number and not contain any other characters")
            file_conversion_prep()

    FromDirectory = "Input"
    ToDirectory = "TempResizingFolder"

    if not os.path.exists(ToDirectory):
        print(f"NOTE: {yellow}Creating {ToDirectory} folder{reset}")
        os.makedirs(ToDirectory)

    print(f"NOTE: {yellow}Copying files from {FromDirectory} to {ToDirectory}.{reset}")
    copy_tree(FromDirectory, ToDirectory)

    print(f"INFO: {yellow}Resizing images{reset}")
    return f"{ToDirectory}\\", os.listdir(ToDirectory), FromDirectory


def image_conversion(path, item, Width, Height):
    global BitConversion
    if os.path.isfile(path + item):
        if BitConversion is True:
            im = Image.open(path + item).convert("RGBA")
        else:
            im = Image.open(path + item)
        imResize = im.resize((Width, Height), Image.NEAREST)
        # TODO: Support JPG & GIFs
        imResize.save(path + item, "PNG")
        return f"INFO: {cyan}Resized {item}{reset}"


def final_stage(path, FromDirectory):
    Output = "Output"
    if not os.path.exists(Output):
        print(f"INFO: {yellow}Creating {Output} folder{reset}")
        os.makedirs(Output)

    FromTemp = path
    print(f"NOTE: {yellow}Moving files from {FromTemp} to {Output}.{reset}")
    Folder = glob.glob(f"{FromTemp}\\*.*")
    OverwriteAll = False
    PassLoop = False
    for file in Folder:
        if OverwriteAll is True:
            print(f"INFO: {cyan}Moving {file} to {Output} folder & overwriting existing file.{reset}")
            Splitted = file.split("\\")
            os.remove(f"{Output}\\{Splitted[1]}")
            shutil.move(file, Output)
        else:
            try:
                shutil.move(file, Output)
                print(f"INFO: {cyan}Moving {file} to {Output} folder.{reset}")
            except Exception as e:
                if PassLoop is True:
                    pass
                else:
                    # TODO: Allow merging of files with existing files
                    print(f"WARN: {red}{e}{reset}")
                    print(f"{yellow}You got 6 choices{reset}")
                    print(f"{yellow} 1. {cyan}Overwrite the file{reset}")
                    print(f"{yellow} 2. {cyan}Overwrite all files in the process{reset}")
                    print(f"{yellow} 3. {cyan}Don't overwrite the file{reset}")
                    print(f"{yellow} 4. {cyan}Don't overwrite any files.{reset}")

                    i = input("Choice: ")

                    if int(i) == 1:
                        try:
                            print(f"INFO {cyan}Overwriting {file} in {Output} folder{reset}")
                            Splitted = file.split("\\")
                            os.remove(f"{Output}\\{Splitted[1]}")
                            shutil.move(file, Output)
                        except Exception as e:
                            print(e)

                    elif int(i) == 2:
                        print(f"INFO: {cyan}Program will now overwrite all files in {Output}{reset}")
                        try:
                            print(f"INFO {cyan}Overwriting {file} in {Output} folder{reset}")
                            Splitted = file.split("\\")
                            os.remove(f"{Output}\\{Splitted[1]}")
                            shutil.move(file, Output)
                        except Exception as e:
                            print(e)
                        OverwriteAll = True

                    elif int(i) == 3:
                        print("Ignoring file")

                    elif int(i) == 4:
                        print(f"INFO: {cyan}Now ignoring all existing files{reset}")
                        PassLoop = True

                    elif i is not int:
                        print("Did not register any request. Passing")
                        pass

    #  TODO: Display print command. If files didn't get moved. Don't display it
    print(f"NOTE: {yellow}Moved files from {FromTemp} to {Output}{reset}")

    try:
        print(f"NOTE: {yellow}Deleting {FromTemp} folder{reset}")
        os.rmdir(FromTemp)
    except:
        print(f"WARN: {red}Unable to delete {FromTemp}{reset}")

    if DeleteInputFiles is True:
        try:
            print(f"NOTE: {yellow}Deleting contents of {FromDirectory} folder{reset}")
            shutil.rmtree(FromDirectory)
        except:
            print(f"WARN: {red}Unable to delete some or all of {FromDirectory}'s folder content{reset}")

    output_folder = os.path.realpath(Output)
    os.startfile(output_folder)


def multi_process():

    time_start = time.perf_counter()
    path, dirs, FromDirectory = file_conversion_prep()

    if __name__ == "__main__":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            processes = []
            for item in dirs:
                process = executor.submit(image_conversion, path, item, Width, Height)
                processes.append(process)

            for f in processes:
                print(f.result())

    final_stage(path, FromDirectory)
    time_end = time.perf_counter()
    print(f"It took {round(time_end-time_start, 2)} second(s)!")


menu()
multi_process()
