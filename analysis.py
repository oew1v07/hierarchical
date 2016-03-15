import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from misc import *
from cleaning import *
# This function should be unnecessary since
# Only uses words where it is mentioned in corpus at least 3 times

def BoW(texts):
    """Takes a list of texts and creates a matrix BoWs"""

    CV = CountVectorizer(min_df = 3)
    BoWs = CV.fit_transform(texts)

    return CV, BoWs


def vocab_size(texts, min_count=[1,2,3,4,5], visualise=False, save=False):

    sizes = []
    for i in min_count:
        CV = CountVectorizer(min_df = i)
        BoWs = CV.fit_transform(texts)
        sizes.append(BoWs.shape[1])

    if visualise:
        plt.plot(min_count, sizes, 'bo-')
        if save:
            plt.savefig("Count_vs_vocabSize.png")

    return sizes


def hier(CV, BoWs, method = "ward", metric= "euclidean"):

    # Take the BoWs and make into an ndarray
    X = BoWs.toarray()

    # Create linkage matrix
    Z = linkage(X, metric=metric)
    return X, Z


def analysis(folder, notitles=False, metric="euclidean", method="ward"):
    text_list = read_txts(folder, notitles)
    CV, BoWs = BoW(text_list)
    X, Z = hier(CV, BoWs, method, metric)

    dend = dendrogram(Z, labels=abbrev, orientation="left")
    plt.title("Dendrogram of Antiquity Texts")
    plt.xlabel("Distance between items")
    plt.tight_layout()
    if notitles:
        name = "Dendrogram_notitles_{}.pdf".format(metric)
    else:
        name = "Dendrogram_{}.pdf".format(metric)
    plt.savefig(name)

    return CV, BoWs, Z, dend

def k_clustering(folder,notitles=False, n_clusters=8, metric="euclidean"):
    """Clusters the given data and outputs a latex table of the clusters

    Returns
    -------
    cluster_names: list of list
        Each item represents a cluster. Each item then has the titles
        of the containing books.
    table_text: String
        A string to create a latex table without captions"""
    text_list = read_txts(folder, notitles)
    CV, BoWs = BoW(text_list)
    X, Z = hier(CV, BoWs, metric = metric)
    
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

# no titles euclidean 8 clusters [4, 5, 7, 5, 7, 3, 1, 7, 4, 7, 1, 5, 5, 6, 1, 1, 7, 0, 4, 1, 5, 6, 7, 2]
