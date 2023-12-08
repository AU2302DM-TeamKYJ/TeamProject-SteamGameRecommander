import csv
import requests
import pandas as pd
import time

def fetch_app_details(appid):
    try:
        response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}", timeout=10)
        data = response.json()
        return data[str(appid)]['data']
    except Exception as e:
        print(f"Error fetching appid {appid}: {e}")
        return None

def process_batch(appids, error_appids):
    app_details = []
    count = 0
    for appid in appids:
        print(count, appid)
        detail = fetch_app_details(appid)
        if detail:
            app_details.append(detail)
        else:
            error_appids.append(appid)
        count += 1
    return app_details


file_path = "./data/unique_appids.csv"
app_details = []
error_appids = []
# df = pd.DataFrame()

# columns = ['type', 'name', 'steam_appid', 'required_age', 'is_free', 'detailed_description', 'about_the_game', 
#     'short_description', 'supported_languages', 'header_image', 'capsule_image', 'capsule_imagev5', 
#     'website', 'pc_requirements', 'mac_requirements', 'linux_requirements', 'developers', 'publishers', 
#     'price_overview', 'packages', 'package_groups', 'platforms', 'metacritic', 'categories', 'genres', 
#     'screenshots', 'recommendations', 'release_date', 'support_info', 'background', 'background_raw', 
#     'content_descriptors', 'legal_notice', 'movies', 'controller_support', 'achievements', 'dlc', 
#     'reviews', 'ext_user_account_notice', 'drm_notice', 'demos']


# df = pd.DataFrame(app_details, columns=columns)  # 나머지 열 이름을 계속 추가
df = pd.DataFrame()
start_index = 0

with open(file_path, 'r') as file:
    rdr = csv.reader(file)
    next(rdr)  # 헤더 건너뛰기

    appids = [line[0] for line in rdr]

    for i in range(start_index, len(appids), 100):
        batch_appids = appids[i:i+100]
        app_details = process_batch(batch_appids, error_appids) # 100 개씩
        # df = df.append(pd.DataFrame(app_details), ignore_index=True)
        df = pd.concat([df, pd.DataFrame(app_details)], ignore_index=True)
        df.to_csv('./data/app_details.csv', mode='a', header=False, index=False)
        print(error_appids)
        # 1초 대기
        time.sleep(1) 
    
        # 에러가 난 appid에 대해 다시 시도
        for appid in error_appids:
            detail = fetch_app_details(appid)
            if detail:
                df = pd.concat([df, pd.DataFrame(detail)], ignore_index=True)
                df.to_csv('app_details.csv', mode='a', header=False, index=False)
        print("error appids done")
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

