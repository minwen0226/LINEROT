import json
file = open("data.txt",mode = "r", encoding = "utf-8")
data = json.load(file)
file.close()

#flask
from flask import * #載入flask
app = Flask("My Website") #建立一個網站應用程式物件
#網址網站http:/主機名稱/路徑?參數名稱=資料&參數名稱=資料&...
#https://minwen.herokuapp.com/
@app.route("/") #指定對應網址路徑
def home(): #對應的處理函式
    return render_template("home.html") #回應給前端的信息

#eg:https://minwen.herokuapp.com/test.php?keyword=關鍵字
@app.route("/test.php") #指定對應網址路徑
def test(): #對應的處理函式
    #取得網址列上參數:request.args.get("參數名稱". 預設值)
    keyword = request.args.get("keyword", None)
    if keyword == None:
        return redirect("/")
    else:
        if keyword in data:
            return render_template("result.html",result = data[keyword])
        else:
            return render_template("result.html",result = "沒有翻譯")
if __name__=="__main__": #如果以主程式執行，立即啟動伺服器
    app.run() #啟動伺服器 #ctrl+c--暫停

# https://minwen.herokuapp.com/static/images/meow2.jpg
# https://minwen.herokuapp.com/static/images/small.jpg
import json # 解讀json套件
import urllib.request # 發送連線套件
@app.route("/linebot", methods = ["GET", "POST"]) # 指定對應網址路徑
def linebot():

    # 取得Line傳遞過來的
    content = request.json  # 整包資訊
    event = content["events"][0] # 發生的事件(使用者傳遞訊息、使用者加入好友等等)
    eventType = event["type"] # 事件型態
    replyToken = event["replyToken"] # 回應這個訊息，需要的key(token)
    text = event["message"]["text"] # 取得使用者真正傳遞的訊息文字
    # 準備回傳給使用者
    if "圖片" in text:
        message = {
            "type":"image",
            "originalContentUrl":"https://minwen.herokuapp.com/static/images/meow2.jpg",
            "previewImageUrl":"https://minwen.herokuapp.com/static/images/small.jpg"
        }
    else:
        if text == "你是誰":
            replyText = "敏妏真的棒"
        elif "雨量" in text:
            #抓取雨量資料
            url ="http://117.56.59.17/OpenData/API/Rain/Get?stationNo=&loginId=open_rain&dataKey=85452C1D"
            response = urllib.request.urlopen(url)
            response = response.read().decode("utf-8")
            weather = json.loads(response)
            #準備回應
            replyText = "雨量觀測資料："
            stations = weather["data"]
            # 確認想找的地區
            areas = ["文山", "大安", "中正", "中山", "松山", "信義", "南港", "內湖", "萬華", "士林", "北投"]
            area = None # 記錄使用者的搜尋目標
            for a in areas:
                if a in text:
                    area = a
                    break
            # 根據使用者想找的地區給資料
            if area == None:
                replyText+="沒有資料"
            else:
                for station in stations:
                    if area in station["stationName"]:
                        replyText+="\n"+station["stationName"]+":"+str(station["rain"])+" 公厘"
        else:
            replyText = "hello"
        message = {"type":"text", "text":replyText} # 單一回訊息
    body = {  # 整包回應:可以包含很多則訊息
        "replyToken":replyToken,
        "messages":[message]
    }
    # 處理網路連線，把整包回應傳給Line
    #
    req = urllib.request.Request("https://api.line.me/v2/bot/message/reply", headers = {
        "Content-Type":"application/json",
        "Authorization":"Bearer "+"dKnTl8b6UkSZGbdiT1blhtomSr3H1k8S4LX9iVuLIyRhgqYoB1wrzjyKtiKf38eELUfqjXmWoPelWtTbK8VXRUwKvvm5tnZKfWM4RSEJwnkDZMLlq/0G+/7vjEMaVn98KjMFgcy+FZ1BI/6pvg4UKAdB04t89/1O/w1cDnyilFU="
    }, data = json.dumps(body).encode("utf8"))
    # 發出連線並取得回應
    response = urllib.request.urlopen(req)
    response = response.read().decode("utf-8")
    print(response)
    return "ok"


