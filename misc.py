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