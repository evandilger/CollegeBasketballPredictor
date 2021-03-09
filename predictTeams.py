from sportsipy.ncaab.teams import Team
from sklearn import svm
from sklearn.model_selection import train_test_split
import pandas as pd

training_data = pd.read_csv('transformData.csv')
clf = svm.SVC()

def get_teams():
    teams = list(list())
    team_names = pd.read_csv('teamData.csv', skipinitialspace=True, usecols=['abbreviation'])

    while True:
        while True:
            team1 = input('Team 1: ')
            if not team_names.loc[team_names['abbreviation'] == team1].empty:
                break
            else:
                print("Invalid team (ohio state --> OHIO-STATE)")
        print('vs')
        while True:
            team2 = input('Team 2: ')
            if not team_names.loc[team_names['abbreviation'] == team2].empty:
                break
            else:
                print("Invalid team")

        teams.append([team1, team2])
        cont = input('More Games? (y/n): ')
        if(cont.lower() == 'y'):
            print('\n')
        else:
            break
    

    fit_model()

    for game in teams:
        mylist = []
        for team in game:
            mylist.append(team)
        make_predictions(mylist)

def fit_model():
    X = training_data.drop(['did_win'], axis=1)
    y = training_data['did_win']


    clf.fit(X, y)


def make_predictions(teams):

    team1 = Team(teams[0])
    team2 = Team(teams[1])

    team1_data = team1.dataframe
    team2_data = team2.dataframe
    team1_data['did_win'] = 'NaN'
    team2_data['did_win'] = 'NaN'

    team1_data = team1_data[training_data.columns]
    team2_data = team2_data[training_data.columns]
    team1_data = team1_data.astype(float)
    team2_data = team2_data.astype(float)

    combined = pd.DataFrame()
    team1_data = team1_data.append(team2_data)
    combined = combined.append(team1_data.iloc[0] - team1_data.iloc[1], ignore_index=True)


    test = combined.drop(['did_win'], axis=1)
    results = clf.predict(test)

    if str(results[0]) == '1':
        print("{}[x] vs {}[]".format(teams[0], teams[1]))
    else:
        print("{}[] vs {}[x]".format(teams[0], teams[1]))

    # clf2 = svm.SVC()
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    # clf2.fit(X_train, y_train)
    # score = clf2.score(X_test, y_test)
    # print(score)

    return


get_teams()
