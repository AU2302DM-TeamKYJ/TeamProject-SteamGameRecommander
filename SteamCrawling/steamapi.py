from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

app_id = 105600
user = steam.apps.get_app_details(app_id, filters="genres")
app_detail = user[str(app_id)]['data']['genres']
genre_descriptions = [genre['description'] for genre in app_detail]

print(genre_descriptions)