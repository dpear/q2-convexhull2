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

INDEX_CROSS_DIR = 'plot_assets_cross'
INDEX_DIR = 'plot_assets'

NAME_GROUP_HULLS = 'group_hulls'
NAME_3D_HULLS = '3d_hulls'
NAME_INDIV_HULLS = 'indiv_hulls'

def _validate(metadata):
    """ Ensure metadata is correct type. 
        This essentially does the job of a transformer.
        Transformer should be implemented but isn't. 
        See this post: https://forum.qiime2.org/t/metadata-
        type-handling-transforming-in-qiime2-plugins/32514
    """

    if type(metadata) == pd.DataFrame:
        return metadata
    else:
        return metadata.to_dataframe().reset_index()


def save_hulls_output(output_dir, name, fig, df, has_df=True):
    """ Save hulls plots as svg and df's as tsvs.
        Inputs: output_dir, name, df, fig.
    """
    
    f_svg = os.path.join(output_dir, f'{name}.svg')
    f_tsv = os.path.join(output_dir, f'{name}.tsv')
    fig.savefig(f_svg, bbox_inches='tight')
    
    # Add option to not save df for 3d hulls plot
    if has_df:
        df.to_csv(f_tsv, sep='\t', index=False)

 
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
    """ Creates the three hulls plots and saves in temp
        qiime2 directory to be viewed in the visualization file. 
    """

    metadata = _validate(metadata)

    # MAKE 3d PLOT AND SAVE
    fig, hp = ch_plot_3d_hulls(
        ordination=ordination,
        metadata=metadata,
        groupc=groupc,
        subjc=subjc,
        timec=timec,
        axis=axis,
        rotation=rotation)
    save_hulls_output(
        output_dir=output_dir,
        name=NAME_3D_HULLS,
        df=None,
        fig=fig,
        has_df=False)
    plt.clf()
    
    # MAKE GROUP PLOT AND SAVE
    group_df, group_fig = ch_plot_group_hulls_over_time(
        ordination=ordination,
        metadata=metadata,
        groupc=groupc,
        subjc=subjc,
        timec=timec,
        n_subsamples=n_subsamples,
        n_iters=n_iters,
        hp=hp)
    
    save_hulls_output(
        output_dir=output_dir,
        name=NAME_GROUP_HULLS,
        df=group_df,
        fig=group_fig,
        has_df=True)
    plt.clf()

    # MAKE INDIVIDUAL PLOT AND SAVE
    indiv_df, indiv_fig = ch_plot_indiv_hulls_by_group(
        ordination=ordination, 
        metadata=metadata,
        groupc=groupc,
        subjc=subjc,
        timec=timec,
        n_subsamples=None,
        hp=hp)
    save_hulls_output(
        output_dir=output_dir,
        name=NAME_INDIV_HULLS,
        df=indiv_df,
        fig=indiv_fig,
        has_df=True)
    plt.clf()

    # CREATE VISUALIZER
    context = {}
    index = os.path.join(TEMPLATES, INDEX_DIR, 'index.html')
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
    """ Creates the 3d plot and group plot in the case that
        there are no timepoints and only group characteristics are
        of interest.
    """

    metadata = _validate(metadata)
    
    # Create metadata column with only one value
    metadata['o'] = [0 for i in range(len(metadata))]

    fig, hp = ch_plot_3d_hulls(
        ordination, metadata,  #necessary
        groupc, subjc, 'o',    #column names
        axis=axis, rotation=rotation)
    save_hulls_output(
        output_dir=output_dir,
        name=NAME_3D_HULLS,
        df=None,
        fig=group_fig,
        has_df=False)
    plt.clf()
    
    group_df, group_fig = ch_plot_group_cross_sectional(
        ordination=ordination, 
        metadata=metadata,
        groupc=groupc, 
        subjc=subjc,
        n_subsamples=None,
        hp=hp,
    )
    save_hulls_output(
        output_dir=output_dir,
        name=NAME_GROUP_HULLS,
        df=group_df,
        fig=group_fig,
        has_df=True)
    plt.clf()

    # VISUALIZER
    context = {}
    index = os.path.join(TEMPLATES, INDEX_CROSS_DIR, 'index.html')
    q2templates.render(index, output_dir, context=context)
    
