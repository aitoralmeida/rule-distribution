# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:58:18 2013

@author: aitor
"""

import unittest
from community_creator import CommunityCreator

class TestRuleEstructureSim(unittest.TestCase):
    
    def test_import_gml(self):
        c = CommunityCreator(True)
        c.import_edgelist('./testfiles/test.csv')
        self.assertEquals(323, len(c.G.nodes()))
        self.assertEquals(836, len(c.G.edges()))

if __name__ == '__main__':
    unittest.main()