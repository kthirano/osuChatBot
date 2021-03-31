import requests
import os
from dotenv import load_dotenv
import json

def getAccessToken():
    accessToken = "failed"
    load_dotenv()
    response = requests.post(
        'https://osu.ppy.sh/oauth/token',
        data = {
            'client_id' : os.getenv('OSU_CLIENT_ID'),
            'client_secret' : os.getenv('OSU_CLIENT_SECRET'),
            'grant_type' : 'client_credentials',
            'scope' : 'public'
        }
    )
    if (response.status_code == 200):
        json_response = response.json()
        accessToken = json_response["access_token"]
    return accessToken

def getBeatMap(mapId):
    token = getAccessToken()
    if (token == "failed"):
        return {"error" : "getaccesstoken"}
    response = requests.get(
        'https://osu.ppy.sh/api/v2/beatmaps/' + str(mapId),
        headers = {'Authorization' : 'Bearer ' + token}
    )
    return response.json()

def verifyLink(link):
    split = link.split("/")
    return_id = -1
    if (len(split) == 6 and split[2] == "osu.ppy.sh"):
        return_id = split[5]
    return return_id

def getInvalidLinkErrorMessage():
    return "Sorry, I think the link is invalid. You can check out https://osu.ppy.sh/beatmapsets"

def getUserRank():
    with open('userinfo.json') as f:
        data = json.load(f)
    token = getAccessToken()
    if (token == "failed"):
        return {"error" : "getaccesstoken"}
    response = requests.get(
        'https://osu.ppy.sh/api/v2/users/' + str(data['user_id']),
        headers = {'Authorization' : 'Bearer ' + token}
    )
    return response.json()
    


if __name__ == "__main__":
    print(getUserRank())

