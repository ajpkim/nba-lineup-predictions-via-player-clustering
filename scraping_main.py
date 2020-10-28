import pandas as pd
import numpy as np

from datetime import datetime
from functools import reduce

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from scraping.scraping_funcs import *

## Vars defining what to scrape
stat_types = ['traditional', 'advanced', 'misc', 'scoring', 'usage', 'defense']

## commented out when wanted to rescrape with stat type prefixes and chaned funcs to not need stat_cols but didn't do it yet

# stat_cols = ['%3PA',
#             '%3PM',
#             '%AST',
#             '%BLK',
#             '%BLKA',
#             '%DREB',
#             '%FGA',
#             '%FGA 2PT',
#             '%FGA 3PT',
#             '%FGM',
#             '%FTA',
#             '%FTM',
#             '%OREB',
#             '%PF',
#             '%PFD',cd 
#             '%PTS',
#             '%PTS 2PT',
#             '%PTS 2PT MR',
#             '%PTS 3PT',
#             '%PTS FBPS',
#             '%PTS FT',
#             '%PTS OFFTO',
#             '%PTS PITP',
#             '%REB',
#             '%STL',
#             '%TOV',
#             '+/-',
#             '2FGM %AST',
#             '2FGM %UAST',
#             '2ND PTS',
#             '3FGM %AST',
#             '3FGM %UAST',
#             '3P%',
#             '3PA',
#             '3PM',
#             'AGE',
#             'AST',
#             'AST RATIO',
#             'AST%',
#             'AST/TO',
#             'BLK',
#             'BLKA',
#             'DD2',
#             'DEF WS',
#             'DEFRTG',
#             'DREB',
#             'DREB%',
#             'EFG%',
#             'FBPS',
#             'FG%',
#             'FGA',
#             'FGM',
#             'FGM %AST',
#             'FGM %UAST',
#             'FP',
#             'FT%',
#             'FTA',
#             'FTM',
#             'GP',
#             'L',
#             'NETRTG',
#             'OFFRTG',
#             'OPP 2ND PTS',
#             'OPP FBPS',
#             'OPP PITP',
#             'OPP PTS OFF TO',
#             'OREB',
#             'OREB%',
#             'PACE',
#             'PF',
#             'PFD',
#             'PIE',
#             'PITP',
#             'PTS',
#             'PTS OFF TO',
#             'REB',
#             'REB%',
#             'STL',
#             'TD3',
#             'TEAM',
#             'TO RATIO',
#             'TOT MIN',
#             'TOV',
#             'TS%',
#             'USG%',
#             'W']

if __name__ == '__main__':
    start = datetime.now()
    years = [year for year in range(1996, 2020)]
    stat_dir = 'season_data_prefix/'    
    df_all = scrape(years, stat_types, stat_dir)
    df_all.to_csv(stat_dir + 'master_1996_2019_prefix.csv')
    print(df_all.shape)
    print(df_all.head())
    print('Run time:', datetime.now()-start)


    