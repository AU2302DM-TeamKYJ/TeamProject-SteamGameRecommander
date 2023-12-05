from dotenv import load_dotenv
import os

from steam_functions import get_friends_list, get_friends_in_count, get_user_game_list, get_users_games_list, get_user_game_data, get_users_game_data, get_users_game_data_range
from read_write_csv import write_ids_to_csv, read_ids_from_csv, read_ids_from_csv_2


def get_steam_ids(steam_id, api_key):
  # ==== 친구 리스트로 원하는 수 만큼의 스팀id 뽑기 ====
  friends_in_count_400 = get_friends_in_count(steam_id, api_key, 400)
  print(friends_in_count_400[:5])
  # CSV 파일에 저장
  write_ids_to_csv("steamIds.csv", friends_in_count_400)


def test(steam_id, api_key):
  # 친구 리스트 가져오기
  friends_list = get_friends_list(steam_id, api_key)
  print(friends_list[:5])

  # 특정 사용자의 게임 목록 가져오기
  steam_id = '76561198342608169'  # https://www.steamidfinder.com/lookup/ganpraflo/
  game_list = get_user_game_list(steam_id, api_key)
  print(game_list)


def main():
  # load .env
  load_dotenv()
  API_KEY = os.environ.get('API_KEY')

  # API key와 steam id 설정
  api_key = API_KEY  #'YOUR_API_KEY_HERE'
  steam_id = '76561198003081163'  # 예: 스트리머 우왁굳의 Steam ID

  # test(steam_id, api_key);
  # get_steam_ids(steam_id,api_key);

  # ==== userid 리스트로 여러 사용자의 게임 목록 데이터 만들기 ====
  # csv 파일 읽어오기
  # steam_ids = read_ids_from_csv("data/steamIds.csv")
  n = 16
  steam_ids = read_ids_from_csv_2("data/UniqueFriends_2.csv")
  print(len(steam_ids))
  print(500*(n-1),500*n)

  # # 스팀id 리스트로 보유게임(플레이한) 리스트를 뽑아오기
  # users_games_list = get_users_game_data(steam_ids[500*(n-1):500*n], api_key,"data/game_data_" + str(n) + ".json")
  # print(users_games_list[:5])
  n=20
  users_games_list = get_users_game_data(steam_ids[:10], api_key,"data/game_data_" + str(n) + ".json")
  # print(users_games_list[:5])

  # while n < 21:  # n이 1부터 20까지 반복
  #   try:
  #       steam_ids = read_ids_from_csv_2("data/UniqueFriends_2.csv")
  #       print("Processing for n =", n)
  #       print("IDs range:", 500*(n-1), "to", 500*n)

  #       # 스팀 ID 리스트로부터 사용자별 게임 리스트 추출
  #       users_games_list = get_users_game_data(steam_ids[500*(n-1):500*n], api_key, "data/game_data_" + str(n) + ".json")
  #       # print(users_games_list[:5])
  #       print("success n:", n)
  #       n += 1

  #   except Exception as e:
  #       print(f"An error occurred at n = {n}: {e}")
  #       # 오류 발생 시 n의 값을 파일에 기록
  #       with open("data/error_log.txt", "a") as file:
  #           file.write(f"Error at n = {n}: {e}\n")

if __name__ == "__main__":
  main()
