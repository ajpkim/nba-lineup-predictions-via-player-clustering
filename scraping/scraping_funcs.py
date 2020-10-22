import time
import pandas as pd

from datetime import datetime
from functools import reduce

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


############### FUNCTIONS FOR NAVIGATING NBA.COM/STATS ###############

def sort_by_name(browser):
    """Sort table descending alphabetical order by player name"""
    xpath_player_sort = '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[2]'
    browser.find_element_by_xpath(xpath_player_sort).click()
    browser.find_element_by_xpath(xpath_player_sort).click()
    return

def select_all_pages(browser):
    """Select display all pages"""
    xpath_page_selection = '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select'
    xpath_all_pages = xpath_page_selection + '/option[1]'
    browser.find_element_by_xpath(xpath_all_pages).click()
    return

def select_per_100(browser):
    """Navigate to per 100 possessions stat mode"""
    xpath_per_mode = '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select'
    browser.find_element_by_xpath(xpath_per_mode).click()
    
    xpath_per_100 = '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select/option[3]'
    browser.find_element_by_xpath(xpath_per_100).click()
    
def select_stat_type(browser, stat_type):
    """Navigate to given stat table e.g. "traditional", "advanced", "misc", etc."""
    stat_table_dict = {'traditional': 1, 'advanced': 2, 'misc': 3, 'scoring': 4, 'usage': 5, 'opponent': 6, 'defense':7}
    n = stat_table_dict[stat_type]
    
    ## select the header to get drop down
    xpath_stat_type_button = '/html/body/main/div[2]/div/div[2]/div/nav-dropdown/nav/section[3]/div/a'
    browser.find_element_by_xpath(xpath_stat_type_button).click()

    ## navigate to different stat type
    xpath_stat_type = f'/html/body/main/div[2]/div/div[2]/div/nav-dropdown/nav/section[3]/ul/li[{n}]/a/span'
    browser.find_element_by_xpath(xpath_stat_type).click()
    
    if n in [1, 3, 6, 7]:  # need to select mode for given stat type i.e. per 100 possesion
        time.sleep(2)
        select_per_100(browser)
    return

def select_season(browser, season):
    """Navigate to given season"""
    seasons_dict = dict(zip(range(2019, 1995, -1), [i for i in range(1, 100)]))
    n = seasons_dict[season]
    ## click 'SEASON' header
    xpath_season_header = '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select'
    browser.find_element_by_xpath(xpath_season_header).click()
    ## select season
    xpath_select_season = f'/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[{n}]'
    browser.find_element_by_xpath(xpath_select_season).click()
    return


############### FUNCTIONS FOR HANDLING RAW TABLE AND SCRAPED DFS ###############

def scrape_table(browser, stat_type: str):
    """
    Scrapes stats table present on browser and returns pandas DF. 
    stat_type is one of following str: 'traditional', 'advanced', 'misc', 'scoring', 'usage', 'opponent', 'defense'
    """
    stat_table_dict = {'traditional': 1, 'advanced': 2, 'misc': 3, 'scoring': 4, 'usage': 5, 'opponent': 6, 'defense':7}
    n = stat_table_dict[stat_type]
    
    ## read in raw table data
    xpath_stats_table = '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]'
    raw_table = browser.find_element_by_xpath(xpath_stats_table)
    table = raw_table.text.split('\n')
    
    ## columns for each stat table type...
    if n == 1:  # traditional
        cols = ['TEAM', 'AGE', 'GP', 'W', 'L', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF', 'FP', 'DD2', 'TD3', '+/-']
    
    elif n == 2:  # advanced
        cols = ['TEAM', 'AGE', 'GP', 'W', 'L', 'MIN', 'OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']
    
    elif n == 3: # misc
        cols = ['TEAM','AGE','GP','W','L','MIN','PTS OFF TO','2ND PTS','FBPS','PITP','OPP PTS OFF TO','OPP 2ND PTS','OPP FBPS','OPP PITP','BLK','BLKA','PF','PFD']

    elif n == 4: # scoring
        cols = ['TEAM', 'AGE', 'GP', 'W','L','MIN','%FGA 2PT','%FGA 3PT','%PTS 2PT','%PTS 2PT MR','%PTS 3PT','%PTS FBPS','%PTS FT','%PTS OFFTO','%PTS PITP','2FGM %AST','2FGM %UAST','3FGM %AST','3FGM %UAST','FGM %AST','FGM %UAST']
    
    elif n == 5:  # usage, adjusting 'MIN' to 'TOT MIN' as this is what usage provides and is different than MIN per 100 poss.
        cols = ['TEAM', 'AGE', 'GP', 'W', 'L', 'TOT MIN', 'USG%', '%FGM', '%FGA', '%3PM', '%3PA', '%FTM', '%FTA', '%OREB', '%DREB', '%REB', '%AST', '%TOV', '%STL', '%BLK', '%BLKA', '%PF', '%PFD', '%PTS']
    
#     ## MISSING DATA FROM PRIOR 2010'S, not using opponent stats
#     elif table_num == 6: # opponent
#         cols = ['TEAM','GP','W','L','MIN','OPP FGM','OPP FGA','OPP FG%','OPP 3PM','OPP 3PA','OPP 3P%','OPP FTM','OPP FTA','OPP FT%','OPP OREB','OPP DREB','OPP REB','OPP AST','OPP TOV','OPP STL','OPP BLK','OPP BLKA','OPP PF','OPP PFD','OPP PTS','+/-',]
    
    elif n == 7:  # defense
        cols = ['TEAM','AGE','GP','W','L','MIN','DEF RTG','DREB','DREB%','%DREB','STL','STL%','BLK','%BLK','OPP PTS OFF TOV','OPP PTS 2ND CHANCE','OPP PTS FB','OPP PTS PAINT','DEF WS']

    ## extract position of first player row
    for i, line in enumerate(table):
        if line and line[0] == 'A' and len(line.split(' ')) == 2:
            body = table[i:] 
            break
            
    ## parse body of table now and extract player name index, stats
    player_names, all_stats = [], []
    for i in range(0, len(body), 2):
        player = body[i]
        
        if player in player_names:
            ## need to add team name to player index when players have multiple rows
            team = body[i+1].split(' ')[0]
            player += f' ({team})' # e.g. Marcus Williams (GSW)
            ## need to add team name to previous same player entry as well as order is different for varying tables within a season
            team = all_stats[-1][0]
            player_names[-1] += f' ({team})'
            
        if len(player.split(' ')) > 0 and len(player.split(' ')) < 4:  # avoid weird missing data rows
            player_names.append(player)
            player_stats = body[i+1].split(' ')
            all_stats.append(player_stats)
        
    return pd.DataFrame(all_stats, index=player_names, columns=cols)

def remove_equal_cols(df):
    """
    Remove equivalent columns from df irrespective of column name.
    Works with non-unique column names as it uses column indices.
    """
    dup_col_idxs = set()
    for i in range(len(df.columns)-1):
        if i in dup_col_idxs: continue
        for j in range(i+1, len(df.columns)):
            if df.iloc[:, i].equals(df.iloc[:, j]):
                dup_col_idxs.add(j)
    df = df.iloc[:, list(set(range(len(df.columns)))-dup_col_idxs)].copy()
    return df


def scrape_combine_season_data(season: int, stat_types: list):
    """ 
    Given a season and stat types, Returns a DF combining the stats tables based
    on player name index. time.sleep(x) is used to ensure page loading and navigation success. 
    """
    ## Set up selenium driver
    options = webdriver.firefox.options.Options()
    options.headless = True
    browser = webdriver.Firefox(executable_path="./drivers/geckodriver", options=options)
    generic_nba_stats_url = 'https://stats.nba.com/players/traditional/?sort=PTS&dir=-1'
    browser.get(generic_nba_stats_url)
    time.sleep(4)
    
    ## Scrape the stats table for each stat type
    dfs = []    
    for stat_type in stat_types:
        select_stat_type(browser, stat_type); time.sleep(5)
        select_season(browser, season); time.sleep(5)
        sort_by_name(browser); time.sleep(5)
        select_all_pages(browser); time.sleep(5)
        df = scrape_table(browser, stat_type)
        dfs.append(df)
        time.sleep(5)
    browser.quit()
    
    ## Combine the scraped tables into single season table based on player name index and only using unique column names
    combined_stats = reduce(lambda left, right: pd.merge(left, right[right.columns.difference(left.columns)], left_index=True, right_index=True), dfs)
    combined_stats = remove_equal_cols(combined_stats)  # remove equal columns with diff names e.g. %STL and STL%

    return combined_stats


############### FUNCTIONS FOR HANDLING SCRAPED DATA ###############

def process_write_season_data(df, season, stat_cols, filepath):
    """Extract the relevant columns, write out as csv, return DF"""    
    df = df.loc[:, stat_cols].copy()
    df.set_index(df.index.astype(str) + ' ' + str(season)[-4:], inplace=True)
    
    with open(filepath, 'w') as f:
        df.to_csv(filepath)
    
    return df    

############### WRAPPERS FOR EVERYTHING ###############

def scrape(seasons, stat_types, stat_cols, stat_dir, verbose=True):
    """Scrape stats for given seasons, write out season data, and return combined DF"""
    dfs = []
    for season in seasons:
        if verbose: print('scraping:', season, '   |   ', datetime.now())
        filepath = stat_dir + 'stats_' + str(season) + '.csv'
        df = scrape_combine_season_data(season, stat_types)
        df = process_write_season_data(df, season, stat_cols, filepath)
        dfs.append(df)

    df_combined = pd.concat(dfs)
    
    return df_combined


def combine_data(data_dir):
    pass
