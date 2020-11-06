import time
from functools import reduce

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


def select_season(browser, season):
    url = f'https://www.basketball-reference.com/leagues/NBA_{season}_per_poss.html'
    browser.get(url)

def select_stat_table(browser, stat_table):
    ### DEPENDS ON YEAR ... E.G. OLDER STATS HAVE NO PLAY-BY-PLAY SO NUMBERS ARE DIFF
    ## key names are such that they match bball ref internal reference for links and stuff
    stat_table_dict = {'totals': 1, 'per_game': 2, 'per_minute': 3, 'per_poss': 4, 'advanced': 5, 'pbp': 6, 'shooting': 7, 'adj_shooting': 8}
    n = stat_table_dict[stat_table]
    button_xpath = f'/html/body/div[2]/div[5]/div[2]/div[{n}]/a'
    browser.find_element_by_xpath(button_xpath).click()
    
def toggle_partial_rows(browser, stat_type):
    button_xpath = f'//*[@id="{stat_type}_stats_toggle_partial_table"]'
    browser.find_element_by_xpath(button_xpath).click()

def remove_mobile_fmt(browser):
    action = ActionChains(browser)
    menu_xpath =  '/html/body/div[2]/div[5]/div[3]/div[1]/div/ul/li[1]/span'
    share_menu = browser.find_element_by_xpath(menu_xpath)
    action.move_to_element(share_menu).perform(); time.sleep(5)
    button_xpath = '/html/body/div[2]/div[5]/div[3]/div[1]/div/ul/li[1]/div/ul/li[5]/button'
    browser.find_element_by_xpath(button_xpath).click()
    
def read_stat_table(soup):
    table = soup.find(class_="table_outer_container")
    tbody = table.find('tbody')
    tbody_tr = tbody.find_all('tr')
    stat_cols, all_stats, all_ids = [], [], []
    
    for row in tbody_tr:
        if row['class'] != ["full_table"]: continue  # skip partial entries for players with multiple teams
        cols = row.find_all('td')
        if stat_cols == []:  # get the stat column names
            stat_cols = [col.get('data-stat') for col in cols]
        player_stats = [col.text for col in cols]
        all_stats.append(player_stats)
        player_id = cols[0].get('data-append-csv')
        all_ids.append(player_id)

    df = pd.DataFrame(all_stats, columns=stat_cols).set_index('player')
    df['player_id'] = all_ids
    
    return df

def process_scraped_table(df, season):
    # drop_cols = [col for col in df if not df[col].any()]  ## ambiguous truth value
    nunique = df.apply(pd.Series.nunique)
    drop_cols = nunique[nunique == 1].index
    df.drop(drop_cols, axis=1, inplace=True)
    df['year'] = [season] * len(df)
    df.index += f' {str(season)}'
    return df

def combine_season_stats(dfs):
    dfs = [df.reset_index().set_index('player_id') for df in dfs]
    season_df = reduce(lambda left, right: pd.merge(left, right[right.columns.difference(left.columns)], left_index=True, right_index=True), dfs)
    return season_df.reset_index().set_index('player')

def scrape(seasons, stat_types, data_dir):
    options = webdriver.firefox.options.Options()
    options.headless = True
    browser = webdriver.Firefox(executable_path="scraping/drivers/geckodriver", options=options)
    dfs = []
    
    for season in seasons:
        print('scraping:', season)
        season_dfs = []
        select_season(browser, season); time.sleep(3)
        
        for stat_type in stat_types:
            select_stat_table(browser, stat_type); time.sleep(3)
            page_source = browser.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            df = read_stat_table(soup)
            df = process_scraped_table(df, season)        
            filename = data_dir + str(season) + '_' + str(stat_type).replace(' ', '_') + '.csv'
            df.to_csv(filename)
            season_dfs.append(df)

        combo_season_df = combine_season_stats(season_dfs)
        filename = data_dir + str(season) + '_' + '_'.join(stat_types) + '.csv'
        combo_season_df.to_csv(filename)
        dfs.append(combo_season_df)
    
    if len(seasons) < 2:
        return dfs[0]
    
    master_df = pd.concat(dfs)
    filename = data_dir + str(seasons[0]) + '_to_' + str(seasons[-1]) + '_' + '_'.join(stat_types) + '.csv'
    master_df.to_csv(filename)
    
    return master_df