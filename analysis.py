import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
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

def hier(CV, BoWs, metric= "ward"):

    # Take the BoWs and make into an ndarray
    X = BoWs.toarray()

    # Create linkage matrix
    Z = linkage(X, metric)
    return Z

def run_to_hier(folder, output_folder, titles_remove, metric):
    save_all_books(folder, output_folder, titles_remove)
    text_list = read_txts(folder, titles_remove)
    CV, BoWs = BoW(text_list)
    Z = hier(CV, BoWs, metric= "ward")

    return CV, BoWs, Z


