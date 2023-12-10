import data_preprocessing
from sklearn.cluster import KMeans
import csv
import json
import numpy as np
import time
import urllib.request
from urllib.error import HTTPError
import pandas as pd
import random

# get all the games that users have
data_preprocessing.extract_games("SteamData/UsersGamesData.json",
                                 "SteamData/games.csv")

# extract game features from Steam URL
with open("SteamData/games.csv", "r") as csvfile:
  games_id = list(csv.reader(csvfile, delimiter=","))[0]
print(f"Number of games : {len(games_id)}")

age = []
is_free = []
genre = []
for idx, game_id in enumerate(games_id):
  print(f"{idx+1}th game started!!!")
  game_URL = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
  time.sleep(0.1)  # to avoid HTTPError 429
  try:
    text = urllib.request.urlopen(game_URL).read().decode('utf-8')
  except HTTPError:  # Handling HTTPError 429

    with open('GamesMatrix/genres.csv', 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(genre)
    with open('GamesMatrix/ages.csv', 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(age)
    with open('GamesMatrix/free_or_not.csv', 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(is_free)
    # after writing to csv file clean up the list
    age = []
    is_free = []
    genre = []
    print("\nWait for 300 seconds...\n")
    time.sleep(300)
    text = urllib.request.urlopen(game_URL).read().decode('utf-8')  # try again
  json_return = json.loads(text)

  if json_return[game_id]["success"] == 'false':
    continue

  try:
    required_age = json_return[game_id]["data"]["required_age"]
  except:
    required_age = "NULL"
  age.append(required_age)

  try:
    free_or_not = json_return[game_id]["data"]["is_free"]
  except:
    free_or_not = "NULL"
  is_free.append(free_or_not)

  try:
    genre_list = json_return[game_id]["data"]["genres"]
    num_genre = len(genre_list)
    what_genre = genre_list[random.randint(0, num_genre) - 1]["description"]
  except:
    what_genre = "NULL"
  genre.append(what_genre)

#####################################################################

# preprocessing data for clustering

# Ages
with open('GamesMatrix/ages.csv', 'r') as csvfile:
  ages = list(csv.reader(csvfile, delimiter=","))[0]
numeric_ages = []
for age in ages:
  if age == 'NULL':
    numeric_ages.append(0)
  elif age == '17+':
    numeric_ages.append(17)
  else:
    numeric_ages.append(int(age))
numeric_ages = (numeric_ages - np.mean(numeric_ages)) / np.std(numeric_ages)
# Free or not
with open('GamesMatrix/free_or_not.csv', 'r') as csvfile:
  is_free = list(csv.reader(csvfile, delimiter=","))[0]
numeric_free = [1 if f == 'True' else 0 for f in is_free]
numeric_free = (numeric_free - np.mean(numeric_free)) / np.std(numeric_free)
# Genres
with open('GamesMatrix/genres.csv', 'r') as csvfile:
  genres = list(csv.reader(csvfile, delimiter=","))[0]
genre_dict = {}
for idx, genre in enumerate(np.unique(genres)):
  genre_dict[genre] = idx * 5
numeric_genres = []
for genre in genres:
  numeric_genres.append(genre_dict[genre])
numeric_genres = (numeric_genres -
                  np.mean(numeric_genres)) / np.std(numeric_genres)

with open("SteamData/games.csv", "r") as csvfile:
  games_id = list(csv.reader(csvfile, delimiter=","))[0]

#####################################################################

# create DataFrame(Matrix) of games

data = {
    "GameID": games_id,
    "Genre": numeric_genres,
    "Age": numeric_ages,
    "isFree": numeric_free
}
df = pd.DataFrame(data)
df = df.set_index('GameID')

# Declaring Model: K-Means
model = KMeans(n_clusters=5)

# Fitting Model
kmeans = model.fit(df)

df.loc[:, "cluster"] = kmeans.labels_

print(df)

# save DataFrame
df.to_pickle("game_feature_matrix.pkl")

#####################################################################

# Results
df = pd.read_pickle("pure_game_feature_matrix.pkl")

print(df.info)

# USER1 : game feature (Action, Free, 0)
user1_game = [
    10, 20, 30, 40, 50, 60, 70, 80, 92, 100, 130, 220, 240, 280, 300, 320, 340,
    360, 380, 400, 420, 440
]

cluster_value_for_user1 = []
for game in user1_game:
  cluster_value_for_user1.append(df._get_value(str(game), 'cluster'))
print("User1 Tag : ", np.mean(cluster_value_for_user1))

# USER2 : game feature (Strategy, Free, 1)
user2_game = [
    1500, 1510, 1520, 1530, 1600, 1610, 1630, 1640, 1670, 1690, 1700, 1840
]

cluster_value_for_user2 = []
for game in user2_game:
  cluster_value_for_user2.append(df._get_value(str(game), 'cluster'))
print("User2 Tag : ", np.mean(cluster_value_for_user2))
