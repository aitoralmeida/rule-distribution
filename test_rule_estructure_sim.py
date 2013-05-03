# -*- coding: utf-8 -*-
"""
Created on Fri May 03 10:48:35 2013

@author: aitor
"""

import unittest
from rule_structure_sim import RuleStructureSim

class TestRuleEstructureSim(unittest.TestCase):
    
    def test_create_concepts(self):
        sim = RuleStructureSim()
        sim.create_concepts([5,3,2])
        
        self.assertEquals(len(sim.nodes), 5+3+2)        
        
        self.assertEquals(len(sim.stage_nodes), 3)
        self.assertEquals(len(sim.stage_nodes[0]), 5)
        self.assertEquals(len(sim.stage_nodes[1]), 3)
        self.assertEquals(len(sim.stage_nodes[2]), 2)
    
    def test_create_simulation_prob_1(self):
        sim = RuleStructureSim()
        sim.create_simulation([2,2,2], 1, 1)
        
        # concepts created correctly?
        self.assertEquals(len(sim.nodes), 2+2+2)        
        self.assertEquals(len(sim.stage_nodes), 3)
        self.assertEquals(len(sim.stage_nodes[0]), 2)
        self.assertEquals(len(sim.stage_nodes[1]), 2)
        self.assertEquals(len(sim.stage_nodes[2]), 2)
        
        stage_0_keys = [node.id for node in sim.stage_nodes[0]]
        stage_1_keys = [node.id for node in sim.stage_nodes[1]]
        stage_2_keys = [node.id for node in sim.stage_nodes[2]]

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
                
              
        
        
if __name__ == '__main__':
    unittest.main()

