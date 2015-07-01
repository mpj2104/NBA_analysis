# -*- coding: utf-8 -*-
"""
Created on Thu May 21 18:17:53 2015

@author: mpjiang
"""

import matplotlib.pyplot as plt
import numpy as np

# Show per game drought average over entire season
fig = plt.figure(1);plt.clf()
ax = fig.add_subplot(1, 1, 1)
team_city = 'Phoenix'
ax.plot(df.game_no[df.team_away==team_city].values, df.avg_drought_away[df.team_away==team_city].values,c='b',marker = 'o',label = 'AWAY')
ax.plot(df.game_no[df.team_home==team_city].values, df.avg_drought_home[df.team_home==team_city].values,c='r',marker = 'o',label = 'HOME')
ax.set_xlabel('Game Number')
ax.set_ylabel('Average Drought (seconds)')
#ax.set_ylim([min(avg_droughts)-5,max(avg_droughts)+5])
ax.set_title(season + ' ' + team + ' Average Scoring Drought')
plt.legend(loc='upper left')
plt.grid()
plt.show()


# Show single game points flow
game_idx = 8
game_curr = df.loc[game_idx]
fig = plt.figure(2);plt.clf()
ax = fig.add_subplot(1, 1, 1)
ax.plot(game_curr.time_scored_away, game_curr.score_running_away,c='b',marker = 's',label = game_curr.team_away + ' (away)')
ax.plot(game_curr.time_scored_home, game_curr.score_running_home,c='r',marker = 'o',label = game_curr.team_home + ' (home)')
# Marks quarters
plt.plot((720, 720), (0, max(game_curr.score_final)), 'k-')
plt.plot((1440, 1440), (0, max(game_curr.score_final)), 'k-')
plt.plot((2160, 2160), (0, max(game_curr.score_final)), 'k-')
plt.plot((2880, 2880), (0, max(game_curr.score_final)), 'k-')
plt.plot((3180, 3180), (0, max(game_curr.score_final)), 'k-')
plt.plot((3480, 3480), (0, max(game_curr.score_final)), 'k-')
plt.plot((3780, 3780), (0, max(game_curr.score_final)), 'k-')
plt.plot((4080, 4080), (0, max(game_curr.score_final)), 'k-')
ax.set_xlabel('Gametime Elapsed (seconds)')
ax.set_ylabel('Running Score (points)')
ax.set_xlim([0,max(game_curr.time_scored_home + game_curr.time_scored_away)])
ax.set_ylim([0,max(game_curr.score_final)])
ax.set_title(game_curr.team_away + ' at ' + game_curr.team_home + ' (' + str(int(game_curr.game_mon)) + '/' + str(int(game_curr.game_day)) + '/' + str(int(game_curr.game_yr)) + ')')
textstr = game_curr.team_away + ' drought (sec): avg = ' + str(np.round(game_curr.avg_drought_away,decimals=1)) + ', sd = ' + \
    str(np.round(game_curr.sd_drought_away,decimals=1)) + '\n' + game_curr.team_home + ' drought (sec): avg = ' + \
    str(np.round(game_curr.avg_drought_home,decimals=1)) + ', sd = ' + str(np.round(game_curr.sd_drought_home,decimals=1))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, verticalalignment='top', bbox=props)
plt.legend(loc='lower right')
plt.grid()
plt.show()


# Show single game droughts distribution histogram
game_idx = 8
game_curr = df.loc[game_idx]
fig = plt.figure(3);plt.clf()
ax = fig.add_subplot(1, 1, 1)
ax.hist(game_curr.droughts_away,25,lw=1,fc = (0,0,1,0.6),label = game_curr.team_away + ' (away)')
ax.hist(game_curr.droughts_home,25,lw=1,fc = (1,0,0,0.6),label = game_curr.team_home + ' (home)')
#ax.set_ylim([min(avg_droughts)-5,max(avg_droughts)+5])
ax.set_xlabel('Drought Times (seconds)')
ax.set_ylabel('Number of Droughts')
ax.set_title(game_curr.team_away + ' at ' + game_curr.team_home + ' (' + str(int(game_curr.game_mon)) + '/' + str(int(game_curr.game_day)) + '/' + str(int(game_curr.game_yr)) + ')')
plt.legend(loc='upper right')
plt.grid()
plt.show()


# Show full season droughts distribution histogram
fig = plt.figure(4);plt.clf()
ax = fig.add_subplot(1, 1, 1)
ax.hist(droughts_season_away,150,lw=1,fc = (0,0,1,0.4),label = 'AWAY')
ax.hist(droughts_season_home,150,lw=1,fc = (1,0,0,0.4),label = 'HOME')
ax.set_xlabel('Drought Times (seconds)')
ax.set_ylabel('Number of Droughts')
ax.set_title(season + ' ' + team + ' Scoring Drought Distribution')
textstr = 'AWAY drought (sec): avg = ' + str(np.round(droughts_season_away_avg,decimals=1)) + ', sd = ' + \
    str(np.round(droughts_season_away_sd,decimals=1)) + '\n' + 'HOME drought (sec): avg = ' + \
    str(np.round(droughts_season_home_avg,decimals=1)) + ', sd = ' + str(np.round(droughts_season_home_sd,decimals=1))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.2, 0.95, textstr, transform=ax.transAxes, verticalalignment='top', bbox=props)
plt.legend(loc='upper right')
plt.grid()
plt.show()





running_score_away.insert(0,0)
running_score_home.insert(0,0)
time_scored_away.insert(0,0)
time_scored_home.insert(0,0)
running_score_away_btwn = np.array(running_score_away[:-1])+np.diff(running_score_away)/2.
running_score_home_btwn = np.array(running_score_home[:-1])+np.diff(running_score_home)/2.
time_scored_away_btwn = np.array(time_scored_away[:-1])+np.diff(time_scored_away)/2.
time_scored_home_btwn = np.array(time_scored_home[:-1])+np.diff(time_scored_home)/2.
running_score_away.remove(0)
running_score_home.remove(0)
time_scored_away.remove(0)
time_scored_home.remove(0)
droughts_away_net = droughts_away-avg_drought_away
droughts_home_net = droughts_home-avg_drought_home
    
fig = plt.figure(3);plt.clf()
#fig.set_size_inches(14.6,5.0)
ax = fig.add_subplot(1, 1, 1)
#ax.plot(time_scored_away, droughts_away,'-r',marker = 's',label = team_away + ' (away)')
#ax.plot(time_scored_home, droughts_home,'-b',marker = 'o',label = team_home + ' (home)')
#ax.plot(time_scored_away, running_score_away,c='r',marker = 's',label = team_away + ' (away)')
ax.scatter(time_scored_away_btwn,running_score_away_btwn,c=-droughts_away_net,s=abs(droughts_away_net),marker = 's',label = team_away + ' (away)')
#ax.plot(time_scored_home, running_score_home,c='b',marker = 'o',label = team_home + ' (home)')
ax.scatter(time_scored_home_btwn,running_score_home_btwn,c=-droughts_home_net,s=abs(droughts_home_net),marker = 'o',label = team_home + ' (home)')
#ax.scatter(time_scored_away,droughts_away_net,s=abs(droughts_away_net),marker = 's')
#ax.scatter(time_scored_home,droughts_home_net,c=-droughts_home_net,s=abs(droughts_home_net))
# Marks quarters
plt.plot((720, 720), (0, max(score)), 'k-')
plt.plot((1440, 1440), (0, max(score)), 'k-')
plt.plot((2160, 2160), (0, max(score)), 'k-')
plt.plot((2880, 2880), (0, max(score)), 'k-')
ax.set_xlabel('Gametime Elapsed (seconds)')
#ax.set_ylabel('Gametime Elapsed between Scoring Events (seconds)')
ax.set_ylabel('Running Score (points)')
ax.set_xlim([0,2880])
ax.set_ylim([0,max(score)])
ax.set_title(team_away + ' at ' + team_home + ' (' + game_month + '/' + game_day + '/' + game_year + ')')
textstr = team_away + ' drought (sec): avg = ' + str(np.round(avg_drought_away,decimals=1)) + ', sd = ' + \
    str(np.round(sd_drought_away,decimals=1)) + '\n' + team_home + ' drought (sec): avg = ' + \
    str(np.round(avg_drought_home,decimals=1)) + ', sd = ' + str(np.round(sd_drought_home,decimals=1))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, verticalalignment='top', bbox=props)
plt.legend(loc='lower right')
plt.grid()
plt.show()