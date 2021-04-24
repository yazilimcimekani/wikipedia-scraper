import requests, json, datetime
from bs4 import BeautifulSoup
from os import path
now = datetime.datetime.now()
database = open("config.json")
data = json.load(database)
USER_AGENT = data["user"]["USER_AGENT"]
systemLang = data["user"]["language"]
dirPath = data["user"]["file_dir"]
sep = data["system"][systemLang]["sep"]
if systemLang in data["system"]:
    today = now.day
    this_month = data["system"][systemLang]["months"]["_" + str(now.month)]
    this_year = now.year
    startupText = data["system"][systemLang]["sentences"]["startupText"].format(
        day=today, month=this_month, year=this_year
    )
    confirmText = data["system"][systemLang]["sentences"]["confirm"].lower()
    dirError = data["system"][systemLang]["sentences"]['dirError']
    end = data["system"][systemLang]["sentences"]['end']
    url = f"https://{systemLang}.wikipedia.org/wiki/{today}_{this_month}"
    inputText = data["system"][systemLang]["sentences"]["inputText"].format(
        confirm=confirmText
    )
    print(f"<<< {startupText} >>>")
    processText = data["system"][systemLang]["sentences"]["processText"].format(url=url)
    fileWritingText = data["system"][systemLang]["sentences"]["writing"]
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
                quit()
            else:
                print(processText)
                file = open(f"{dirPath}{today}_{this_month}.txt","w")
                # file.write(f"{today} {this_month} ({systemLang})\n/* Is there a problem with the code? https://github.com/mertssmnoglu/wikipedia-scraper/issues */")
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
        quit()
else:
    print(f"{systemLang} is not supported :/")