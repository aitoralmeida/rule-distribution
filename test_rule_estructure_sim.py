# -*- coding: utf-8 -*-
"""
Created on Fri May 03 10:48:35 2013

@author: aitor
"""

import unittest
from rule_structure_sim import RuleStructureSim
from proteus_graph import Graph

class TestRuleEstructureSim(unittest.TestCase):
    
    def test_create_concepts(self):
        sim = RuleStructureSim()
        sim.create_concepts([5,3,2])
        
        self.assertEquals(len(sim.nodes), 5+3+2)        
        
        self.assertEquals(len(sim.stage_nodes), 3)
        self.assertEquals(len(sim.stage_nodes[0]), 5)
        self.assertEquals(len(sim.stage_nodes[1]), 3)
        self.assertEquals(len(sim.stage_nodes[2]), 2)
    
    # inter-stage prob 1, intra-stage prob 0
    def test_create_simulation_prob_1_0(self):
        sim = RuleStructureSim()
        sim.create_simulation([2,2,2], 1, 0)
        
        # concepts created correctly?
        self.assertEquals(len(sim.nodes), 2+2+2)        
        self.assertEquals(len(sim.stage_nodes), 3)
        self.assertEquals(len(sim.stage_nodes[0]), 2)
        self.assertEquals(len(sim.stage_nodes[1]), 2)
        self.assertEquals(len(sim.stage_nodes[2]), 2)
        
        stage_0_keys = [node.id for node in sim.stage_nodes[0]]
        stage_1_keys = [node.id for node in sim.stage_nodes[1]]
        stage_2_keys = [node.id for node in sim.stage_nodes[2]]

        #connections between stages done correctly
        for key0 in stage_0_keys:
            for key1 in stage_1_keys:
                is_in = False              
                for n in sim.nodes[key0].targets:
                    if n.id == key1:
                        is_in = True
                        break
                self.assertTrue(is_in)
                
        for key1 in stage_1_keys:
            for key0 in stage_0_keys:
                is_in = False              
                for n in sim.nodes[key1].sources:
                    if n.id == key0:
                        is_in = True
                        break
                self.assertTrue(is_in)
                
        for key1 in stage_1_keys:
            for key2 in stage_2_keys:
                is_in = False              
                for n in sim.nodes[key1].targets:
                    if n.id == key2:
                        is_in = True
                        break
                self.assertTrue(is_in)
                
        for key2 in stage_2_keys:
            for key1 in stage_1_keys:
                is_in = False              
                for n in sim.nodes[key2].sources:
                    if n.id == key1:
                        is_in = True
                        break
                self.assertTrue(is_in)
        
        #No concepts of the same stage connected with each other
        for key0 in stage_0_keys:
            for key0 in stage_0_keys:
                is_in = False              
                for n in sim.nodes[key0].targets:
                    if n.id == key0:
                        is_in = True
                        break
                self.assertFalse(is_in)
                
        for key1 in stage_1_keys:
            for key1 in stage_1_keys:
                is_in = False              
                for n in sim.nodes[key1].targets:
                    if n.id == key1:
                        is_in = True
                        break
                self.assertFalse(is_in)
                
        for key2 in stage_2_keys:
            for key2 in stage_2_keys:
                is_in = False              
                for n in sim.nodes[key2].targets:
                    if n.id == key2:
                        is_in = True
                        break
                self.assertFalse(is_in)
                
     # inter-stage prob 0, intra-stage prob 1
    def test_create_simulation_prob_0_1(self):
        sim = RuleStructureSim()
        sim.create_simulation([2,2,2], 0, 1, False)
        
        # concepts created correctly?
        self.assertEquals(2+2+2, len(sim.nodes))        
        self.assertEquals(3, len(sim.stage_nodes))
        self.assertEquals(2, len(sim.stage_nodes[0]))
        self.assertEquals(2, len(sim.stage_nodes[1]))
        self.assertEquals(2, len(sim.stage_nodes[2]))
        
        stage_0_keys = [node.id for node in sim.stage_nodes[0]]
        stage_1_keys = [node.id for node in sim.stage_nodes[1]]
        stage_2_keys = [node.id for node in sim.stage_nodes[2]]

        #No connections between stages
        for key0 in stage_0_keys:
            for key1 in stage_1_keys:
                is_in = False              
                for n in sim.nodes[key0].targets:
                    if n.id == key1:
                        is_in = True
                        break
                self.assertFalse(is_in)
                
        for key1 in stage_1_keys:
            for key0 in stage_0_keys:
                is_in = False              
                for n in sim.nodes[key1].sources:
                    if n.id == key0:
                        is_in = True
                        break
                self.assertFalse(is_in)
                
        for key1 in stage_1_keys:
            for key2 in stage_2_keys:
                is_in = False              
                for n in sim.nodes[key1].targets:
                    if n.id == key2:
                        is_in = True
                        break
                self.assertFalse(is_in)
                
        for key2 in stage_2_keys:
            for key1 in stage_1_keys:
                is_in = False              
                for n in sim.nodes[key2].sources:
                    if n.id == key1:
                        is_in = True
                        break
                self.assertFalse(is_in)
        
        #Concepts of the same stage connected correctly. Stage 0 nodes had no sources
        node_A_stage_1 = sim.nodes[stage_1_keys[0]]
        node_B_stage_1 = sim.nodes[stage_1_keys[1]]
        self.assertEquals(node_A_stage_1.sources[0].id, node_B_stage_1.id)
        self.assertEquals(node_A_stage_1.targets[0].id, node_B_stage_1.id)
        self.assertEquals(node_B_stage_1.sources[0].id, node_A_stage_1.id)
        self.assertEquals(node_B_stage_1.targets[0].id, node_A_stage_1.id)    
        
        node_A_stage_2 = sim.nodes[stage_2_keys[0]]
        node_B_stage_2 = sim.nodes[stage_2_keys[1]]
        self.assertEquals(node_A_stage_2.sources[0].id, node_B_stage_2.id)
        self.assertEquals(node_A_stage_2.targets[0].id, node_B_stage_2.id)
        self.assertEquals(node_B_stage_2.sources[0].id, node_A_stage_2.id)
        self.assertEquals(node_B_stage_2.targets[0].id, node_A_stage_2.id)   

    def test_create_graph(self):     
        sim = RuleStructureSim()
        sim.create_simulation([2,2,2], 0, 1, False)
        
        self.assertEquals(2+2+2, len(sim.graph.nodes))
        self.assertEquals(4, len(sim.graph.edges))  
        sim.export_gml('./test2.gml')
        
    def test_check_next_stage_true(self):     
        sim = RuleStructureSim()
        sim.create_simulation([2,2,2], 1, 0)    
        stage_0_id = sim.stage_nodes[0][0].id
        self.assertTrue(sim.check_next_stage(sim.nodes[stage_0_id].id))
    
    def test_check_next_stage_false(self):     
        sim = RuleStructureSim()
        sim.create_simulation([2,2,2], 0, 1, False)  
        stage_0_id = sim.stage_nodes[0][0].id
        self.assertFalse(sim.check_next_stage(sim.nodes[stage_0_id].id))
    
    def test_disintegrate_node(self):
        sim = RuleStructureSim()
        sim.create_simulation([1], 1, 1)  
        
        self.assertEquals(1, len(sim.nodes))
        self.assertEquals(1, len(sim.stage_nodes[0]))
        
        sim.disintegrate_node(sim.nodes.values()[0].id)
        
        self.assertEquals(0, len(sim.nodes))
        self.assertEquals(0, len(sim.stage_nodes[0]))
        
    def test_disintegrate_node_2(self):
        sim = RuleStructureSim()
        sim.create_simulation([1, 1], 1, 1)  
        stage_0_id = sim.stage_nodes[0][0].id
        
        self.assertEquals(2, len(sim.nodes))
        self.assertEquals(1, len(sim.stage_nodes[0]))
        self.assertEquals(1, len(sim.stage_nodes[1]))
        
        sim.disintegrate_node(stage_0_id)
        
        self.assertEquals(1, len(sim.nodes))
        self.assertEquals(0, len(sim.stage_nodes[0]))
        self.assertEquals(1, len(sim.stage_nodes[1]))
        self.assertFalse(sim.nodes.values()[0].id == stage_0_id)
        
    def test_export_gml(self):
        sim = RuleStructureSim()
        sim.create_simulation([1, 1], 1, 0)        
        sim.export_gml('./test.gml')

        g = Graph()
        g.import_graph_gml('./test.gml')
        self.assertEquals(2, len(g.nodes))
        self.assertEquals(1, len(g.edges))
    
    def test_export_gml_create(self):
        sim = RuleStructureSim()
        sim.create_simulation([300, 100, 75, 10], 0.05, 0.001)
        
        sim.export_gml('./result.gml')
        
    def test_prune_non_consecuential_1(self):
        sim = RuleStructureSim()
        sim.create_simulation([1,1,1], 0, 1, False)
        
        stage_0_nodes = sim.stage_nodes[0]    
        stage_1_nodes = sim.stage_nodes[1]    
        
        sim.prune_non_consecuential()
        
        for n in stage_0_nodes:
            self.assertFalse(n in sim.nodes.keys())
        for n in stage_1_nodes:
            self.assertFalse(n in sim.nodes.keys())

        self.assertEquals(0, len(sim.stage_nodes[0]))
        self.assertEquals(0, len(sim.stage_nodes[1]))
        self.assertEquals(1, len(sim.stage_nodes[2]))
        
    def test_prune_non_consecuential_2(self):
        sim = RuleStructureSim()
        sim.create_simulation([2,2,2], 0, 0, False)
        
        stage_0_nodes = sim.stage_nodes[0]    
        stage_1_nodes = sim.stage_nodes[1]    
        
        sim.prune_non_consecuential()
        
        for n in stage_0_nodes:
            self.assertFalse(n in sim.nodes.keys())
        for n in stage_1_nodes:
            self.assertFalse(n in sim.nodes.keys())

        self.assertEquals(0, len(sim.stage_nodes[0]))
        self.assertEquals(0, len(sim.stage_nodes[1]))
        self.assertEquals(2, len(sim.stage_nodes[2]))
        
    def test_prune_non_consecuential_3(self):
        sim = RuleStructureSim()
        sim.create_simulation([2,2,2], 0, 1, False)
        
        stage_0_nodes = sim.stage_nodes[0]    
        stage_1_nodes = sim.stage_nodes[1]    
        
        sim.prune_non_consecuential()
        
        for n in stage_0_nodes:
            self.assertFalse(n in sim.nodes.keys())
        for n in stage_1_nodes:
            self.assertFalse(n in sim.nodes.keys())
        
        self.assertEquals(0, len(sim.stage_nodes[0]))
        self.assertEquals(0, len(sim.stage_nodes[1]))
        self.assertEquals(2, len(sim.stage_nodes[2]))
        
    def test_prune_non_consecuential_4(self):
        sim = RuleStructureSim()
        sim.create_simulation([2,2,2], 1, 1, False)
        
        sim.prune_non_consecuential()
        
        self.assertEquals(2, len(sim.stage_nodes[0]))
        self.assertEquals(2, len(sim.stage_nodes[1]))
        self.assertEquals(2, len(sim.stage_nodes[2]))
        self.assertEquals(2+2+2, len(sim.nodes))
        
if __name__ == '__main__':
    unittest.main()

