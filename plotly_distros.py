# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 08:11:50 2023

@author: nkgar
"""
import pandas as pd

#Import qsorter files
datafiles = ["./raw_data/21-L-2161.jpg.csv",
             "./raw_data/22-L-1072.jpg.csv",
             "./raw_data/21-R-1030.jpg.csv"]



store = {}


for i in datafiles:
    test = pd.read_csv(i)
    store[i] = test['el_width']

import plotly.figure_factory as ff

hist_data = [store[datafiles[0]].tolist(), store[datafiles[1]].tolist(), store[datafiles[2]].tolist()]
group_labels = ['Small','Medium','Large'] # name of the dataset
colors = ['Black','DarkGrey', 'Red']

# mean = np.mean(hist_data)
# stdev_pluss = np.std(hist_data)
# stdev_minus = np.std(hist_data)*-1

fig = ff.create_distplot(hist_data, group_labels, show_hist=False, curve_type='kde', colors=colors)

# Add shape regions


fig.add_vrect(
    x0="7", x1="13.5",
    fillcolor="Gold", opacity=0.3,
    layer="below", line_width=0,
)

fig.add_vrect(
    x0="13.5", x1="15.1",
    fillcolor="LightSalmon", opacity=0.3,
    layer="below", line_width=0,
)

fig.add_vrect(
    x0="15.1", x1="23",
    fillcolor="OrangeRed", opacity=0.3,
    layer="below", line_width=0,
)



fig.update_layout(
    plot_bgcolor='white', legend_traceorder='reversed', title = "Small, Medium and Large Pod Distributions"
)
fig.update_xaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='whitesmoke'
)
fig.update_yaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='whitesmoke')

fig.show()