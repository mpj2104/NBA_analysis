# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 12:47:34 2015

@author: mpjiang
"""

import requests
import pandas as pd
import numpy as np

def extract_player_IDs(url):
    resp = requests.get(url)
    resp = requests.get(url)
    resp.raise_for_status() # raise exception if invalid response
    player_data = resp.json()['resultSets'][0]['rowSet'] # collects player data
    col_names = resp.json()['resultSets'][0]['headers'] # gets table headers
    player_data = pd.DataFrame(player_data,columns=col_names) #creates dataframe
    player_IDs = np.array(player_data.PLAYER_ID) # gets player IDs
    
    return (player_IDs,player_data)

    
    
season = '2013-14'
url = 'http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country' + \
      '=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&' + \
      'Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&Opponent' + \
      'TeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&Player' + \
      'Experience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=' + season + \
      '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID' + \
      '=0&VsConference=&VsDivision=&Weight='
(player_IDs,player_data) = extract_player_IDs(url)