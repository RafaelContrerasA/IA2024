from sklearn.datasets import load_iris
from sklearn import tree
import graphviz

iris = load_iris()

X, y = iris.data, iris.target
print(X,y)

clf = tree.DecisionTreeClassifier()

