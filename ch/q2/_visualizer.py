from ch.ch_plots import plot_3d_hulls as ch_plot_3d_hulls
from ch.ch_plots import plot_indiv_hulls_by_group as ch_plot_indiv_hulls_by_group
from ch.ch_plots import plot_group_hulls_over_time as ch_plot_group_hulls_over_time

import q2templates
import pandas as pd
import matplotlib.pyplot as plt
import pkg_resources
import skbio
import os

TEMPLATES = pkg_resources.resource_filename('ch', 'q2')


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
    ):

    fig, hp = ch_plot_3d_hulls(
        ordination, metadata,  #necessary
        groupc, subjc, timec,  #column names
        axis=axis, rotation=rotation)
    fpath = os.path.join(output_dir, '3d_hulls.svg')
    plt.savefig(fpath, bbox_inches='tight')

    plt.clf()


    group_df, ax = ch_plot_group_hulls_over_time(
        ordination, metadata,
        groupc, subjc, timec,
        n_subsamples=None, n_iters=n_iters)
    
    fpath = os.path.join(output_dir, 'group_hulls.svg')
    plt.savefig(fpath, bbox_inches='tight')
    plt.clf()


    indiv_df, ax = ch_plot_indiv_hulls_by_group(
        ordination, metadata,
        groupc, subjc, timec,
        n_subsamples=None)
    fpath = os.path.join(output_dir, 'indiv_hulls.svg')
    plt.savefig(fpath, bbox_inches='tight')

    plt.clf()


    # VISUALIZER
    context = {}
    TEMPLATES = pkg_resources.resource_filename('ch', 'q2')
    index = os.path.join(TEMPLATES, 'plot_assets', 'index.html')
    q2templates.render(index, output_dir, context=context)


# TEMPLATES = pkg_resources.resource_filename('gemelli', 'q2')


# index = os.path.join(
#         TEMPLATES, 'qc_assests', 'index.html')
#     q2templates.render(index, output_dir, context=context)

