# -*- coding: utf-8 -*-
"""
Created on Tue May 26 16:57:04 2015

@author: mpjiang
"""

import numpy as np

team_city = 'Phoenix'

droughts_season_away = np.hstack(df.droughts_away[df.team_away==team_city].values)
droughts_season_home = np.hstack(df.droughts_home[df.team_home==team_city].values)

droughts_season_away_avg = np.mean(droughts_season_away[np.nonzero(droughts_season_away)])
droughts_season_home_avg = np.mean(droughts_season_home[np.nonzero(droughts_season_home)])
droughts_season_away_sd = np.std(droughts_season_away[np.nonzero(droughts_season_away)])
droughts_season_home_sd = np.std(droughts_season_home[np.nonzero(droughts_season_home)])