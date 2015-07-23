# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 16:24:22 2015

@author: mpjiang
"""

from __future__ import division
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
import pickle

def load_NBA_streaks_data(streak_cutoff):
    
    ### which database?
    os.chdir('/Users/mpjiang/Python_Learning/NBA_stats/data/')
    database_name = 'NBA_stats.db'
    engine = create_engine('sqlite:///:' + database_name + ':')
    table_name = 'NBA_player_streakstats'

    ### extract select streak stats
    streak_stats = pd.read_sql_query('SELECT * ' + \
                                     'FROM ' + table_name + ' ' + \
                                     'WHERE total_streaks >= ' + str(streak_cutoff),engine)

    ### load player names ordered by total streaks
    specific_players = streak_stats.player_name.tolist()
                               
    ### load cluster information
    streak_clusters = pickle.load( open( "NBA_2013-15_streak-clusters.p", "rb" ) )
    #pickle.dump( streak_clusters, open( "NBA_2013-15_streak-clusters.p", "wb" ) )
    
    return (streak_stats,specific_players,streak_clusters)