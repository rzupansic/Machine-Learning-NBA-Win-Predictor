from datetime import date
import numpy as np
import pandas as pd
import tensorflow as tf

abbrev_to_team_name = {
    "ATL": "Atlanta Hawks",
    "BOS": "Boston Celtics",
    "BKN": "Brooklyn Nets",
    "CHA": "Charlotte Hornets",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DAL": "Dallas Mavericks",
    "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons",
    "GSW": "Golden State Warriors",
    "HOU": "Houston Rockets",
    "IND": "Indiana Pacers",
    "LAC": "Los Angeles Clippers",
    "LAL": "Los Angeles Lakers",
    "MEM": "Memphis Grizzlies",
    "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks",
    "MIN": "Minnesota Timberwolves",
    "NOP": "New Orleans Pelicans",
    "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder",
    "ORL": "Orlando Magic",
    "PHI": "Philadelphia 76ers",
    "PHX": "Phoenix Suns",
    "POR": "Portland Trail Blazers",
    "SAC": "Sacramento Kings",
    "SAS": "San Antonio Spurs",
    "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz",
    "WAS": "Washington Wizards"
}


# Get the current time for logging
current_date = str(date.today())

# Set up callbacks
tensorboard = tf.keras.callbacks.TensorBoard(log_dir='./Logs/{}'.format(current_date))
earlyStopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
mcp_save = tf.keras.callbacks.ModelCheckpoint('./Models/Trained-Model-ML-' + current_date +".keras", save_best_only=True, monitor='val_loss', mode='min')

# Load train data from CSV files
train_data = pd.read_csv('upData.csv')

# We will not use playoff data to train
train_data = train_data.drop(train_data[train_data['playoff'] == True].index)

# Training Data
y_train = train_data['WL']
X_train = train_data[['ELO_H', 'ELO_A', 'LAST_5_H', 'LAST_5_A', 'BACK_H', 'BACK_A']]


# Build the model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(512))
model.add(tf.keras.layers.Activation('relu6'))
model.add(tf.keras.layers.Dense(512))
model.add(tf.keras.layers.Activation('relu6'))
model.add(tf.keras.layers.Dense(256))
model.add(tf.keras.layers.Activation('relu6'))
model.add(tf.keras.layers.Dense(128))
model.add(tf.keras.layers.Activation('relu6'))
model.add(tf.keras.layers.Dense(2))
model.add(tf.keras.layers.Activation('softmax'))

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, validation_split=0.1, batch_size=32, callbacks=[tensorboard, earlyStopping, mcp_save])

