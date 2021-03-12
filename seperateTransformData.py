from datetime import datetime
from sportsipy.ncaab.boxscore import Boxscores
from sportsipy.ncaab.schedule import Schedule
from sportsipy.ncaab.boxscore import Boxscore
import pandas as pd

def get_game_data():
    # Pulls all games between and including November 15, 2016 and March 10, 2019
    games = Boxscores(datetime(2019, 2, 11), datetime(2019, 3, 10))
    games_str = str(games.games)
    game_URIs = games_str.split('boxscore\': \'')
    game_URIs.pop(0)

    list_games = []

    for g in game_URIs:
        end_index = g.find('\'')
        updated_URI = g[:end_index]
        list_games.append(str(updated_URI))

    # df = pd.DataFrame()

    for game in list_games:
        game_data = Boxscore(game)
        game_dataframe = game_data.dataframe
        game_dataframe.to_csv('sportsData.csv', mode='a', header=False)
        # df = df.append(game_dataframe)

    # print(df)
    # df.to_csv('sportsData.csv')


def transform_data(teamData, gamesData):
    team_data = pd.read_csv(teamData)
    games_data = pd.read_csv(gamesData)
    
    df = pd.DataFrame()

    cnt = 0
    for index, row in games_data.iterrows():
        winner = row['winning_abbr']
        loser = row['losing_abbr']
        winner_score = 0
        loser_score = 0

        if (row['winner'] == 'Home'):
            winner_score = row['home_points']
            loser_score = row['away_points']
        else:
            loser_score = row['home_points']
            winner_score = row['away_points']

        year = int(row['year'])

        d = {
            'winner': [winner], 
            'loser': [loser],
            'winner_score': [winner_score],
            'loser_score': [loser_score],
            'year': [year]
        }

        winRow = pd.DataFrame(data=d, index=[cnt])
        winRow['joincol'] = '1'
        loseRow = pd.DataFrame(data=d, index=[cnt])
        loseRow['joincol'] = '1'
        

    
        if (int(year) == 2016):
            year = 2017

        win = pd.DataFrame()
        win = win.append(team_data.loc[(team_data['abbreviation'] == winner) & (team_data['year'] == year),'assist_percentage':'wins'])

        lose = pd.DataFrame()
        lose = lose.append(team_data.loc[(team_data['abbreviation'] == loser) & (team_data['year'] == year),'assist_percentage':'wins'])

        if (not win.empty) and (not lose.empty):
        

            lose = lose.astype(float)
            win = win.astype(float)
            win['joincol'] = '1'
            lose['joincol'] = '1'

            # combinedWin = pd.DataFrame()
            # combinedLose = pd.DataFrame()
            

            # win = win.append(lose)
            # combinedWin = combinedWin.append(win.iloc[0] - win.iloc[1], ignore_index=True)
            # combinedWin['joincol'] = '1'
            # combinedWin['did_win'] = '1'
            # combinedWin = combinedWin.astype(object)
            winRow = pd.merge(left=win,right=lose, on='joincol', how='outer')
            winRow['did_win'] = '1'

            df = df.append(winRow)

            # combinedLose = combinedLose.append(win.iloc[1] - win.iloc[0], ignore_index=True)
            # combinedLose['joincol'] = '1'
            # combinedLose['did_win'] = '0'
            # combinedLose = combinedLose.astype(object)
            loseRow = pd.merge(left=lose,right=win, on='joincol', how='outer')
            loseRow['did_win'] = '0'

            df = df.append(loseRow)



        cnt += 1


    df.to_csv('seperateTransformData.csv')


transform_data('teamData.csv', 'sportsData.csv')










# Prints a dictionary of all results from November 11, 2017 and November 12,
# 2017
#print(games.games)
# for game in games.games:
#     #df = game.dataframe
#     print(game)
#     print(games.games)
#     print('\n\n\n')

# from sportsipy.ncaab.boxscore import Boxscore

# game_data = Boxscore('2018-04-02-21-purdue')
# print(game_data.home_points)  # Prints 79
# print(game_data.away_points)  # Prints 62
# df = game_data.dataframe  # Returns a Pandas DataFrame of game metrics



# purdue_schedule = Schedule('purdue')
# for game in purdue_schedule:
#     gameURI = game.boxscore_index 

#     game_data = Boxscore('2021-03-06-14-purdue')
#     print(game_data.home_points)
    
    
