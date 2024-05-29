from fastapi import FastAPI
import re
import requests
import json

app = FastAPI()

def playerInfo(profileId):

    aoedeApi = 'https://api.ageofempires.com/api/v2/AgeII/GetMPFull'
    payload = {
        'profileId': profileId,
        'playerNumber': '0',
        'gameId': '0',
        'matchType': "3"
    }

    data = requests.post(aoedeApi, json = payload)

    data = data.json()

    aoe2insightsPlayerProfile = 'https://www.aoe2insights.com/user/{}/'.format(profileId)

    htmlContent = requests.get(aoe2insightsPlayerProfile).text

    pattern = r"fi\sfi[\w-]*"

    results = re.findall(pattern, str(htmlContent))

    countryCode = results[0].split('-')[1]

    playerInfo = data['user']
    playerInfo['coutryCode'] = countryCode
    playerInfo['flag'] = 'https://flagsapi.com/{}/flat/64.png'.format(countryCode.upper())

    return playerInfo

@app.get("/playerinfo/{profileId}")

async def root(profileId):

    return {"playerInfo": playerInfo(profileId)}

@app.get("/playerinfo/csv/{profileId}")

async def playerinfocsv(profileId):

    playerInfoData = playerInfo(profileId)

    return "{};{};{};{};{}".format(
        playerInfoData['userName'], 
        playerInfoData['elo'],
        playerInfoData['avatarUrl'],
        playerInfoData['coutryCode'],
        playerInfoData['flag']
        )