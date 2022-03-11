import requests, json, datetime
from bs4 import BeautifulSoup
from os import path
now = datetime.datetime.now()
database = open("config.json",encoding='utf-8')
data = json.load(database)
USER_AGENT = data["user"]["USER_AGENT"]
systemLang = data["user"]["language"]
dirPath = data["user"]["file_dir"]
lang = data["system"][systemLang]
sep = lang["sep"]
if systemLang in data["system"]:
    today = now.day
    this_month = lang["months"]["_" + str(now.month)]
    this_year = now.year
    startupText = lang["sentences"]["startupText"].format(day=today, month=this_month, year=this_year)
    confirmText = lang["sentences"]["confirm"].lower()
    dirError = lang["sentences"]['dirError']
    end = lang["sentences"]['end']
    url = f"https://{systemLang}.wikipedia.org/wiki/{today}_{this_month}"
    inputText = lang["sentences"]["inputText"].format(confirm=confirmText)
    print(f"<<< {startupText} >>>")
    processText = lang["sentences"]["processText"].format(url=url)
    fileWritingText = lang["sentences"]["writing"]
    fileWriting = input(fileWritingText.format(confirm=confirmText))
    answer = input(inputText)
    if answer.lower() == confirmText:
        params = {"User Agent": USER_AGENT}
        content = requests.get(url, params).content
        soup = BeautifulSoup(content, "html.parser")
        all_Lists = soup.find_all("li", {"class": "", "id": ""})
        if fileWriting.lower() == confirmText:
            if not path.isdir(dirPath):
                print(dirError)
            else:
                print(processText)
                file = open(f"{dirPath}{today}_{this_month}.txt","w",encoding='utf-8')
                for job in all_Lists:
                    theindex = str(job.text).find(sep)
                    if(theindex != -1):
                        file.write(f"\n{job.text}")
                        print(job.text)
                print(end)
        else:
            database.close()
            print(processText)
            for job in all_Lists:
                theindex = str(job.text).find(sep)
                if(theindex != -1):
                    print(job.text)
            print(end)
    else:
        print(end)
        database.close()
else:
    print(f"{systemLang} is not supported :/")