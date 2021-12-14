import pandas as pd

### load in csv files of our scraped data, change file paths if reproducing project
concat_4 = pd.read_csv(r'C:\Users\kshin\Desktop\Sports Comps\concat_1_ranks.csv')
concat_4_defense = pd.read_csv(r'C:\Users\kshin\Desktop\Sports Comps\concat_1_def_ranks.csv')

four_factors = pd.read_csv(r'C:\Users\kshin\Desktop\Sports Comps\df_ff.csv')

### clean df
four_factors = four_factors.fillna(0)
four_factors = four_factors.drop(labels=[0, 1], axis=0)

### turn df rank columns into numeric values
four_factors['Off Pts/Poss Rank'] = four_factors['Off Pts/Poss Rank'].astype(int)
four_factors['EFG% Rank'] = four_factors['EFG% Rank'].astype(int)
four_factors['TOV% Rank'] = four_factors['TOV% Rank'].astype(int)
four_factors['ORb% Rank'] = four_factors['ORb% Rank'].astype(int)
four_factors['FT Rate Rank'] = four_factors['FT Rate Rank'].astype(int)

########################################################################################

# get rid of any possible repeat players in dataframe
for index, row in concat_4_defense.iterrows():
    count = 0
    for index2, row2 in concat_4_defense.iterrows():
        if row['Name'] == row2['Name']:
            count += 1
            if count > 1:
                concat_4_defense = concat_4_defense.drop(index)


########################################################################################

### test out comparing players and making algo
def suggest_players(team, abbr):
    # create temp values for the four factors
    temp_values = {
        'temp_off_pts_poss': 0,
        'temp_off_efg': 0,
        'temp_off_tov': 0,
        'temp_off_orb': 0,
        'temp_off_ft': 0,
        'temp_def_pts_poss': 0,
        'temp_def_efg': 0,
        'temp_def_tov': 0,
        'temp_def_orb': 0,
        'temp_def_ft': 0,
    }

    # check to see which of the four factors are below average for designated team
    for index, row in four_factors.iterrows():
        if row['Team'] == team:
            if row['Off Pts/Poss Rank'] > 15: # rankings above 15 mean team is below league average
                temp_values['temp_off_pts_poss'] = row['Off Pts/Poss Rank'] - 15
            if row['EFG% Rank'] > 15:
                temp_values['temp_off_efg'] = row['EFG% Rank'] - 15
            if row['TOV% Rank'] > 15:
                temp_values['temp_off_tov'] = row['TOV% Rank'] - 15
            if row['ORb% Rank'] > 15:
                temp_values['temp_off_orb'] = row['ORb% Rank'] - 15
            if row['FT Rate Rank'] > 15:
                temp_values['temp_off_ft'] = row['FT Rate Rank'] - 15
            if row['Def Pts/Poss Rank'] > 15:
                temp_values['temp_def_pts_poss'] = row['Def Pts/Poss Rank'] - 15
            if row['Def EFG% Ramk'] > 15:
                temp_values['temp_def_efg'] = row['Def EFG% Ramk'] - 15
            if row['Def TOV% Rank'] > 15:
                temp_values['temp_def_tov'] = row['Def TOV% Rank'] - 15
            if row['Def ORb% Rank'] > 15:
                temp_values['temp_def_orb'] = row['Def ORb% Rank'] - 15
            if row['Def FT Rate Rank'] > 15:
                temp_values['temp_def_ft'] = row['Def FT Rate Rank'] - 15

    # create dataframe of team roster
    team_roster = []

    for index, row in concat_4_defense.iterrows():
        if row['Team_x'] == abbr:  ### change abbreviation
            team_roster.append(row)

    team_roster = pd.DataFrame(team_roster)

    for index, row in team_roster.iterrows():
        count = 0
        for index2, row2 in team_roster.iterrows():
            if row['Name'] == row2['Name']:
                count += 1
                if count > 1:
                    print(row['Name'])
                    print(index)
                    team_roster = team_roster.drop(index)

    ### sort value dict in descending order
    sorted_values = sorted(temp_values.items(), key=lambda x: x[1], reverse=True)

    ### loop through our sorted list and find weaknesses
    weakness_list = []

    for pair in sorted_values:
        if pair[1] > 0:
            weakness_list.append(pair[0])


    ### create dataframe of weaknesses and which stat categories fall within them

    # first create dictionaries of each weakness

    off_pts_poss = ['EFG% Rank', 'PPG Rank', 'FGM Rank', 'FG% Rank']
    off_efg = ['EFG% Rank', 'FG% Rank', '3pt% Rank', '2pt% Rank']
    off_tov = ['TO Rank']
    off_orb = ['ORb Rank', 'TRb Rank']
    off_ft = ['FTM Rank', 'FTA Rank', 'FT% Rank']
    def_pts_poss = ['PCT_PM Rank', 'D_FG% Rank', 'BLK Rank', 'STL Rank']
    def_efg = ['PCT_PM Rank', 'D_FG% Rank', 'BLK Rank']
    def_tov = ['STL Rank']
    def_orb = ['DRb Rank', 'TRb Rank']
    def_ft = ['PF Rank', 'STL Rank']

    ### determine which categories to sort by

    
    tuple_list = []
    
    ### loop through weakness list
    ### enumerate adds indexes to the weaknesses
    for index, weakness in enumerate(weakness_list):

        ### find first weakness and make weight of stats == 3

        if weakness == 'temp_off_pts_poss' and index == 0:
            for stat in off_pts_poss:
                temp_tuple = (stat, 3)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_efg' and index == 0:
            for stat in off_efg:
                temp_tuple = (stat, 3)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_tov' and index == 0:
            for stat in off_tov:
                temp_tuple = (stat, 3)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_orb' and index == 0:
            for stat in off_orb:
                temp_tuple = (stat, 3)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_ft' and index == 0:
            for stat in off_ft:
                temp_tuple = (stat, 3)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_pts_poss' and index == 0:
            for stat in def_pts_poss:
                temp_tuple = (stat, 3)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_efg' and index == 0:
            for stat in def_efg:
                temp_tuple = (stat, 3)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_tov' and index == 0:
            for stat in def_tov:
                temp_tuple = (stat, 3)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_orb' and index == 0:
            for stat in def_orb:
                temp_tuple = (stat, 3)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_ft' and index == 0:
            for stat in def_ft:
                temp_tuple = (stat, 3)
                tuple_list.append(temp_tuple)

        ### find second most important weakness and make weight of stats related == 2

        if weakness == 'temp_off_pts_poss' and index == 1:
            for stat in off_pts_poss:
                temp_tuple = (stat, 2)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_efg' and index == 1:
            for stat in off_efg:
                temp_tuple = (stat, 2)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_tov' and index == 1:
            for stat in off_tov:
                temp_tuple = (stat, 2)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_orb' and index == 1:
            for stat in off_orb:
                temp_tuple = (stat, 2)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_ft' and index == 1:
            for stat in off_ft:
                temp_tuple = (stat, 2)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_pts_poss' and index == 1:
            for stat in def_pts_poss:
                temp_tuple = (stat, 2)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_efg' and index == 1:
            for stat in def_efg:
                temp_tuple = (stat, 2)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_tov' and index == 1:
            for stat in def_tov:
                temp_tuple = (stat, 2)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_orb' and index == 1:
            for stat in def_orb:
                temp_tuple = (stat, 2)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_ft' and index == 1:
            for stat in def_ft:
                temp_tuple = (stat, 2)
                tuple_list.append(temp_tuple)

        ### find rest of stats related to remaining weaknesses and make weights == 1

        if weakness == 'temp_off_pts_poss' and index > 1:
            for stat in off_pts_poss:
                temp_tuple = (stat, 1)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_efg' and index > 1:
            for stat in off_efg:
                temp_tuple = (stat, 1)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_tov' and index > 1:
            for stat in off_tov:
                temp_tuple = (stat, 1)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_orb' and index > 1:
            for stat in off_orb:
                temp_tuple = (stat, 1)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_off_ft' and index > 1:
            for stat in off_ft:
                temp_tuple = (stat, 1)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_pts_poss' and index > 1:
            for stat in def_pts_poss:
                temp_tuple = (stat, 1)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_efg' and index > 1:
            for stat in def_efg:
                temp_tuple = (stat, 1)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_tov' and index > 1:
            for stat in def_tov:
                temp_tuple = (stat, 1)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_orb' and index > 1:
            for stat in def_orb:
                temp_tuple = (stat, 1)
                tuple_list.append(temp_tuple)
        if weakness == 'temp_def_ft' and index > 1:
            for stat in def_ft:
                temp_tuple = (stat, 1)
                tuple_list.append(temp_tuple)

    ###################################################################################
    
    # create list to hold th names
    
    th_list = []
    
    # loop through weakness_list and append th names to th_list
    for weakness in weakness_list:

        # find weaknesses and add relevant stats to th_list

        if weakness == 'temp_off_pts_poss':
            for stat in off_pts_poss:
                th_list.append(stat)
        if weakness == 'temp_off_efg':
            for stat in off_efg:
                th_list.append(stat)
        if weakness == 'temp_off_tov':
            for stat in off_tov:
                th_list.append(stat)
        if weakness == 'temp_off_orb':
            for stat in off_orb:
                th_list.append(stat)
        if weakness == 'temp_off_ft':
            for stat in off_ft:
                th_list.append(stat)
        if weakness == 'temp_def_pts_poss':
            for stat in def_pts_poss:
                th_list.append(stat)
        if weakness == 'temp_def_efg':
            for stat in def_efg:
                th_list.append(stat)
        if weakness == 'temp_def_tov':
            for stat in def_tov:
                th_list.append(stat)
        if weakness == 'temp_def_orb':
            for stat in def_orb:
                th_list.append(stat)
        if weakness == 'temp_def_ft':
            for stat in def_ft:
                th_list.append(stat)
    
    
    ###################################################################################

    ### create list to hold roster tallies
    roster_counts = []

    ### gather tallies for worst five players of each important stat, append to roster_counts
    for pair in tuple_list:
        i = 0
        team_roster = team_roster.sort_values(by=pair[0])
        for index, player in team_roster.iterrows():
            if i < 5:
                i += 1
                player_count = (player['Name'], pair[1])
                roster_counts.append(player_count)

    ### create list of all roster players for us to add up tallies in
    roster_sums = []
    for index, row in team_roster.iterrows():
        player = {}
        player['Name'] = row['Name']
        player['Count'] = 0
        player['Role'] = row['Role']
        player['Status'] = row['Status']
        roster_sums.append(player)

    ### add up tallies
    for tally in roster_counts:
        for player_sum in roster_sums:
            if tally[0] == player_sum['Name']:
                player_sum['Count'] = player_sum['Count'] + tally[1]

    ### sort list of players by their counts
    roster_sums = sorted(roster_sums, key=lambda i: i['Count'], reverse=True)

    ### get the roles for the top 3 players with highest counts
    list_weak_roles = []
    list_weak_players = []
    
    for i in [0, 1, 2]:
        list_weak_roles.append(roster_sums[i]['Role'])
        list_weak_players.append(roster_sums[i]['Name'])

    ### get rid of any repeat roles
    for role in list_weak_roles:
        count = 0
        for role2 in list_weak_roles:
            if role == role2:
                count += 1
                if count > 1:
                    list_weak_roles.remove(role)

    ### make a temp copy of concat_4_defense
    temp_concat = concat_4_defense

    # get rid of all players with irrelevant roles
    for index, row in temp_concat.iterrows():
        if len(list_weak_roles) == 3:
            if row['Role'] != list_weak_roles[0] and row['Role'] != list_weak_roles[1] and row['Role'] != \
                    list_weak_roles[2]:
                temp_concat = temp_concat.drop(index)
        elif len(list_weak_roles) == 2:
            if row['Role'] != list_weak_roles[0] and row['Role'] != list_weak_roles[1]:
                temp_concat = temp_concat.drop(index)
        else:
            if row['Role'] != list_weak_roles[0]:
                temp_concat = temp_concat.drop(index)

    # get rid of players from designated team (don't want to suggest players already on team)
    for index, row in temp_concat.iterrows():
        if row['Team_x'] == abbr:
            temp_concat = temp_concat.drop(index)

    ### create list to hold roster tallies
    fa_counts = []

    ### gather tallies for best ten players of each important stat, append to fa_count
    for pair in tuple_list:
        i = 0
        temp_concat = temp_concat.sort_values(by=pair[0], ascending=False)
        for index, player in temp_concat.iterrows():
            if i < 10:
                i += 1
                player_count = (player['Name'], pair[1])
                fa_counts.append(player_count)

    ### create list of all fa players for us to add up tallies in
    fa_sums = []
    for index, row in temp_concat.iterrows():
        player = {}
        player['Name'] = row['Name']
        player['Count'] = 0
        player['Role'] = row['Role']
        player['Status'] = row['Status']
        fa_sums.append(player)

    ### add up tallies
    for tally in fa_counts:
        for player_sum in fa_sums:
            if tally[0] == player_sum['Name']:
                player_sum['Count'] = player_sum['Count'] + tally[1]

    ### sort free agents by their tallies
    fa_sums = sorted(fa_sums, key=lambda i: i['Count'], reverse=True)

    ### create dataframes for each type of status
    upcoming_fa = temp_concat
    future_fa = temp_concat
    multiyear = temp_concat

    ### get rid of non-upcoming free agents/two-way players
    for index, row in upcoming_fa.iterrows():
        count = 0
        if row['Status'] == 'Upcoming FA' or row['Status'] == 'Two-Way':
            count += 1
        if count == 0:
            upcoming_fa = upcoming_fa.drop(index)

    ### get rid of non-future free agents
    for index, row in future_fa.iterrows():
        count = 0
        if row['Status'] == 'Future FA':
            count += 1
        if count == 0:
            future_fa = future_fa.drop(index)

    ### get rid of non-multiyear players
    for index, row in multiyear.iterrows():
        count = 0
        if row['Status'] == 'Multiyear Player':
            count += 1
        if count == 0:
            multiyear = multiyear.drop(index)

    ### get rid of players in fa_sums with a 0 count
    for i in range(len(fa_sums) - 1, 0, -1):
        if fa_sums[i]['Count'] == 0:
            del fa_sums[i]

    ### create list that will turn into dataframe for upcoming fa
    upcoming_fa_df = []

    ### appending players to list so we can keep the order of fa_sums
    for player in fa_sums:
        for index, row in upcoming_fa.iterrows():
            if player['Name'] == row['Name']:
                upcoming_fa_df.append(row)

    ### turn list into df
    upcoming_fa_df = pd.DataFrame(upcoming_fa_df)

    ### create list that will turn into dataframe for upcoming fa
    future_fa_df = []

    ### appending players to list so we can keep the order of fa_sums
    for player in fa_sums:
        for index, row in future_fa.iterrows():
            if player['Name'] == row['Name']:
                future_fa_df.append(row)

    ### turn list into df
    future_fa_df = pd.DataFrame(future_fa_df)

    ### create list that will turn into dataframe for upcoming fa
    multiyear_df = []

    ### appending players to list so we can keep the order of fa_sums
    for player in fa_sums:
        for index, row in multiyear.iterrows():
            if player['Name'] == row['Name']:
                multiyear_df.append(row)

    ### turn list into df
    multiyear_df = pd.DataFrame(multiyear_df)

    return upcoming_fa_df, future_fa_df, multiyear_df, list_weak_players, th_list

