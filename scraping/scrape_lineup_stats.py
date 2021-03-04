from bballref_lineup_scraping_funcs import scrape_lineup_data

data_dir = 'bballref_data/lineups/'
n_man_lineup = 5
seasons = [year for year in range(1997, 2021)]
teams = [
        'ATL',
        'NJN',  # switches to BKN 
        'BOS',
        'CHH',  # switches to CHA then CHO
        'CHI',
        'CLE',
        'DAL',
        'DEN',
        'DET',
        'GSW',
        'HOU',
        'IND',
        'LAC',
        'LAL',
        'VAN',  # switches to MEM
        'MIA',
        'MIL',
        'MIN',
        'NOH',  # switches to NOP
        'NYK',
        'SEA',  # switches to OKC
        'ORL',
        'PHI',
        'PHO',
        'POR',
        'SAC',
        'SAS',
        'TOR',
        'UTA',
        'WSB', # switches to WAS
        ]


if __name__ == '__main__':
    scrape_lineup_data(teams, seasons, n_man_lineup, data_dir)

