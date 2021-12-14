import pandas as pd
import requests
from bs4 import BeautifulSoup



# headers used for web-scraping, very important!
headers = {'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'}

# abbreviations for NBA teams used for looping through url during web-scraping
team_names = [
    'ATL',
    'BOS',
    'BRK',
    'CHO',
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
    'MEM',
    'MIA',
    'MIL',
    'MIN',
    'NOP',
    'NYK',
    'OKC',
    'ORL',
    'PHI',
    'PHO',
    'POR',
    'SAC',
    'SAS',
    'TOR',
    'UTA',
    'WAS',
]

# list of team abbreviations from 2021 playoffs, also used for web-scraping loops
team_playoff_names_2021 = [
    'ATL',
    'BOS',
    'BRK',
    'DAL',
    'DEN',
    'LAC',
    'LAL',
    'MEM',
    'MIA',
    'MIL',
    'NYK',
    'PHI',
    'PHO',
    'POR',
    'UTA',
    'WAS',
]

team_playoff_names_2020 = [
    'LAL',
    'POR',
    'HOU',
    'OKC',
    'DEN',
    'UTA',
    'LAC',
    'DAL',
    'MIL',
    'ORL',
    'IND',
    'MIA',
    'BOS',
    'PHI',
    'TOR',
    'BRK',
]

team_playoff_names_2019 = [
    'GSW',
    'LAC',
    'HOU',
    'UTA',
    'POR',
    'OKC',
    'DEN',
    'SAS',
    'MIL',
    'DET',
    'BOS',
    'IND',
    'PHI',
    'BRK',
    'TOR',
    'ORL',
]

team_playoff_names_2018 = [
    'HOU',
    'MIN',
    'OKC',
    'UTA',
    'POR',
    'NOP',
    'GSW',
    'SAS',
    'TOR',
    'WAS',
    'CLE',
    'IND',
    'PHI',
    'MIA',
    'BOS',
    'MIL',
]

### ended up using only the most recent stats of current season and last season for project, however the project -
### can be continued to use data from varying lengths of seasons which would alter the outcomes of the web-app

######################################################################################

# scrape player totals for stats from basketball-reference
# this function scrapes the stat totals from the totals table for every player of the designated team
# uses the team, year/season, and type of totals (regular season or playoffs) as inputs
def get_totals(team, year, table):
    
    # assign site url to variable
    team_url = (f'https://www.basketball-reference.com/teams/{team}/{year}.html')

    # make request using site url
    team_res = requests.get(team_url)

    #BeautifulSoup Library parses the content of an HTML document, in this case clips_res
    team_soup = BeautifulSoup(team_res.content, 'lxml')

    # identify table we want to scrape data from (team totals)
    team_totals = team_soup.find(name = 'table', attrs = {'id' : table})

    # create list of dictionaries to hold each player's stats
    team_stats = []

    # print team to help keep track of any bugs and know where you are
    print(team + f' totals {year}')
    
    # loop through totals table for each player and get each stat
    for row in team_totals('tr')[1:]:
        # this loop will go through each row in the totals table (row represents a player in the table)
        # goes through each row and scrapes all stats in the row
        
        # create dict for the row(represents each player)
        player = {}
        
        # use .find to get info we want for every stat
        player['Name'] = row.find('td', {'data-stat' : 'player'}).text
        print(row.find('td', {'data-stat' : 'player'}).text) # print out names of player to help with bugs/ know where we are
        
        # continue using .find to get rest of stats in table
        player['Age'] = row.find('td', {'data-stat' : 'age'}).text
        # use int() to turn info we scrape into a numeric value
        player['Games'] = int(row.find('td', {'data-stat' : 'g'}).text)
        
        # use try and except for cases where players don't have a value for the stat we are scraping
        try:
            player['GS'] = int(row.find('td', {'data-stat' : 'gs'}).text)
        except:
            player['GS'] = 0 # if a player doesn't have a value, assign stat value as 0
            
        # repeat int() and .find to scrape more stats
        player['Min'] = int(row.find('td', {'data-stat' : 'mp'}).text)
        player['FGM'] = int(row.find('td', {'data-stat' : 'fg'}).text)
        player['FGA'] = int(row.find('td', {'data-stat' : 'fga'}).text)
        
        # use try and except for cases where players don't have a value for the stat we are scraping
        try:
            # using float() instead of int() here since value has decimals
            player['Field Goal %'] = float(row.find('td', {'data-stat' : 'fg_pct'}).text)
        except:
            player['Field Goal %'] = 0
        
        # continue scraping rest of stats in the row for the current player and turning them into numeric values
        player['3pt'] = int(row.find('td', {'data-stat' : 'fg3'}).text)
        player['3ptA'] = int(row.find('td', {'data-stat' : 'fg3a'}).text)
        try:
            player['3pt %'] = float(row.find('td', {'data-stat' : 'fg3_pct'}).text)
        except:
            player['3pt %'] = 0
        player['2pt'] = int(row.find('td', {'data-stat' : 'fg2'}).text)
        player['2ptA'] = int(row.find('td', {'data-stat' : 'fg2a'}).text)
        try:
            player['2pt %'] = float(row.find('td', {'data-stat' : 'fg2_pct'}).text)
        except:
            player['2pt %'] = 0
        try:
            player['EFG %'] = float(row.find('td', {'data-stat' : 'efg_pct'}).text)
        except:
            player['EFG %'] = 0
        player['FTM'] = int(row.find('td', {'data-stat' : 'ft'}).text)
        player['FTA'] = int(row.find('td', {'data-stat' : 'fta'}).text)
        try:
            player['FT %'] = float(row.find('td', {'data-stat' : 'ft_pct'}).text)
        except:
            player['FT %'] = 0
        player['ORb'] = int(row.find('td', {'data-stat' : 'orb'}).text)
        player['DRb'] = int(row.find('td', {'data-stat' : 'drb'}).text)
        player['Rebounds'] = int(row.find('td', {'data-stat' : 'trb'}).text)
        player['Assists'] = int(row.find('td', {'data-stat' : 'ast'}).text)
        player['Steals'] = int(row.find('td', {'data-stat' : 'stl'}).text)
        player['Blocks'] = int(row.find('td', {'data-stat' : 'blk'}).text)
        player['Turnovers'] = int(row.find('td', {'data-stat' : 'tov'}).text)
        player['PF'] = int(row.find('td', {'data-stat' : 'pf'}).text)
        player['Points'] = int(row.find('td', {'data-stat' : 'pts'}).text)
        
        # this makes sure to append only players since one row in the table will be the team totals with a min value above 10000
        if player['Min'] < 10000:
            team_stats.append(player)
    
    # turn list of stats into df
    team_roster_df = pd.DataFrame(team_stats)
    
    # return the final df of all players and their stat totals for the designated team
    return team_roster_df

###########################################################################################
# use function above to scrape player totals stats

# empty list to store player stats from 2021 regular season
list_totals_2021 = []

# loop through list of teams to get teams 2020-21 player stats
for team in team_names:
    list_totals_2021.append(get_totals(team, 2021, 'totals'))
    
# empty list to store player stats from 2021 playoffs
list_playoff_totals_2021 = []

# loop through teams that played in 2021 playoffs and get player totals
for team in team_playoff_names_2021:
    list_playoff_totals_2021.append(get_totals(team, 2021, 'playoffs_totals'))
    
# repeat stat scraping for seasons 2018-2022
    
list_playoff_totals_2020 = []

for team in team_playoff_names_2020:
    list_playoff_totals_2020.append(get_totals(team, 2020, 'playoffs_totals'))
    
list_playoff_totals_2019 = []

for team in team_playoff_names_2019:
    list_playoff_totals_2019.append(get_totals(team, 2019, 'playoffs_totals'))
    
list_playoff_totals_2018 = []

for team in team_playoff_names_2018:
    list_playoff_totals_2018.append(get_totals(team, 2018, 'playoffs_totals'))
    
list_totals_2020 = []

for team in team_names:
    list_totals_2020.append(get_totals(team, 2020, 'totals'))
    
list_totals_2019 = []

for team in team_names:
    list_totals_2019.append(get_totals(team, 2019, 'totals'))
    
list_totals_2018 = []

for team in team_names:
    list_totals_2018.append(get_totals(team, 2018, 'totals'))
    
list_totals_2022 = []

for team in team_names:
    list_totals_2022.append(get_totals(team, 2022, 'totals'))
    
#################################################################################################
# concat lists of player totals and turn into one dataframe

all_player_totals_2022 = pd.concat(list_totals_2022, ignore_index=True)

all_player_totals_2021 = pd.concat(list_totals_2021, ignore_index=True)

all_playoff_totals_2021 = pd.concat(list_playoff_totals_2021, ignore_index=True)

all_player_totals_2020 = pd.concat(list_totals_2020, ignore_index=True)

all_playoff_totals_2020 = pd.concat(list_playoff_totals_2020, ignore_index=True)

all_player_totals_2019 = pd.concat(list_totals_2019, ignore_index=True)

all_playoff_totals_2019 = pd.concat(list_playoff_totals_2019, ignore_index=True)

all_player_totals_2018 = pd.concat(list_totals_2018, ignore_index=True)

all_playoff_totals_2018 = pd.concat(list_playoff_totals_2018, ignore_index=True)

#################################################################################################

# function to retrieve current roster of designated team
def get_current_roster(team):
    
    # assign site url to variable
    team_url = (f'https://www.basketball-reference.com/teams/{team}/2022.html')
    
    # make request using site url
    team_res = requests.get(team_url)

    #BeautifulSoup Library parses the content of an HTML document, in this case clips_res
    team_soup = BeautifulSoup(team_res.content, 'lxml')

    # identify table we want to scrape data from (roster table)
    team_roster = team_soup.find(name = 'table', attrs = {'id' : 'roster'})

    # create list of dictionaries
    team_players = []
    
    # print team to help keep track of bugs/know where we are
    print(team)
    
    for row in team_roster('tr')[1:]:
        # this loop scrapes the general player info of the designated team's current roster
        
        # create dict for the row(represents each player)
        player = {}
        # scrape player's name
        player['Name'] = row.find('a').text.strip()
        player['Position'] = row.find('td', {'data-stat' : 'pos'}).text
        player['Number'] = row.find('th', {'data-stat' : 'number'}).text
        # append players to our list of dictionaries
        team_players.append(player)
        
    # turn list of dictionaries (players) into a df    
    current_roster_df = pd.DataFrame(team_players)
    
    # return df of designated team's current roster
    return(current_roster_df)

##################################################################################################

# loop through teams again to make list of current rosters
list_current_rosters = []

# loop through list of teams and use current roster function to get the current roster for all nba teams
for team in team_names:
    # append team's current roster to list
    list_current_rosters.append(get_current_roster(team))
    
#################################################################################################

# create a function to add stats of each year together for each player
def get_player_stats(player, seasons):
    
    # create empty list that will hold player stats
    player_stats = []
    # create variable placeholder for age that will be updated
    age = 0
    
    # this function is written so that you can get the per game averages for a player ranging for the past 4 seasons
        # to just the past season. all totals will also include stat totals from the current season
        
    #loop through totals of past nba seasons and add to list
    
    if seasons == 4: # get stat totals from the last 4 seasons
        
        for index, row in all_player_totals_2022.iterrows(): #loop through season totals of 2022 season
            if player == row['Name']: # if player from our function == player from season totals df
                player_stats.append(all_player_totals_2022.loc[index,:]) # append row from df to our empty list
                age = row['Age'] # update age value
        
        for index, row in all_player_totals_2021.iterrows(): #loop through season totals of 2021 season
            if player == row['Name']: # if player from our function == player from season totals df
                player_stats.append(all_player_totals_2021.loc[index,:]) # append row from df to our empty list
                if age == 0:
                    age = row['Age'] # update age value if it wasn't before
        # repeat for rest of seasons/playoffs
        for index, row in all_playoff_totals_2021.iterrows():
            if player == row['Name']:
                player_stats.append(all_playoff_totals_2021.loc[index,:])
        for index, row in all_player_totals_2020.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2020.loc[index,:])
        for index, row in all_playoff_totals_2020.iterrows():
            if player == row['Name']:
                player_stats.append(all_playoff_totals_2020.loc[index,:])
        for index, row in all_player_totals_2019.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2019.loc[index,:])
        for index, row in all_playoff_totals_2019.iterrows():
            if player == row['Name']:
                player_stats.append(all_playoff_totals_2019.loc[index,:])
        for index, row in all_player_totals_2018.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2018.loc[index,:])
        for index, row in all_playoff_totals_2018.iterrows():
            if player == row['Name']:
                player_stats.append(all_playoff_totals_2018.loc[index,:])
    
    # get season stats for last three seasons
    elif seasons == 3:
        for index, row in all_player_totals_2022.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2022.loc[index,:])
                age = row['Age']
        for index, row in all_player_totals_2021.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2021.loc[index,:])
                if age == 0:
                    age = row['Age']
        for index, row in all_playoff_totals_2021.iterrows():
            if player == row['Name']:
                player_stats.append(all_playoff_totals_2021.loc[index,:])
        for index, row in all_player_totals_2020.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2020.loc[index,:])
        for index, row in all_playoff_totals_2020.iterrows():
            if player == row['Name']:
                player_stats.append(all_playoff_totals_2020.loc[index,:])
        for index, row in all_player_totals_2019.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2019.loc[index,:])
        for index, row in all_playoff_totals_2019.iterrows():
            if player == row['Name']:
                player_stats.append(all_playoff_totals_2019.loc[index,:])
    
    # get season stats for last two seasons
    elif seasons == 2:
        for index, row in all_player_totals_2022.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2022.loc[index,:])
                age = row['Age']
        for index, row in all_player_totals_2021.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2021.loc[index,:])
                if age == 0:
                    age = row['Age']
        for index, row in all_playoff_totals_2021.iterrows():
            if player == row['Name']:
                player_stats.append(all_playoff_totals_2021.loc[index,:])
        for index, row in all_player_totals_2020.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2020.loc[index,:])
        for index, row in all_playoff_totals_2020.iterrows():
            if player == row['Name']:
                player_stats.append(all_playoff_totals_2020.loc[index,:])
    
    # get season stats for last season
    else:
        for index, row in all_player_totals_2022.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2022.loc[index,:])
                age = row['Age']
        for index, row in all_player_totals_2021.iterrows():
            if player == row['Name']:
                player_stats.append(all_player_totals_2021.loc[index,:])
                if age == 0:
                    age = row['Age']
        for index, row in all_playoff_totals_2021.iterrows():
            if player == row['Name']:
                player_stats.append(all_playoff_totals_2021.loc[index,:])
                
    #turn list into df
    player_totals_df = pd.DataFrame(player_stats)
    
    if len(player_totals_df) >= 1:
    
        #create row in df that adds up all stat totals of the seasons
        player_totals_df = player_totals_df.append(player_totals_df.sum(axis = 0, skipna = True), ignore_index= True)
        
        final_stats = {}
        
        # now go through sums of all stats and get per game averages for each
        final_stats['Name'] = player
        final_stats['Age'] = age
        final_stats['Games'] = player_totals_df.loc[len(player_totals_df)-1, 'Games']
        
        # create gp to hold total number of games player has played in allotted time
        gp = player_totals_df.loc[len(player_totals_df)-1, 'Games']
        final_stats['GS'] = player_totals_df.loc[len(player_totals_df)-1, 'GS']
        # round stats to second decimal mark, use gp to get per game avg for stats
        final_stats['Min'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'Min'] / gp),2)
        final_stats['FGM'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'FGM'] / gp),2)
        final_stats['FGA'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'FGA'] / gp),2)
        # create fga to get percentage stat
        fga = (player_totals_df.loc[len(player_totals_df)-1, 'FGA'])
        final_stats['FG %'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'FGM'] / fga),2) # fgm/fga
        final_stats['3pt'] = round(float(player_totals_df.loc[len(player_totals_df)-1, '3pt'] / gp),2)
        final_stats['3ptA'] = round(float(player_totals_df.loc[len(player_totals_df)-1, '3ptA'] / gp),2)
        # create threeptA to get percentage stat
        threeptA = (player_totals_df.loc[len(player_totals_df)-1, '3ptA'])
        final_stats['3pt %'] = round(float(player_totals_df.loc[len(player_totals_df)-1, '3pt'] / threeptA),2)
        final_stats['2pt'] = round(float(player_totals_df.loc[len(player_totals_df)-1, '2pt'] / gp),2)
        final_stats['2ptA'] = round(float(player_totals_df.loc[len(player_totals_df)-1, '2ptA'] / gp),2)
        # create twoptA to get percentage stat
        twoptA = (player_totals_df.loc[len(player_totals_df)-1, '2ptA'])
        final_stats['2pt %'] = round(float(player_totals_df.loc[len(player_totals_df)-1, '2pt'] / twoptA),2)
        # create twoptm for use in efg%
        twoptm = (player_totals_df.loc[len(player_totals_df)-1, '2pt'])
        # efg_threes represents value of 3ptm in efg%
        efg_threes = 1.5 * (player_totals_df.loc[len(player_totals_df)-1, '3pt'])
        # efg% = (1.5(3ptm) + twoptm) / fga
        final_stats['EFG %'] = round(float((twoptm + efg_threes) / fga),2)
        final_stats['FTM'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'FTM'] / gp),2)
        final_stats['FTA'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'FTA'] / gp),2)
        # create fta to get percentage stat
        fta = (player_totals_df.loc[len(player_totals_df)-1, 'FTA'])
        final_stats['FT %'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'FTM'] / fta),2)
        final_stats['ORb'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'ORb'] / gp),2)
        final_stats['DRb'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'DRb'] / gp),2)
        final_stats['Rebounds'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'Rebounds'] / gp),2)
        final_stats['Assists'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'Assists'] / gp),2)
        final_stats['Steals'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'Steals'] / gp),2)
        final_stats['Blocks'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'Blocks'] / gp),2)
        final_stats['Turnovers'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'Turnovers'] / gp),2)
        final_stats['PF'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'PF'] / gp),2)
        final_stats['PPG'] = round(float(player_totals_df.loc[len(player_totals_df)-1, 'Points'] / gp),2)
   
    else:
        # create else for players that haven't played a game yet but are on current rosters
        final_stats = {}
        
        final_stats['Name'] = player
        
        return(final_stats)
    
    # return dict of player's stats
    return(final_stats)

###########################################################################################################
# use get_player_stats function to create final df of player per game avg in specified amount of seasons

all_player_final_stats_4 = []

for i in range(len(team_names)):
    # loop through all teams
    print(team_names[i])
    
    # set loop roster as team's current roster
    loop_roster = list_current_rosters[i]
    
    list_all_current_stats = []

    # loop through current roster of team
    for index, row in loop_roster.iterrows():
        # use get_player_stats for all players on current roster, append player stats to list
        list_all_current_stats.append(get_player_stats(row['Name'], 4))
        print(row['Name'])
        
    # turn list of stats into df
    df_list = pd.DataFrame(list_all_current_stats)
        
    # append df to final_stats list
    all_player_final_stats_4.append(df_list)
    
# make dataframes for past 3 seasons    
# repeat same process for other ranges of seasons
all_player_final_stats_3 = []

for i in range(len(team_names)):
    print(team_names[i])
    loop_roster = list_current_rosters[i]
    
    list_all_current_stats = []

    for index, row in loop_roster.iterrows():
        list_all_current_stats.append(get_player_stats(row['Name'], 3))
        print(row['Name'])
        
    df_list = pd.DataFrame(list_all_current_stats)
        
    all_player_final_stats_3.append(df_list)

# make dataframes for past 2 seasons    
all_player_final_stats_2 = []

for i in range(len(team_names)):
    print(team_names[i])
    loop_roster = list_current_rosters[i]
    
    list_all_current_stats = []

    for index, row in loop_roster.iterrows():
        list_all_current_stats.append(get_player_stats(row['Name'], 2))
        print(row['Name'])
        
    df_list = pd.DataFrame(list_all_current_stats)
        
    all_player_final_stats_2.append(df_list)
    
# make dataframes for past season    
all_player_final_stats_1 = []

for i in range(len(team_names)):
    print(team_names[i])
    loop_roster = list_current_rosters[i]
    
    list_all_current_stats = []

    for index, row in loop_roster.iterrows():
        list_all_current_stats.append(get_player_stats(row['Name'], 1))
        print(row['Name'])
        
    df_list = pd.DataFrame(list_all_current_stats)
        
    all_player_final_stats_1.append(df_list)
    
#####################################################################################################

# add team name to dataframes
team_index = 0
for roster in all_player_final_stats_4:
    loop_team = team_names[team_index]
    roster['Team'] = loop_team
    team_index = team_index + 1
    
# repeat adding team names for rest of season durations
team_index = 0
for roster in all_player_final_stats_3:
    loop_team = team_names[team_index]
    roster['Team'] = loop_team
    team_index = team_index + 1
    
team_index = 0
for roster in all_player_final_stats_2:
    loop_team = team_names[team_index]
    roster['Team'] = loop_team
    team_index = team_index + 1
    
team_index = 0
for roster in all_player_final_stats_1:
    loop_team = team_names[team_index]
    roster['Team'] = loop_team
    team_index = team_index + 1
    

# combine all stats of each year spans into their own separate dataframe using concat

concat_final_4 = pd.concat(all_player_final_stats_4, ignore_index=True)

concat_final_3 = pd.concat(all_player_final_stats_3, ignore_index=True)

concat_final_2 = pd.concat(all_player_final_stats_2, ignore_index=True)

concat_final_1 = pd.concat(all_player_final_stats_1, ignore_index=True)


################################################################################################

# get defensive stats from nba website

def get_nba_stats(url):
    
    # use url variable and request info from nba site, turn to json file
    json_file = requests.get(url, headers=headers).json()

    # from json file, assign variables that will represent the rows of the info and the headers/columns
    data = json_file['resultSets'][0]['rowSet']
    columns = json_file['resultSets'][0]['headers']
    
    # turn records of stats into a dataframe
    nba_stats = pd.DataFrame.from_records(data, columns=columns) 
    
    return(nba_stats)

# get defensive stats using stats.nba.com url (2020-21 season)
defense_stats = get_nba_stats('https://stats.nba.com/stats/leaguedashptdefend?College=&Conference=&Country=&DateFrom=&DateTo=&DefenseCategory=Overall&Division=&DraftPick=&DraftYear=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season=2020-21&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=')

# get rid of columns that we don't need
defense_stats = defense_stats.drop(columns=['CLOSE_DEF_PERSON_ID', 'PLAYER_LAST_TEAM_ID', 'PLAYER_LAST_TEAM_ABBREVIATION', 'PLAYER_POSITION', 'AGE', 'GP', 'G', 'FREQ'])

# replace names with correct names to be consistent with basketball-reference
defense_stats['PLAYER_NAME'].replace({'Robert Williams':'Robert Williams III','Marcus Morris':'Marcus Morris Sr.','Derrick Walton':'Derrick Walton Jr.','Juan Hernangomez':'Juancho Hernangomez','Sviatoslav Mykhailiuk':'Svi Mykhailiuk','Zach Norvell':'Zach Norvell Jr.','Lonnie Walker':'Lonnie Walker IV','Charlie Brown':'Charles Brown Jr.','C.J. Miles':'CJ Miles','Wesley Iwundu':'Wes Iwundu','J.J. Redick':'JJ Redick','B.J. Johnson':'BJ Johnson','Melvin Frazier':'Melvin Frazier Jr.','Otto Porter':'Otto Porter Jr.','James Ennis':'James Ennis III','Danuel House':'Danuel House Jr.','Brian Bowen':'Brian Bowen II','Kevin Knox':'Kevin Knox II','Frank Mason III':'Frank Mason','Harry Giles':'Harry Giles III','T.J. Leaf':'TJ Leaf','J.R. Smith':'JR Smith','Vince Edwards':'Vincent Edwards','D.J. Stephens':'DJ Stephens','Mitch Creek':'Mitchell Creek','R.J. Hunter':'RJ Hunter','Wade Baldwin':'Wade Baldwin IV'},inplace=True)

# round numbers to three digits
defense_stats['D_FG_PCT'] = round(defense_stats['D_FG_PCT'], 3)
defense_stats['PCT_PLUSMINUS'] = round(defense_stats['PCT_PLUSMINUS'], 3)

### list of names that don't match up to our existing names of nba players
# this is usally due to titles (like III or sr./jr.) or letter accents
result_names = [
    'Bogdan Bogdanovic',
    'Timothe Luwawu-Cabarrot',
    'Dennis Schroder',
    'Robert Williams III',
    'Juancho Hernangomez',
    'Nic Claxton',
    'Nikola Vucevic',
    'Luka Doncic',
    'Kristaps Porzingis',
    'Boban Marjanovic',
    'Nikola Jokic',
    'P.J. Dozier',
    'Vlatko Cancar',
    'Otto Porter Jr.',
    'Danuel House Jr.',
    'Marcus Morris Sr.',
    'Jonas Valanciunas',
    'Tomas Satoransky',
    'Willy Hernangomez',
    'Kevin Knox II',
    'Luka Samanic',
    'Theo Maledon',
    'Dario Saric',
    'Jusuf Nurkic',
    'Lonnie Walker IV',
    'Goran Dragic',
    'Bojan Bogdanovic',
    'Davis Bertans',
    ]

# create list of replacement names that are consistent with the names we have for our scraped data
replacement_names = [
    'Bogdan Bogdanović',
    'Timothé Luwawu-Cabarrot',
    'Dennis Schröder',
    'Robert Williams',
    'Juan Hernangómez',
    'Nicolas Claxton',
    'Nikola Vučević',
    'Luka Dončić',
    'Kristaps Porziņģis',
    'Boban Marjanović',
    'Nikola Jokić',
    'PJ Dozier',
    'Vlatko Čančar',
    'Otto Porter',
    'Danuel House',
    'Marcus Morris',
    'Jonas Valančiūnas',
    'Tomáš Satoranský',
    'Willy Hernangómez',
    'Kevin Knox',
    'Luka Šamanić',
    'Théo Maledon',
    'Dario Šarić',
    'Jusuf Nurkić',
    'Lonnie Walker',
    'Goran Dragić',
    'Bojan Bogdanović',
    'Dāvis Bertāns'
]

# correct names from nba stats site to be consistent with replacement names (names on baskatball-ref)
i = 0
for name in result_names:
    for index, row in defense_stats.iterrows():
        if name == row['PLAYER_NAME']:
            # replacing names in defense_stats df with correct names 
            defense_stats = defense_stats.replace(row['PLAYER_NAME'], replacement_names[i])
            print(replacement_names[i] + ' ' + row['PLAYER_NAME'])
    i+=1
    
# check if players in defense stats df are in our concat df
for index, row in defense_stats.iterrows():
    is_in_result = False
    
    for index2, row2 in concat_final_1.iterrows():
        if row2['Name'] == row['PLAYER_NAME']:
            
            is_in_result = True
    
    # if player from defense stats isn't in our concat df, drop the player from the defense df
    if is_in_result != True:
        print(row['PLAYER_NAME'])
        defense_stats = defense_stats.drop(labels=index, axis=0)
        
#########################################################################
# attach player roles to stats dataframes
# read in csv files of roles

# if replicating project, make sure to change pathway for your csv files
trad_big = pd.read_csv (r'C:\Users\kshin\Desktop\Sports Comps\trad_big.csv')   #read the csv file (put 'r' before the path string to address any special characters in the path, such as '\'). Don't forget to put the file name at the end of the path + ".csv"
ball_dom = pd.read_csv (r'C:\Users\kshin\Desktop\Sports Comps\ball_dom.csv')
high_usg_big = pd.read_csv (r'C:\Users\kshin\Desktop\Sports Comps\high_usg_big.csv')
off_bench = pd.read_csv (r'C:\Users\kshin\Desktop\Sports Comps\off_bench.csv')
role_big = pd.read_csv (r'C:\Users\kshin\Desktop\Sports Comps\role_big.csv')
role_guard = pd.read_csv (r'C:\Users\kshin\Desktop\Sports Comps\role_guard.csv')
secondary = pd.read_csv (r'C:\Users\kshin\Desktop\Sports Comps\secondary.csv')
vers_forwards = pd.read_csv (r'C:\Users\kshin\Desktop\Sports Comps\vers_forwards.csv')


### replace names with correct versions in our role df
# similar to what we did for our defense stats
i = 0
for name in result_names:
    for index, row in trad_big.iterrows():
        if name == row['player']:
            trad_big = trad_big.replace(row['player'], replacement_names[i])
            print(replacement_names[i] + ' ' + row['player'])
    i+=1
    
# repeat for all role df
i = 0
for name in result_names:
    for index, row in ball_dom.iterrows():
        if name == row['player']:
            ball_dom = ball_dom.replace(row['player'], replacement_names[i])
            print(replacement_names[i] + ' ' + row['player'])
    i+=1
    
i = 0
for name in result_names:
    for index, row in high_usg_big.iterrows():
        if name == row['player']:
            high_usg_big = high_usg_big.replace(row['player'], replacement_names[i])
            print(replacement_names[i] + ' ' + row['player'])
    i+=1

i = 0
for name in result_names:
    for index, row in off_bench.iterrows():
        if name == row['player']:
            off_bench = off_bench.replace(row['player'], replacement_names[i])
            print(replacement_names[i] + ' ' + row['player'])
    i+=1
    
i = 0
for name in result_names:
    for index, row in role_big.iterrows():
        if name == row['player']:
            role_big = role_big.replace(row['player'], replacement_names[i])
            print(replacement_names[i] + ' ' + row['player'])
    i+=1

i = 0
for name in result_names:
    for index, row in role_guard.iterrows():
        if name == row['player']:
            role_guard = role_guard.replace(row['player'], replacement_names[i])
            print(replacement_names[i] + ' ' + row['player'])
    i+=1

i = 0
for name in result_names:
    for index, row in secondary.iterrows():
        if name == row['player']:
            secondary = secondary.replace(row['player'], replacement_names[i])
            print(replacement_names[i] + ' ' + row['player'])
    i+=1

i = 0
for name in result_names:
    for index, row in vers_forwards.iterrows():
        if name == row['player']:
            vers_forwards = vers_forwards.replace(row['player'], replacement_names[i])
            print(replacement_names[i] + ' ' + row['player'])
    i+=1
 
##################################################################################################
    
### combine roles to stats dataframes

# create temp spot for player roles
concat_final_1['Role'] = 'temp'

for index, row in trad_big.iterrows():
    # loop through players in role df
    i = 0
    for index2, row2 in concat_final_1.iterrows():
        if row['player'] == row2['Name']:
            # if players in concat match player in role df, assign the role
            concat_final_1.at[i, 'Role'] = 'Traditional Big'
        i+=1
    
# repeat process for all role df
for index, row in ball_dom.iterrows():
    i = 0
    for index2, row2 in concat_final_1.iterrows():
        if row['player'] == row2['Name']:
            concat_final_1.at[i, 'Role'] = 'Ball Dominant'
        i+=1
    
for index, row in high_usg_big.iterrows():
    i = 0
    for index2, row2 in concat_final_1.iterrows():
        if row['player'] == row2['Name']:
            concat_final_1.at[i, 'Role'] = 'High Usage Big'
        i+=1
        
for index, row in off_bench.iterrows():
    i = 0
    for index2, row2 in concat_final_1.iterrows():
        if row['player'] == row2['Name']:
            concat_final_1.at[i, 'Role'] = 'Off Bench'
        i+=1
    
for index, row in role_big.iterrows():
    i = 0
    for index2, row2 in concat_final_1.iterrows():
        if row['player'] == row2['Name']:
            concat_final_1.at[i, 'Role'] = 'Roleplaying Big'
        i+=1

for index, row in role_guard.iterrows():
    i = 0
    for index2, row2 in concat_final_1.iterrows():
        if row['player'] == row2['Name']:
            concat_final_1.at[i, 'Role'] = 'Roleplaying Guard'
        i+=1

for index, row in secondary.iterrows():
    i = 0
    for index2, row2 in concat_final_1.iterrows():
        if row['player'] == row2['Name']:
            concat_final_1.at[i, 'Role'] = 'Secondary Playmaker'
        i+=1

for index, row in vers_forwards.iterrows():
    i = 0
    for index2, row2 in concat_final_1.iterrows():
        if row['player'] == row2['Name']:
            concat_final_1.at[i, 'Role'] = 'Versatile Forward'
        i+=1
        


#######################################################################
### attach defense stats to concat
# only using concat_1 for now but process can be used for all ranges of seasons

concat_final_1_defense = pd.merge(concat_final_1, defense_stats, left_on='Name', right_on='PLAYER_NAME')

#######################################################################


# scrape slary information using similar functions
def get_salary(team):
    
    # set url to contracts page on basketball-ref
    team_url = (f'https://www.basketball-reference.com/contracts/{team}.html')

    team_res = requests.get(team_url)

    #BeautifulSoup Library parses the content of an HTML document, in this case clips_res
    team_soup = BeautifulSoup(team_res.content, 'lxml')
    
    # scrape table with contracts info
    team_salaries = team_soup.find(name = 'table', attrs = {'id' : 'contracts'})

    #create list of dictionaries
    salary_info = []

    print(team)
    
    for row in team_salaries('tr')[2:]:
        print(row)
        player = {}
        
        # we will be using try since players have varying ranges in salary info
        try:
            player['Name'] = row.find('th', {'data-stat' : 'player'}).text
            print(player['Name'])
            player['Age'] = row.find('td', {'data-stat' : 'age_today'}).text
            try:
                # this try is for scraping current year contract info
                player['y1'] = row.find('td', {'data-stat' : 'y1'}).text
                
                # create variable to hold non numeric characters
                remove_characters = '$,'
                
                salary_num = row.find('td', {'data-stat' : 'y1'}).text
                # get rid of non numeric characters so we can get int value
                for character in remove_characters:
                    salary_num = salary_num.replace(character,"")
                player['Int'] = int(salary_num)
                    
                try:    
                    # repeat process from y1 contract for next year contract (y2)
                    player['y2'] = row.find('td', {'data-stat' : 'y2'}).text
                    
                    remove_characters = '$,'
                    salary_num = row.find('td', {'data-stat' : 'y2'}).text
                    for character in remove_characters:
                        salary_num = salary_num.replace(character,"")
                    player['Int2'] = int(salary_num)
                    if salary_num == 0:
                        player['Int2'] = 0
                except:
                    player['Int2'] = 0
                
                try:
                    # repeat process for year3 contract
                    player['y3'] = row.find('td', {'data-stat' : 'y3'}).text
                    
                    remove_characters = '$,'
                    salary_num = row.find('td', {'data-stat' : 'y3'}).text
                    for character in remove_characters:
                        salary_num = salary_num.replace(character,"")
                    player['Int3'] = int(salary_num)
                    if salary_num == 0:
                            player['Int3'] = 0
                except:
                    player['Int3'] = 0
                
            except:
                # if player has no contract info, set all int values to 0
                player['Int'] = 0
                player['Int2'] = 0
                player['Int3'] = 0
                
            # assign free agent status based on how many years they have on their contracts
            if player['Int'] == 0:
                player['Status'] = 'Two-Way'
            elif player['Int2'] == 0:
                # free agent after this season
                player['Status'] = 'Upcoming FA'
            elif player['Int3'] == 0:
                # free agent after next season
                player['Status'] = 'Future FA'
            elif player['Int'] > 78000000:
                # label team totals values
                player['Status'] = 'Team Totals'
            else:
                # players with int3>0 are multiyear players, (under contract for 3+ years)
                player['Status'] = 'Multiyear Player'
            
            # assign team value to players for organization
            player['Team'] = team
            salary_info.append(player)
        except:
            salary_info.append(player)
            
    team_salary_df = pd.DataFrame(salary_info)
    return team_salary_df

# loop through teams and get all player salaries
team_salaries = []

for team in team_names:
    salaries = get_salary(team)
    team_salaries.append(salaries)

# concat salary values    
concat_salary = pd.concat(team_salaries, ignore_index=True)

# merge defense and salary stats to concat stats

concat_final_1_defense = pd.merge(concat_final_1_defense, concat_salary, left_on='Name', right_on='Name')

concat_final_1 = pd.merge(concat_final_1, concat_salary, left_on='Name', right_on='Name')

# get rid of columns that are repeat info
concat_final_1_defense = concat_final_1_defense.drop(columns = 'Age_y')
concat_final_1_defense = concat_final_1_defense.drop(columns = 'Team_y')
concat_final_1_defense = concat_final_1_defense.drop(columns = 'PLAYER_NAME')

# get rid of columns that are repeat info
concat_final_1 = concat_final_1.drop(columns = 'Age_y')
concat_final_1 = concat_final_1.drop(columns = 'Team_y')


################################################################################################

#turn dataframes into csv files to use DBbrowser and make database
concat_final_1.to_csv('new_concat_1.csv', index=False, encoding='utf-8')

# uncomment section here for stats on different spans of years 
'''
concat_final_3.to_csv('new_concat_3.csv', index=False, encoding='utf-8')

concat_final_2.to_csv('new_concat_2.csv', index=False, encoding='utf-8')

concat_final_1.to_csv('new_concat_1.csv', index=False, encoding='utf-8')
'''

concat_final_1_defense.to_csv('new_concat_1_defense.csv', index=False, encoding='utf-8')


#################################################################################################

# get four factor stats for each team

def get_four_factors():
    
    # assign site url to variable
    team_url = ('https://cleaningtheglass.com/stats/league/fourfactors#')
    
    # make request using site url
    team_res = requests.get(team_url)

    #BeautifulSoup Library parses the content of an HTML document
    team_soup = BeautifulSoup(team_res.content, 'lxml')
    
    # identify table we want to scrape data from (league four factors)
    league_stats = team_soup.find(name = 'table', attrs = {'id' : 'league_four_factors'})
    
    # create empty list to hold four factors stats
    four_factors = []
    
    # create index variable and set it to 0
    index = 0
    
    # loop through each row of table to get team four factors stats (each row is a different nba team)
    for row in league_stats('tr')[0:]:
        
        # create dict that will hold stat values for team's four factors
        stats = {}
        
        # go through each row and based on column index, retrieve the values of the four factors and league rankings
        for col in row:
            
            # column to help with determining where we are in loop/help with bugs
            print(col.string)
            
            # based on index of column, give stat the appropriate name and add value to our dict
            if index == 3:
                stats['Team'] = col.string
            elif index == 5:
                stats['Wins'] = col.string
            elif index == 7:
                stats['Losses'] = col.string
            elif index == 11:
                stats['Diff Rank'] = col.string
            elif index == 13:
                stats['Diff'] = col.string
            elif index == 17:
                stats['Off Pts/Poss Rank'] = col.string
            elif index == 19:
                stats['Off Pts/Poss'] = col.string
            elif index == 21:
                stats['EFG% Rank'] = col.string
            elif index == 23:
                stats['EFG%'] = col.string
            elif index == 25:
                stats['TOV% Rank'] = col.string
            elif index == 27:
                stats['TOV%'] = col.string
            elif index == 29:
                stats['ORb% Rank'] = col.string
            elif index == 31:
                stats['ORb%'] = col.string
            elif index == 33:
                stats['FT Rate Rank'] = col.string
            elif index == 35:
                stats['FT Rate'] = col.string
            elif index == 39:
                stats['Def Pts/Poss Rank'] = col.string
            elif index == 41:
                stats['Def Pts/Poss'] = col.string
            elif index == 43:
                stats['Def EFG% Ramk'] = col.string
            elif index == 45:
                stats['Def EFG%'] = col.string
            elif index == 47:
                stats['Def TOV% Rank'] = col.string
            elif index == 49:
                stats['Def TOV%'] = col.string
            elif index == 51:
                stats['Def ORb% Rank'] = col.string
            elif index == 53:
                stats['Def ORb%'] = col.string
            elif index == 55:
                stats['Def FT Rate Rank'] = col.string
            elif index == 57:
                stats['Def FT Rate'] = col.string
            
            # add one to index so that it will match the column index    
            index += 1
            # print index to know where we are/help with bugs
            print(index)
        
        # append stats dict to our four factors list
        four_factors.append(stats)
        # reset index to 0
        index = 0
    
    # turn four_factors list of stats into df        
    fourfactors_df = pd.DataFrame(four_factors)
    
    # return df of four factors stats
    return(fourfactors_df)
    
# use get_four_factors function to get df of four factors stats from cleaning the glass site
df_ff = get_four_factors()

# turn four factors df into csv file
df_ff.to_csv('df_ff.csv', index=False, encoding='utf-8')


