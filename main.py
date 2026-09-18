import re
import json
import urllib.request


chromecastHomeURL = 'https://clients3.google.com/cast/chromecast/home/v/c9541b08'
initJSONStateRegex = r"(JSON\.parse\(.+'\))"


def parseChromecastHome(htmlString):

    JSONParse = re.search(initJSONStateRegex, htmlString).group(1)

    decoded = bytes(
        JSONParse[12:-2].replace("\\/", "/"),
        "utf-8"
    ).decode("unicode_escape")

    json_text = decoded.split("')). constant", 1)[0]
    data = json.loads(json_text)

    backgrounds = []

    for entry in data[0]:
        if isinstance(entry[1], str):
            backgrounds.append({
                "url": entry[0],
                "author": entry[1]
            })

    return backgrounds


def getChromecastHome():

    with urllib.request.urlopen(chromecastHomeURL) as response:
        htmlString = response.read().decode("utf-8")

    return parseChromecastHome(htmlString)


backgrounds = getChromecastHome()

print(backgrounds)
