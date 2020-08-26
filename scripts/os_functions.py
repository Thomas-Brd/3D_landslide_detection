# coding: utf-8
# Thomas Bernard
# fonctions gérant les fichiers et dossiers


import os


def create_folder(path):
    if os.path.isdir(path) == True:
        contenu=os.listdir(path)
        for x in contenu:
           os.remove(path+x)#on supprime tous les fichier dans le dossier
        os.rmdir(path)#puis on supprime le dossier
    os.mkdir(path)
    
def open_folder(path):
    if os.path.isdir(path) == True:
        os.chdir(path)
    else:
        os.mkdir(path)
    
def open_windowsfolder(path):
    import webbrowser
    webbrowser.open(path) 
    
def delete_file_extension(folder_path,extension):
    from os import listdir
    
    for file_name in listdir(folder_path):
        if file_name.endswith(extension):
            os.remove(folder_path + file_name)