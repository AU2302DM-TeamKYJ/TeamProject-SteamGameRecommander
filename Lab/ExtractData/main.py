import json
import csv
import subfunctions as sub

API_KEY = ""  # API KEY
STARTING_ID = "76561198005169633"  # Random initialization

# get user data using API and store it in the user.csv file
userID = sub.get_friends_in_depth(STARTING_ID, API_KEY, 100)
with open('users.csv', 'a', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(userID)

# get user-game data using API and store it in the user-games.json file
with open('users.csv', 'r') as csvfile:
  userID = list(csv.reader(csvfile, delimiter=","))[0]
user_dict = sub.get_user_info(userID, API_KEY)
with open('SteamData/UsersGamesData.json', 'w') as jsonfile:
  json.dump(user_dict, jsonfile)
