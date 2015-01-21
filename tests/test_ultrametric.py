from viridis import tree
from six.moves import range

def test_split():
    t = tree.Ultrametric(list(range(6)))
    t.merge(0, 1, 0.1)
    t.merge(6, 2, 0.2)
    t.merge(3, 4, 0.3)
    t.merge(8, 5, 0.4)
    t.merge(7, 8, 0.5)
    t.split(0, 2)
    assert t.node[9]['num_leaves'] == 3
    t.split(0, 4) # nothing to do
    assert t.node[9]['num_leaves'] == 3
