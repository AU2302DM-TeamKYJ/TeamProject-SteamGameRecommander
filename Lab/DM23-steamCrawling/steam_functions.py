import random
import json
import numpy as np
import pandas as pd
import urllib.request
from pandas import json_normalize
from urllib.parse import urlencode, quote_plus, unquote
from urllib.error import URLError, HTTPError


def get_friends_list(steam_id, api_key):
  """
  Input
    - steam_id : steam ID for one user
    - api_key : API KEY for accessing steam dataset

  Output
    - friends_id_list : list of input user's friends
  """
  get_friends_API_URL = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/"
  queryParams = '?' + urlencode({
      quote_plus('key'): api_key,
      quote_plus('steamid'): steam_id,
      quote_plus('relationship'): 'friend'
  })
  url = get_friends_API_URL + queryParams
  # print(url)
  friends_id_list = []
  # 데이터를 요청하고 변환합니다.
  try:
    text = urllib.request.urlopen(url).read().decode('utf-8')
    json_return = json.loads(text)
    friends_data = json_return.get('friendslist').get('friends')
    print("count:", len(friends_data))
    # 반환된 JSON에서 친구 목록만 가져오기
    for friend in friends_data:
      friends_id_list.append(friend.get('steamid'))
    friends_id_list = np.unique(friends_id_list)  # 중복제거
  except:
    # 유저데이터 비공개 예외처리
    print(steam_id, '401에러: 유저데이터 비공개')
    friends_id_list = []

  return friends_id_list

def get_friends_in_count(root_id, api_key, max_count):
  """
  Input
    - root_id : steam ID for root user to recursively search friends
    - api_key : API KEY for accessing steam dataset
    - max_count : number of friends

  Output
    - total_list : list of user ID
  """
  total_list = []
  total_list.extend(get_friends_list(root_id, api_key))  # initialize
  while True:
    print("total count:", len(total_list))
    if len(total_list) > 0:
      # 친구리스트에서 랜덤으로 스팀id를 뽑아서 친구리스트에 새로 추가한다.
      random_idx = random.randint(0, len(total_list) - 1)
      total_list.extend(get_friends_list(total_list[random_idx], api_key))
    if len(total_list) > max_count:
      print("finish with:", len(total_list))
      break
  return total_list

def get_user_game_list(user_id, api_key):
  """
  Input
    - user_id : user ID
    - api_key : API KEY for accessing steam dataset

  Output
    - user_game_list : list of dictionaries {"user_id" : [game_id1, game_id2, ...]}
  """
  get_games_API_URL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
  queryParams = '?' + urlencode({
      quote_plus('key'): api_key,
      quote_plus('steamid'): user_id,
      quote_plus('include_played_free_games'): 1,
      quote_plus('format'): 'json'
  })
  url = get_games_API_URL + queryParams
  # print(url)
  user_games_list = []
  games_data = []
  # 데이터를 요청하고 변환합니다.
  try:
    text = urllib.request.urlopen(url).read().decode('utf-8')
    json_return = json.loads(text)
    # print(json_return)
    if json_return.get('response') == {}:
      print("response:{}")
    else:
      games_data = json_return.get('response').get('games')

    for game in games_data:
      ## 플레이타임 0시간 제외
      if game.get('playtime_forever') == 0:
        continue
      user_games_list.append(game.get('appid'))
    user_games_list = np.unique(user_games_list)  # 중복제거
    # user_games_list.append({user_id: user_games_list})
  except HTTPError as e:
    # 유저데이터 비공개 예외처리
    print(user_id, e, '401에러: 유저데이터 비공개')
    user_games_list = []

  if len(games_data) != 0:
    print("Number of games played / purchased:", len(user_games_list), "/",
          len(games_data))
  return {user_id: user_games_list}

def get_users_games_list(user_id_list, api_key, testNum=0):
  """
  Input
    - user_id_list : list of user ID
    - api_key : API KEY for accessing steam dataset

  Output
    - users_games_list : list of dictionaries [{"user_id" : [game_id1, game_id2, ...]}, {"user_id" : [game_id1, game_id2, ...]}]
  """
  total_list = []
  count_of_response_empty = 0
  n = 0
  for user_id in user_id_list:
    print(n)
    if testNum != 0 and n == testNum:
      break
    game_dict = get_user_game_list(user_id, api_key)
    if len(game_dict[user_id]) == 0:
      count_of_response_empty = count_of_response_empty + 1
    total_list.extend(game_dict)
    n += 1
  print("empty / total:", count_of_response_empty, "/",
        len(user_id_list) if testNum == 0 else testNum)
  print("count_of_response_empty:", count_of_response_empty)
  return total_list

def get_user_game_data(user_id, api_key):
  """
  Input
    - user_id : user ID
    - api_key : API KEY for accessing steam dataset

  Output
    - user_game_list : list of dictionaries {"user_id" : [game_id1, game_id2, ...]}
  """
  get_games_API_URL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
  queryParams = '?' + urlencode({
      quote_plus('key'): api_key,
      quote_plus('steamid'): user_id,
      quote_plus('include_played_free_games'): 1,
      quote_plus('format'): 'json'
  })
  url = get_games_API_URL + queryParams
  # print(url)
  user_games_list = []
  games_data = []
  # 데이터를 요청하고 변환합니다.
  try:
    text = urllib.request.urlopen(url).read().decode('utf-8')
    json_return = json.loads(text)
    # print(json_return)
    if json_return.get('response') == {}:
      print("response:{}")
    else:
      games_data = json_return.get('response', {}).get('games', [])
    for game in games_data:
      ## 플레이타임 0시간 제외
      if game.get('playtime_forever') > 0:
        game_info = {
            'appid': game.get('appid'),
            'playtime_forever': game.get('playtime_forever')
        }
        user_games_list.append(game_info)
  except HTTPError as e:
    # 유저데이터 비공개 예외처리
    print(user_id, e, '401에러: 유저데이터 비공개')
    user_games_list = []

  if len(games_data) != 0:
    print("Number of games played / purchased:", len(user_games_list), "/",
          len(games_data))
  return {user_id: user_games_list}

def get_users_game_data(user_id_list, api_key, file_name, testNum=0):
  """
  Input
    - user_id_list : list of user ID
    - api_key : API KEY for accessing steam dataset

  Output
    - users_games_list : list of dictionaries [{"user_id" : [game_id1, game_id2, ...]}, {"user_id" : [game_id1, game_id2, ...]}]
  """
  total_data_list = []
  count_of_response_empty = 0
  n = 0
  for user_id in user_id_list:
    print(n)
    if testNum != 0 and n == testNum:
      break
    game_data = get_user_game_data(user_id, api_key)
    # print(game_data)
    if len(game_data[user_id]) == 0:
      count_of_response_empty = count_of_response_empty + 1
    total_data_list.append(
        game_data)  # append 대신 extend를 사용하면 딕셔너리가 아닌 요소들이 추가됩니다.
    # save_data_incrementally(game_data, "game_data.json")  # 데이터 추가
    n += 1
  print("empty / total:", count_of_response_empty, "/",
        len(user_id_list) if testNum == 0 else testNum)
  print("count_of_response_empty:", count_of_response_empty)
  print(total_data_list)

  # JSON 파일로 저장
  save_to_json(total_data_list, file_name)
  print("finish process...")
  return total_data_list

def get_users_game_data_range(user_id_list, api_key, testNum=0):
  """
  Input
    - user_id_list : list of user ID
    - api_key : API KEY for accessing steam dataset

  Output
    - users_games_list : list of dictionaries [{"user_id" : [game_id1, game_id2, ...]}, {"user_id" : [game_id1, game_id2, ...]}]
  """
  total_data_list = []
  count_of_response_empty = 0
  n = 0
  for user_id in user_id_list:
    print(n)
    if testNum != 0 and n == testNum:
      break
    game_data = get_user_game_data(user_id, api_key)
    # print(game_data)
    if len(game_data[user_id]) == 0:
      count_of_response_empty = count_of_response_empty + 1
    total_data_list.append({user_id: game_data[user_id]})
    # total_data_list.append(game_data)  # append 대신 extend를 사용하면 딕셔너리가 아닌 요소들이 추가됩니다.
    # save_data_incrementally(game_data, "game_data.json")  # 데이터 추가
    n += 1
  print("empty / total:", count_of_response_empty, "/",
        len(user_id_list) if testNum == 0 else testNum)
  print("count_of_response_empty:", count_of_response_empty)
  # print(total_data_list)

  # JSON 파일로 저장
  save_to_json(total_data_list, "game_data.json")
  print("finish process...")
  return total_data_list

def save_to_json(data, file_name):
  """
  주어진 데이터를 JSON 파일로 저장합니다.

  :param data: 저장할 데이터
  :param file_name: 생성할 JSON 파일의 이름
  """
  with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

def save_data_incrementally(data, file_name):
  """데이터를 점진적으로 JSON 파일에 추가합니다."""
  with open(file_name, 'a', encoding='utf-8') as f:
      # 파일에 새로운 데이터를 JSON 형식으로 추가
      json.dump(data, f, ensure_ascii=False)
      f.write("\n")  # 각 데이터 뒤에 줄바꿈 추가

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
