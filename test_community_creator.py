# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:58:18 2013

@author: aitor
"""

import unittest
from community_creator import CommunityCreator

class TestRuleEstructureSim(unittest.TestCase):
    
#    def test_import_gml(self):
#        c = CommunityCreator(True)
#        c.import_edgelist('./testfiles/test.csv')
#        self.assertEquals(323, len(c.G.nodes()))
#        self.assertEquals(836, len(c.G.edges()))
#        
    def test_find_cliques(self):
        c = CommunityCreator(True)
        c.import_edgelist('./testfiles/test.csv')
        res = c.find_cliques()
        self.assertEquals(766, res)
        
    def test_find_common_subsets(self):
        c = CommunityCreator(False)
        groups1 = [ { 'A', 'B' }, { '1', '2', '3' }, { 'B', 'D'}, { 'X', 'Y' }, {'D', '4'} ]
        groups1_results = [ { 'A', 'B', 'D', '4' }, {'1', '2', '3'}, { 'X', 'Y' } ]
        
        result = c.find_common_subsets(groups1)
        self.assertEquals(result, groups1_results)

        groups2 = [ { 'A', 'B' }, { '1', '2', '3', '4' }, { 'B', 'D'}, { 'X', 'Y' }, {'D', '4'} ] 
        groups2_results = [ { 'A', 'B', 'D', '4', '1', '2', '3'}, { 'X', 'Y' } ]
        
        result = c.find_common_subsets(groups2)
        self.assertEquals(result, groups2_results)
        
        groups3 = [ { 'A', 'B' }, { '1', '2', '3', '4' }, { 'D', '4'}, { 'X', 'Y' }, {'B', 'D'} ] 
        groups3_results = [ { 'A', 'B', 'D', '4', '1', '2', '3'}, { 'X', 'Y' } ]
        
        result = c.find_common_subsets(groups3)
        self.assertEquals(result, groups3_results)
        
        groups4 = [ { 'A', 'B' }, { '1', '2', '3' }, { 'D', '4'}, { 'X', 'Y' }, {'B', 'D'} ]
        groups4_results = [ { 'A', 'B', 'D', '4' }, {'1', '2', '3'}, { 'X', 'Y' } ]
        
        result = c.find_common_subsets(groups4)
        self.assertEquals(result, groups4_results)
        
        groups5 = [ { 'A'}, { '1', '2', '3' }, {'D', '4', 'A'}, { 'X', 'Y' }, {'B', 'D'} ]
        groups5_results = [ { 'A', 'B', 'D', '4' }, {'1', '2', '3'}, { 'X', 'Y' } ]
        
        result = c.find_common_subsets(groups5)
        self.assertEquals(result, groups5_results)
        
        groups6 = [ {'A'}, {'B'}, {'A', 'B'}, { '1', '2', '3' }, {'D', '4', 'A'}, { 'X', 'Y' }, {'B', 'D'} ]
        groups6_results = [ { 'A', 'B', 'D', '4' }, {'1', '2', '3'}, { 'X', 'Y' } ]
        
        result = c.find_common_subsets(groups6)
        self.assertEquals(result, groups6_results)
        
        groups7 = [ {'A'}, {'B'}, {'C'} ]
        groups7_results = [ {'A'}, {'B'}, {'C'}  ]
        
        result = c.find_common_subsets(groups7)
        self.assertEquals(result, groups7_results)
        
        
#        
#    def test_find_k_cliques(self):
#        c = CommunityCreator(True)
#        c.import_edgelist('./testfiles/test.csv')
#        res = c.find_k_cliques(3)
#        self.assertEquals(766, res)
        

if __name__ == '__main__':
    unittest.main()