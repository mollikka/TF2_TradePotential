from json import loads as jsonparse
from json.decoder import JSONDecodeError

from python_littlelib.utils_cached_query import get_external

STEAM_VANITY_URL = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={key}&vanityurl={name}"
STEAM_PLAYER_ITEMS = "http://api.steampowered.com/IEconItems_{gameid}/GetPlayerItems/v0001/?key={key}&SteamID={steamid}"
STEAM_ITEM_DATA = "http://api.steampowered.com/IEconItems_{gameid}/GetSchema/v0001/?key={key}"

with open("API_KEY") as key_file:
    API_KEY = key_file.read().strip()

def _steam_get(url, arguments):

    arguments["key"] = API_KEY
    url = url.format(**arguments)
    try:
        response = jsonparse(get_external(url))
        return response
    except JSONDecodeError:
        return None

def steam_vanity_name_to_id(name):

    answer = _steam_get(STEAM_VANITY_URL, {'name': name})
    if answer and answer["response"]["success"] == 1:
        return answer["response"]["steamid"]
    else:
        return None

def steam_player_items(steamid, gameid):

    answer = _steam_get(STEAM_PLAYER_ITEMS, {"steamid": steamid, "gameid": gameid})
    if answer and answer["result"]["status"] == 1:
        return answer["result"]["items"]
    else:
        return None

def steam_item_data(gameid):

    answer = _steam_get(STEAM_ITEM_DATA, {"gameid": gameid})
    if answer:
        return answer["result"]["items"]

