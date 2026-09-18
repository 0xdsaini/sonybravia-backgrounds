"""
Updates backgrounds.json
Updates README.md
with latest backgrounds from server

Run & Update.
"""


import re
import json
import urllib.request
from time import sleep


chromecastHomeURL = 'https://clients3.google.com/cast/chromecast/home/v/c9541b08'
initJSONStateRegex = r"(JSON\.parse\(.+'\))"

FETCH_TIMES = 100
SLEEP_BETWEEN_REQUESTS = 2  # seconds

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


def uniqueBackgroundsOnly(new_backgrounds):

    unique_backgrounds = []
    urls = set()

    for background in backgrounds:
        url = background["url"]

        if url not in urls:
            unique_backgrounds.append(background)
            urls.add(url)
        else:
            pass
            # print(url)

    return unique_backgrounds


def createREADME(backgrounds):

    with open("README.md", "w", encoding="utf-8") as file:

        total_count = len(backgrounds)
        file.write(f"Total Count: {total_count}\n\n")

        for background in backgrounds:

            url = background["url"]
            author = background["author"]

            file.write(f"[![Wallpaper]({url})]({url})\n\n")
            file.write(f"{author}\n\n")


# Load previous backgrounds list from backgrounds.json
with open("backgrounds.json", "r", encoding="utf-8") as file:
    content = file.read()

if content:
    backgrounds = json.loads(content)
else:
    backgrounds = []


# 49 backgrounds returned per request. fetch a couple of times.
for i in range(FETCH_TIMES):

    # Get latest backgrounds from server
    new_backgrounds = getChromecastHome()

    backgrounds += new_backgrounds

    sleep(SLEEP_BETWEEN_REQUESTS)

# Only unique background survives
unique_backgrounds = uniqueBackgroundsOnly(backgrounds)


# rewrite backgrounds.json completely with updated list.
with open("backgrounds.json", "w", encoding="utf-8") as file:
    json.dump(backgrounds, file, indent=2, ensure_ascii=False)


# rewrite README.md file completely with updated list.
createREADME(unique_backgrounds)
