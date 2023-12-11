import json
import csv
import numpy as np
import pandas as pd


def extract_games(user_games_json_file, games_json_file):
  """
  Input
    - user_games_json_file : user-games.json

  store games_id in games.csv file
  """

  with open(user_games_json_file, 'r') as jsonfile:
    user_games_data = json.load(jsonfile)

  games = []
  for user_id in user_games_data:
    for i in user_games_data[user_id]:
      game_id = i["appid"]
      games.append(game_id)
  games = list(np.unique(games))

  with open(games_json_file, "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(games)


def json_to_df(json_file_path):
  """
  Input
    - json_file_path : path of json file

  Output
    - df : DataFrame of user and game matrix
           row with user_id, column with game_id
           if user has game then 1 else 0
  """

  # Load data
  with open(json_file_path, 'r') as file:
    data_list = json.load(file)

  # Flatten the list of dictionaries into a single dictionary
  data = {
      str(user_id): games
      for user_data in data_list for user_id, games in user_data.items()
  }

  # Create an empty DataFrame
  df = pd.DataFrame(index=data.keys())

  # Iterate over each game_id and populate the DataFrame with 0s and 1s
  for game_id in set(game_id for games_list in data.values()
                     for game_id in games_list):
    df[game_id] = df.index.map(lambda user_id: 1
                               if game_id in data.get(str(user_id), []) else 0)

  # Fill NaN values with 0
  df = df.fillna(0)

  return df
