import pandas as pd
import numpy as np

import sklearn as sk
from datetime import datetime as dt

from matplotlib import pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots
import plotly.graph_objects as go

"""
Load data
"""
path = './data/'
mobility_filename = 'Global_Mobility_Report.csv'
confirmed_filename = 'time_series_covid19_confirmed_global.csv'
death_filename = 'time_series_covid19_deaths_global.csv'

mob = pd.read_csv(path+mobility_filename)
con = pd.read_csv(path+confirmed_filename)
death = pd.read_csv(path+death_filename)
"""
Constants
"""
MED_COLS = mob.columns[-7:]
CODE_EXAMPLE = 'BE-BRU' # an example of country_region_codes: Belgium-Brussel
COUNTRY = "United Kingdom"
MED_SHORTS = ['date','retail','grocery','parks','transit','workplaces','residential']
MEDIATORS = MED_SHORTS[1:]
SHIFT = 28 # default shift for mobility data - have tried with 7,10,14,28,30
"""
Functions
"""

def create_join_data(country, shift=0, mobility=mob, confirmed=con, death=death):
    """
    create a join datasets from mobility and confirmed cases
    Input:
        shift: mobility data shift (idea: lag between mobility and confirmed cases)
                (thinking shift>=0)
    Return:
        a dataframe with 6 first columns are mobility and the last column
        is the confirmed cases
    """
    mobil = mobility[mobility['country_region']==country]
    mobil = mobil[mobil['sub_region_1'].isna()]
    mobil = mobil[MED_COLS]
    mobil.columns = MED_SHORTS   # shorten the column names
    mobil['date'] = pd.to_datetime(mobil['date'], format='%Y-%m-%d')
    mobil = mobil.set_index('date')
    mobil_shift = mobil.shift(shift)
    # remove na rows b/c shifting
    if shift > 0:
        mobil_shift = mobil_shift.iloc[shift:,:]
    elif shift < 0:
        mobil_shift = mobil_shift.iloc[:shift,:]

    # confirmed time series
    conf = confirmed[confirmed['Country/Region']==country]
    # taking data aggregated for the entire country (not a region)
    conf = conf[conf['Province/State'].isna()]
    conf = conf.iloc[:,4:]
    conf = conf.T
    conf.index = pd.to_datetime(conf.index, format='%m/%d/%y', errors='ignore')
    # match the time index
    conf = conf[conf.index >= mobil_shift.index[0]]
    conf = conf[conf.index <= mobil_shift.index[-1]]

    # death time series
    de = death[death['Country/Region']==country]
    # taking data aggregated for the entire country (not a region)
    de = de[de['Province/State'].isna()]
    de = de.iloc[:,4:]
    de = de.T
    de.index = pd.to_datetime(de.index, format='%m/%d/%y', errors='ignore')
    # match the time index
    de = de[de.index >= mobil_shift.index[0]]
    de = de[de.index <= mobil_shift.index[-1]]
    # join 2 dataframe
    join = mobil_shift.merge(conf, left_index=True, right_index=True)
    join = join.merge(de, left_index=True, right_index=True)
    join = join.rename(columns={'223_x': 'confirmed', '223_y': 'death'})
    join['con_diff'] = join['confirmed'].diff()
    join['death_diff'] = join['death'].diff()
    return join

def plot_mobil(df, shift, country=COUNTRY,
                          confirmed_color='red', death_color='black'):
    """
    Plot the two time series on the same plot: factor vs confirmed
        Input: a dataframe with 6 factors and a column of confirmed positives
        Output: A plot of two time series on the same coordinate system.
    """
    fig = make_subplots(rows=3, cols=6,
                        shared_xaxes=True)

    t_index = df.index
    # confirmed cases are in the last column
    confirmed_series = df['confirmed'].diff()
    death_series = df['death'].diff()

    retail_series = df['retail']
    grocery_series = df['grocery']
    parks_series = df['parks']
    transit_series = df['transit']
    workplaces_series = df['workplaces']
    residential_series = df['residential']

    confirmed_data = go.Scatter(x=t_index, y=confirmed_series,
                       line_color=confirmed_color, name='confirmed diffence')
    death_data = go.Scatter(x=t_index, y=death_series,
                       line_color=death_color, name='death difference')

    retail_data = go.Scatter(x=t_index, y=retail_series,
                       line_color='darkblue', name='retail')
    grocery_data = go.Scatter(x=t_index, y=grocery_series,
                       line_color='darkgreen', name='grocery')
    parks_data = go.Scatter(x=t_index, y=parks_series,
                       line_color='darkmagenta', name='parks')
    transit_data = go.Scatter(x=t_index, y=transit_series,
                       line_color='darkviolet', name='transit')
    workplaces_data = go.Scatter(x=t_index, y=workplaces_series,
                       line_color='chocolate', name='workplaces')
    residential_data = go.Scatter(x=t_index, y=residential_series,
                       line_color='darkorange', name='residential')


    fig.add_trace(confirmed_data, row=1, col=1)
    fig.add_trace(confirmed_data, row=1, col=2)
    fig.add_trace(confirmed_data, row=1, col=3)
    fig.add_trace(confirmed_data, row=1, col=4)
    fig.add_trace(confirmed_data, row=1, col=5)
    fig.add_trace(confirmed_data, row=1, col=6)

    fig.add_trace(death_data, row=2, col=1)
    fig.add_trace(death_data, row=2, col=2)
    fig.add_trace(death_data, row=2, col=3)
    fig.add_trace(death_data, row=2, col=4)
    fig.add_trace(death_data, row=2, col=5)
    fig.add_trace(death_data, row=2, col=6)


    fig.add_trace(retail_data, row=3, col=1)
    fig.add_trace(grocery_data, row=3, col=2)
    fig.add_trace(parks_data, row=3, col=3)
    fig.add_trace(transit_data, row=3, col=4)
    fig.add_trace(workplaces_data, row=3, col=5)
    fig.add_trace(residential_data, row=3, col=6)

    # fig.update_layout(xaxis_rangeslider_visible=True)
    """
    fig.update_yaxes(title_text="confirmed_cases", row=1, col=1)
    fig.update_yaxes(title_text="confirmed_cases", row=1, col=2)
    fig.update_yaxes(title_text="confirmed_cases", row=1, col=3)
    fig.update_yaxes(title_text="confirmed_cases", row=1, col=4)
    fig.update_yaxes(title_text="confirmed_cases", row=1, col=5)
    fig.update_yaxes(title_text="confirmed_cases", row=1, col=6)

    fig.update_yaxes(title_text='retail', row=2, col=1)
    fig.update_yaxes(title_text='grocery', row=2, col=2)
    fig.update_yaxes(title_text='parks', row=2, col=3)
    fig.update_yaxes(title_text='transit', row=2, col=4)
    fig.update_yaxes(title_text='workplaces', row=2, col=5)
    fig.update_yaxes(title_text='residential', row=2, col=6)
    """
    fig.update_layout(legend_orientation='v',
                      title_text=country+', shift={}'.format(shift))
    # fig.update_xaxes(rangeslider_visible=True)
    """
    range_slider as you wish
    for i in range(number_of_subplots,0,-1):
        fig.update_xaxes(row=i, col=1, rangeslider_visible=True)
    """
    fig.show()

"""
Put six factors into bins of 6 quantiles
"""
def bin_mediator(df, num_bin=6):
    """
    use pandas qcut to divide up numeric mediators into bin by quantiles
    Output:
        a new dataframe with added bins
    """
    assert num_bin>0
    for c in MEDIATORS:
        df[c+'_bin'] = pd.qcut(df[c], num_bin)

"""
An experiment
"""
# plot_mobil(df, shift=SHIFT)

def run_experiment(country=COUNTRY, shift_range = range(28, 100)):
    co = np.zeros(10)
    shift_op = 0
    for shift in shift_range:
        df = create_join_data(country=country, shift=shift)
        df['con_diff'] = df['confirmed'].diff()
        df['de_diff'] = df['death'].diff()
        corr = df.corr().iloc[:,-1]
        if shift_op == 0:
            shift_op = shift
            co = np.array(corr)
        elif co[0] < corr[0]:
            co = np.array(corr)
            shift_op = shift

    return shift_op, co

"""
experiment results
"""
shift_op=50
# correlations between difference of death, de_diff and mobility features
corr_op = {'retail': 0.824, 'grocery': 0.679, 'parks':0.563,
           'transit': 0.802, 'workplaces': 0.717, 'residential':-0.690}
