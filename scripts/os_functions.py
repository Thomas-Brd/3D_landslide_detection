# coding: utf-8
# Thomas Bernard


import os


def create_folder(path):
    if os.path.isdir(path) == True:
        contenu=os.listdir(path)
        for x in contenu:
            os.remove(path+x)
        os.rmdir(path)
    os.mkdir(path)
    
def open_folder(path):
    if os.path.isdir(path) == True:
        os.chdir(path)
    else:
        os.mkdir(path)
