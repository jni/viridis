from __future__ import absolute_import
# built-ins
import itertools as it

# libraries
import numpy as np
import networkx as nx

# local modules

def lowest_common_ancestor(t, u, v):
    """Find the lowest common ancestor of two nodes

    Parameters
    ----------
    t : an `Ultrametric` tree or `nx.DiGraph`
        The tree or directed acyclic graph on which to find ancestors.
    u, v : int
        The node IDs in `t` for which to find the common ancestor

    Returns
    -------
    c : int or None
        The lowest common ancestor of `u` and `v` in `t`. ``None`` if
        they do not have any common ancestors.

    Examples
    --------
    >>> t = Ultrametric([0, 1, 2])
    >>> t.merge(0, 1)
    3
    >>> t.merge(2, 3)
    4
    >>> t.ancestors(0)
    [3, 4]
    >>> t.ancestors(1)
    [3, 4]
    >>> t.ancestors(2)
    [4]
    >>> lowest_common_ancestor(t, 0, 1)
    3
    >>> t.split(0, 2)
    >>> lowest_common_ancestor(t, 1, 2) is None
    True
    """
    au = t.ancestors(u)
    av = t.ancestors(v)
    common = set(au) & set(av)
    short = au if len(au) < len(av) else av
    for c in short:
        if c in common:
            return c
    return None

lca = lowest_common_ancestor

class Ultrametric(nx.DiGraph):
    """An ultrametric tree data structure"""
    def __init__(self, init_nodes=()):
        super(Ultrametric, self).__init__()
        self.maxw = -np.inf
        self.add_nodes_from(init_nodes, w=self.maxw, num_leaves=1)
        self.id_counter = it.count(np.max([0] + list(init_nodes)) + 1)

    def merge(self, u, v, w=0.0):
        """Merge two nodes u, v and return the ID of the new node.

        Parameters
        ----------
        u, v : int
            The nodes being merged.
        w : float
            The weight of the merge.

        Returns
        -------
        node_id : int
            The generated ID of the node resulting from the (u, v)
            merge.

        Notes
        -----
        To preserve the ultrametric condition, the true weight of the
        merge is the maximum of w, weight(u), and weight(v).
        """
        node_id = next(self.id_counter)
        self.maxw = max(w, self.maxw)
        subtree_maxw = max(w, self.nodes[u]['w'], self.nodes[v]['w'])
        num_leaves = self.num_leaves(u) + self.num_leaves(v)
        self.add_node(node_id, w=subtree_maxw, num_leaves=num_leaves)
        self.add_edges_from([(node_id, u), (node_id, v)])
        return node_id

    def split(self, u, v):
        split_node = lowest_common_ancestor(self, u, v)
        if split_node is None:
            return
        a = self.ancestors(split_node)
        num_leaves = self.nodes[split_node]['num_leaves']
        self.remove_node(split_node)
        for n in a:
            self.nodes[n]['num_leaves'] -= num_leaves

    def get_map(self, t=np.inf, source=None):
        """Compute a map from leaf nodes to roots at a certain height.

        Parameters
        ----------
        t : float, optional
            The threshold at which to cut the tree.
        source : int, optional
            Compute the map only for the tree rooted at `source`.

        Examples
        --------
        >>> t = Ultrametric(np.arange(6)) # tree with 6 leaves
        >>> t.merge(0, 1, 0.1) # merge nodes 1 and 2
        6
        >>> t.merge(2, 6, 0.2)
        7
        >>> t.merge(3, 7, 0.3)
        8
        >>> t.merge(4, 5, 0.1)
        9
        >>> t.merge(7, 8, 0.2)
        10
        >>> t.get_map(0.25)
        array([7, 7, 7, 3, 9, 9])
        >>> t.get_map(source=7)
        array([7, 7, 7])
        >>> t.get_map(source=9)
        array([0, 0, 0, 0, 9, 9])
        >>> t.get_map(0.15, 7)
        array([6, 6, 2])
        """
        if source is not None:
            des = nx.descendants(self, source)
            des.add(source)
            g = self.subgraph(des)
        else:
            g = self
        nodes = [n for n in g.nodes() if self.nodes[n]['w'] <= t]
        g = self.subgraph(nodes)
        ccs = nx.algorithms.connected_components(g.to_undirected())
        ccs = [self.subgraph(ns) for ns in ccs]
        leavess = [list(filter(h.is_leaf, h.nodes())) for h in ccs]
        roots = [list(filter(h.is_root, h.nodes())) for h in ccs]
        max_leaf = max(list(map(max, leavess)))
        forward_map = np.zeros(max_leaf + 1, int)
        for root, leaves in zip(roots, leavess):
            forward_map[leaves] = root
        return forward_map

    def leaves(self, node):
        """Get all the leaves rooted at `node`.

        Parameters
        ----------
        node : int
            The ancestor of all leaves we want.

        Returns
        -------
        leaves : iter of int
            The leaves of `node`.
        """
        return filter(self.is_leaf, nx.descendants(self, node))

    def is_leaf(self, node):
        return self.out_degree(node) == 0

    def is_root(self, node):
        return self.in_degree(node) == 0

    def num_leaves(self, n):
        return self.nodes[n]['num_leaves']

    def parent(self, n):
        p = list(self.predecessors(n))
        if len(p) == 1:
            return p[0]
        return None

    def ancestors(self, n):
        a = []
        node = n
        while self.parent(node) is not None:
            node = self.parent(node)
            a.append(node)
        return a

    def highest_ancestor(self, n):
        """Return the earliest ancestor of node `n`.

        In a complete tree, this returns the root.

        Parameters
        ----------
        n : int
            The query node.

        Returns
        -------
        a : int
            The highest possible ancestor of `n`.

        Notes
        -----
        This is equivalent to `self.ancestors(n)[-1]`, but slightly
        more efficient, because it avoids the creation of intermediate
        lists.
        """
        while self.parent(n) is not None:
            n = self.parent(n)
        return n

    def children(self, n):
        return self.successors(n)

def num_leaves(g, n):
    return g.nodes[n]['num_leaves']


if __name__ == '__main__':   # pragma: no cover
    import doctest
    doctest.testmod()
