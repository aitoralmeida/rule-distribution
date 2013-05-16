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
        self.cliques = []
        self.clique_groups = []
        self.k_cliques = []
        self.k_clique_groups = []
        self.k_cores = []
    
    def import_edgelist(self, filepath):
        if self.verbose:
            print 'Importing ' + filepath
        self.G = nx.read_edgelist(filepath)
        if self.verbose:
            print 'Number of nodes: %s' % (len(self.G.nodes()))
            print 'Number of edges: %s' % (len(self.G.edges()))
    
    def find_cliques(self):
        for clique in list(nx.find_cliques(self.G)) :
            self.cliques.append(set(clique))
        self.clique_groups = self.find_common_subsets(self.cliques)
        if self.verbose:
            print 'CLIQUES' 
            print 'Found %s cliques' %(len(self.cliques))
            print 'Found %s clique groups' %(len(self.clique_groups))
        return len(self.cliques)  
        
    def find_k_cliques(self, k = 3):
        for kc in nx.k_clique_communities(self.G, k):
            self.k_cliques.append(set(kc))
        self.k_clique_groups = self.find_common_subsets(self.k_cliques)
        if self.verbose:
            print 'K-CLIQUES' 
            print 'Found %s k-cliques' %(len(self.k_cliques))
            print 'Found %s k-clique groups' %(len(self.k_clique_groups))
            
        return len(self.k_clique_groups)
        
    def find_k_cores(self, max_k):       
        current_graph = self.G
        if self.verbose:
            print 'K-CORES' 
        for i in range(max_k,0,-1):
            core_k = nx.k_core(current_graph, i)
            if len(core_k) > 0:
                self.k_cores.append(core_k.nodes())
                current_graph = nx.k_crust(current_graph, i)  
        if self.verbose:
            print 'Found %s k-cores' %(len(self.k_cores))
        return len(self.k_cores)
  
    def populate_index(self, group):
        index = {
            # element : [ pos1, pos2 ]
        }
        for pos, subset in enumerate(group):
            for elem in subset:
                index[elem] = index.get(elem, []) + [pos]
        return index
    
    def find_common_subsets(self, group):
        index = self.populate_index(group)
    
        taken = set()
    
        aggregations = []
    
        for pos_subset, subset in enumerate(group):
            if pos_subset not in taken:
                aggregations.append( self.find_related(index, group, subset, pos_subset, taken) )
    
        final_groups = []
    
        for aggregation in aggregations:
            current = set()
            for pos in aggregation:
                current = current.union(group[pos])
            final_groups.append(current)
    
        return final_groups
    
        
    
    def find_related(self, index, group, subset, current_pos, taken):
        taken.add(current_pos)
        aggregation = [current_pos]
    
        for elem in subset:
            for pos in index[elem]:
                if pos not in taken:
                    aggregation += self.find_related(index, group, group[pos], pos, taken)
    
        return aggregation
            
        
#    def group_cliques(self):
#        print self.cliques[0]
#        cliques = self.cliques[:]
#        
#        cliques = [ ['A', 'B'], [ '1', '2', '3' ], [ 'B', 'D'], [ 'X', 'Y'], ['D', '4'] ]
#        cliques = [ set(clique) for clique in cliques ]
#
#        
#        current_cliques  = cliques
#        previous_cliques = []
#        
#        while current_cliques != previous_cliques:
#            taken = []
#            aggregations = []
#
#            for pos1, clique1 in enumerate(current_cliques):
#                
#                current = clique1            
#                
#                if pos1 in taken:
#                    continue
#                
#                for pos2, clique2 in enumerate(current_cliques[pos1 + 1:]):
#                    if pos1 + 1 + pos2 in taken:
#                        continue
#                    
#                    if current.intersection(clique2):
#                        taken.append(pos1 + 1 + pos2)
#                        current = current.union(clique2)
#                aggregations.append(current)
#                
#            previous_cliques = current_cliques
#            current_cliques  = aggregations[:]
#            
#            
#        print current_cliques         
#        
#             
#        return len(self.clique_groups)
                        
        
    
    
    
        