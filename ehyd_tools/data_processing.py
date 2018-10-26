__author__ = "David Camhy, Markus Pichler"
__copyright__ = "Copyright 2017, University of Technology Graz"
__credits__ = ["David Camhy", "Markus Pichler"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "David Camhy, Markus Pichler"

import pandas as pd
from pandas.tseries.offsets import _delta_to_tick as delta_to_freq
from kostra import Kostra
from kostra.definitions import DWA, PARTIAL


def export_series(series, save_as='csv'):
    """

    :type series: pd.Series
    :param save_as: export format
    :type save_as: str
    """
    if save_as is 'csv':
        series.to_csv('{}.csv'.format(series.name))


def r720_1(series, name):
    """

    :type name: str
    :type series: pd.Series
    :rtype: float
    """
    kostra = Kostra(series_kind=PARTIAL, worksheet=DWA)
    kostra.set_series(series.resample('1h').sum()
                      , name=name)
    kostra.result_plot()
    return kostra.r_720_1()


def year_delta(years):
    return pd.Timedelta(days=365.2425 * years)


def max_10a(frame, name):
    # get minimal gaps and minimal nan - return series
    df = frame.copy()
    avail = ~(df['nans'] | df['gaps'])
    avail_sum = avail.rolling(delta_to_freq(year_delta(years=10))).sum()
    max_avail_end = avail_sum.idxmax()
    max_avail_start = max_avail_end - year_delta(years=10)
    return df.loc[max_avail_start:max_avail_end, name].copy()


def data_analysis(series):
    # add gaps sum & nan sum to series - return frame
    df = series.to_frame()
    df['nans'] = pd.isna(series).astype(int)
    df['gaps'] = pd.isna(series.fillna(0).resample('T').sum()).astype(int)
    return df
