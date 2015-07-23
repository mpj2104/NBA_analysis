# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:50:31 2015

@author: mpjiang
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as spatial
import scipy.stats as stats
import os
os.chdir('/Users/mpjiang/Python_Learning/NBA_stats/analysis/')
from NBA_streak_analysis import load_NBA_streaks_data

### Load data (argument is streak cutoff number)
(streak_stats,specific_players,streak_clusters) = load_NBA_streaks_data(24)

### Which clusters to compare?
select_cluster_ID = [2,4]

### Which statistic to compare?
select_feature = 'season_tot_FGP_15ft'

### Extract arrays of this feature from select clusters
feature_arrays = {}
for cluster in select_cluster_ID:
    cluster_name = 'cluster' + str(cluster)
    feature_arrays[cluster_name] = {}
    temp_array = []
    for player in streak_clusters[cluster_name]['player_names']:
        temp_array.append(np.array(streak_stats[select_feature][streak_stats.player_name==player]).tolist())
    feature_arrays[cluster_name] = np.array(temp_array)

### Performs statistical test
for cluster in select_cluster_ID:
    print('cluster' + str(cluster) + ' ' + select_feature + ' mean is ' + str(np.mean(feature_arrays['cluster' + str(cluster)])))
    print('cluster' + str(cluster) + ' ' + select_feature + ' variance is ' + str(np.var(feature_arrays['cluster' + str(cluster)])))

(t,p) = stats.ttest_ind(feature_arrays['cluster'+str(select_cluster_ID[0])],feature_arrays['cluster'+str(select_cluster_ID[1])],equal_var=False)

print('two-tailed t-test result: t = ' + str(t[0]) + ', p = ' + str(p[0]))