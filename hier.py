"""Script to analyse the antiquity texts"""

import numpy as np
import re
from sklearn.cluster import AgglomerativeClustering, KMeans

def read_html(html_file):
    """Reads in any .html file from a specified folder.

    This function will strip the file of all html tags,
    returning a string of the text in the html file excluding
    the words "OCR Output".

    Args
    ----
    html_file: String
        The folder to read the txt's from

    Returns
    -------
    out: String
        The text contained within the html file excluding html tags.
    """

    with open(html_file, 'r') as f:
        html = f.read()

    # Replace all html tags using regular expression
    # from http://stackoverflow.com/questions/11229831/regular-expression-to-remove-html-tags-from-a-string
    repl = re.sub("<[^>]*>"," ",html)

    # Replace all whitespace
    repl = re.sub("[^\w]+", " ", repl)

    # Replace any spaces at the beginning of the string
    repl = re.sub("^\s", "", repl)

    # and at the end!
    repl = re.sub("\s$", "", repl)

    # Finally the first 10 characters are always "OCR Output "
    # we remove them

    out = repl[11:]

    return out


def read_book(folder):
    """Takes a folder of 