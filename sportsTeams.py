from sportsipy.ncaab.teams import Team
from sportsipy.ncaab.teams import Teams
import pandas as pd


# df = pd.DataFrame()

# team = Team('PURDUE', year='2018')
# team_dataframe = team.dataframe
# df = df.append(team_dataframe)

# print(df)

df = pd.DataFrame()

teams_2019 = Teams(year=2019)
dataframe_2019 = teams_2019.dataframes
dataframe_2019['year'] = '2019'
df = df.append(dataframe_2019)

teams_2018 = Teams(year=2018)
dataframe_2018 = teams_2018.dataframes
dataframe_2018['year'] = '2018'
df = df.append(dataframe_2018)

teams_2017 = Teams(year=2017)
dataframe_2017 = teams_2017.dataframes
dataframe_2017['year'] = '2017'
df = df.append(dataframe_2017)

print(df)
df.to_csv('teamData.csv')
