# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:36:35 2023

@author: nkgar
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

epoch_file = "C:/Users/nkgar/NC State PB&G Dropbox/Nick Garrity/mrcnn_train_files/epoch_loss.csv"
val_file = "C:/Users/nkgar/NC State PB&G Dropbox/Nick Garrity/mrcnn_train_files/val_loss.csv"


epoch = pd.read_csv(epoch_file)
val = pd.read_csv(val_file)
val["style"] = "Validation"
epoch["style"] = "Epoch"
merged = pd.concat([val, epoch])


l = [*range(30,52,1)]
later = merged[merged['Step'].isin(l)] 

both = (merged, later)

fig, (ax1, ax2) = plt.subplots(1,2, layout = 'constrained', sharey=False)
ax1 = sns.lineplot(data = merged, x = "Step", y = "Value", hue = "style", ax = ax1)
ax1.set_xlabel('Steps')
ax1.set_ylabel('Loss')
ax1.get_legend().remove()

ax2 = sns.lineplot(data = later, x = "Step", y = "Value", hue = "style", ax = ax2)
ax2.set_xlabel('Steps')
ax2.set_ylabel('Loss')
ax2.get_legend().remove()
handles, labels = ax2.get_legend_handles_labels()

fig.legend(handles, labels, loc = 'upper right', ncol = 2, bbox_to_anchor = (0.7,0.9))
fig.suptitle('Loss over epochs during MRCNN training', fontsize = 16)









fig, axes = plt.subplots(1, 2)
counter = 0
for i in both:
    
    ax = sns.lineplot(data = i, x = "Step", y = "Value", hue = "style", ax = axes[counter])
    ax.get_legend().remove()
    counter += 1
    

handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc = 'upper right', ncol = 2, bbox_to_anchor = (0.7,0.9))

fig.suptitle("Validation and Training Loss During MRCNN Training")
plt.show()


#first seaborn attempts - goodish
sns.set(style='whitegrid')
fig, ax = plt.subplots()
lossplot = sns.lineplot(data = merged, y = "Value", x = "Step", hue = "style", ax = ax).set(
    title = "Validation and Epoch Loss over 50 MRCNN Training Epochs", xlabel = "Steps",
    ylabel = "Loss").legend_.set_title(None)


lossplot.legend(bbox_to_anchor = (10.2,1))
plt.setp(lossplot.get_legend().get_texts(), fontsize = '15')
plt.show()


lossplot = sns.lineplot(data = later, y = "Value", x = "Step", hue = "style").set(
    title = "Validation and Epoch Loss over 50 MRCNN Training Epochs", xlabel = "Steps", ylabel = "Loss")