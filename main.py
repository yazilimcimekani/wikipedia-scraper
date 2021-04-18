import requests, json, datetime
from bs4 import BeautifulSoup

now = datetime.datetime.now()
database = open("config.json")
data = json.load(database)
USER_AGENT = data["user"]["USER_AGENT"]
systemLang = data["user"]["language"]
sep = data["system"][systemLang]["sep"]
if systemLang in data["system"]:
    bugun = now.day
    ay = data["system"][systemLang]["months"]["_" + str(now.month)]
    startupText = data["system"][systemLang]["sentences"]["startupText"].format(
        day=bugun, month=ay, year=now.year
    )
    url = f"https://{systemLang}.wikipedia.org/wiki/{bugun}_{ay}"
    inputText = data["system"][systemLang]["sentences"]["inputText"].format(
        confirm=data["system"][systemLang]["sentences"]["confirm"].lower()
    )
    processText = data["system"][systemLang]["sentences"]["processText"].format(url=url)
    confirmText = data["system"][systemLang]["sentences"]["confirm"].lower()
    print(f"<<< {startupText} >>>")
    answer = input(inputText)
    if answer.lower() == confirmText:
        database.close()
        print(processText)
        params = {"User Agent": USER_AGENT}
        content = requests.get(url, params).content
        soup = BeautifulSoup(content, "html.parser")
        all_Lists = soup.find_all("li", {"class": "", "id": ""})
        for job in all_Lists:
            theindex = str(job.text).find(sep)
            if(theindex != -1):
                print(job.text)
else:
    print(f"{systemLang} is not supported :/")