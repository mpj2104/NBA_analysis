# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 22:49:57 2015

@author: mpjiang
"""

from __future__ import division
import numpy as np
from Tkinter import *
import ttk
import scipy.stats as stats
import os
os.chdir('/Users/mpjiang/Python_Learning/NBA_stats/analysis/')
from NBA_load_pickle import load_NBA_streaks_data

def run_test(*args):
    (streak_stats,specific_players,streak_clusters) = load_NBA_streaks_data(24)
    select_cluster_ID = []
    select_cluster_ID.append(clusterA.get())
    select_cluster_ID.append(clusterB.get())
    select_feature = feature.get()
    feature_arrays = {}
    for cluster in select_cluster_ID:
        cluster_name = 'cluster' + str(cluster)
        feature_arrays[cluster_name] = {}
        temp_array = []
        for player in streak_clusters[cluster_name]['player_names']:
            temp_array.append(np.array(streak_stats[select_feature][streak_stats.player_name==player]).tolist())
            feature_arrays[cluster_name] = np.array(temp_array)
    try:
        clusterA_mean.set(np.mean(feature_arrays['cluster' + str(select_cluster_ID[0])]))
        clusterB_mean.set(np.mean(feature_arrays['cluster' + str(select_cluster_ID[1])]))
        (t,p) = stats.ttest_ind(feature_arrays['cluster'+str(select_cluster_ID[0])],feature_arrays['cluster'+str(select_cluster_ID[1])],equal_var=False)
        t_stat.set(t[0])
        p_stat.set(p[0])
        if p[0] <= 0.05:
            result.set('Reject Null Hypothesis (' + u'\u03b1' + ' = 0.05)')
        else:
            result.set('Accept Null Hypothesis (' + u'\u03b1' + ' = 0.05)')
    except ValueError:
        pass
    
root = Tk()
root.title("Two-tailed Welch's t-test Comparison")

mainframe = ttk.Frame(root, padding="5 4 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

clusterA = StringVar()
clusterB = StringVar()
feature = StringVar()
clusterA_mean = StringVar()
clusterB_mean = StringVar()
t_stat = StringVar()
p_stat = StringVar()
result = StringVar()

clusterA_entry = ttk.Entry(mainframe, width=7, textvariable=clusterA)
clusterA_entry.grid(column=2, row=1, sticky=(W, E))
clusterB_entry = ttk.Entry(mainframe, width=7, textvariable=clusterB)
clusterB_entry.grid(column=4, row=1, sticky=(W, E))
feature_entry = ttk.Entry(mainframe, width=14, textvariable=feature)
feature_entry.grid(column=2, row=2, sticky=(W, E))

ttk.Label(mainframe, textvariable=clusterA_mean).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=clusterB_mean).grid(column=4, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=t_stat).grid(column=2, row=4, sticky=(W, E))
ttk.Label(mainframe, textvariable=p_stat).grid(column=4, row=4, sticky=(W, E))
ttk.Label(mainframe, textvariable=result).grid(column=3, row=5, sticky=(W, E))
ttk.Button(mainframe, text="Run Test", command=run_test).grid(column=3, row=2, sticky=W)

ttk.Label(mainframe, text="Cluster A:").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Cluster B:").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Feature:").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Cluster A mean:").grid(column=1, row=3, sticky=E)
ttk.Label(mainframe, text="Cluster B mean:").grid(column=3, row=3, sticky=E)
ttk.Label(mainframe, text="t = ").grid(column=1, row=4, sticky=E)
ttk.Label(mainframe, text="p = ").grid(column=3, row=4, sticky=E)
ttk.Label(mainframe, text="verdict:").grid(column=2, row=5, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#clusterA_entry.focus()
#root.bind('<Return>', calculate)

root.mainloop()