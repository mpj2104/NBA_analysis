# -*- coding: utf-8 -*-
"""
Created on Thu May 28 23:55:01 2015

@author: mpjiang
"""

from __future__ import division
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
os.chdir('/Users/mpjiang/Python_Learning/NBA_stats/definitions/')
import NBA_streak_finder_defs as NBA_streak

# which database?
os.chdir('/Users/mpjiang/Python_Learning/NBA_stats/data/')
database_name = 'NBA_stats.db'
engine = create_engine('sqlite:///:' + database_name + ':')
table_name = 'NBA_player_basic_info'

# extract player information
player_IDs = np.array(pd.read_sql_query('SELECT PLAYER_ID FROM ' + table_name,engine))
players = np.array(pd.read_sql_query('SELECT PLAYER_NAME FROM ' + table_name,engine))
FGP = np.array(pd.read_sql_query('SELECT FG_PCT FROM ' + table_name,engine))
FGP3 = np.array(pd.read_sql_query('SELECT FG3_PCT FROM ' + table_name,engine))

# define parameters
min_shot_dist = 15 # in feet

# loop through all players and find streaks
counter = 0
uniq_IDs = np.unique(player_IDs)
for idx,ID in enumerate(uniq_IDs):
    try:
        temp_shot_table = 'NBA_player_shotlogs'
        shot_data = pd.read_sql_query('SELECT * FROM ' + temp_shot_table + ' WHERE ' + temp_shot_table + '.PLAYER_ID = ' + str(ID),engine)
    except:
        continue # skip to the next loop iteration if the shot data doesn't exist
    
    game_IDs = np.array(shot_data.GAME_ID.unique())
    player = players[np.where(player_IDs==ID)[0][0]][0]        
    FGP_temp = FGP[np.where(player_IDs==ID)[:]].tolist()
    FGP3_temp = FGP3[np.where(player_IDs==ID)[:]].tolist()
    print(player)
    (streaks_data,details) = NBA_streak.find_consecutive_shots(ID,game_IDs,shot_data,min_shot_dist)
    if streaks_data.empty:
        continue
    else:
        if counter == 0:
            streak_log = streaks_data
            streak_details = details
            stats_log = NBA_streak.calc_basic_streak_nums(streaks_data,details,ID,player,FGP_temp,FGP3_temp)
            counter = counter + 1
        else:
            streak_log = pd.concat((streak_log,streaks_data))
            streak_details = pd.concat((streak_details,details))
            stats_log = pd.concat((stats_log,NBA_streak.calc_basic_streak_nums(streaks_data,details,ID,player,FGP_temp,FGP3_temp)))