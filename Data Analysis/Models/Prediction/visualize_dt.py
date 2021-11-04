from pydotplus import graph_from_dot_data
from IPython.display import Image

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import export_graphviz
import numpy as np

def show_tree(tree, filename):
    dot_data = export_graphviz(
        tree,
        out_file=None, filled=True, rounded=True,
        special_characters=True,
        proportion=False, impurity=False, # enable them if you want
    )
    graph = graph_from_dot_data(dot_data)
    Image(graph.write_png(filename))