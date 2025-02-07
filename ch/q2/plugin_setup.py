# ----------------------------------------------------------------------------
# Copyright (c) 2025--, Daniela Perry.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin
import qiime2.sdk
import importlib

from ch.q2._visualizer import hulls_plots

from ch import __version__


from ._type import Hulls
from ._format import HullsFormat, HullsDirectoryFormat

from qiime2.plugin import (Int, Str, Bool,
                           Metadata, Visualization)
from q2_types.ordination import PCoAResults
from qiime2.plugin import Metadata


citations = qiime2.plugin.Citations.load(
    'citations.bib', package='gemelli')

plugin = qiime2.plugin.Plugin(
    name='convexhull2',
    version=__version__,
    website="https://github.com/dpear/q2-convexhull2",
    citations=[],
    short_description=('Plugin for calculating '
        'and visualizing Convex Hull Volume'),
    description=('This is a QIIME 2 plugin for '
        'calculating and visualizing Convex Hull Volume'),
    package='convexhull2')

plugin.visualizers.register_function(
    function=hulls_plots,
    inputs={
        'ordination': PCoAResults,
    },
    parameter_descriptions={
        'metadata': 'Metadata',
        'groupc': 'Str',
        'subjc': 'Str',
        'timec': 'Str',
        'axis': 'Bool default True',
        'rotation': 'Int = default 60',
        'n_iters': 'Int = default 20',
        'n_subsamples': 'int = None',
    },
    input_descriptions={
        'ordination': 'PCoAResults',
    },
    parameters={
        'metadata': Metadata,
        'groupc': Str,
        'subjc': Str,
        'timec': Str,
        'axis': Bool,
        'rotation': Int,
        'n_iters': Int,
        'n_subsamples': Int,
    },
    name='Calculate all 3 types of plots',
    description=('Generate a qiime2 visualization '
                 'that allows for generating and easy download '
                 'of 3d hulls plot, line plot of group dispersion '
                 'and boxplot of individual dispersion by group'),
    citations=[],
)

importlib.import_module('ch.q2._transformer')
