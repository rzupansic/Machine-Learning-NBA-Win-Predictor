import numpy as np
import pandas as pd

# Hides INFO logs from tensorflow
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import tensorflow as tf
from datetime import datetime, timedelta
import datetime
from nba_api.live.nba.endpoints import scoreboard
import glob
import json
import subprocess

# Team IDs for future use
abbrev_to_team_id = {
    "ATL": 1610612737,
    "BOS": 1610612738,
    "BRK": 1610612751,
    "CH0": 1610612766,
    "CHI": 1610612741,
    "CLE": 1610612739,
    "DAL": 1610612742,
    "DEN": 1610612743,
    "DET": 1610612765,
    "GSW": 1610612744,
    "HOU": 1610612745,
    "IND": 1610612754,
    "LAC": 1610612746,
    "LAL": 1610612747,
    "MEM": 1610612763,
    "MIA": 1610612748,
    "MIL": 1610612749,
    "MIN": 1610612750,
    "NOP": 1610612740,
    "NYK": 1610612752,
    "OKC": 1610612760,
    "ORL": 1610612753,
    "PHI": 1610612755,
    "PHO": 1610612756,
    "POR": 1610612757,
    "SAC": 1610612758,
    "SAS": 1610612759,
    "TOR": 1610612761,
    "UTA": 1610612762,
    "WAS": 1610612764
}

# Check if dataset is up to date
f = open('update.json')
data = json.load(f)

if data["lastUpdate"] != str(datetime.date.today()):
   print("Dataset needs to update, updating.....")
   subprocess.run(["python", "featureEngineering.py"])
else:
   pass


# Use most recent model
list_of_files = glob.glob('./Models/*.keras') 
latest_file = max(list_of_files, key=os.path.getctime)
predictor = tf.keras.models.load_model(latest_file)

# Open feature engineered dataset
df = pd.read_csv('upData.csv')

f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameStatusText}"


# Get today's date
today = str(datetime.date.today())

board = scoreboard.ScoreBoard()
games = board.games.get_dict()
print("\nToday's Games\n")

for game in games:
  day = datetime.datetime.strptime((game['gameEt'][:game['gameEt'].index('T')]), "%Y-%m-%d").date()
  tip = game['gameEt'][game['gameEt'].index('T') + 1:]

  # Time check and calculate

  tip = tip[:tip.index('Z')]
  tip = datetime.datetime.strptime(tip, '%H:%M:%S').time()
  convert = datetime.datetime.combine(datetime.datetime.min, tip)
  tip = convert - timedelta(hours=12)
  tip = tip.time()

  now = datetime.datetime.now()
  now = now - timedelta(hours=12)
  current_time = now.time()
  

  if tip > current_time:
    print(f"{game['homeTeam']['teamName']} vs. {game['awayTeam']['teamName']} @ {tip} ET")
    print("Predicting......")
  else:
    print(f"{game['homeTeam']['teamName']} vs. {game['awayTeam']['teamName']} (GAMEOVER)")
    print("Our prediction:")
  
  
  previous_day = day - timedelta(days=1)

  # Calculates needed stats for prediction
  eloH = 0
  eloA = 0
  last5h = 0
  last5a = 0
  backH = 0
  backA = 0
  
  h = game['homeTeam']['teamTricode']
  a = game['awayTeam']['teamTricode']
  avg = 0
  count = 0
  
  # home team ELO and back-to-back calc
  for ind in reversed(df.index):
    if df.at[ind, 'HOME'] == h:
      eloH = df.at[ind, 'ELO_Ha']
      if df.at[ind, 'date'] == previous_day:
        backH = 1
      break
    elif df.at[ind, 'AWAY'] == a:
      eloH = df.at[ind, 'ELO_Aa']
      if df.at[ind, 'date'] == previous_day:
        backH = 1
      break
  # away team ELO and back-to-back calc
  for ind in reversed(df.index):
    if df.at[ind, 'HOME'] == a:
      eloA = df.at[ind, 'ELO_Ha']
      if df.at[ind, 'date'] == previous_day:
        backA = 1
      break
    elif df.at[ind, 'AWAY'] == a:
      eloA = df.at[ind, 'ELO_Aa']
      if df.at[ind, 'date'] == previous_day:
        backA = 1
      break

  #home last 5 PPG
  avg = 0
  count = 0
  # Iterate backward from the row before the current row
  for i in range(df.index[-1], -1, -1):
      row = df.iloc[i]
      # counted 5 games, calculate the average
      if count == 5:
          last5h = avg / count
          break

      # If the HOME value matches, add the PTS to the average
      if row['HOME'] == h:
          avg += row['H_SCORE']
          count += 1
      elif row['AWAY'] == h:
          avg += row['A_SCORE']
          count += 1

  #away last 5 PPG
  avg = 0
  count = 0
  # Iterate backward from the row before the current row
  for i in range(df.index[-1], -1, -1):
      row = df.iloc[i]
      # counted 5 games, calculate the average
      if count == 5:
          last5a = avg / count
          break

      # If the HOME value matches, add the PTS to the average
      if row['HOME'] == a:
          avg += row['H_SCORE']
          count += 1
      elif row['AWAY'] == a:
          avg += row['A_SCORE']
          count += 1


  # print(f"{eloH} {eloA} {last5h} {last5a} {backH} {backA}")
  prediction = predictor.predict(np.array([[eloH, eloA, last5h, last5a, backH, backA]]))
  if prediction[0][0] > prediction[0][1]:
      print(f"{game['homeTeam']['teamName']} win!")
  else:
     print(f"{game['awayTeam']['teamName']} win!" )
  print("\n")
