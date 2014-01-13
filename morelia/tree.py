# built-ins
import itertools as it

# libraries
import numpy as np
import networkx as nx

# local modules

def lowest_common_ancestor(t, u, v):
    au = t.ancestors(u)
    av = t.ancestors(v)
    common = set(au) & set(av)
    short = au if len(au) < len(av) else av
    for s in short:
        if s in common:
            return s
    return None

lca = lowest_common_ancestor

class Ultrametric(nx.DiGraph):
    """An ultrametric tree data structure"""
    def __init__(self, init_nodes=[]):
        super(Ultrametric, self).__init__()
        self.maxw = -np.inf
        self.add_nodes_from(init_nodes, w=self.maxw, num_leaves=1)
        self.id_counter = it.count(max([0] + init_nodes) + 1)

    def merge(self, u, v, w=0.0):
        node_id = self.id_counter.next()
        self.maxw = max(w, self.maxw)
        num_leaves = self.num_leaves(u) + self.num_leaves(v)
        self.add_node(node_id, w=self.maxw, num_leaves=num_leaves)
        self.add_edges_from([(node_id, u), (node_id, v)])
        return node_id

    def split(self, u, v):
        split_node = lowest_common_ancestor(self, u, v)
        if split_node is None:
            return
        a = self.ancestors(split_node)
        num_leaves = self.node[split_node]['num_leaves']
        self.remove_node(split_node)
        for n in a:
            self.node[n]['num_leaves'] -= num_leaves

    def get_map(self, t=np.inf):
        """Compute a map from leaf nodes to roots at a certain height."""
        nodes = filter(lambda n: self.node[n]['w'] < t, self.nodes())
        g = self.subgraph(nodes)
        ccs = nx.algorithms.connected_components(g.to_undirected())
        ccs = [self.subgraph(ns) for ns in ccs]
        leavess = [filter(h.is_leaf, h.nodes()) for h in ccs]
        roots = [filter(h.is_root, h.nodes()) for h in ccs]
        max_leaf = max(map(max, leavess))
        forward_map = np.zeros(max_leaf + 1, int)
        for root, leaves in zip(roots, leavess):
            forward_map[leaves] = root
        return forward_map
    
    def is_leaf(self, node):
        return self.out_degree(node) == 0

    def is_root(self, node):
        return self.in_degree(node) == 0

    def num_leaves(self, n):
        return self.node[n]['num_leaves']

    def parent(self, n):
        p = self.predecessors(n)
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

    def children(self, n):
        return self.successors(n)

def num_leaves(g, n):
    return g.node[n]['num_leaves']
