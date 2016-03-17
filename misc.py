from glob import glob
import numpy as np
from os.path import join, split
import re
from sklearn.cluster import AgglomerativeClustering, KMeans


names = ["gap_y-AvAAAAYAAJ", "gap_XmqHlMECi6kC",
         "gap_WORMAAAAYAAJ", "gap_VPENAAAAQAAJ",
         "gap_udEIAAAAQAAJ", "gap_TgpMAAAAYAAJ",
         "gap_RqMNAAAAYAAJ", "gap_pX5KAAAAYAAJ",
         "gap_ogsNAAAAIAAJ", "gap_MEoWAAAAYAAJ",
         "gap_m_6B1DkImIoC", "gap_IlUMAQAAMAAJ",
         "gap_GIt0HMhqjRgC", "gap_fnAMAAAAYAAJ",
         "gap_DqQNAAAAYAAJ", "gap_dIkBAAAAQAAJ",
         "gap_DhULAAAAYAAJ", "gap_CSEUAAAAYAAJ",
         "gap_CnnUAAAAMAAJ", "gap_Bdw_AAAAYAAJ",
         "gap_aLcWAAAAQAAJ", "gap_9ksIAAAAQAAJ",
         "gap_2X5KAAAAYAAJ", "gap_-C0BAAAAQAAJ"]

titles = ["The Works of Flavius Josephus Vol 3",
          "Gibbons History of the Decline and Fall of the Roman Empire Vol 6",
          "The Histories of Caius Cornelius Tacitus with Notes for Colleges",
          "The History of the Decline and Fall of the Roman Empire Vol 5",
          "The First and Thirty-Third Book of Pliny's Natural History", 
          "The Genuine works of Flavius Josephus the Jewish historian Vol 1",
          "Livy Vol 5", 
          "The Works of Cornelius Tacitus Vol 4",
          "The Works of Josephus Vol 4", 
          "The Historical Annals of Cornelius Tacitus Vol 1",
          "Titus Livius Roman History", 
          "Gibbons History of the Decline and Fall of the Roman Empire Vol 2",
          "Gibbons History of the Decline and Fall of the Roman Empire Vol 4", 
          "The History of the Peloponnesian War Vol 1",
          "Livy Vol 3", 
          "The History of Rome Vol 3",
          "The Description of Greece by Pausania Vol 4", 
          "The History of the Decline and Fall of the Roman empire Vol 3",
          "The Whole Genuine Works of Flavius Josephus Vol 2", 
          "The History of Rome by Titus Livius Vol 1",
          "Gibbons History of the Decline and Fall of the Roman Empire Vol 1", 
          "The History of the Peloponnesian War Vol 2",
          "The Works of Cornelius Tacitus Vol 5", 
          "Dictionary of Greek and Roman Geography"]

abbrev = ["Flavius Josephus 3",
          "Gibbon's DaF 6",
          "Cornelius Tacitus",
          "DaF 5",
          "Pliny's Natural History",
          "Flavius Josephus 1",
          "Livy: Vol 5",
          "Cornelius Tacitus 4",
          "Flavius Josephus 4",
          "Cornelius Tacitus 1",
          "Titus Livius",
          "Gibbon's DaF 2",
          "Gibbon's DaF 4",
          "Peloponnesian War 1",
          "Livy: Vol 3",
          "History of Rome 3",
          "Description of Greece",
          "DaF 3",
          "Flavius Josephus 2", 
          "History of Rome TL 1",
          "Gibbon's DaF 1", 
          "Peloponnesian War 2",
          "Cornelius Tacitus 5", 
          "Greek and Roman\n Geography"]

abb = ["FJ3",
       "G DaF 6",
       "CT",
       "DaF 5",
       "PNH",
       "FJ1",
       "Livy 5",
       "CT4",
       "FJ4",
       "CT1",
       "TL",
       "G DaF 2",
       "G DaF 4",
       "PW 1",
       "Livy 3",
       "HoR3",
       "D Greece",
       "DaF 3",
       "FJ2", 
       "HoR TL 1",
       "G DaF 1", 
       "PW2",
       "CT5", 
       "Geog"]

# I thought it would be interesting to create my own linkage table with what
# should be linked (only by the titles and my knowledge of the Roman empire)


def read_txts(folder, notitles=False):

    name_list = []
    for name in names:
        if notitles:
            new_name = name + "_notitles.txt"
        else:
            new_name = name + ".txt"
        new = join(folder, new_name)
        name_list.append(new)

    text_list = []
    for file in name_list:
        with open(file, 'r') as f:
            texts = f.read()
        text_list.append(texts)

    return text_list