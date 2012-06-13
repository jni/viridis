# built-ins
import itertools as it
import argparse
import random
import sys
import logging
import json

# libraries
import numpy as np
import networkx as nx
from scipy.misc import comb as nchoosek

# local modules

class Ultrametric(nx.DiGraph):
    """An ultrametric tree data structure"""
    def __init__(self, init_nodes=[]):
        super(Ultrametric, self).__init__()
        self.maxw = -np.inf
        self.add_nodes_from(init_nodes, w=self.maxw, num_leaves=1)
        self.id_counter = it.count(max([0] + init_nodes) + 1)

    def merge(self, n1, n2, w=0.0):
        node_id = self.id_counter.next()
        self.maxw = max(w, self.maxw)
        num_leaves = self.num_leaves(n1) + self.num_leaves(n2)
        self.add_node(node_id, w=self.maxw, num_leaves=num_leaves)
        self.add_edges_from([(node_id, n1), (node_id, n2)])
        return node_id

    def get_map(self, t=0.5):
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

def num_leaves(g, n):
    return g.node[n]['num_leaves']
