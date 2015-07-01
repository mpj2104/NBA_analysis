# -*- coding: utf-8 -*-
"""
Created on Thu May 28 23:55:01 2015

@author: mpjiang
"""

from __future__ import division
import pandas as pd
import numpy as np
import itertools
import re

def find_consecutive_shots(ID,game_IDs,shot_data,min_shot_dist):   
    d = {'PLAYER_ID':pd.Series(np.zeros(100)+ID),
         'season_ID':pd.Series(),
         'streak_num':pd.Series(range(100)),
         'streak_type':pd.Series(),
         'streak_length':pd.Series(),
         'game_ID':pd.Series(),
         'game_location':pd.Series(),
         'avg_btwn_shot_time':pd.Series(),
         'avg_num_dribbles':pd.Series(),
         'avg_touch_time':pd.Series(),
         'avg_shot_dist':pd.Series(),
         'avg_def_dist':pd.Series(),
         'total_shots_taken':pd.Series()}
    f = {'PLAYER_ID':pd.Series(np.zeros(400)+ID),
         'season_ID':pd.Series(),
         'streak_num':pd.Series(),
         'shot_number':pd.Series(),
         'game_ID':pd.Series(),
         'btwn_shot_time_elapsed':pd.Series(),
         'def_dist':pd.Series(),
         'game_clock':pd.Series(),
         'num_dribbles':pd.Series(),
         'quarters':pd.Series(),
         'shot_dist':pd.Series(),
         'touch_time':pd.Series()}
    df = pd.DataFrame(d)
    df_details = pd.DataFrame(f)
    del d
    del f
    
    streak_counter = 0 # keeps track of the streak number
    streak_details_idx = 0 # keeps track of the streak details index number    
    for game in game_IDs: # iterate over each game played 
        temp_data = shot_data[(shot_data.GAME_ID==game) & (shot_data.SHOT_DIST>=min_shot_dist)] # looks at shot data for particular game and for particular shot distance       
        temp_shot_groups = [] # will store groups of consecutive identical shot results
        length_shot_groups = [] # will store lengths of those groups (missed,missed,missed = 3)
        streak_key = [] # identifies streak type        
        for k,g in itertools.groupby(temp_data.SHOT_RESULT):
            streak_key.append(k)            
            temp_shot_groups.append(list(g))
            length_shot_groups.append(len(temp_shot_groups[-1]))
        length_shot_groups = np.array(length_shot_groups)    
        shot_group_ind = np.where(length_shot_groups>=3) # only interested in shot groups that are at least length 3    
        
        if not shot_group_ind[0].size: # move on to next game if no streaks
            continue
        else:
            season = np.array(temp_data.season_ID)[0]
            shot_numbers = np.array(temp_data.SHOT_NUMBER)     
            start_shot_num_ind = [] # identify starting shot number for select shot groups        
            for ind in shot_group_ind[0]:
                start_shot_num_ind.append(np.sum(length_shot_groups[0:ind]))
                temp_shot_num_ind = range(start_shot_num_ind[-1],start_shot_num_ind[-1]+length_shot_groups[ind])

                temp_shot_numbers = shot_numbers[temp_shot_num_ind]             
                if np.all(np.diff(temp_shot_numbers)==1): # check if shots are actually consecutive
                    streak_counter += 1 # confirmed as a streak
                    df.streak_num[streak_counter-1] = streak_counter
                    df.streak_type[streak_counter-1] = streak_key[ind]
                    damn_index = temp_data.index[temp_data.SHOT_NUMBER==temp_shot_numbers[0]][0] # picks out actual index of temp_data
                    damn_index = range(damn_index,damn_index+length_shot_groups[ind])
                    df.game_location[streak_counter-1] = temp_data.LOCATION[damn_index[0]]                 
                    
                    # figure out elapsed times
                    times = np.array(temp_data.GAME_CLOCK[damn_index])
                    minutes = [int(re.findall('(\d*)\:',a)[0]) for a in times]
                    seconds = [int(re.findall('\:(.*)',a)[0]) for a in times]
                    times = [minutes[a]*60+seconds[a] for a in range(len(times))] # in seconds                
                    
                    periods = np.array(temp_data.PERIOD[damn_index])         
                    elapsed_times = []
                    for ii in range(len(times)-1):
                        if periods[ii+1]-periods[ii] == 0: # the case where two consecutive shots occurred in same quarter
                            elapsed_times.append(times[ii]-times[ii+1])
                        elif (periods[ii+1]-periods[ii] > 0) & (periods[ii+1] <= 4) & (periods[ii] <= 4): # the case where two consecutive shots occurred in two different quarters (both in regulation)
                            period_diff = periods[ii+1]-periods[ii]
                            elapsed_times.append(times[ii]+(12*60*period_diff)-times[ii+1])
                        elif (periods[ii+1]-periods[ii] > 0) & (periods[ii+1] > 4) & (periods[ii] <= 4): # the case where two consecutive shots occurred in two different quarters (first in regulation, second in OT)
                            period_diff = periods[ii+1]-periods[ii]
                            elapsed_times.append(times[ii]+(12*60*period_diff)-(7*60*(periods[ii+1]-4))-times[ii+1])
                        elif (periods[ii+1]-periods[ii] > 0) & (periods[ii+1] > 4) & (periods[ii] > 4): # the case where two consecutive shots occurred in two different quarters (both in OT)
                            period_diff = periods[ii+1]-periods[ii]
                            elapsed_times.append(times[ii]+(5*60*period_diff)-times[ii+1])     
                    df.avg_btwn_shot_time[streak_counter-1] = np.mean(elapsed_times)
                    
                    # fill in streak details
                    elapsed_times = [0] + elapsed_times # to make all details same length
                    for jj in range(len(times)):
                        df_details.game_clock[streak_details_idx] = np.array(temp_data.GAME_CLOCK[damn_index])[jj]   
                        df_details.quarters[streak_details_idx] = np.array(temp_data.PERIOD[damn_index])[jj]
                        df_details.season_ID[streak_details_idx] = season                        
                        df_details.touch_time[streak_details_idx] = np.array(temp_data.TOUCH_TIME[damn_index])[jj]
                        df_details.shot_number[streak_details_idx] = jj + 1 
                        df_details.btwn_shot_time_elapsed[streak_details_idx] = elapsed_times[jj]
                        df_details.def_dist[streak_details_idx] = np.array(temp_data.CLOSE_DEF_DIST[damn_index])[jj]
                        df_details.num_dribbles[streak_details_idx] = np.array(temp_data.DRIBBLES[damn_index])[jj]                        
                        df_details.shot_dist[streak_details_idx] = np.array(temp_data.SHOT_DIST[damn_index])[jj]                        
                        df_details.game_ID[streak_details_idx] = game  
                        df_details.streak_num[streak_details_idx] = streak_counter
                        streak_details_idx += 1
                
                    df.avg_num_dribbles[streak_counter-1] = np.mean(temp_data.DRIBBLES[damn_index])
                    df.avg_touch_time[streak_counter-1] = np.mean(temp_data.TOUCH_TIME[damn_index])
                    df.avg_shot_dist[streak_counter-1] = np.mean(temp_data.SHOT_DIST[damn_index])
                    df.avg_def_dist[streak_counter-1] = np.mean(temp_data.CLOSE_DEF_DIST[damn_index])
                    df.total_shots_taken[streak_counter-1] = len(temp_data)
                    df.game_ID[streak_counter-1] = game
                    df.season_ID[streak_counter-1] = season
                    df.streak_length[streak_counter-1] = length_shot_groups[ind]
                else:
                    continue
    
    df = df.drop(df.index[streak_counter:])
    df_details = df_details.drop(df_details.index[streak_details_idx:])        
    return (df,df_details)

def calc_basic_streak_nums(streaks_data,details,ID,player,FGP,FGP3):
    temp_streaks = streaks_data.streak_type # get list of all streak types   
    missed_idx = temp_streaks=='missed'
    made_idx = temp_streaks=='made'
    total_streaks_miss = sum(missed_idx) # count all "missed" streaks
    total_streaks_made = sum(made_idx) # count all "made" streaks
    total_streaks_all = total_streaks_made + total_streaks_miss
    if total_streaks_all > 0:
        pct_streaks_miss = 100*(total_streaks_miss/total_streaks_all)
        pct_streaks_made = 100*(total_streaks_made/total_streaks_all)
    else:
        pct_streaks_miss = 0
        pct_streaks_made = 0
    
    # figure out various averages
    
    total_shots_miss = sum(streaks_data.streak_length[missed_idx])
    total_shots_made = sum(streaks_data.streak_length[made_idx])
    
    avg_btwn_shot_time_miss = [a*b for a,b in zip(streaks_data.avg_btwn_shot_time[missed_idx],streaks_data.streak_length[missed_idx])]
    avg_def_dist_miss = [a*b for a,b in zip(streaks_data.avg_def_dist[missed_idx],streaks_data.streak_length[missed_idx])]    
    avg_num_dribbles_miss = [a*b for a,b in zip(streaks_data.avg_num_dribbles[missed_idx],streaks_data.streak_length[missed_idx])]
    avg_shot_dist_miss = [a*b for a,b in zip(streaks_data.avg_shot_dist[missed_idx],streaks_data.streak_length[missed_idx])]
    avg_touch_time_miss = [a*b for a,b in zip(streaks_data.avg_touch_time[missed_idx],streaks_data.streak_length[missed_idx])]
    if total_shots_miss == 0: # no miss streaks
        avg_btwn_shot_time_miss = np.nan
        avg_def_dist_miss = np.nan
        avg_num_dribbles_miss = np.nan
        avg_shot_dist_miss = np.nan
        avg_touch_time_miss = np.nan
    else:
        avg_btwn_shot_time_miss = sum(avg_btwn_shot_time_miss)/total_shots_miss
        avg_def_dist_miss = sum(avg_def_dist_miss)/total_shots_miss
        avg_num_dribbles_miss = sum(avg_num_dribbles_miss)/total_shots_miss
        avg_shot_dist_miss = sum(avg_shot_dist_miss)/total_shots_miss
        avg_touch_time_miss = sum(avg_touch_time_miss)/total_shots_miss
    avg_streak_length_miss = np.mean(streaks_data.streak_length[missed_idx])
    
    
    avg_btwn_shot_time_made = [a*b for a,b in zip(streaks_data.avg_btwn_shot_time[made_idx],streaks_data.streak_length[made_idx])]
    avg_def_dist_made = [a*b for a,b in zip(streaks_data.avg_def_dist[made_idx],streaks_data.streak_length[made_idx])]
    avg_num_dribbles_made = [a*b for a,b in zip(streaks_data.avg_num_dribbles[made_idx],streaks_data.streak_length[made_idx])]    
    avg_shot_dist_made = [a*b for a,b in zip(streaks_data.avg_shot_dist[made_idx],streaks_data.streak_length[made_idx])]
    avg_touch_time_made = [a*b for a,b in zip(streaks_data.avg_touch_time[made_idx],streaks_data.streak_length[made_idx])]
    if total_shots_made == 0: # no made streaks
        avg_btwn_shot_time_made = np.nan
        avg_def_dist_made = np.nan
        avg_num_dribbles_made = np.nan
        avg_shot_dist_made = np.nan
        avg_touch_time_made = np.nan
    else:
        avg_btwn_shot_time_made = sum(avg_btwn_shot_time_made)/total_shots_made
        avg_def_dist_made = sum(avg_def_dist_made)/total_shots_made
        avg_num_dribbles_made = sum(avg_num_dribbles_made)/total_shots_made
        avg_shot_dist_made = sum(avg_shot_dist_made)/total_shots_made
        avg_touch_time_made = sum(avg_touch_time_made)/total_shots_made
    avg_streak_length_made = np.mean(streaks_data.streak_length[made_idx])
    
    num_games_multi_streaks = np.array([len(list(group)) for key, group in itertools.groupby(streaks_data.game_ID)])
    num_games_multi_streaks = len(np.where(num_games_multi_streaks>1)[0]) # number of times in which the player had multiple streaks in a single game
    
    game_locs = np.array(streaks_data.game_location)
    num_home_games = len(np.where(game_locs=='H')[0])
    num_away_games = len(np.where(game_locs=='A')[0])
    
    qtr_count = []
    for i in range(int(max(details.quarters))):
        qtr_count.append(len(np.where(details.quarters==i+1)[0]))
    qtr_count = str(qtr_count)
    
    d = {'player_ID':pd.Series(ID),
         'player_name':pd.Series(player),
         'num_miss_streaks':pd.Series(total_streaks_miss),
         'num_made_streaks':pd.Series(total_streaks_made),
         'total_streaks':pd.Series(total_streaks_all),
         'pct_miss_streaks':pd.Series(pct_streaks_miss),
         'pct_made_streaks':pd.Series(pct_streaks_made),
         'season_FGP':pd.Series(str(FGP)),
         'season_3FGP':pd.Series(str(FGP3)),
         'avg_elapsed_time_miss':pd.Series(avg_btwn_shot_time_miss),
         'avg_elapsed_time_made':pd.Series(avg_btwn_shot_time_made),
         'avg_def_dist_miss':pd.Series(avg_def_dist_miss),
         'avg_def_dist_made':pd.Series(avg_def_dist_made),
         'avg_num_dribbles_miss':pd.Series(avg_num_dribbles_miss),
         'avg_num_dribbles_made':pd.Series(avg_num_dribbles_made),
         'avg_shot_dist_miss':pd.Series(avg_shot_dist_miss),
         'avg_shot_dist_made':pd.Series(avg_shot_dist_made),
         'avg_touch_time_miss':pd.Series(avg_touch_time_miss),
         'avg_touch_time_made':pd.Series(avg_touch_time_made),
         'avg_streak_length_miss':pd.Series(avg_streak_length_miss),
         'avg_streak_length_made':pd.Series(avg_streak_length_made),
         'num_games_multi_streaks':pd.Series(num_games_multi_streaks),
         'num_home_games':pd.Series(num_home_games),
         'num_away_games':pd.Series(num_away_games),
         'qtr_count':pd.Series(qtr_count)}
    df = pd.DataFrame(d)
    
    return df