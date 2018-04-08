from sklearn import tree

dt = tree.DecisionTreeClassifier(criterion='entropy')

# [e1,e2,e3,e4,e5,e6,e7,e8,r9]
X = [['attr_1:2', 'attr_1:2', 'attr_1:2', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'target'],
     ['attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:5', 'attr_2:5', 'attr_2:5', 'target'],
     ['attr_2:1', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:5', 'attr_2:5', 'attr_2:5', 'target'],
     ['attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:4', 'target'],
     ['attr_1:1', 'attr_1:2', 'attr_1:2', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'target']]

Y = ['man', 'woman', 'woman', 'man', 'woman']

clf = dt.fit(X, Y)
prediction = clf.predict([['attr_1:2', 'attr_1:2', 'attr_1:2', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'target']])
print(prediction)

dotfile = open("dt.dot", 'w')
tree.export_graphviz(dt, out_file=dotfile, feature_names=[e1,e2,e3,e4,e5,e6,e7,e8,r9])
dotfile.close()

from sklearn.tree import _tree
def tree_to_code(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print
    "def tree({}):".format(", ".join(feature_names))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print
            "{}if {} <= {}:".format(indent, name, threshold)
            recurse(tree_.children_left[node], depth + 1)
            print
            "{}else:  # if {} > {}".format(indent, name, threshold)
            recurse(tree_.children_right[node], depth + 1)
        else:
            print
            "{}return {}".format(indent, tree_.value[node])

    recurse(0, 1)

tree_to_code(dt,[e1,e2,e3,e4,e5,e6,e7,e8,r9])