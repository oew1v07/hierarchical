"""Script to analyse google antiquity texts"""

from glob import glob
import numpy as np
from os.path import join, split
import re
from sklearn.cluster import AgglomerativeClustering, KMeans
from nltk.corpus import stopwords

def list_of_books(folder):
    pattern = join(folder, "*")
    book_list = glob(pattern)
    return book_list

def remove_titles(html_text):
    """Removes the chapter files from the html text.

    Args
    ----
    html_text: String
        Text from an html file

    Returns
    -------
    out: String
        The text contained within the html file excluding chapter titles.
    """

    pattern = "<div class='ocrx_block'.+?>.+?</div>"

    # DOTALL means it works over newlines!
    out = re.sub(pattern, " ", html_text, count=1, flags=re.DOTALL)
    return out


def read_html(html_file):
    """Reads in any .html file from a specified folder.

    Args
    ----
    html_file: String
        The folder to read the txt's from

    Returns
    -------
    out: String
        The text contained within the html file
    """

    with open(html_file, 'r') as f:
        html = f.read()

    return html


def remove_nonwords(html_text):
    """Strips file of all html tags, and whitespace.

    Returning a string of the text in the html file excluding
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

    # Replace all html tags using regular expression
    # from http://stackoverflow.com/questions/11229831/regular-expression-to-remove-html-tags-from-a-string
    repl = re.sub("<[^>]*>"," ",html_text)

    # Replace all whitespace
    repl = re.sub("[^A-Za-z]+", " ", repl)

    # Replace any spaces at the beginning of the string
    repl = re.sub("^\s", "", repl)

    # and at the end!
    repl = re.sub("\s$", "", repl)

    # Finally the first 10 characters are always "OCR Output "
    # we remove them

    out = repl[11:]

    return out

def remove_stopwords(html_text):
    """Removes stopwords, makes all letters lowercase.

    Possibly will include stemming and lemmatisation"""
    
    # Split text on spaces and create set (performance)
    text = html_text.lower().split()

    words = [w for w in text if not w in stopwords.words("english")]

    words2 = [w for w in words if len(w) > 2]

    # return to a string

    out = " ".join(words2)

    return out



def read_book(folder, save=True, output_folder=None, titles_remove=False):
    """Takes a folder of html files and reads them all into one string

    Args
    ----
    folder: String
        The folder to read html files from
    save: boolean
        Saves the output into a txt file
    titles_remove: boolean
        Removes the chapter titles from the text

    Returns
    -------
    out: String
        The text from each of the html files
    """
    # Define the glob pattern
    pattern = join(folder, "*.html")

    # Get list of html files in each folder
    html_files = glob(pattern)

    text_list = []

    for html in html_files:
        text = read_html(html)

        if titles_remove:
            clean = remove_stopwords(remove_nonwords(remove_titles(text)))
        else:
            clean = remove_stopwords(remove_nonwords(text))
        text_list.append(clean)

    repl = " ".join(text_list)

    # Replace all whitespace since joining using spaces
    repl = re.sub("[^\w]+", " ", repl)

    # Replace any spaces at the beginning of the string
    repl = re.sub("^\s+", "", repl)

    # and at the end!
    out = re.sub("\s+$", "", repl)

    if save:
        x, name = split(folder)
        if titles_remove:
            name = name + "_notitles.txt"
        else:
            name = name + ".txt"
        name = join(output_folder, name)
        with open(name, 'w') as f:
            f.write(out)

    return out

def save_all_books(folder, output_folder, titles_remove=False):
    """Cleans data and saves as new text files"""

    book_list = list_of_books(folder)

    for book in book_list:
        read_book(book, save=True, output_folder=output_folder, titles_remove=titles_remove)
