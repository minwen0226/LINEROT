import json
file = open("data.txt",mode = "r", encoding = "utf-8")
data = json.load(file)
file.close()

#flask
from flask import * #載入flask
app = Flask("My Website") #建立一個網站應用程式物件
#網址網站http:/主機名稱/路徑?參數名稱=資料&參數名稱=資料&...
#http://127.0.0.1:5000/
@app.route("/") #指定對應網址路徑
def home(): #對應的處理函式
    return"<h3>Hello Flack</h3><div>This is line 1</div><script>alert('I hate math');</script>" #回應給前端的信息

#eg:http://127.0.0.1:5000/test.php?keyword=關鍵字
@app.route("/test.php") #指定對應網址路徑
def test(): #對應的處理函式
    #取得網址列上參數:request.args.get("參數名稱". 預設值)
    keyword = request.args.get("keyword", None)
    if keyword == None:
        return redirect("/")
    else:
        if keyword in data:
            return"中文"+data[keyword]
        else:
            return"沒有翻譯"
if __name__=="__main__": #如果以主程式執行，立即啟動伺服器
    app.run() #啟動伺服器 #ctrl+c--暫停
