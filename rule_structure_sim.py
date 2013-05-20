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
    
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.rules = {}
        self.stage_nodes = {}
        self.nodes = {}
        self.node_graph = Graph()
        self.rule_directed_graph = Graph()
        self.rule_undirected_graph = Graph()
    
    def create_simulation (self, stages = [3, 2, 1], prob_prev = 1, prob_same = 1, prune = True):
        if self.verbose:
            print '\n\n**********************************'
            print '******* Creating simulation ******'
            print '**********************************\n'
            
        self._create_concepts(stages)
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
        if prune:
            while len(self._prune_non_consecuential()) > 0:
                pass
        
        self._create_rules()
        
        self._create_node_graph()
        self._create_rule_graphs()        
    
    def _create_concepts(self, stages):
        if self.verbose:
            print 'Creating concepts for ' + str(len(stages)) + ' stages'
            
        i = 0;    
        for stage in stages:
            stage_nodes = []
            for e in range(0, stage):
                n = Node(i)
                stage_nodes.append(n)
                self.nodes[n.id] = n
            self.stage_nodes[i] = stage_nodes
            i += 1 
            
    def _create_rules(self):
        if self.verbose:
            print 'Creating rules'
            
        # stage 0 nodes are not the output of any node
        for stage in range(1, len(self.stage_nodes)):
            node_ids = [n.id for n in self.stage_nodes[stage]]
            for node_id in node_ids:
                node = self.nodes[node_id]
                if len(node.sources) > 0:
                    rule_id = 'rule' + str(stage) + str(0011) + str(time.time()) + str(random.random())
                    rule_id = rule_id.replace('.', '')
                    self.rules[rule_id] = Rule(rule_id, [n.id for n in node.sources], node_id)
            
    def _prune_non_consecuential(self):
        if self.verbose:
            print 'Pruning rule tree'
            
        num_stages = len(self.stage_nodes.keys())
        nodes_to_disintegrate = []
        for key in range(num_stages-2, -1, -1): #last stage can't be non-consecuential
            for node in self.stage_nodes[key]:
                # Node has no targets, disintegrate
                if len(self.nodes[node.id].targets) == 0:
                    nodes_to_disintegrate.append(node.id)
                # do the targets lead to the next stage?
                else:
                    if not self._check_next_stage(node.id): 
                        #check if one of the same stage targets go to the next
                        #stage
                        leads_to_next_stage = False
                        for t in node.targets:
                            if self._check_next_stage(t.id):
                                leads_to_next_stage = True
                        if not leads_to_next_stage:
                            nodes_to_disintegrate.append(node.id)
        
        #nodes in last stage must have some antecedent
        for node in self.stage_nodes[num_stages-1]:
            if len(node.sources) <= 0:
                nodes_to_disintegrate.append(node.id)
        
        for node_id in nodes_to_disintegrate:
            self._disintegrate_node(node_id)
        
        if self.verbose:
                print 'Disintegrated nodes: '
                print '**************************'
                print nodes_to_disintegrate
                print '**************************'
        return nodes_to_disintegrate
                        
                            
    
    #checks if the node leads to the next stage    
    def _check_next_stage(self, node_id):
        targets = self.nodes[node_id].targets
        to_next_stage = False
        for t in targets:
            if self.nodes[t.id].stage > self.nodes[node_id].stage:
                to_next_stage = True
                break            
        return to_next_stage         
    
    #delete a node and all its references                
    def _disintegrate_node(self, node_id):
        self.nodes.pop(node_id)
        for node in self.nodes.values():
            for target in node.targets:
                if node_id == target.id:
                    self.nodes[node.id].targets.remove(target)
            for source in node.sources:
                if node_id == source.id:
                    self.nodes[node.id].sources.remove(source)               
        
        for stage in self.stage_nodes:
            for n in self.stage_nodes[stage]:
                if node_id == n.id:                 
                    self.stage_nodes[stage].remove(n)                   
    
    # creates the proteus-graph Graph()        
    def _create_node_graph(self):
        if self.verbose:
            print 'Creating node graph. Total nodes: ' + str(len(self.nodes))
            
        self.node_graph = Graph(directed = True)
        for key in self.nodes:
            n = self.nodes[key]
            self.node_graph.add_node(id = n.id, label = 'stage' + str(n.stage))
        
        for key in self.nodes:
            n = self.nodes[key]
            for target in n.targets:
                self.node_graph.add_edge(n.id, target.id)
                
    def _create_rule_graphs(self):
        if self.verbose:
            print 'Creating rule Graphs. Total rules: ' + str(len(self.rules))
            
        for rule in self.rules.values():
            self.rule_directed_graph.add_node(id = rule.id)
            self.rule_undirected_graph.add_node(id = rule.id)
            
        for rule1 in self.rules.values():
            for rule2 in self.rules.values():
                if rule1.id != rule2.id:
                    #undirected
                    for rule1_input in rule1.inputs:
                        if rule1_input in rule2.inputs:
                            self.rule_undirected_graph.add_edge(rule1.id, rule2.id)
                    
                    if rule1.output == rule2.output:
                        self.rule_undirected_graph.add_edge(rule1.id, rule2.id)
                        
                    #directed
                    if rule1.output in rule2.inputs:
                        self.rule_directed_graph.add_edge(rule1.id, rule2.id)

    
    def export_gml(self, filename):
        if self.verbose:
            print 'Exporting to GML: ' + filename
            
        self.node_graph.export_graph_gml(filename + '_node_directed.gml')
        self.rule_directed_graph.export_graph_gml(filename + '_rule_directed.gml')
        self.rule_undirected_graph.export_graph_gml(filename + '_rule_undirected.gml')
        
    def export_edgelist(self, filename):
        if self.verbose:
            print 'Exporting to ncol: ' + filename           
        self.rule_directed_graph.export_graph_edgelist_ncol(filename + '_rule_directed.csv')
    

class Rule:   
    def __init__ (self, rule_id, inputs, output):
        self.id = rule_id
        self.inputs = inputs
        self.output = output
        
class Node:    
    def __init__(self, stage = -1):
        self.targets = []
        self.sources = []
        self.stage = stage
        self.id = 'stage' + str(stage) + str(0011) + str(time.time()) + str(random.random())
        self.id = self.id.replace('.', '')
        
if __name__ == "__main__":
    sim = RuleStructureSim(True)
    sim.create_simulation([500, 300, 100, 10], 0.05, 0.001, True)    
    sim.export_gml('./result')
    sim.export_edgelist('./test')
        
        
