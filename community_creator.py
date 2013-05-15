# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:35:32 2013

@author: aitor
"""

import networkx as nx

class CommunityCreator:
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.G = nx.Graph()
    
    def import_edgelist(self, filepath):
        if self.verbose:
            print 'Importing ' + filepath
        self.G = nx.read_edgelist(filepath)
        if self.verbose:
            print 'Number of nodes: %s' % (len(self.G.nodes()))
            print 'Number of edges: %s' % (len(self.G.edges()))
        
    
    
        