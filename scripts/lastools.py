# coding: utf-8
# Thomas Bernard
# Liste de fonctions utilisant lastools (ltl)

import subprocess

def clip_ptcloud(filename,shapefile):
    commande = "lasclip -i " + filename + " -poly " + shapefile+ ' -v' 
    subprocess.call(commande)
    return True

def set_boundary(filename,concavity):
    commande = "lasboundary -i " + filename + " -concavity "+str(concavity)+" -disjoint -oshp"
    subprocess.call(commande)
    return True
    