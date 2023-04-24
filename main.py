import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

API = os.getenv("WEATHER_KEY") 
WEBHOOK = os.getenv("BOT_WEBHOOK") 


# 定义一个获取天气信息并推送到飞书机器人的函数
def send_weather():
    # 获取天气数据
    url = "https://api.seniverse.com/v3/weather/daily.json"
    payload = {
        "key":API,
        "location": "shanghai",
        "language": "zh-Hans",
        "unit": "c",
        "start": 0,
        "days": 1
    }
    response = requests.get(url, params=payload)
    data = response.json()["results"][0]["daily"][0]

    # 构造要推送的消息
    message = f"上海今日天气：{data['text_day']}，\n最高气温：{data['high']}℃，\n最低气温：{data['low']}℃，" \
              f"\n风向：{data['wind_direction']}，\n风速：{data['wind_speed']}，\n风力等级：{data['wind_scale']}，" \
              f"\n降水量：{data['rainfall']}mm，\n降水概率：{data['precip']}%，\n相对湿度：{data['humidity']}% "

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
    response = requests.post(WEBHOOK,
                             headers=headers, json=data)


# 程序入口
if __name__ == "__main__":
    # 构造定时任务
    scheduler = BlockingScheduler()
    scheduler.add_job(send_weather, "cron", hour =6 , minute = 45 , day_of_week='mon-fri' ,timezone ='Asia/Shanghai')

    # 启动定时任务
    scheduler.start()
