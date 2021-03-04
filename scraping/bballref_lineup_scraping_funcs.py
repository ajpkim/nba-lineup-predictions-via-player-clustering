import os
from datetime import datetime

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def select_team_and_year_lineups(browser, team, year):
    url = f'https://www.basketball-reference.com/teams/{team}/{year}/lineups/'
    browser.get(url)
    
def read_lineup_table(soup, n_man_lineup: int):
    "n is the lineup number i.e. 5man, 4man, 3man lineup"
    all_stats, all_lineup_ids, stat_cols = [], [], []
    table = soup.find('table', {'id': f'lineups_{n_man_lineup}-man_'})
    tbody = table.find('tbody')
    
    for row in tbody.find_all('tr')[0:-1]:
        cols = row.find_all('td')
        stat_cols = [col.get('data-stat') for col in cols]
        
        lineup_ids = [cols[0].get('csk')]
        all_lineup_ids.append(lineup_ids)
        
        lineup_stats = [col.text for col in cols]
        all_stats.append(lineup_stats)
        
    df = pd.DataFrame(all_stats, columns=stat_cols).set_index('lineup')
    df['player_ids'] = all_lineup_ids
    df['number_players'] = [n_man_lineup] * len(df)
        
    return df

def process_lineup_df(df, team, year):
    ## convert minutes played to minute in decimals and improve player_ids format
    df.loc[:, 'mp'] = df['mp'].apply(lambda x: float(x.split(':')[0]) + float(x.split(':')[1])/60)
    df.loc[:, 'player_ids'] = df['player_ids'].apply(lambda x: x[0].replace(':', ', '))
    ## convert differential stat columns to floats
    df.replace('', np.nan)  # e.g. no 3's taken so differential fg% is ''
    conv_to_float_cols = df.columns[df.columns.str.contains('diff')]
    df.loc[:, conv_to_float_cols] = df[conv_to_float_cols].apply(lambda series: pd.to_numeric(series, errors='ignore'))
    ## add year and team cols, improve index
    df['year'] = [year] * len(df)
    df['team'] = [team] * len(df)
    df.index = df.index + f' {team} {year}'
    
    return df

def scrape_lineup_data(teams, seasons, n_man_lineup, data_dir):
    options = webdriver.firefox.options.Options()
    options.headless = True
    browser = webdriver.Firefox(executable_path="scraping/drivers/geckodriver", options=options)
    start = datetime.now()
    all_dfs = []
    for team in teams:
        team_dfs = []
        print('scraping:', team, '   |   ', datetime.now()-start)
        for season in seasons:
            # print(season)
            # handle team name switches etc.
            if team == 'NJN' and season > 2012: team = 'BRK'; print('Season:', season, '-->', team)
            if team == 'NOH' and season < 2003: continue # not a team prior to 2002-03
            if team == 'NOH' and season == 2006: team = 'NOK'; print('Season:', season, '-->', team)
            if team == 'NOK' and season == 2008: team = 'NOH'; print('Season:', season, '-->', team)
            if team == 'NOH' and season == 2014: team = 'NOP'; print('Season:', season, '-->', team)
            if team == 'SEA' and season > 2008: team = 'OKC'; print('Season:', season, '-->', team)
            if team == 'WSB' and season > 1997: team = 'WAS'; print('Season:', season, '-->', team)
            if team == 'CHH' and season > 2002: team = 'CHA'; print('Season:', season, '-->', team)  
            if team == 'CHA' and season in [2002, 2003, 2004]: continue  # no charlotte team 2002-2004
            if team == 'CHA' and season > 2014: team = 'CHO'; print('Season:', season, '-->', team)
            if team == 'VAN' and season > 2001 : team = 'MEM'; print('Season:', season, '-->', team)

            select_team_and_year_lineups(browser, team, season)
            page_source = browser.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            df = read_lineup_table(soup, n_man_lineup)
            df = process_lineup_df(df, team, season)
            team_dfs.append(df)
        
        combined_team_df = pd.concat(team_dfs)
        filename = data_dir + f'{team}/{team}_{n_man_lineup}_man_lineups_{seasons[0]}_{seasons[-1]}.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        combined_team_df.to_csv(filename)
        all_dfs.append(combined_team_df)
    
    df = pd.concat(all_dfs)
    filename = f'bballref_data/raw_all_teams_{n_man_lineup}_man_lineups_{seasons[0]}_{seasons[-1]}.csv'
    df.to_csv(filename)
    return df
