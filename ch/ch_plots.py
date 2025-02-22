import pandas as pd
import os
import skbio


from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

from matplotlib.colors import rgb2hex
import matplotlib.colors as mcolors


import random
import warnings


class HullsPlot:
    """ Store attributes about our plots that are
        shared based on a metadata and ordination """
    
    def __init__(self, ordination, metadata, groupc, subjc=None, timec=None):
        
        self.o_ord = ordination # o = original
        self.o_meta = metadata
        self.groupc = groupc
        self.subjc = subjc
        self.timec = timec
        
        self.id = self.get_id()
        self.ord, self.meta = self.filter_ids()
        self.colors = self.get_colors()
        
    def get_id(self):
        """ Get the sample id column name from metadata """
        # TODO make compatible with diff sample name columns
        return 'sample_name'
    
    def get_times(self):
        """ Get unique timepoints from the time column and metadata """
        return sorted(list(self.meta[self.timec].unique()))

    def get_groups(self):
        """ Get unique groups from the group column and metadata """
        return sorted(list(self.meta[self.groupc].unique()))
    
    def get_colors(self, palette='tab10'):
        """ Assign colors to each of the groups 
            Returns:
            colors (dictionary): colors dictionary 
        """
        
        groups = self.meta[self.groupc].unique()
        
        if palette == 'viridis':
            cmap = plt.cm.viridis
        if palette == 'tab10':
            cmap = plt.cm.tab10
            
        colors = {groups[i]:mcolors.to_hex(cmap.colors[i]) for i in range(len(groups))}
        return colors
    
    def get_color_from_group(self, group):
        """ Returns color from group """
        return self.colors[group]
        
    def filter_ids(self):
        """ Matches metadata to ordination. 
            Returns:
            ord (pd.DataFrame): Ordination samples
            meta (pd.DataFrame): Metadata matched """
        
        o = self.o_ord.samples
        m = self.o_meta
        ID = self.id
        
        ids = list(set(o.index) & set(m[ID]))
        if len(ids) == 0:
            raise KeyError("No matching ids found between metadata and ordination.")
        ord = o.loc[ids]
        meta = m.set_index(ID).loc[ids].reset_index()
        
        return ord, meta
    

#### PLOT 3D HULLS FUNCTIONS ####
def match_ids(hp, ids):
    """ Input HullsPlot, ids. Output overlapping ids as list."""
    
    matched_ids = list(set(hp.ord.index) & set(ids))
    
    if len(matched_ids) < 3:
        raise ValueError('Error in match_ids. Too few points.')
    
    return matched_ids

def add_hull(points, simplex, color, ax):
    """ Adds 3d hull panes around points that form hull.
        Draws white lines between hull points.

        Parameters: 
        points (np.array): 2d array of points
        simplex (np.array): list of points that define a hull
        color: any valid matplotlib color,
        ax: working axis
    """
    
    simplex_points = points[simplex]
    poly = Poly3DCollection([simplex_points], alpha=0.2, facecolor=color)
    ax.add_collection3d(poly)
    edges = [[simplex_points[i], simplex_points[j]] for i, j in [(0, 1), (1, 2), (2, 0)]]
    edge_lines = Line3DCollection(edges, colors='white', linewidths=0.5)
    ax.add_collection3d(edge_lines)


def get_site_ids(hp, group, time):
    """ Return metadata ids of a group at a time as list.
    
    Parameters:
    group
    time
    """
    
    s = hp.meta[hp.groupc] == group
    t = hp.meta[hp.timec] == time

    return list(hp.meta[s & t][hp.id])

def get_points(hp, matched_ids):
    """ Get points from ids
    
    Parameters:
    hp (HullsPlot): object with stored info
    matched_ids: list of ids to extract
    """
    return hp.ord.loc[matched_ids].to_numpy()

def get_hull(group_points, group, time):
    """ Find convex hull around a group of points.
        If not possible, return None but don't error
    """

    try:
        return ConvexHull(group_points)
    except:
        print(f'Error with convex hulls {group} {time}')
        return None


def draw_points_hull(hp, group, group_points, group_hull, ax):
    """ Draws points from a group at a time 

        Parameters:
        hp (HullsPlot)
        group (str): group name
        group_points (pd.DataFrame): points
        group_hull (ConvexHull)
        ax: working axis
    """
    color = hp.get_color_from_group(group)
    ax.scatter(
        group_points[:, 0], 
        group_points[:, 1],
        group_points[:, 2],
        color=color,
        alpha=0.7,
        label=group)

    for simplex in group_hull.simplices:
        add_hull(group_points, simplex, color, ax)


def make_points_hull(hp, group, time, ax):

    ids = get_site_ids(hp, group, time)
    matched_ids = match_ids(hp, ids)
    group_points = get_points(hp, matched_ids)
    group_hull = get_hull(group_points, group, time)

    if not group_hull == None:
        draw_points_hull(hp, group, group_points, group_hull, ax)

def _plot_3d_hulls(hp, axis=True, rotation=45, elev=30):
    """ Draw all hulls with each axis being a different timepoint """
    
    times = hp.get_times()
    groups = hp.get_groups()
    
    # Configure plot
    scale = 10
    fig = plt.figure(figsize=(scale*len(times), scale))
    ncol = len(times)
    
    for i, what_time in enumerate(times):

        ax = fig.add_subplot(1, ncol, i+1, projection='3d')
        for group in groups:
            make_points_hull(hp, group, what_time, ax)

        # Decorate plot
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.legend()

        if not axis:
            ax.axis('off')

        ax.view_init(elev=elev, azim=rotation)  # Adjust these angles as desired
        plt.title(f"Convex Hulls at {what_time}")

    return fig
   
   
def plot_3d_hulls(ordination, metadata,  #necessary
                  groupc, subjc, timec,  #column names
                  axis=True,
                  rotation=45, hp=None):
    """ Wraps 3d hulls plot and creates hp object if not passed. 
        This functionality is to allow users to generate a different plot
        first and use the same metadata and ordination to draw any other plot. 
    """           
    if hp == None:
        hp = HullsPlot(
            ordination=ordination,
            metadata=metadata,
            groupc=groupc,
            subjc=subjc,
            timec=timec,
        )
    fig = _plot_3d_hulls(hp, axis=axis, rotation=rotation, elev=30)
    return fig, hp


class SubsampledCH:
    """ Class for tracking a hulls volume df.
        Instead of having to manually define all empty lists
        in subsequent functions we can create an object class that 
        has pre-defined empty lists for fields we wish to track
    """
    
    def __init__(self):
        self.vols = []
        self.areas = []
        self.times = []
        self.npoints = []
        self.categ = []
        self.iter = []
        self.indiv = []
        
def calculate_hull(ord, ids, ndim):
    coords = ord.loc[ids].values[:, :ndim]
    return ConvexHull(coords)
        
        
def subsample_ids(group, n):
    ids = list(group.index)
    return random.sample(ids, n)


def find_n_subsamples(groups, n_subsamples):
    """ If no subsampling depth is provided we set the 
        subsampling depth to be the size of the smallest 
        group - 1.
    """
    smallest_n = min([len(group) for g, group in groups])
    
    if n_subsamples is not None:
        return n_subsamples
    
    if smallest_n - 1 < 3:
        raise ValueError('Some groups have less than 3 members.')
    
    return smallest_n - 1 


def df_from_ch(hp, ch):
    """ Generate the hulls df from all fields """

    all_hulls = pd.DataFrame({
        hp.timec: ch.times,
        hp.groupc: ch.categ,
        'convexhull_volume': ch.vols,
        'convexhull_area': ch.areas,
        'npoints': ch.npoints,
        'iteration': ch.iter,
        'individual': ch.indiv,
    })
    return all_hulls


def ch_by_groups(hp, ch, groups, n_subsamples, i, ndim=3, time=True):
    """ Generate hull volumes for each group and 
        track results in a SubsampledCH object
    """
    
    for g, group in groups:
        group.set_index('sample_name', inplace=True)
        
        if n_subsamples != None:
            ids = subsample_ids(group, n_subsamples)
        else:
            ids = list(group.index)

        if len(ids) <= 3:
            warnings.warn(f"Not enough samples for this group. Skipping {g}")
            continue

        c_hull = calculate_hull(hp.ord, ids, ndim)
        ch.vols.append(c_hull.volume)
        ch.areas.append(c_hull.area)
        ch.npoints.append(len(ids))
        ch.iter.append(f'iter-{i}')
        
        if time:
            ch.times.append(g[1])
            ch.categ.append(g[0])
            ch.indiv.append('not applicable')
        else:
            ch.times.append(None)
            ch.categ.append(list(group[hp.groupc])[0])
            ch.indiv.append(g)

    return ch


def generate_hulls_df(hp, n_subsamples=None, n_iters=10, ndim=3):
    """ Generate hull volumes iteratively for the bootstrapping step. """
    
    groups = hp.meta.groupby([hp.groupc, hp.timec])
    n_subsamples = find_n_subsamples(groups, n_subsamples)
    
    ch = SubsampledCH()
    
    for i in range(n_iters):
        ch = ch_by_groups(hp, ch, groups, n_subsamples, i, ndim=3, time=True)
    
    all_hulls = df_from_ch(hp, ch)
    return all_hulls


def _plot_hulls_group(hp, df):
    """ Line plots from hp object and df """
    x = hp.timec
    y = 'convexhull_volume'
    hue = hp.groupc
    data = df
    
    fig, ax = plt.subplots(1, 1)
    sns.lineplot(
        data=data, x=x, y=y,
        hue=hue,
        legend=False,
        palette=hp.colors,
        ax=ax
    )
    sns.scatterplot(
        data=data, x=x, y=y,
        hue=hue,
        palette=hp.colors,
        ax=ax
    )
    
    return fig

def plot_group_hulls_over_time(
    ordination: skbio.OrdinationResults, 
    metadata: pd.DataFrame,
    groupc: str, 
    subjc : int,
    timec : int,
    n_subsamples: int = 10,
    n_iters: int = 20,
    hp = None):
    """ Main group hulls function that generates hulls df
        and plots it. This is called within the visualization
        for q2 integration
    """

    if hp == None:
        hp = HullsPlot(
            ordination=ordination,
            metadata=metadata,
            groupc=groupc,
            subjc=subjc,
            timec=timec,
        )
    
    df = generate_hulls_df(hp, n_subsamples=n_subsamples, n_iters=n_iters)
    fig = _plot_hulls_group(hp, df)
    
    return df, fig


### INDIVIDUAL PLOTS
def ch_df_by_indiv(
        hp, 
        n_subsamples=None,
    ):
    """ Operates the same as for groups but passes 0 as a 
        parameter for the iteration number.
    """
    groups = hp.meta.groupby(hp.subjc)
    ch = SubsampledCH()
    ch = ch_by_groups(hp, ch, groups, n_subsamples, 0, ndim=3, time=False)
    df = df_from_ch(hp, ch)
    return df

def plot_individuals(hp, df, y='convexhull_volume'):
    """ Plots df of individual hull volumes """
    
    data = df
    x = hp.groupc
    fig, ax = plt.subplots(1,1)
    sns.boxplot(data=data, x=x, y=y, palette=hp.colors, ax=ax)
    sns.swarmplot(data=data, x=x, y=y, color='black', ax=ax)
    return fig
    
def plot_indiv_hulls_by_group(
    ordination, metadata,
    groupc, subjc, timec,
    n_subsamples=None, hp=None):
    """ Main individual plotting function that is called from
        the visualizer
    """

    if hp == None:
        hp = HullsPlot(
            ordination=ordination,
            metadata=metadata,
            groupc=groupc,
            subjc=subjc,
            timec=timec,
        )
    df = ch_df_by_indiv(hp, n_subsamples=n_subsamples)
    fig = plot_individuals(hp, df)
    
    return df, fig


def plot_group_cross_sectional(
    ordination, metadata,
    groupc, subjc,
    n_subsamples=None,
    hp=None):
    """ Main function called from cross-sectional
        group plotting action.
    """

    if hp == None:
        hp = HullsPlot(
            ordination=ordination,
            metadata=metadata,
            groupc=groupc,
            subjc=subjc,
            timec='o',
        )
    
    df = generate_hulls_df(hp, n_subsamples=n_subsamples)
    fig = plot_individuals(hp, df)
    
    return df, fig
