from textnode import *
import os
import shutil
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
    # clear_directory_contents(dest)
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            shutil.copy(item_path, dest)
        # elif os.path.isdir(item_path):
        #     copy_source(item_path, )

def main():
    print("main")
    copy_source("../static/", "../public/")

main()