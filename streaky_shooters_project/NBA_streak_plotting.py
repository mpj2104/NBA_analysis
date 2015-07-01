# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:36:53 2015

@author: mpjiang
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import scipy.spatial as spatial
#import scipy.stats.pearsonr

specific_players = streak_stats.player_name.tolist()

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

# Show player total streaks distribution histogram
fig = plt.figure(1);plt.clf()
ax = fig.add_subplot(1, 1, 1)
#total_streaks = np.array(streak_stats.total_streaks)
#total_streaks = total_streaks[np.nonzero(total_streaks)]
#ax.hist(total_streaks,60,lw=1,fc = (0,0,1,0.6))
ax.hist(streak_stats.total_streaks,70,lw=1,fc = (0,0,1,0.6))
plt.plot((20, 20), (0, 35), 'r-')
ax.set_ylim([0, 35])
ax.set_xlabel('NUMBER OF STREAKS')
ax.set_ylabel('NUMBER OF PLAYERS')
ax.set_title('NBA 2013-14 and 2014-15 Total Streak Distribution')
ax.text(21, 27, '75th percentile' + '\n' + '        cutoff', color = 'r')
plt.grid()
plt.show()

fig.savefig('NBA_total-streaks_dist_zoomed.png', format='png', dpi=1200)

# Show bar chart of individual player streak information
fig = plt.figure(2);plt.clf()
ax = fig.add_subplot(1, 1, 1)
max_count = 20 # look at top [#] of players by number of streaks
width = 0.5
# select list of players based on descending number of total streaks
xx_temp = np.array(specific_players)[np.array(np.argsort(streak_stats.total_streaks,1)[::-1])]
xx_temp = xx_temp[0:max_count]
xx = []
[xx.append(str(a)) for a in xx_temp]
del xx_temp
x = range(0,max_count*2,2)
# select numbers of made streaks and missed streaks from these top [#] of players
yy_made = np.array(streak_stats.num_made_streaks[np.argsort(streak_stats.total_streaks,1)[::-1]])
yy_miss = np.array(streak_stats.num_miss_streaks[np.argsort(streak_stats.total_streaks,1)[::-1]])
yy_made = yy_made[0:max_count]
yy_miss = yy_miss[0:max_count]
# make bar chart
made_bar = ax.bar(x, yy_made, width, color='b', label='make streak')
miss_bar = ax.bar([a+width for a in x], yy_miss, width, color='r', label='miss streak')
ax.set_xlabel('PLAYER')
#ax.set_xlim([0,40])
ax.set_xticks(x)
ax.set_xticklabels((xx), rotation=75)
ax.set_ylabel('NUMBER OF STREAKS')
ax.set_title('NBA 2013-14 and 2014-15 Seasons Total Streaks (Top 20)')
#plt.grid()
plt.show()
plt.legend(loc='upper right')
plt.gcf().subplots_adjust(bottom=0.25)

fig.savefig('myimage.png', format='png', dpi=1200)


# Show bar chart of make streak percentage
fig = plt.figure(3);plt.clf()
ax = fig.add_subplot(1, 1, 1)
width = 0.57
max_count = 20 # look at top [#] of players by number of streaks
# select list of players based on descending number of total streaks
xx_temp = np.array(specific_players)[np.array(np.argsort(streak_stats.pct_made_streaks,1)[::-1])]
xx_temp = xx_temp[0:max_count]
xx = []
[xx.append(str(a)) for a in xx_temp]
del xx_temp
x = np.linspace(0,20,20)
# select numbers of made streaks and missed streaks from these top [#] of players
yy_make_pct = np.array(streak_stats.pct_made_streaks[np.argsort(streak_stats.pct_made_streaks,1)[::-1]])
yy_make_pct = yy_make_pct[0:max_count]
# make bar chart
made_bar = ax.bar(x, yy_make_pct, width, color=(0,193/256,242/256,1))
ax.set_xlabel('PLAYER')
ax.set_xlim([0,21])
ax.set_xticks(x)
ax.set_xticklabels((xx), rotation=75)
ax.set_ylabel('PERCENTAGE OF MAKE STREAKS (%)')
ax.set_title('NBA 2013-14 and 2014-15 Seasons Make Streak Percentage (Top 20)')
#plt.grid()
plt.show()
plt.gcf().subplots_adjust(bottom=0.3)

fig.savefig('NBA_make-streak-pct_top20_bar.png', format='png', dpi=1200)


# Show num streaks versus FGP
fig = plt.figure(4);plt.clf()
#fig.set_size_inches(12,6)
ax = fig.add_subplot(1, 1, 1)
xx = 100*np.array(streak_stats.season_tot_FGP_15ft)
yy_made = np.array(streak_stats.num_made_streaks)
#yy_miss = np.array(streak_stats.num_miss_streaks)
#ax.scatter(player_FGP,made_streaks,c = (200/256,0/256,0/256,0.75),s=total_streaks,marker = 'o')
#ax.scatter(player_FGP,miss_streaks,c = (0/256,0/256,200/256,0.75),s=total_streaks,marker = '^')
#ax.scatter(xx,yy_made,color=(122/256,20/256,212/256))
sc=ax.scatter(xx,yy_made,c=streak_stats.pct_made_streaks, s=60, cmap = mpl.cm.seismic)
m, b = np.polyfit(xx, yy_made, 1)
xx_fit = np.array(range(32,49))
plt.plot(xx_fit, m*xx_fit + b, '-g')
#ax.scatter(xx,yy_miss,color=(255/256,128/256,16/256))
ymin = 0
ymax = 45
xmin = 32
xmax = 48
#plt.plot((35.2, 35.2), (ymin, ymax), 'k-')
#ax.text(35.4, 41, 'league' + '\n' + 'average', color = 'k')
#plt.plot((35.2+8.8, 35.2+8.8), (ymin, ymax), 'r-')
#ax.text(44.1, 41.5, r'+1$\sigma$', color = 'r')
plt.plot((35.8, 35.8), (ymin, ymax), 'k-')
ax.text(35.9, 41, 'league' + '\n' + 'average', color = 'k')
plt.plot((35.2+5.7, 35.2+5.7), (ymin, ymax), 'r-')
ax.text(40.1, 41.5, r'+1$\sigma$', color = 'r')
#plt.plot((35.2-5.7, 35.2-5.7), (ymin, ymax), 'r-')
#ax.text(40.1, 41.5, r'-1$\sigma$', color = 'r')
#plt.plot((35.2-8.8, 35.2-8.8), (ymin, ymax), 'r-')
ax.set_xlabel('FIELD GOAL PERCENTAGE ( > 15 FEET) (%)')
ax.set_xlim([xmin,xmax])
ax.set_ylabel('TOTAL NUMBER OF MAKE STREAKS')
ax.set_ylim([ymin,ymax])
#ax.text(25.25, 95, r'-1$\sigma$', color = 'r')
cbr=plt.colorbar(sc)
cbr.set_label('PERCENTAGE OF MAKE STREAKS (%)')
ax.set_title('NBA 2013-14 and 2014-15 Seasons Make Streak Stats vs. FGP' + '\n' + '(75th Percentile of Total Streaks)')
#ax.set_title('20' + season[0:2] + '-' + season[3:5] + ' Number of Streaks: "made" vs. FGP')
cursor = FollowDotCursor(ax, xx, yy_made, specific_players)
plt.grid()
plt.show()

fig.savefig('NBA_make-streak-stats_vs_FGP.png', format='png', dpi=1200)

# Show streak length versus number of made streaks
fig = plt.figure(5);plt.clf()
#fig.set_size_inches(12,6)
ax = fig.add_subplot(1, 1, 1)
xx = np.array(streak_stats.num_made_streaks)
yy_made = np.array(streak_stats.avg_streak_length_made)
sc=ax.scatter(xx,yy_made, s=60, c=streak_stats.pct_made_streaks, cmap = mpl.cm.seismic)
#m, b = np.polyfit(xx, yy_made, 1)
#xx_fit = np.array(range(32,49))
#plt.plot(xx_fit, m*xx_fit + b, '-g')
ymin = 2.9
ymax = 4.1
xmin = 0
xmax = 45
ax.set_xlabel('TOTAL NUMBER OF MAKE STREAKS')
ax.set_xlim([xmin,xmax])
ax.set_ylabel('AVG STREAK LENGTH ON MAKES')
ax.set_ylim([ymin,ymax])
ax.set_title('NBA 2013-14 and 2014-15 Seasons Make Streak Stats vs. FGP' + '\n' + '(75th Percentile of Total Streaks)')
cbr=plt.colorbar(sc)
cbr.set_label('PERCENTAGE OF MAKE STREAKS (%)')
cursor = FollowDotCursor(ax, xx, yy_made, specific_players)
plt.grid()
plt.show()

# Show elapsed time versus number of made streaks
fig = plt.figure(6);plt.clf()
#fig.set_size_inches(12,6)
ax = fig.add_subplot(1, 1, 1)
xx = 100*np.array(streak_stats.season_tot_FGP_15ft)
#yy_made = np.array(streak_stats.avg_elapsed_time_made)
yy_made = np.array(streak_stats.avg_elapsed_time_made)
sc=ax.scatter(xx,yy_made, s=60, c=streak_stats.pct_made_streaks, cmap = mpl.cm.seismic)
m, b = np.polyfit(xx, yy_made, 1)
xx_fit = np.array(range(32,49))
plt.plot(xx_fit, m*xx_fit + b, '-g')
ymin = 100
ymax = 500
xmin = 32
xmax = 48
ax.set_xlabel('FIELD GOAL PERCENTAGE ( > 15 FEET) (%)')
ax.set_xlim([xmin,xmax])
ax.set_ylabel('AVG TIME ELAPSED BTWN MAKES (seconds)')
ax.set_ylim([ymin,ymax])
ax.set_title('NBA 2013-14 and 2014-15 Seasons Elapsed Time in Make Streaks')
plt.plot((35.8, 35.8), (ymin, ymax), 'k-')
ax.text(35.9, 450, 'league' + '\n' + 'average', color = 'k')
plt.plot((35.2+5.7, 35.2+5.7), (ymin, ymax), 'r-')
ax.text(40.25, 450, r'+1$\sigma$', color = 'r')
cbr=plt.colorbar(sc)
cbr.set_label('PERCENTAGE OF MAKE STREAKS (%)')
#cursor = FollowDotCursor(ax, xx, yy_made, specific_players)
plt.grid()
plt.show()

fig.savefig('NBA_elapsed-time-make_vs_FGP.png', format='png', dpi=1200)

# Show average defender distance versus number of made streaks
fig = plt.figure(7);plt.clf()
#fig.set_size_inches(12,6)
ax = fig.add_subplot(1, 1, 1)
#xx = 100*np.array(streak_stats.season_tot_FGP_15ft)
xx = np.array(streak_stats.avg_def_dist_miss)
#yy_made = np.array(streak_stats.avg_elapsed_time_made)
yy_made = np.array(streak_stats.avg_def_dist_made)
sc=ax.scatter(xx,yy_made, s=60,color='black')
m, b = np.polyfit(xx, yy_made, 1)
#xx_fit = np.array(range(32,49))
xx_fit = np.array(range(3,9))
plt.plot(xx_fit, m*xx_fit + b, '-g')
ymin = 3.5
ymax = 7
#xmin = 32
#xmax = 48
xmin = 3.5
xmax = 7
ax.set_xlabel('AVG DEFENDER DISTANCE ON MISS STREAKS (feet)')
ax.set_xlim([xmin,xmax])
ax.set_ylabel('AVG DEFENDER DISTANCE ON MAKE STREAKS (feet)')
ax.set_ylim([ymin,ymax])
ax.set_title('NBA 2013-14 and 2014-15 Defender Distance on Streaks')
ax.fill_between(range(3,8), 3.5, range(3,8), facecolor='yellow', alpha=0.2)
plt.plot((35.8, 35.8), (ymin, ymax), 'k-')
ax.text(35.9, 3.2, 'league' + '\n' + 'average', color = 'k')
plt.plot((35.2+5.7, 35.2+5.7), (ymin, ymax), 'r-')
ax.text(40.1, 3.2, r'+1$\sigma$', color = 'r')
#cbr=plt.colorbar(sc)
#cbr.set_label('FIELD GOAL PERCENTAGE ( > 15 FEET) (%)')
cursor = FollowDotCursor(ax, xx, yy_made, specific_players)
plt.grid()
plt.show()

fig.savefig('NBA_defender_distance_streaks.png', format='png', dpi=1200)

fig = plt.figure(8);plt.clf()
#fig.set_size_inches(12,6)
ax = fig.add_subplot(1, 1, 1)
xx = 100*np.array(streak_stats.season_tot_FGP_15ft)
#xx = np.array(streak_stats.season_tot_FGP_15ft)
#yy_made = np.array(streak_stats.avg_elapsed_time_made)
yy_made = np.array(streak_stats.avg_num_dribbles_made)
sc=ax.scatter(xx,yy_made, s=60,c=streak_stats.pct_made_streaks,cmap = mpl.cm.seismic)
m, b = np.polyfit(xx, yy_made, 1)
#xx_fit = np.array(range(32,49))
#xx_fit = np.array(range(3,9))
plt.plot(range(0,5),range(0,5), '-g')
ymin = 0
ymax = 8
#xmin = 32
#xmax = 48
xmin = 32
xmax = 48
ax.set_xlabel('AVG STREAK LENGTH ON MISS STREAKS (shots)')
ax.set_xlim([xmin,xmax])
ax.set_ylabel('AVG STREAK LENGTH ON MAKE STREAKS (shots)')
ax.set_ylim([ymin,ymax])
ax.set_title('NBA 2013-14 and 2014-15 Length of Streaks')
#ax.fill_between(range(3,8), 3.5, range(3,8), facecolor='yellow', alpha=0.2)
#plt.plot((35.8, 35.8), (ymin, ymax), 'k-')
#ax.text(35.9, 3.2, 'league' + '\n' + 'average', color = 'k')
#plt.plot((35.2+5.7, 35.2+5.7), (ymin, ymax), 'r-')
#ax.text(40.1, 3.2, r'+1$\sigma$', color = 'r')
cbr=plt.colorbar(sc)
cbr.set_label('PERCENTAGE OF MAKE STREAKS (%)')
cursor = FollowDotCursor(ax, xx, yy_made, specific_players)
plt.grid()
plt.show()
