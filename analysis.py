import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.manifold import MDS
from misc import *
from cleaning import *
# This function should be unnecessary since
# Only uses words where it is mentioned in corpus at least 3 times

def BoW(texts, vectorizerType="count", min_df=3):
    """Takes a list of texts and creates a BoWs object

    Args
    ----
    texts: List of Strings
        all the texts
    vectorizerType: String
        One of "count" or "tfidf"
    min_df: int
        Minimum number of letters a word must be

    Returns
    -------
    CV: Vectorizer object
        One of CountVectorizer or 
    BoWs: Fitted Vectorizer object
    """

    if vectorizerType == "count":
        CV = CountVectorizer(min_df=min_df)
    elif vectorizerType == "tfidf":
        CV = TfidfVectorizer(min_df=min_df)

    BoWs = CV.fit_transform(texts)

    return CV, BoWs


def vocab_size(texts, min_count=[1,2,3,4,5], visualise=False, save=False):
    """Plots vocab size as a function of minimum letter count

    Args
    ----
    texts: list of Strings
        List of all the texts

    Returns
    -------
    sizes: List of ints
        Size of vocabulary
    """
    sizes = []
    for i in min_count:
        CV = CountVectorizer(min_df = i)
        BoWs = CV.fit_transform(texts)
        sizes.append(BoWs.shape[1])

    if visualise:
        plt.clf()
        plt.plot(min_count, sizes, 'bo-')
        if save:
            plt.savefig("Count_vs_vocabSize.png")

    return sizes


def folder_to_array(folder, notitles=False, vectorizerType="count", min_df=3):
    """Takes folder and returns BoWs array
    Args
    ----
    folder: String
        folder containing the text strings for each book
    notitles: bool
        Whether to use text strings without chapter titles (default:False)
    
    Returns
    -------
    CV: Vectorizer
        The vectorizer object used to create
    X: ndarray
        BoWs array
    """
    text_list = read_txts(folder, notitles)
    CV, BoWs = BoW(text_list, vectorizerType, min_df)
    X = BoWs.toarray()
    return CV, X, text_list


def dend(X, notitles=False, metric="euclidean"):
    """Takes BoWs array creates linkage and dendrogram.

    Args
    ----
    X: ndarray
        BoWs array
    metric: String
        Distance metric to use (default: "euclidean")

    Returns
    -------
    Z: ndarray
        Linkage array
    dend: dict
        dendrogram as a leaf and branch tree.
    """

    Z = linkage(X, metric=metric)

    plt.clf()
    den = dendrogram(Z, labels=abbrev, orientation="left")
    plt.title("Dendrogram of Antiquity Texts")
    plt.xlabel("Distance between items")
    plt.tight_layout()
    if notitles:
        name = "Dendrogram_notitles_{}.pdf".format(metric)
    else:
        name = "Dendrogram_{}.pdf".format(metric)
    plt.savefig(name)

    return Z, den


def k_clustering(X, n_clusters=8):
    """Clusters the given data and outputs a latex table of the clusters

    Returns
    -------
    cluster_names: list of list
        Each item represents a cluster. Each item then has the titles
        of the containing books.
    table_text: String
        A string to create a latex table without captions"""
    
    # Create a kmeans object
    kmeans_obj = KMeans(n_clusters=n_clusters)

    kmeans_obj.fit(X)

    labels = kmeans_obj.labels_

    # Make each title no spaces
    new_names = []

    for name in titles:
        new_name = name.title().replace(" ", "")
        new_names.append(new_name)

    cluster_names = []
    table_string = ""

    # Take labels and created a linked word cloud?
    for i in range(n_clusters):
        group = labels == i
        (indices), = np.nonzero(group)
        indiv = []
        new_string = ""

        for j in indices:
            indiv.append(titles[j])
        for k in indiv:
            new_string += k + ' \\\ '
        new_string += '\hline '

        table_string += new_string
        cluster_names.append(indiv)

    # This does give the right output but repr screws it up
    start_table = '\\begin{table} \centering \\begin{tabular}{l} \hline'

    end_table = '\end{tabular} \end{table}'

    table_text = start_table + " " + table_string + " " + end_table
    return cluster_names, table_text


def multidim(X, vectorizerType="tf", notitles=False, metric="euclidean"):
    """Multidimensional scaling on a books x word count array

    Args
    ----
    X: ndarray
        The array of term frequencies or TF-IDF

    Returns
    out: ndarray

    """
    multi = MDS()

    # Provides the points to plot each of the books
    out = multi.fit_transform(X)

    min_x, min_y = np.min(out, axis=0)
    max_x, max_y = np.max(out, axis=0)

    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ylim((min_y-0.5, max_y+0.5))
    plt.xlim((min_x-0.5, max_x+0.5))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Multi-Dimensional Scaling of Antiquity Texts')

    for i, book in enumerate(abb):
        ax.annotate(book, xy=out[i])
    
    plt.tight_layout()

    if notitles:
        name = "MDS_{}_notitles_{}.pdf".format(vectorizerType, metric)
    else:
        name = "MDS_{}_{}.pdf".format(vectorizerType, metric)
    plt.savefig(name)
    return out


def most_weighted(X, CV, n=10, save=False):
    """Finds the most weighted words within an array.

    Args
    ----
    X: ndarray
        Term-document array with books on each row and words
        for each column
    CV: vectorizer object
        Provides the vocabulary. 
        Can either be a CountVectoriser or TfidfVectoriser.
    n: int
        The top n weighted words
    save: bool
        Whether to save out 

    Returns
    -------
    out: ndarray
        Array of Strings
    """

    # You have a 2d array: rows are books, cols are words
    # You have a vocab dict with 'word': array_index
    vocab = CV.vocabulary_

    # Create zeros array of size vocab
    vocab_array = np.chararray((len(vocab),), itemsize=18)
    # Convert dict to an actual 1D array, where you have the right word at the right index
    for k, v in vocab.items():
        vocab_array[v] = k

    # Get the sorted indices
    ind = X.argsort(axis=1)

    out = np.chararray((ind.shape[0], n), itemsize=18)

    # For each row in ind
    for i in range(ind.shape[0]):
        # Grab the row from ind (this is the ordering you need to make it sorted)
        ind_row = ind[i, :]
        
        # Index your 1D words at indexes array with the row from ind - which puts it in order
        # (basically, sorts according to the counts from X)
        sorted = vocab_array[ind_row]

        # Grab the last N values using [-n:]
        out[i, :] = sorted[-n:]

    top = pd.DataFrame(out, index=abbrev, columns=np.arange(10, 0, -1))

    if save:
        top.to_csv("top_{}_words.csv".format(n))



    return top


def analysis(folder, notitles=False, vectorizerType="count", min_df=3,
             metric="euclidean", n_clusters=8, n=10, save=False):
    CV, X, text_list = folder_to_array(folder, notitles, vectorizerType, min_df)
    Z, den = dend(X, notitles, metric)
    cluster_names, table_text = k_clustering(X, n_clusters)
    top_ten_words = most_weighted(X, CV, n, save)

    return CV, X, Z, cluster_names, table_text, top_ten_words
