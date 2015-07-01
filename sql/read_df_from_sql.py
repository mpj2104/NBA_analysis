# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 00:13:09 2015

@author: mpjiang
"""

import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import numpy as np
import os

database_name = 'NBA_stats.db'
table_name = 'NBA_player_streakstats'
os.chdir('/Users/mpjiang/Python_Learning/NBA_stats/data/')

engine = create_engine('sqlite:///:NBA_stats.db:')
streak_stats = pd.read_sql_table(table_name,engine,index_col='index')
#player_IDs = np.array(pd.read_sql_query('SELECT PLAYER_ID FROM ' + table_name + ' WHERE season_ID==1415',engine))
#players = np.array(pd.read_sql_query('SELECT PLAYER_NAME FROM ' + table_name + ' WHERE season_ID==1415',engine))