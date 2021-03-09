import json
import requests

api_key = '4ea8252ab03e240b40b78530165444e3'
sports_key = 'baseball_mlb'
region = 'us'

odds_response = requests.get('https://api.the-odds-api.com/v3/odds/', params={'api_key': api_key, 'sport': sports_key, 'region': region})

odds_json = json.loads(odds_response.text)
if not odds_json['success']:
    print(odds_json['msg'])
else:
    #print(odds_json['data'][0])

    for game in odds_json['data']:
        team1 = game['teams'][0]
        team2 = game['teams'][1]

        print("{} vs {}".format(team1, team2))

        for odds in game['sites']:

            odds1 = float(odds['odds']['h2h'][0])
            odds2 = float(odds['odds']['h2h'][1])

            if odds1 < 2.00:
                odds1 = (-100)/(odds1 - 1)
            else:
                odds1 = (odds1 - 1) * 100

            if odds2 < 2.00:
                odds2 = (-100)/(odds2 - 1)
            else:
                odds2 = (odds2 - 1) * 100


            
            print("{}: {}".format(team1, odds1))
            print("{}: {}".format(team2, odds2))
    
        print(" ")
        
