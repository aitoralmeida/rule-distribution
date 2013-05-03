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
        
        self.assertEquals(len(sim.stages), 3)
        self.assertEquals(len(sim.stages[0]), 5)
        self.assertEquals(len(sim.stages[1]), 3)
        self.assertEquals(len(sim.stages[2]), 2)
        
if __name__ == '__main__':
    unittest.main()

