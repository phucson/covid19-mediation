import pandas as pd
import numpy as np

import sklearn as sk

from matplotlib import pyplot as plt
import seaborn as sns

from datetime import datetime as dt
"""
Load data
"""
path = './data/'

mobility_filename = 'Global_Mobility_Report.csv'
confirmed_filename = 'time_series_covid19_confirmed_global.csv'

mob = pd.read_csv(path+mobility_filename)
con = pd.read_csv(path+confirmed_filename)

"""
Constants
"""
med_cols = mob.columns[-7:]
code_example = 'BE-BRU' # an example of country_region_codes: Belgium-Brussel
country_ex = "Belgium"
med_short = ['date','retail','grocery','parks','transit','workplaces','residential']
"""
Functions
"""
def create_join_data(country='United Kingdom', mobility=mob, confirmed=con):
    """
    create a join datasets from mobility and confirmed cases
    Return:
        a dataframe with 6 first columns are mobility and the last column
        is the confirmed cases
    """
    mobil = mobility[mobility['country_region']==country]
    mobil = mobil[mobil['sub_region_1'].isna()]
    mobil = mobil[med_cols]
    mobil.columns = med_short   # shorten the column names
    mobil['date'] = pd.to_datetime(mobil['date'], format='%Y-%m-%d')
    mobil = mobil.set_index('date')

    conf = confirmed[confirmed['Country/Region']==country]
    conf = conf[conf['Province/State'].isna()]
    conf = conf.iloc[:,4:]
    conf = conf.T
    conf.index = pd.to_datetime(conf.index, format='%m/%d/%y', errors='ignore')
    # match the time index
    conf = conf[conf.index >= mobil.index[0]]
    conf = conf[conf.index <= mobil.index[-1]]

    # join 2 dataframe
    join = mobil.merge(conf, left_index=True, right_index=True)

    return join
"""
An example
"""
countries = mob.country_region.unique()
country_region_codes = mob.iso_3166_2_code.unique()

ex = mob[mob['country_region'] == country_ex]
ex = ex[med_cols]


ex.columns = med_short
# confirmed positive case of example country
ex_con = con[con['Country/Region'] == country_ex]
ex_con = ex_con.iloc[:,4:]
ex_con = ex_con.T
ex_con.index = pd.to_datetime(ex_con.index, format="%m/%d/%y", errors='ignore')

# match the timestamp in example 6 factors and the example confirmed positives
ex_con = ex_con[ex_con.index>=ex.index[0]]
ex_con = ex_con[ex_con.index<=ex.index[-1]]
# plot confirmed cases vs one of six factors
plt.figure()
x = ex.index
y1 = ex.iloc[:,0]
y2 = ex_con
plt.plot(x,y1)
plt.plot(x,y2)
plt.show()
# correlations
join = ex.merge(ex_con, left_index=True, right_index=True)

# add shift forward 7 days
shift_step = 7
join_shift = ex.shift(shift_step)
join_shift = join_shift.merge(ex_con, left_index=True, right_index=True)
join_shift = join_shift.iloc[10:,:]

# correlation matrix
join.corr()[23]
join['parks'].diff().plot()
plt.show()
