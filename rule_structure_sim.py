# -*- coding: utf-8 -*-
"""
Created on Fri May 03 09:47:24 2013

@author: aitor
"""

import time
import random
from proteus_graph import Graph

class RuleStructureSim: 
    
    def __init__(self):
        self.rules = {}
        self.stage_nodes = {}
        self.nodes = {}
        self.graph = Graph()
    
    def create_simulation (self, stages = [3, 2, 1], prob_prev = 1, prob_same = 1):
        self.create_concepts(stages)
        for key in self.stage_nodes.keys():
            if key != 0:
                stage_nodes = self.stage_nodes[key]
                prev_nodes = self.stage_nodes[key-1] #TODO add not only stage -1 but also range(key-1,0,-1)
                for node in stage_nodes:
                    for prev_node in prev_nodes:
                        if random.random() < prob_prev:
                            self.nodes[node.id].sources.append(prev_node)
                            self.nodes[prev_node.id].targets.append(node)
                    for node2 in stage_nodes:
                        if node.id != node2.id:
                            if random.random() < prob_same:
                                self.nodes[node.id].sources.append(node2)                           
                                self.nodes[node2.id].targets.append(node)                   
                
    
    def create_concepts(self, stages):
        i = 0;    
        for stage in stages:
            stage_nodes = []
            for e in range(0, stage):
                n = Node(i)
                stage_nodes.append(n)
                self.nodes[n.id] = n
            self.stage_nodes[i] = stage_nodes
            i += 1 
    
    def create_graph(self):
        self.graph = Graph(directed = True)
        for key in self.nodes:
            n = self.nodes[key]
            self.graph.add_node(n.id)
        
        for key in self.nodes:
            n = self.nodes[key]
            for target in n.targets:
                self.graph.add_edge(n.id, target.id)

    

class Rule:   
    def __init__ (self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        
class Node:    
    def __init__(self, stage = -1):
        self.targets = []
        self.sources = []
        self.stage = stage
        self.id = 'stage-' + str(stage) + '-' + str(time.time()) + str(random.random())
