# -*- coding: utf-8 -*-
"""
Created on Fri May 03 09:47:24 2013

@author: aitor
"""

import time
import random
#https://github.com/aitoralmeida/proteus-graph-exporter
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
                prev_nodes = []
                i = key - 1
                while i >= 0:
                    for n in self.stage_nodes[i]:
                        prev_nodes.append(n)
                    i = i -1
                
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
        #self.prune_non_consecuential()
        self.create_graph()        
    
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
            
    def prune_non_consecuential(self):
        num_stages = len(self.stage_nodes.keys())
        for key in range(num_stages-2, -1, -1): #last stage can't be non-consecuential
            for node in self.stage_nodes[key]:
                # Node has no targets, disintegrate
                if len(self.nodes[node.id].targets) == 0:
                    self.disintegrate_node(node.id)
                    print 'Disintegrating ' + str(node.id)
                # do the targets lead to the next stage?
                else:
                    if not self.check_next_stage(node.id): 
                        #check if one of the same stage targets go to the next
                        #stage
                        leads_to_next_stage = False
                        for t in node.targets:
                            if self.check_next_stage(t.id):
                                leads_to_next_stage = True
                                break
                        if not leads_to_next_stage:
                            self.disintegrate_node(node.id)
                        
                            
    
    #checks if the node leads to the next stage    
    def check_next_stage(self, id):
        targets = self.nodes[id].targets
        to_next_stage = False
        for t in targets:
            if self.nodes[t.id].stage > self.nodes[id].stage:
                to_next_stage = True
                break
        return to_next_stage
                        
                    
                    
    def disintegrate_node(self, id):
        self.nodes.pop(id)
        for node in self.nodes.values():
            if id in node.targets:
                self.nodes[node.id].targets.remove(id)
            if id in node.sources:
                self.nodes[node.id].sources.remove(id)
        
        for stage in self.stage_nodes:
            for n in self.stage_nodes[stage]:
                if id == n.id:                 
                    self.stage_nodes[stage].remove(n)                   
    
    # creates the proteus-graph Graph()        
    def create_graph(self):
        self.graph = Graph(directed = True)
        for key in self.nodes:
            n = self.nodes[key]
            self.graph.add_node(id = n.id, label = 'stage' + str(n.stage))
        
        for key in self.nodes:
            n = self.nodes[key]
            for target in n.targets:
                self.graph.add_edge(n.id, target.id)
                
    def export_gml(self, filepath):
        self.graph.export_graph_gml(filepath)
    

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
        
        
