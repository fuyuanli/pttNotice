import json
import requests
from bs4 import BeautifulSoup

BOARD = "Gossiping"
PTT = "https://www.ptt.cc"
URL = "https://www.ptt.cc/bbs/" + BOARD + "/index.html"
cookies = {"over18":"1"}
session = requests.Session()
homeReq = session.get(URL, cookies=cookies)
soup = BeautifulSoup(homeReq.text, "html.parser")
indexResult = soup.find_all("div", class_="r-ent")
prev = PTT + soup.find("a", string = "‹ 上頁")["href"]
prevReq = session.get(prev, cookies=cookies)
prevSoup = BeautifulSoup(prevReq.text, "html.parser")
prevResult = prevSoup.find_all("div", class_="r-ent")

postDB = "posts.json"
sentDB = "sent.json"

def saveJson(data, db):
    with open(db, "w") as outfile:
        json.dump(data ,outfile, ensure_ascii=False)
def loadJson(fileName):
    with open(fileName) as jsonFile:
        data = json.load(jsonFile)
    return data

def findAllPost(pageContent):
    newest = ""
    removeSpace = lambda string: string[1:] if string[0] == " " else string
    getTag = lambda string: string.split(" ")[1] if string.split(" ")[0] == "Re:" else string.split(" ")[0]
    isReply = lambda string: True if string.split(" ")[0] == "Re:" else False
    msgList = []
    for item in pageContent:
    #    print(PTT+item.find("a")["href"], item.find("a").getText())
        date = item.find("div", class_="date").getText().replace(" ","")
        info = item.find("div", class_="title").find("a")
        if info != None:
            fulltitle = info.string
            url = PTT + info["href"]
            #tag = fulltitle.split("]")[0][1:]
            #tag = getTag(fulltitle).replace("[", "").replace("]", "")
            tag = ""
            #title = removeSpace(fulltitle.split(" ", )[1])
            title = fulltitle
            #print(date, url, tag, title)
            #print(date, fulltitle, url, tag, isReply(fulltitle))
            msg = date + " " + url + " " + tag + " " + fulltitle
            msgJson = {
                "reply": isReply(fulltitle),
                "date": date,
                "url": url,
                "tag": tag,
                "title": title
            }
            msgList.append(msgJson)
    return msgList

def searchNewPost(pageResult):
    try:
        oldPost = loadJson(postDB)
    except:
        currentPosts = findAllPost(pageResult)
        saveJson(currentPosts, postDB)
        return currentPosts
    
    currentPosts = findAllPost(pageResult)
    newPosts = []
    for item in currentPosts:
        newPost = True
        for old in oldPost:
            if item["url"] == old["url"]:
                newPost = False
        if newPost:
            newPosts.append(item)
    saveJson(oldPost + currentPosts, postDB)
    return newPosts

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code
  
token = ''
newPosts = searchNewPost(prevResult)
newPosts += searchNewPost(indexResult)
try:
    noticedPosts = loadJson(sentDB)
except:
    noticedPosts = []

for item in newPosts:
    #msg = "\n日期: " + item["date"] + "\n"
    #msg += "回覆: " + str(item["reply"]) + "\n"
    #msg += "標籤: " + item["tag"] + "\n"
    #msg = "\n" + item["date"] + "\n"
    msg = "\n" + item["title"] + "\n"
    msg += item["url"] 
    print(item["title"])
    if item["url"] not in noticedPosts:
        lineNotifyMessage(token, msg)
        noticedPosts.append(item["url"])
saveJson(noticedPosts, sentDB)
