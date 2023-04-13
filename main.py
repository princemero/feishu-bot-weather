import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler


# 定义一个获取天气信息并推送到飞书机器人的函数
def send_weather():
    # 获取天气数据
    url = "https://api.seniverse.com/v3/weather/daily.json"
    payload = {
        "key":os.getenv(WEATHER_KEY) ,
        "location": "shanghai",
        "language": "zh-Hans",
        "unit": "c",
        "start": 0,
        "days": 1
    }
    response = requests.get(url, params=payload)
    data = response.json()["results"][0]["daily"][0]

    # 构造要推送的消息
    message = f"上海今日天气：{data['text_day']}，最高气温：{data['high']}℃，最低气温：{data['low']}℃。"

    # 推送消息到飞书机器人
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    response = requests.post(os.getenv(BOT_WEBHOOK) ,
                             headers=headers, json=data)


# 程序入口
if __name__ == "__main__":
    # 构造定时任务
    scheduler = BlockingScheduler()
    scheduler.add_job(send_weather, "cron", hour=10)

    # 启动定时任务
    scheduler.start()
