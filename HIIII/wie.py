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
