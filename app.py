from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
# time getting model
from datetime import datetime,timezone,timedelta
# global var
time_int = 0
# time schedule
climbNorth = [
	"7:20 Red\n7:45 Red\n7:50 Red",
	"8:05 Red\n8:15 Red\n8:25 Red\n8:35 Red\n8:40 Red\n8:45 Red\n8:50 Red\n8:55 Red",
	"9:00 Green\n9:05 Red\n9:15 Green\n9:25 Red\n9:35 Red\n9:40 Red\n9:45 Red\n9:50 Red\n9:55 Red",
	"10:00 Red\n10:05 Red\n10:10 Red\n10:20 Green\n10:35 Red\n10:55 Green",
	"11:15 Red\n11:35 Green\n11:55 Red",
	"12:00 Red\n12:05 Red\n12:10 Red\n12:15 Green\n12:30 Red\n12:40 Red\n12:50 Red\n12:55 Red",
	"13:00 Red\n13:05 Red\n13:10 Red\n13:10 Red\n13:15 Red\n13:20 Red\n13:25 Green\n13:35 Red\n13:45 Red\n13:55 Red",
	"14:00 Green\n14:05 Red\n14:10 Green\n14:15 Red\n14:25 Green\n14:35 Red\n14:45 Green\n14:55 Red",
	"15:00 Red\n15:05 Red\n15:10 Red\n15:15 Red\n15:20 Red\n15:25 Red\n15:30 Green\n15:35 Red\n15:50 Green",
	"16:10 Red\n16:20 Green\n16:25 Red\n16:35 Green\n16:50 Red",
	"17:05 Red\n17:15 Red\n17:20 Red\n17:25 Red\n17:35 Red\n17:45 Green\n17:55 Red",
	"18:05 Green\n18:10 Red\n18:15 Red\n18:18 Red\n18:20 Red\n18:25 Red\n18:35 Red\n18:50 Green",
	"19:05 Green\n19:25 Red\n19:55 Green",
	"20:25 Green",
	"21:00 Red\n21:10 Green\n21:25 Green\n21:45 Red",
	"22:00 Green\n22:20 Green"
]
Descent = [
	"7:27 Red\n7:52 Red\n7:57 Red",
	"8:12 Red\n8:22 Red\n8:32 Red\n8:42 Both\n8:47 Red\n8:52 Both\n8:57 Both",
	"9:02 Both\n9:07 Green\n9:12 Red\n9:22 Green\n9:32 Both\n9:42 Both\n9:47 Both\n9:52 Both\n9:57",
	"10:02 Both\n10:07 Both\n10:12 Both\n10:17 Both\n10:27 Green\n10:42 Red",
	"11:02 Green\n11:22 Red\n11:42 Green",
	"12:02 Both\n12:07 Both\n12:12 Both\n12:17 Both\n12:22 Green\n12:37 Both\n12:47 Both\n12:57 Both",
	"13:02 Red\n13:07 Both\n13:12 Both\n13:17 Both\n13:22 Both\n13:27 Red\n13:32 Green\n13:42 Red\n13:52 Both",
	"14:02 Both\n14:07 Green\n14:12 Red\n14:17 Green\n14:22 Red\n14:32 Green\n14:42 Red\n14:52 Green\n14:47 Both",
	"15:02 Both\n15:07 Red\n15:12 Both\n15:17 Both\n15:22 Both\n15:27 Both\n15:32 Red\n15:37 Green\n15:42 Red\n15:57 Green",
	"16:17 Red\n16:27 Green\n16:32 Red\n16:42 Green\n16:57 Red",
	"17:12 Both\n17:22 Both\n17:27 Red\n17:32 Both\n17:42 Red\n17:52 Green",
	"18:02 Red\n18:12 Green\n18:17 Red\n18:22 Both\n18:25 Red\n18:27 Both\n18:32 Both\n18:42 Red\n18:57 Green",
	"19:12 Green\n19:32 Red",
	"20:02 Green\n20:32 Green",
	"21:07 Red\n21:17 Green\n21:32 Green\n21:52 Red",
	"22:07 Green\n22:27 Green" 
]
app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('4oJtXmZnyETMFX+ZjYA2PbaQtoqLBqdI5sYsrdbHhPOtBjmkGkMrFTjlHOA0YGg/CpEflx2pARxFZfv8LG8KKFYO37oniaa6QZVRw4dzknvVCCaeRoqzqT5NXgDzPslAtiQv/UCpJzU9bKw4wr86hgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('9a44296ac9206bd2d47145c976fcfe34')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "上山下一班":
        check_back = time_check_up()
        if check_back == "0":
            message = TextSendMessage(text="假日機器人也要休息啦～")
        else:
            message = TextSendMessage(text=check_back)
        # rely to the client
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text == "下山下一班":
        check_back = time_check_down()
        if check_back == "0":
            message = TextSendMessage(text="假日機器人也要休息啦～")
        else:
            message = TextSendMessage(text=check_back)
        # rely to the client
        line_bot_api.reply_message(event.reply_token, message)

# checking time
def time_check_up():
    # current time getting
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    dt2 = dt2.strftime("%H%M")
    time_int = int(dt2)
    dayWeek = datetime.now().weekday() # 0~6是星期一到星期日
    # 平日情形
    if dayWeek < 5:
        if time_int < 799:
            if time_int > 750:
                return climbNorth[1]
            return climbNorth[0]
        elif time_int < 899:
            if time_int > 855:
                return climbNorth[2]
            return climbNorth[1]
        elif time_int < 999:
            if time_int > 955:
                return climbNorth[3]
            return climbNorth[2]
        elif time_int < 1099:
            if time_int > 1055:
                return climbNorth[4]
            return climbNorth[3]
        elif time_int < 1199:
            if time_int > 1155:
                return climbNorth[5]
            return climbNorth[4]
        elif time_int < 1299:
            if time_int > 1255:
                return climbNorth[6]
            return climbNorth[5]
        elif time_int < 1399:
            if time_int > 1355:
                return climbNorth[7]
            return climbNorth[6]
        elif time_int < 1499:
            if time_int > 1455:
                return climbNorth[8]
            return climbNorth[7]
        elif time_int < 1599:
            if time_int > 1550:
                return climbNorth[9]
            return climbNorth[8]
        elif time_int < 1699:
            if time_int > 1650:
                return climbNorth[10]
            return climbNorth[9]
        elif time_int < 1799:
            if time_int > 1755:
                return climbNorth[11]
            return climbNorth[10]
        elif time_int < 1899:
            if time_int > 1850:
                return climbNorth[12]
            return climbNorth[11]
        elif time_int < 1999:
            if time_int > 1955:
                return climbNorth[13]
            return climbNorth[12]
        elif time_int < 2099:
            if time_int > 2025:
                return climbNorth[14]
            return climbNorth[13]
        elif time_int < 2199:
            if time_int > 2145:
                return climbNorth[15]
            return climbNorth[14]
        elif time_int < 2299:
            if time_int > 2220:
                return climbNorth[0]
            return climbNorth[15]  
    # 假日情形
    else:
        return "0"
def time_check_down():
    # current time getting
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    dt2 = dt2.strftime("%H%M")
    time_int = int(dt2)
    dayWeek = datetime.now().weekday() # 0~6是星期一到星期日
    # 平日情形
    if dayWeek < 5:
        if time_int < 799:
            if time_int > 757:
                return Descent[1]
            return Descent[0]
        elif time_int < 899:
            if time_int > 857:
                return Descent[2]
            return Descent[1]
        elif time_int < 999:
            if time_int > 957:
                return Descent[3]
            return Descent[2]
        elif time_int < 1099:
            if time_int > 1042:
                return Descent[4]
            return Descent[3]
        elif time_int < 1199:
            if time_int > 1142:
                return Descent[5]
            return Descent[4]
        elif time_int < 1299:
            if time_int > 1257:
                return Descent[6]
            return Descent[5]
        elif time_int < 1399:
            if time_int > 1352:
                return Descent[7]
            return Descent[6]
        elif time_int < 1499:
            if time_int > 1447:
                return Descent[8]
            return Descent[7]
        elif time_int < 1599:
            if time_int > 1557:
                return Descent[9]
            return Descent[8]
        elif time_int < 1699:
            if time_int > 1657:
                return Descent[10]
            return Descent[9]
        elif time_int < 1799:
            if time_int > 1752:
                return Descent[11]
            return Descent[10]
        elif time_int < 1899:
            if time_int > 1857:
                return Descent[12]
            return Descent[11]
        elif time_int < 1999:
            if time_int > 1932:
                return Descent[13]
            return Descent[12]
        elif time_int < 2099:
            if time_int > 2032:
                return Descent[14]
            return Descent[13]
        elif time_int < 2199:
            if time_int > 2152:
                return Descent[15]
            return Descent[14]
        elif time_int < 2299:
            if time_int > 2227:
                return Descent[0]
            return Descent[15]
        
    # 假日情形
    else:
        return "0"

# os setting
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
