import numpy as np
import pandas as pd
from qiime2 import Metadata
from .plugin_setup import plugin
from ._format import HullsFormat


@plugin.register_transformer
def _1(data: pd.DataFrame) -> (HullsFormat):
    ff = HullsFormat()
    with ff.open() as fh:
        data.to_csv(fh, sep='\t', header=True, na_rep=np.nan)
    return ff


@plugin.register_transformer
def _2(ff: HullsFormat) -> (pd.DataFrame):
    # with ff.open() as fh:
    return Metadata.load(str(ff)).to_dataframe()


@plugin.register_transformer
def _3(ff: HullsFormat) -> (Metadata):
    # with ff.open() as fh:
    return Metadata.load(str(ff))