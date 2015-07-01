# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 00:10:47 2015

@author: mpjiang
"""

import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os

database_name = 'NBA_stats.db'
#database_name = 'test.db'
#table_name = 'NBA_player_basic_info_' + season
table_name = 'NBA_player_streakstats'
os.chdir('/Users/mpjiang/Python_Learning/NBA_stats/data/')

engine = create_engine('sqlite:///:' + database_name + ':')
df_streaks.to_sql(table_name,engine,flavor='sqlite',if_exists='replace')