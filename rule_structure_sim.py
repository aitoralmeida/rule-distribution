# -*- coding: utf-8 -*-
"""
Created on Fri May 03 09:47:24 2013

@author: aitor
"""

import time
import random

class RuleStructureSim: 

    rules = {}
    stages = {}
    nodes = {}
    
    def create_simulation (self, stages = [5, 3, 2], prob_prev = 0.4, prob_same = 0.2, max_outcomes = 2):
        self.create_concepts(stages)
        for key in self.nodes.keys:
            if key != 0:
                stage_nodes = stages[key]
                prev_nodes = stages[key-1]
                for node in stage_nodes:
                    for prev_node in prev_nodes:
                        if random.random() < prob_prev:
                            self.nodes[node.id].sources = prev_node
                            self.nodes[prev_node.id].targets = node
                    for node2 in stage_nodes:
                        if node.id != node2.id:
                            if random.random() < prob_same:
                               self.nodes[node.id].sources = node2                            
                               self.nodes[node2.id].targets = node
                    
                
    
    def create_concepts(self, stages):
        i = 0;    
        for stage in stages:
            stage_nodes = []
            for e in range(0, stage):
                n = Node()
                stage_nodes.append(n)
                self.nodes[n.id] = n
            self.stages[i] = stage_nodes
            i += 1 
    
    

class Rule:
    inputs = []
    outputs = []
    
    def __init__ (self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        
class Node:
    targets = []
    sources = []
    
    def __init__(self):
        self.id = str(time.time()) + str(random.random())
