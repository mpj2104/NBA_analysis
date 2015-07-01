# -*- coding: utf-8 -*-
"""
Created on Tue May 12 23:47:28 2015

@author: mpjiang
"""

import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_game_urls(team,year):
    url = 'http://www.basketball-reference.com/teams/' + team + '/' + year + '_games.html'
    resp = requests.get(url)
    
    # extracts regular season and playoffs game list
    soup = BeautifulSoup(resp.text,'xml').find('table',class_='sortable  stats_table')
    rows = soup.find_all('tr')
    
    game_urls = []
    
    for row in rows:
        links = row.find_all('a')
        if links == []:
            continue
        else:
            temp_link = re.findall('href\=\"(.*)\"\>',unicode(links[1]))
            if temp_link == []:
                continue
            else:
                game_urls.append('http://www.basketball-reference.com' +  temp_link[0][:11] + 'pbp/' + temp_link[0][11:])
    return game_urls
    
def extract_drought_times(url):
    resp = requests.get(url)

    # extracts only play-by-play data on page
    soup = BeautifulSoup(resp.text,'xml').find('table',class_='no_highlight stats_table')
    rows = soup.find_all('tr')
    cols_names = rows[1].find_all('th')
    team_away = unicode(cols_names[1].string)
    team_home = unicode(cols_names[3].string)

    # start of game parameters
    score = [0,0]
    running_score_away = []
    running_score_home = []
    times_away = []
    times_home = []
    droughts_away = []
    droughts_home = []
    pts_away = []
    pts_home = []
    time_scored_away = []
    time_scored_home = []
    qtr_counter = 0
    last_qtr_scored_away = 0
    last_qtr_scored_home = 0

    for row in rows:
        if row.find('td',class_='align_center') is not None:
            if row.find('td',class_='align_center').string is not None:
                if row.find('td',class_='align_center').string[:5]=='Start':
                    qtr_counter = qtr_counter + 1
        if row.find('td',class_='align_right background_lime') is not None:
            pts_scored = unicode(row.find('td',class_='align_right background_lime').string)
            time = unicode(row.find('td',class_='align_right').string)
            minute = re.findall('(\d*)\:',time)
            seconds = re.findall('\:(.*)',time)
            time = float(minute[0])*60+float(seconds[0])
            if row.find('td',class_='align_center background_white') is not None:
                temp_score = unicode(row.find('td',class_='align_center background_white').string)
            elif row.find('td',class_='align_center background_yellow') is not None:
                temp_score = unicode(row.find('td',class_='align_center background_yellow').string)
            else:
                temp_score = unicode(row.find('td',class_='align_center background_aqua').string)
            temp_away_score = re.findall('(\d*)-',temp_score)
            temp_away_score = int(temp_away_score[0])
            temp_home_score = re.findall('-(\d*)',temp_score)
            temp_home_score = int(temp_home_score[0])
            if temp_away_score != score[0]:
                score[0] = temp_away_score
                if len(times_away) > 0:
                    #if times_away[-1] >= time:
                    if qtr_counter == last_qtr_scored_away:
                        if time == 720:
                            droughts_away.append(times_away[-1]+720.0-time)
                        else:    
                            droughts_away.append(times_away[-1]-time)
                    else:
                        if qtr_counter in (1,2,3,4): 
                            droughts_away.append(times_away[-1]+720.0-time)
                        else:
                            droughts_away.append(times_away[-1]+300.0-time)
                    last_qtr_scored_away = qtr_counter
                    if time == 720:
                        last_qtr_scored_away = qtr_counter+1
                    time_scored_away.append(time_scored_away[-1]+droughts_away[-1])
                else:
                    droughts_away.append(720-time)
                    time_scored_away.append(720-time)
                    last_qtr_scored_away = qtr_counter
                times_away.append(time)
                temp_pts_add = re.findall('\+(\d*)',pts_scored)
                temp_pts_add = int(temp_pts_add[0])
                pts_away.append(temp_pts_add)
                if len(running_score_away) > 0:
                    running_score_away.append(running_score_away[-1]+pts_away[-1])
                else:
                    running_score_away.append(pts_away[-1])
            elif temp_home_score != score[1]:
                score[1] = temp_home_score
                if len(times_home) > 0:
                    #if times_home[-1] >= time:
                    if qtr_counter == last_qtr_scored_home:
                        if time == 720:
                            droughts_home.append(times_home[-1]+720.0-time)
                        else:    
                            droughts_home.append(times_home[-1]-time)
                    else:
                        if qtr_counter in (1,2,3,4): 
                            droughts_home.append(times_home[-1]+720.0-time)
                        else:
                            droughts_home.append(times_home[-1]+300.0-time)
                    last_qtr_scored_home = qtr_counter  
                    if time == 720:
                        last_qtr_scored_home = qtr_counter+1
                    time_scored_home.append(time_scored_home[-1]+droughts_home[-1])
                else:
                    droughts_home.append(720-time)
                    time_scored_home.append(720-time)
                    last_qtr_scored_home = qtr_counter
                times_home.append(time)
                temp_pts_add = re.findall('\+(\d*)',pts_scored)
                temp_pts_add = int(temp_pts_add[0])
                pts_home.append(temp_pts_add)
                if len(running_score_home) > 0:
                    running_score_home.append(running_score_home[-1]+pts_home[-1])
                else:
                    running_score_home.append(pts_home[-1])
        else:
            continue
    return (score,running_score_away,running_score_home,times_away,times_home,droughts_away, \
            droughts_home,pts_away,pts_home,team_away,team_home,time_scored_away,time_scored_home)

def get_drought_stats(droughts_away,droughts_home):
    a = np.array(droughts_away)
    h = np.array(droughts_home)
    avg_drought_away = np.mean(a[np.nonzero(a)])
    avg_drought_home = np.mean(h[np.nonzero(h)])
    sd_drought_away = np.std(a[np.nonzero(a)])
    sd_drought_home = np.std(h[np.nonzero(h)])
    
    return (avg_drought_away,avg_drought_home,sd_drought_away,sd_drought_home)

def get_game_date(url):
    game_date = re.findall('/pbp/(\d*)',url)
    game_year = game_date[0][:4]
    game_month = game_date[0][4:6]
    game_day = game_date[0][6:8]
    
    return (game_year,game_month,game_day)
   


# Choose team and season
team = 'PHO'
season = '2006'

# Extract urls of each play-by-play page for this team/season
game_urls = get_game_urls(team,season)

# Initialize dataframe for each team for a particular season
d = {'game_no':pd.Series(range(1,len(game_urls)+1)),
     'url':pd.Series(game_urls),
     'game_yr':pd.Series(),
     'game_mon':pd.Series(),
     'game_day':pd.Series(),
     'team_away':pd.Series(),
     'team_home':pd.Series(),
     'score_final':pd.Series(dtype=np.dtype("object")),
     'score_running_away':pd.Series(dtype=np.dtype("object")),
     'score_running_home':pd.Series(dtype=np.dtype("object")),
     'pts_away':pd.Series(dtype=np.dtype("object")),
     'pts_home':pd.Series(dtype=np.dtype("object")),
     'droughts_away':pd.Series(dtype=np.dtype("object")),
     'droughts_home':pd.Series(dtype=np.dtype("object")),
     'avg_drought_away':pd.Series(),
     'avg_drought_home':pd.Series(),
     'sd_drought_away':pd.Series(),
     'sd_drought_home':pd.Series(),
     'time_scored_away':pd.Series(dtype=np.dtype("object")),
     'time_scored_home':pd.Series(dtype=np.dtype("object")),
     'times_away':pd.Series(dtype=np.dtype("object")),
     'times_home':pd.Series(dtype=np.dtype("object"))}
df = pd.DataFrame(d)
del d

# Loop through each game and fill up dataframe
for idx, url in enumerate(game_urls):
    (df.score_final[idx],df.score_running_away[idx],df.score_running_home[idx], \
    df.times_away[idx],df.times_home[idx],df.droughts_away[idx],df.droughts_home[idx], \
    df.pts_away[idx],df.pts_home[idx],df.team_away[idx],df.team_home[idx], \
    df.time_scored_away[idx],df.time_scored_home[idx]) = extract_drought_times(url)

    (df.avg_drought_away[idx],df.avg_drought_home[idx],df.sd_drought_away[idx], \
    df. sd_drought_home[idx]) = get_drought_stats(df.droughts_away[idx],df.droughts_home[idx])
    
    (df.game_yr[idx],df.game_mon[idx],df.game_day[idx]) = get_game_date(url)
    
    print(idx)

del idx,url,game_urls