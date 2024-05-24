#
#
#
# This program was used to perform feature engineering on our original dataset
#
#
#


import pandas as pd
from datetime import datetime
from datetime import timedelta
import datetime
import urllib.request
import json

urllib.request.urlretrieve("https://github.com/Neil-Paine-1/NBA-elo/raw/25fcdcd2faeff0b62a11a0985935338bb0c3dc57/nba_elo.csv", 'upData.csv')

df = pd.read_csv('upData.csv')
n = str(datetime.date.today())


# Save date of update to dataset to improve efficiency
dateUpdate = {
    "lastUpdate": n
}

with open('update.json', 'w') as outfile:
    json.dump(dateUpdate, outfile)

# Create desired features

df['LAST_5_A'] = 0.0
df['LAST_5_H'] = 0.0
df['BACK_H'] = 0
df['BACK_A'] = 0
df['WL'] = 0

df.rename(columns = {'team1':'HOME'}, inplace = True)
df.rename(columns = {'team2':'AWAY'}, inplace = True)
df.rename(columns = {'elo1_pre':'ELO_H'}, inplace = True)
df.rename(columns = {'elo2_pre':'ELO_A'}, inplace = True)
df.rename(columns = {'elo1_post':'ELO_Ha'}, inplace = True)
df.rename(columns = {'elo2_post':'ELO_Aa'}, inplace = True)
df.rename(columns = {'score1':'H_SCORE'}, inplace = True)
df.rename(columns = {'score2':'A_SCORE'}, inplace = True)

today = datetime.date.today()
year = today.year

# Include only home games so that there are not duplicate games
df = df[df["is_home"]==1]
df = df[df["season"]> year - 6]
df = df[['date', 'playoff',  'HOME', 'AWAY', 'ELO_H', 'ELO_A', 'ELO_Ha', 'ELO_Aa', 'H_SCORE', 'A_SCORE', 'LAST_5_H', 'LAST_5_A', 'BACK_H', 'BACK_A', 'WL' ]]

df = df.reset_index()
df = df.drop(['index'], axis=1)

# We will now calculate wins and losses, AVG PPG of last 5 games and back-to-backs
for ind in df.index:
    df.at[ind, 'date'] = datetime.datetime.strptime(df.at[ind, 'date'], "%Y-%m-%d").date()
    previous_day = df.at[ind, 'date'] - timedelta(days=1)
    if df.at[ind, 'H_SCORE'] > df.at[ind, 'A_SCORE']:
      df.at[ind, 'WL'] = 1
    else:
      df.at[ind, 'WL'] = 0

    team = df.at[ind, 'HOME'] # Start with home team
    avg = 0
    count = 0


    # Iterate backward from the row before the current row
    for i in range(ind - 1, -1, -1):
        row = df.iloc[i]
        # If reached the start of the DataFrame or counted 5 games, calculate the average
        if count == 5 or i == 0:
            if count > 0:
                df.at[ind, 'LAST_5_H'] = avg / count
            break

        # If the HOME value matches, add the PTS to the average
        if row['HOME'] == team:
            avg += row['H_SCORE']
            count += 1
            if count == 1 and row['date'] == previous_day:
              df.at[ind, 'BACK_H'] = 1
        elif row['AWAY'] == team:
            avg += row['A_SCORE']
            count += 1
            if count == 1 and row['date'] == previous_day:
              df.at[ind, 'BACK_H'] = 1

    team = df.at[ind, 'AWAY']  # Get the AWAY value for the current row
    avg = 0
    count = 0

    # Iterate backward from the row before the current row
    for i in range(ind - 1, -1, -1):
        row = df.iloc[i]

        # If reached the start of the DataFrame or counted 5 games, calculate the average
        if count == 5 or i == 0:
            if count > 0:
                df.at[ind, 'LAST_5_A'] = avg / count
            break

        # If the HOME value matches, add the PTS to the average
        if row['HOME'] == team:
            avg += row['H_SCORE']
            count += 1
            if count == 1 and row['date'] == previous_day:
                df.at[ind, 'BACK_A'] = 1
        elif row['AWAY'] == team:
            avg += row['A_SCORE']
            count += 1
            if count == 1 and row['date'] == previous_day:
                df.at[ind, 'BACK_A'] = 1

df.to_csv('upData.csv')