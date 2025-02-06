from ch.ch_plots import plot_3d_hulls as ch_plot_3d_hulls
from ch.ch_plots import plot_indiv_hulls_by_group as ch_plot_indiv_hulls_by_group
from ch.ch_plots import plot_group_hulls_over_time as ch_plot_group_hulls_over_time

import q2templates
import pandas as pd
import matplotlib.pyplot as plt
import pkg_resources
import skbio

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

    fig, hp = plot_3d_hulls(
        ordination, metadata,  #necessary
        groupc, subjc, timec,  #column names
        axis=axis, rotation=rotation)
    plt.savefig(os.path.join(output_dir, '3d_hulls.svg'))
    plt.close()


    group_df, ax = plot_group_hulls_over_time(
        ordination, metadata,
        groupc, subjc, timec,
        n_subsamples=None, n_iters=n_iters)
    plt.savefig(os.path.join(output_dir, 'group_hulls.svg'))
    plt.close()


    indiv_df, ax = plot_group_hulls_over_time(
        ordination, metadata,
        groupc, subjc, timec,
        n_subsamples=None)
    plt.savefig(os.path.join(output_dir, 'indiv_hulls.svg'))
    plt.close()


    # VISUALIZER
    context = {}
    TEMPLATES = pkg_resources.resource_filename('ch', 'plot_assetss')
    index = os.path.join(TEMPLATES, 'index.html')
    q2templates.render(index, output_dir, context=context)
