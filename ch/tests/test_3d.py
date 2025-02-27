import unittest
import os
import inspect
import pandas as pd
import numpy as np
import skbio 
from pandas import read_csv
from biom import load_table
from skbio.util import get_data_path
from numpy.testing import assert_allclose

from ch.ch_plots import *

class TestHullsPlot(unittest.TestCase):
    
    def setUp(self):
        
        # Mock ordination
        self.ordination = skbio.OrdinationResults(
            short_method_name='PCA',
            long_method_name='Principal Component Analysis',
            eigvals=pd.Series([0.5, 0.3, 0.2]),
            samples=pd.DataFrame({
                'sample1': [0.1, 0.2, 0.3],
                'sample2': [0.4, 0.5, 0.6],
                'sample3': [0.7, 0.8, 0.9]
            }, index=['dim1', 'dim2', 'dim3']).T
        )
        
        # Mock metadata
        self.metadata = pd.DataFrame({
            'sample_name': ['sample1', 'sample2', 'sample3'],
            'group': ['A', 'B', 'A'],
            'time': [1, 2, 3]
        })

        self.hp = HullsPlot(
            ordination=self.ordination,
            metadata=self.metadata,
            groupc='group',
            subjc='sample_name',
            timec='time'
        )


    def test_get_id(self):
        
        self.assertEqual(
            self.hp.get_id(),
            'sample_name'
        )

    def test_get_times(self):
        
        self.assertListEqual(
            self.hp.get_times(),
            [1, 2, 3]
        )

    def test_get_groups(self):
        
        self.assertListEqual(
            self.hp.get_groups(),
            ['A', 'B']
        )

    def test_get_colors(self):

        colors = self.hp.get_colors()
        self.assertIsInstance(colors, dict)
        self.assertIn('A', colors)
        self.assertIn('B', colors)

    # def test_filter_ids(self):
        
    #     ord, meta = self.hp.filter_ids()
    #     self.assertTrue(not ord.empty)
    #     self.assertTrue(not meta.empty)
    #     # self.assertEqual(
    #     #     list(ord.index),
    #     #     ['sample1', 'sample2', 'sample3'])
    #     self.assertEqual(
    #         'A',
    #         'A')
        
    def test_get_color_from_group(self):

        color = self.hp.get_color_from_group('A')
        self.assertTrue(isinstance(color, str))
        
    def test_get_color_from_group(self):
        
        colors = self.hp.get_colors()
        color = self.hp.get_color_from_group('A')
        self.assertIn(color, colors.values())

    def test_match_ids_error_handling(self):
        with self.assertRaises(ValueError):
            
            # Too few points to create a hull
            match_ids(self.hp, ['sample1'])

    def test_get_hull_error_handling(self):
        
        # 2 points = can NOT make hull
        points = np.random.rand(2, 3)
        x = get_hull(points, 'A', 1)
        self.assertIs(x, None)

    def test_successful_hull_creation(self):
        
        # 4 points = CAN make hull
        points = np.random.rand(4, 3) 
        hull = get_hull(points, 'A', 1)
        self.assertIsInstance(hull, ConvexHull)
        
    def test_subsample(self):
        group = pd.DataFrame({
            's1': [1,2,3],
            's2':[1,2,3]},
            index=[1,2,3])
        subsample_ids(group, 2)

if __name__ == "__main__":
    unittest.main()