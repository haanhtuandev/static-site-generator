from textnode import *
import os
import shutil


def clear_directory_contents(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def copy_source(path, dest):
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        print(item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            shutil.copy(item_path, dest)
        elif os.path.isdir(item_path):
            dir_path = f"{dest}{item}/" 
            os.mkdir(dir_path)
            new_path = item_path + "/"
            copy_source(new_path, dir_path)

def main():
    copy_source("static/", "public/")

clear_directory_contents("public/")
main()
