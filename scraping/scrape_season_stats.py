from bball_ref_scraping_funcs import *

data_dir = 'nba_data/'
seasons = [year for year in range(1997, 2021)]
stat_types = ['advanced', 'shooting', 'pbp', 'per_poss']

if __name__ == '__main__':
    scrape(seasons, stat_types, data_dir)
