import csv
import requests
import pandas as pd
import time
from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

def fetch_app_details(appid):
    try:
        data = steam.apps.get_app_details(appid)
        # response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}", timeout=10)
        # data = response.json()

        app_detail = data[str(appid)]['data']
        selected_data = {
            'type': app_detail.get('type', ''),
            'name': app_detail.get('name', ''),
            'required_age' : app_detail.get('required_age', ''),
            'is_free': app_detail.get('is_free', ''),
            'controller_support': app_detail.get('controller_support', ''),
            'dlc': app_detail.get('dlc', ''),
            'detailed_description': app_detail.get('detailed_description', ''),
            'about_the_game': app_detail.get('about_the_game', ''),
            'header_image': app_detail.get('header_image', ''),
            'short_description': app_detail.get('short_description', ''),
            'supported_languages' : app_detail.get('supported_languages', ''),
            # 'developer': app_detail.get('developer', ''),
            # 'publisher': app_detail.get('publisher', ''),
            # 'price_overview': app_detail.get('price_overview', ''),
            # 'platforms': app_detail.get('platforms', ''),
            # 'metacritic': app_detail.get('metacritic', ''),
            # 'categories': app_detail.get('categories', ''),
            # 'genres': app_detail.get('genres', ''),
            # 'recommendations': app_detail.get('recommendations', ''),
            # 'achievements': app_detail.get('achievements', ''),
            # 'release_date': app_detail.get('release_date', ''),
        }
        # print(selected_data)
        return selected_data
    except Exception as e:
        print(f"Error fetching appid {appid}: {e}")
        return None

def process_batch(appids, error_appids):
    app_details = []
    for count, appid in enumerate(appids):
        print(count, appid)
        detail = fetch_app_details(appid)
        if detail:
            app_details.append(detail)
        else:
            error_appids.append(appid)

        if count < len(appids) - 1:  # 마지막 요청이 아닌 경우
            time.sleep(0.1)  # 100 밀리초 대기

    return app_details


file_path = "./data/unique_appids.csv"
app_details = []
error_appids = []
total_error_appids = []
df = pd.DataFrame()
start_index = 301

# fetch_app_details(252950)

with open(file_path, 'r') as file:
    rdr = csv.reader(file)
    next(rdr)  # 헤더 건너뛰기

    appids = [line[0] for line in rdr]
    count = start_index
    for i in range(start_index, len(appids)):
        appid = appids[i]
    # for appid in appids:
        print(count, appid)
        detail = fetch_app_details(appid)
        if detail:
            app_details.append(detail)
        else:
            error_appids.append(appid)

        if count % 100 == 0 and count > 0:
            # print(count)
            df = pd.DataFrame(app_details)
            df.to_csv(f'./data/app_details_{count}.csv', index=False)
            print("save to csv")
            app_details = []  # 리스트 초기화
            # count = 0
            print(error_appids)
            time.sleep(60)  # 배치 처리 후 대기
            # 에러가 난 appid를 별도의 파일에 저장
            error_df = pd.DataFrame({'error_appids': error_appids})
            error_df.to_csv(f'./data/error_appids_{count}.csv', index=False)
            print(f"Error appids batch {count} saved to CSV")
            # processed_count += 1
            error_appids = []  # 에러 목록 초기화
        count += 1

    # 모든 appid 처리 후
    if app_details:
        df = pd.DataFrame(app_details)
        df.to_csv(f'./data/app_details_final.csv', index=False)
        print("Final batch saved to CSV")

    # # 에러가 난 appid들을 별도의 CSV 파일에 저장
    # if error_appids:
    #     error_df = pd.DataFrame({'error_appids': error_appids})
    #     error_df.to_csv('./data/error_appids.csv', index=False)
    #     print("Error appids saved to CSV")


#     for i in range(start_index, len(appids), 100):
#         batch_appids = appids[i:i+100]
#         app_details = process_batch(batch_appids, error_appids) # 100 개씩
#         df = pd.concat([df, pd.DataFrame(app_details)], ignore_index=True)
#         df.to_csv('./data/app_details.csv', mode='a', header=False, index=False)
#         print(error_appids)
#         # 1초 대기
#         time.sleep(1) 
    
#         # 에러가 난 appid에 대해 다시 시도
#         for appid in error_appids:
#             detail = fetch_app_details(appid)
#             if detail:
#                 df = pd.concat([df, pd.DataFrame([detail])], ignore_index=True)
#                 df.to_csv('./data/app_details.csv', mode='a', header=False, index=False)
#             else:
#                 total_error_appids.append(appid)  # 에러가 다시 발생한 appid를 total_error_appids에 추가
#         error_appids = []
#         print("error appids done")
    
# print("Total error appids:", total_error_appids) 

    # for count, line in enumerate(rdr):
    #   appid = line[0]
    #   print(count, appid)
    #   detail = fetch_app_details(appid)
    #   if detail:
    #     app_details.append(detail)

    #   if count % 100 == 0 and count > 0:
    #     print(count)
    #     df = pd.DataFrame(app_details)
    #     df.to_csv(f'./data/app_details_{count}.csv', index=False)
    #     print("save to csv")
    #     app_details = []  # 리스트 초기화
    #     time.sleep(60)  # 배치 처리 후 대기



# 마지막 배치 저장
# if app_details:
#     df = pd.DataFrame(app_details)
#     df.to_csv(f'./data/app_details_final.csv', index=False)



# count = 0
# app_details = []

# file_path = "./data/unique_appids.csv"
# with open(file_path, 'r') as file:
#   rdr = csv.reader(file)
#   next(rdr)  # 헤더 건너뛰기

#   for line in rdr:
#     if count < 5:
#       # print(line[0])
#       appid = line[0]
#       response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}")
#       data = response.json()
#       app_detail = data[str(appid)]['data']  # 'data' 키에 해당하는 정보를 추출
#       app_details.append(app_detail)
#       count += 1
#     else:
#       break 
#   # print(app_details)
#   df = pd.DataFrame(app_details)
#   print(df)

