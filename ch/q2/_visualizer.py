from ch.ch_plots import plot_3d_hulls as ch_plot_3d_hulls
from ch.ch_plots import plot_indiv_hulls_by_group as ch_plot_indiv_hulls_by_group
from ch.ch_plots import plot_group_hulls_over_time as ch_plot_group_hulls_over_time

from ch.ch_plots import plot_group_cross_sectional as ch_plot_group_cross_sectional

import q2templates
import pandas as pd
import matplotlib.pyplot as plt
import pkg_resources
import skbio
import os
import qiime2

TEMPLATES = pkg_resources.resource_filename('ch', 'q2')

def _validate(metadata):
    
    if type(metadata) == pd.DataFrame:
        return metadata
    else:
        return metadata.to_dataframe().reset_index()

def hulls_plots(
    output_dir: str,
    ordination: skbio.OrdinationResults,
    metadata: pd.DataFrame,
    groupc: str,
    subjc: str,
    timec: str,
    axis: bool = True,
    rotation: int = 60,
    n_iters: int = 20,
    n_subsamples: int = None,
    ) -> None:

    metadata = _validate(metadata)

    fig, hp = ch_plot_3d_hulls(
        ordination, metadata,  #necessary
        groupc, subjc, timec,  #column names
        axis=axis, rotation=rotation)
    fpath = os.path.join(output_dir, '3d_hulls.svg')
    fig.savefig(fpath, bbox_inches='tight')
    plt.clf()

    group_df, group_fig = ch_plot_group_hulls_over_time(
        ordination, metadata,
        groupc, subjc, timec,
        n_subsamples=None, n_iters=n_iters)
    
    fpath = os.path.join(output_dir, 'group_hulls.svg')
    group_fig.savefig(fpath, bbox_inches='tight')
    plt.clf()

    indiv_df, indiv_fig = ch_plot_indiv_hulls_by_group(
        ordination, metadata,
        groupc, subjc, timec,
        n_subsamples=None)
    fpath = os.path.join(output_dir, 'indiv_hulls.svg')
    indiv_fig.savefig(fpath, bbox_inches='tight')
    plt.clf()

    # VISUALIZER
    context = {}
    TEMPLATES = pkg_resources.resource_filename('ch', 'q2')
    index = os.path.join(TEMPLATES, 'plot_assets', 'index.html')
    q2templates.render(index, output_dir, context=context)
    
    

def hulls_plots_cross_sectional(
    output_dir: str,
    ordination: skbio.OrdinationResults,
    metadata: pd.DataFrame,
    groupc: str,
    subjc: str,
    axis: bool = True,
    rotation: int = 60,
    n_iters: int = 20,
    n_subsamples: int = None,
    ) -> None:

    metadata = _validate(metadata)
    metadata['o'] = [0 for i in range(len(metadata))]

    fig, hp = ch_plot_3d_hulls(
        ordination, metadata,  #necessary
        groupc, subjc, 'o',    #column names
        axis=axis, rotation=rotation)
    fpath = os.path.join(output_dir, '3d_hulls.svg')
    fig.savefig(fpath, bbox_inches='tight')
    plt.clf()

    group_df, group_fig = ch_plot_group_cross_sectional(
        ordination, metadata,
        groupc, subjc,
        n_subsamples=None
    )
    fpath = os.path.join(output_dir, 'group_hulls.svg')
    group_fig.savefig(fpath, bbox_inches='tight')
    plt.clf()

    # VISUALIZER
    context = {}
    TEMPLATES = pkg_resources.resource_filename('ch', 'q2')
    index = os.path.join(TEMPLATES, 'plot_assets', 'index_cross.html')
    q2templates.render(index, output_dir, context=context)