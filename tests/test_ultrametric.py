from viridis import tree
from six.moves import range

import pytest

@pytest.fixture
def base_tree():
    t = tree.Ultrametric(list(range(6)))
    t.merge(0, 1, 0.1)
    t.merge(6, 2, 0.2)
    t.merge(3, 4, 0.3)
    t.merge(8, 5, 0.4)
    t.merge(7, 9, 0.5)
    return t


def test_split(base_tree):
    t = base_tree
    t.split(0, 2)
    assert t.node[10]['num_leaves'] == 3
    t.split(0, 4) # nothing to do
    assert tree.num_leaves(t, 10) == 3


def test_children(base_tree):
    t = base_tree
    assert t.children(6) == [0, 1]
