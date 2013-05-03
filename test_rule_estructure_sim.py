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
    
    def test_create_simulation(self):
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
                self.assertTrue(key1 in sim.nodes[key0].targets) #key tiene que ser str
              
        
            
            
        
        
        
if __name__ == '__main__':
    unittest.main()

