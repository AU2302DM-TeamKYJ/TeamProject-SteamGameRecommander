import requests
import json
import re

api = "https://api.steampowered.com/ISteamApps/GetAppList/v0002/"
cache = {}

def get_data():
    if api not in cache:
        response = requests.get(api)
        data = response.json()
        cache[api] = data
    return cache[api]

def by_id(game_id):
    data = get_data()
    for app in data['applist']['apps']:
        if app['appid'] == game_id:
            return app
    return None

def name_exact(name):
    data = get_data()
    for app in data['applist']['apps']:
        if app['name'] == name:
            return app
    return None

def name_regex(pattern):
    data = get_data()
    regex = re.compile(pattern)
    return [app for app in data['applist']['apps'] if regex.match(app['name'])]

def search(test):
    if isinstance(test, str):
        return name_exact(test)
    elif isinstance(test, int):
        return by_id(test)
    elif isinstance(test, re.Pattern):
        return name_regex(test.pattern)
    else:
        raise TypeError("Please supply either a String, a Number, or a Regular Expression")

# 예시 사용
result = search("Some Game Name")  # 문자열로 검색
# result = search(123456)  # ID로 검색
# result = search(re.compile("^Some.*"))  # 정규 표현식으로 검색

print(result)
