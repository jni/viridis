from viridis import tree

import pytest

@pytest.fixture
def base_tree():
    t = tree.Ultrametric(list(range(6)))
    t.merge(0, 1, 0.1)  # 6
    t.merge(6, 2, 0.2)  # 7
    t.merge(3, 4, 0.3)  # 8
    t.merge(8, 5, 0.4)  # 9
    t.merge(7, 9, 0.5)  # 10
    return t


def test_split(base_tree):
    t = base_tree
    t.split(0, 2)
    assert t.nodes[10]['num_leaves'] == 3
    t.split(0, 4) # nothing to do
    assert tree.num_leaves(t, 10) == 3


def test_children(base_tree):
    t = base_tree
    assert list(t.children(6)) == [0, 1]


def test_leaves(base_tree):
    t = base_tree
    assert set(t.leaves(10)) == set(range(6))
    assert set(t.leaves(6)) == set([0, 1])
    assert set(t.leaves(9)) == set(range(3, 6))


def test_highest(base_tree):
    t = base_tree
    for i in range(t.number_of_nodes()):
        assert t.highest_ancestor(i) == 10
    t.remove_node(10)
    t.remove_node(9)
    assert t.highest_ancestor(4) == 8
