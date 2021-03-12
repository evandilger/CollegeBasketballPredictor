from sportsipy.ncaab.teams import Team
from sklearn import svm
from sklearn.model_selection import train_test_split
import pandas as pd

training_data = pd.read_csv('seperateTransformDataPlus.csv')
clf_win = svm.SVC(probability=True)
clf_total = svm.SVC()
clf_spread = svm.SVC()
X = training_data.drop(['did_win', 'total_points', 'spread'], axis=1)
y_win = training_data['did_win']
y_total = training_data['total_points']
y_spread = training_data['spread']

def get_teams():
    teams = list(list())
    team_names = pd.read_csv('teamData.csv', skipinitialspace=True, usecols=['abbreviation'])

    while True:
        while True:
            team1 = input('Team 1: ')
            if not team_names.loc[team_names['abbreviation'] == team1].empty:
                spread = input('Spread: ')
                total = input('OverUnder: ')
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

        teams.append([team1, team2, float(spread), float(total)])
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
    clf_win.fit(X, y_win)
    clf_spread.fit(X, y_spread)
    clf_total.fit(X, y_total)


def make_predictions(teams):

    team1 = Team(teams[0])
    team2 = Team(teams[1])
    spread = teams[2]
    total = teams[3]

    team1_data = team1.dataframe
    team2_data = team2.dataframe
    team1_data['joincol'] = '1'
    team2_data['joincol'] = '1'
    # team1_data['did_win'] = 'NaN'
    # team2_data['did_win'] = 'NaN'
    # team1_data['spread'] = 'NaN'
    # team2_data['spread'] = 'NaN'
    # team1_data['total_points'] = 'NaN'
    # team2_data['total_points'] = 'NaN'

    # team1_data = team1_data[training_data.columns]
    # team2_data = team2_data[training_data.columns]
    # team1_data = team1_data.astype(float)
    # team2_data = team2_data.astype(float)

    combined = pd.DataFrame()

    combined = pd.merge(left=team1_data,right=team2_data, on='joincol', how='outer')
    combined['did_win'] = 'NaN'
    combined['spread'] = 'NaN'
    combined['total_points'] = 'NaN'
    
    combined = combined[training_data.columns]


    test = combined.drop(['did_win', 'spread', 'total_points'], axis=1)
    results_win = clf_win.predict_proba(test)
    results_win = results_win[0]
    results_total = clf_total.predict(test)
    results_spread = clf_spread.predict(test)


    if float(results_win[1]) >= 0.5:
        print("{}[x] vs {}[]  {}".format(teams[0], teams[1], results_win[1]))
    else:
        print("{}[] vs {}[x]  {}".format(teams[0], teams[1], results_win[0]))

    print("Spread: {} Predicted: {}".format(spread, results_spread))
    print("OverUnder: {} Predicted: {}".format(total, results_total))
    print('\n')
    # clf2 = svm.SVC()
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    # clf2.fit(X_train, y_train)
    # score = clf2.score(X_test, y_test)
    # print(score)

    return


get_teams()
