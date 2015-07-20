# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 18:11:39 2015

@author: mpjiang
"""

from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import scipy.spatial as spatial
import os

### create a cursor class
# establish cursor functions for identifying scatter points
def fmt(x, y):
    return 'x: {x:0.2f}\ny: {y:0.2f}'.format(x=x, y=y)

class FollowDotCursor(object):
    """Display the x,y location of the nearest data point."""
    def __init__(self, ax, x, y, specific_players, tolerance=5, formatter=fmt, offsets=(-20, 20)):
        try:
            x = np.asarray(x, dtype='float')
        except (TypeError, ValueError):
            x = np.asarray(mdates.date2num(x), dtype='float')
        y = np.asarray(y, dtype='float')
        self._points = np.column_stack((x, y))
        #self._players = np.column_stack(specific_players)
        self.offsets = offsets
        self.scale = x.ptp()
        self.scale = y.ptp() / self.scale if self.scale else 1
        self.tree = spatial.cKDTree(self.scaled(self._points))
        self.formatter = formatter
        self.tolerance = tolerance
        self.ax = ax
        self.fig = ax.figure
        self.ax.xaxis.set_label_position('bottom')
        self.dot = ax.scatter(
            [x.min()], [y.min()], s=130, color='green', alpha=0.7)
        self.annotation = self.setup_annotation()
        plt.connect('button_press_event', self)

    def scaled(self, points):
        points = np.asarray(points)
        return points * (self.scale, 1)

    def __call__(self, event):
        ax = self.ax
        # event.inaxes is always the current axis. If you use twinx, ax could be
        # a different axis.
        if event.inaxes == ax:
            x, y = event.xdata, event.ydata
        elif event.inaxes is None:
            return
        else:
            inv = ax.transData.inverted()
            x, y = inv.transform([(event.x, event.y)]).ravel()
        annotation = self.annotation
        x, y = self.snap(x, y, specific_players)
        annotation.xy = x, y
        annotation.set_text(self.formatter(x, y))
        self.dot.set_offsets((x, y))
        bbox = ax.viewLim
        event.canvas.draw()

    def setup_annotation(self):
        """Draw and hide the annotation box."""
        annotation = self.ax.annotate(
            '', xy=(0, 0), ha = 'right',
            xytext = self.offsets, textcoords = 'offset points', va = 'bottom',
            bbox = dict(
                boxstyle='round,pad=0.5', fc='yellow', alpha=0.75),
            arrowprops = dict(
                arrowstyle='->', connectionstyle='arc3,rad=0'))
        return annotation

    def snap(self, x, y, specific_players):
        """Return the value in self.tree closest to x, y."""
        dist, idx = self.tree.query(self.scaled((x, y)), k=1, p=1)
        selected_player = specific_players[idx]
        temp = []
        try:
            temp.append(selected_player)
            print(temp[-1])
            return self._points[idx]
            #return self._players[idx]
        except IndexError:
            # IndexError: index out of bounds
            return self._points[0]

### taken from Udacity Machine Learning k_means_clusters.py
#def Draw(pred, features, name="image.png", f1_name="feature 1", f2_name="feature 2"):
def Draw(pred, features, specific_players, f1_name="feature 1", f2_name="feature 2"):
    """ some plotting code designed to help you visualize your clusters """
    
    ### plot each cluster with a different color--add more colors for
    ### drawing more than 4 clusters
    fig = plt.figure(5);plt.clf()
    ax = fig.add_subplot(1, 1, 1)    
    colors = ["b", "c", "k", "m", "g"]
    for ii, pp in enumerate(pred):
        ax.scatter(features[ii][0], features[ii][1], color = colors[pred[ii]], s=60)
    
    ### insert cursor
    #FollowDotCursor(ax, select_data[:,0], select_data[:,1], specific_players)    
    
    ### set axes properties
    ymin = 15
    ymax = 100
    xmin = 32
    xmax = 48
    ax.set_xlabel(f1_name)
    ax.set_xlim([xmin,xmax])
    ax.set_ylabel(f2_name)
    ax.set_ylim([ymin,ymax])
    ax.set_title('NBA 2013-14 and 2014-15 Seasons Total Streak Stats Clusters' + '\n' + '(80th Percentile of Total Streaks)')
  
    ### clustering information
    textstr = 'k-means clustering' + '\n' + 'features:' + '\n' '- Total # of Streaks' + '\n' + \
        '- FGP ( > 15 feet)' + '\n' + '- Pctg of Made Streaks'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(.79, .515, textstr, transform=ax.transAxes, verticalalignment='top', bbox=props)
  
    ### plot leaguewide statistics
    plt.plot((35.8, 35.8), (ymin, ymax), 'k-')
    ax.text(35.9, 91, 'league' + '\n' + 'average', color = 'k')
    plt.plot((35.2+5.7, 35.2+5.7), (ymin, ymax), 'r-')
    ax.text(40.1, 91.5, r'+1$\sigma$', color = 'r')
    #plt.savefig(name)
    plt.grid()
    plt.show()


### extract select streaks_stats
os.chdir('/Users/mpjiang/Python_Learning/NBA_stats/data/')
database_name = 'NBA_stats.db'
engine = create_engine('sqlite:///:' + database_name + ':')
table_name = 'NBA_player_streakstats'

streak_stats = pd.read_sql_query('SELECT * ' + \
                                 'FROM ' + table_name + ' ' + \
                                 'WHERE total_streaks >= 24',engine)


### choose input features
feature_1 = 'season_tot_FGP_15ft'
feature_2 = 'total_streaks'
feature_3 = 'pct_made_streaks'
features_list = [feature_1, feature_2, feature_3]
#features_list = [feature_1, feature_2]
select_data = np.zeros(shape=(len(streak_stats),len(features_list)))
for idx,feature in enumerate(features_list):
    select_data[:,idx] = streak_stats[feature]
# specific to season_tot_FGP_15ft
select_data[:,0] = 100*select_data[:,0]

### scale features
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
rescaled_data = scaler.fit_transform(select_data)

### start clustering
from sklearn.cluster import KMeans
num_clusters = 5
clf = KMeans(n_clusters=num_clusters,n_init=30,max_iter=500)
pred = clf.fit_predict( rescaled_data )
specific_players = streak_stats.player_name.tolist()

### visualize clusters and save
Draw(pred, select_data, specific_players, f1_name='FIELD GOAL PERCENTAGE ( > 15 FEET) (%)', f2_name='TOTAL NUMBER OF STREAKS')

streak_clusters = {}
for ii in range(0,num_clusters):
    cluster_name = 'cluster' + str(ii)
    streak_clusters[cluster_name] = {}
    streak_clusters[cluster_name]['player_names']=np.array(specific_players)[pred==ii]
    streak_clusters[cluster_name]['player_idxs']=np.array(np.where(pred==ii))
    streak_clusters[cluster_name]['avg_total_streaks']=np.mean(select_data[np.array(np.where(pred==ii)),1])
    streak_clusters[cluster_name]['avg_FGP_15ft']=np.mean(select_data[np.array(np.where(pred==ii)),0])
    streak_clusters[cluster_name]['avg_pct_made_streaks']=np.mean(select_data[np.array(np.where(pred==ii)),2])

### calculate more cluster-specific stats
for ii in range(0,len(streak_clusters)):
    cluster_name = 'cluster' + str(ii)
    avg_def_dist_made = []
    avg_def_dist_miss = []
    avg_def_dist_diff = []
    avg_elapsed_time_made = []
    avg_elapsed_time_miss = []
    avg_elapsed_time_diff = []
    avg_num_dribbles_made = []
    avg_num_dribbles_miss = []
    avg_num_dribbles_diff = []
    avg_shot_dist_made = []
    avg_shot_dist_miss = []
    avg_shot_dist_diff = []
    avg_streak_length_made = []
    avg_streak_length_miss = []
    avg_streak_length_diff = []
    avg_touch_time_made = []
    avg_touch_time_miss = []
    avg_touch_time_diff = []
    avg_num_games_multi_streaks = []
    for player in streak_clusters[cluster_name]['player_names']:
        avg_def_dist_made.append(np.array(streak_stats['avg_def_dist_made'][streak_stats.player_name==player]))
        avg_def_dist_miss.append(np.array(streak_stats['avg_def_dist_miss'][streak_stats.player_name==player]))
        avg_def_dist_diff.append(avg_def_dist_made[-1]-avg_def_dist_miss[-1])
        avg_elapsed_time_made.append(np.array(streak_stats['avg_elapsed_time_made'][streak_stats.player_name==player]))
        avg_elapsed_time_miss.append(np.array(streak_stats['avg_elapsed_time_miss'][streak_stats.player_name==player]))
        avg_elapsed_time_diff.append(avg_elapsed_time_made[-1]-avg_elapsed_time_miss[-1])
        avg_num_dribbles_made.append(np.array(streak_stats['avg_num_dribbles_made'][streak_stats.player_name==player]))
        avg_num_dribbles_miss.append(np.array(streak_stats['avg_num_dribbles_miss'][streak_stats.player_name==player]))
        avg_num_dribbles_diff.append(avg_num_dribbles_made[-1]-avg_num_dribbles_miss[-1])
        avg_shot_dist_made.append(np.array(streak_stats['avg_shot_dist_made'][streak_stats.player_name==player]))
        avg_shot_dist_miss.append(np.array(streak_stats['avg_shot_dist_miss'][streak_stats.player_name==player]))
        avg_shot_dist_diff.append(avg_shot_dist_made[-1]-avg_shot_dist_miss[-1])
        avg_streak_length_made.append(np.array(streak_stats['avg_streak_length_made'][streak_stats.player_name==player]))
        avg_streak_length_miss.append(np.array(streak_stats['avg_streak_length_miss'][streak_stats.player_name==player]))
        avg_streak_length_diff.append(avg_streak_length_made[-1]-avg_streak_length_miss[-1])
        avg_touch_time_made.append(np.array(streak_stats['avg_touch_time_made'][streak_stats.player_name==player]))
        avg_touch_time_miss.append(np.array(streak_stats['avg_touch_time_miss'][streak_stats.player_name==player]))
        avg_touch_time_diff.append(avg_touch_time_made[-1]-avg_touch_time_miss[-1])
        avg_num_games_multi_streaks.append(np.array(streak_stats['num_games_multi_streaks'][streak_stats.player_name==player]))
    streak_clusters[cluster_name]['avg_def_dist_made']=np.mean(avg_def_dist_made)
    streak_clusters[cluster_name]['avg_def_dist_miss']=np.mean(avg_def_dist_miss)
    streak_clusters[cluster_name]['avg_def_dist_diff']=np.mean(avg_def_dist_diff)
    streak_clusters[cluster_name]['avg_elapsed_time_made']=np.mean(avg_elapsed_time_made)
    streak_clusters[cluster_name]['avg_elapsed_time_miss']=np.mean(avg_elapsed_time_miss)
    streak_clusters[cluster_name]['avg_elapsed_time_diff']=np.mean(avg_elapsed_time_diff)
    streak_clusters[cluster_name]['avg_num_dribbles_made']=np.mean(avg_num_dribbles_made)
    streak_clusters[cluster_name]['avg_num_dribbles_miss']=np.mean(avg_num_dribbles_miss)
    streak_clusters[cluster_name]['avg_num_dribbles_diff']=np.mean(avg_num_dribbles_diff)
    streak_clusters[cluster_name]['avg_shot_dist_made']=np.mean(avg_shot_dist_made)
    streak_clusters[cluster_name]['avg_shot_dist_miss']=np.mean(avg_shot_dist_miss)
    streak_clusters[cluster_name]['avg_shot_dist_diff']=np.mean(avg_shot_dist_diff)
    streak_clusters[cluster_name]['avg_streak_length_made']=np.mean(avg_streak_length_made)
    streak_clusters[cluster_name]['avg_streak_length_miss']=np.mean(avg_streak_length_miss)
    streak_clusters[cluster_name]['avg_streak_length_diff']=np.mean(avg_streak_length_diff)
    streak_clusters[cluster_name]['avg_touch_time_made']=np.mean(avg_touch_time_made)
    streak_clusters[cluster_name]['avg_touch_time_miss']=np.mean(avg_touch_time_miss)
    streak_clusters[cluster_name]['avg_touch_time_diff']=np.mean(avg_touch_time_diff)
    streak_clusters[cluster_name]['avg_num_games_multi_streaks']=np.mean(avg_num_games_multi_streaks)
        