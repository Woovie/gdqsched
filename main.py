import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs
import json

gdqURL = 'https://gamesdonequick.com/schedule'
scheduleData = {}

req = requests.get(gdqURL)
if (req.status_code == 200):
    print('200 received from gdq site, parsing code...')
    soup = bs(req.content, 'html.parser')
    runTable = soup.find(id="runTable")
    tableBody = runTable.tbody
    for row in tableBody.find_all(class_="second-row"):
        runnerData = row.find_next_sibling("tr")
        if (len(runnerData.select("td:nth-of-type(4)")) > 0):
            runLength = row.select("td:nth-of-type(1)")[0].contents[2][1:][:-1]
            runType, console = row.select("td:nth-of-type(2)")[0].contents[0].split(" — ")
            host = row.select("td:nth-of-type(3)")[0].contents[1][1:]
            runnerData = row.find_next_sibling("tr")
            startTime = datetime.strptime(runnerData.select("td:nth-of-type(1)")[0].contents[0], '%Y-%m-%dT%H:%M:%SZ')
            gameTitle = runnerData.select("td:nth-of-type(2)")[0].contents[0]
            runner = runnerData.select("td:nth-of-type(3)")[0].contents[0]
            setupLength = runnerData.select("td:nth-of-type(4)")[0].contents[2][1:][:-1]
            scheduleData[startTime.timestamp()] = {
                "length": runLength,
                "type": runType,
                "runner": runner,
                "host": host,
                "console": console,
                "title": gameTitle,
                "setup": setupLength
            }
    file = open("schedule.json", "w")
    file.write(json.dumps(scheduleData))
    file.close()
    print('JSON written, finished')
else:
    print('error received! check URL to ensure it resolves without issue')
