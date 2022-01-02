import os
import requests
import json

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate
import matplotlib.pyplot as plt 
import matplotlib.image
from scipy.interpolate import make_interp_spline
import numpy as np


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def get_weather_data_temperature(location):
    if location == "台北市":
        displayLocation = "Taipei City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-063"
        locationName = "大安區"
    if location == "新北市":
        displayLocation = "New Taipei City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-071"
        locationName = "板橋區"
    if location == "桃園市":
        displayLocation = "Taoyuan City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-007"
        locationName = "桃園區"
    if location == "新竹市":
        displayLocation = "Hsinchu City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-055"
        locationName = "東區"
    if location == "台中市":
        displayLocation = "Taichung City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-075"
        locationName = "西區"
    if location == "台南市":
        displayLocation = "Tainan City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-079"
        locationName = "東區"
    if location == "高雄市":
        displayLocation = "Kaohsiung City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-067"
        locationName = "苓雅區"

    params = {
        "Authorization": "CWB-715EF7DE-990A-497E-9908-AA23A028213D",
        "elementName": ["MinT", "MaxT"],
        "locationName": locationName
    }
    response = requests.get(url, params=params)
    # print("------------------------")
    data = json.loads(response.text)
    MinTemperature = []
    MaxTemperature = []
    time = []
    x = []
    index = 1
    startTime = data["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][0]["startTime"]
    for element in data["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"]:
        if not element["startTime"][5:10] in time :
            x.append(index)
            index = index + 1
            MinTemperature.append(int(element["elementValue"][0]["value"]))
            time.append(element["startTime"][5:10])

    time = []
    for element in data["records"]["locations"][0]["location"][0]["weatherElement"][1]["time"]:
        if not element["startTime"][5:10] in time :
            MaxTemperature.append(int(element["elementValue"][0]["value"]))
            time.append(element["startTime"][5:10])
    # print("------------------------")

    # print(MinTemperature)
    # print(MaxTemperature)

    plt.figure(figsize=(12,8), dpi=80)
    
    model=make_interp_spline(x, MaxTemperature)
    xs=np.linspace(1,7,500)
    ys=model(xs)
    plt.plot(xs, ys, color = "#E9736D", linestyle = "--", linewidth = 4.5, label = "Max Temp")

    model=make_interp_spline(x, MinTemperature)
    xs=np.linspace(1,7,500)
    ys=model(xs)
    plt.plot(xs, ys, color = "#5380EA", linestyle = "--", linewidth = 4.5, label = "Min Temp")

    plt.title(displayLocation + ", weekly weather forecast, start time :" + startTime, fontsize = 16, color = "#575757")
    plt.ylim((min(MinTemperature) - 3, max(MaxTemperature) + 3))
    plt.xticks([1,2,3,4,5,6,7], time)
    plt.grid()
    plt.legend()
    plt.xlabel("Date", fontsize = 16, color = "#575757")
    plt.ylabel("Celsius", fontsize = 16, color = "#575757")
    plt.savefig("temperature.png")
    
    return 

def get_weather_discription(location):
    if location == "台北市":
        displayLocation = "Taipei City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-061"
        locationName = "大安區"
    if location == "新北市":
        displayLocation = "New Taipei City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-069"
        locationName = "板橋區"
    if location == "桃園市":
        displayLocation = "Taoyuan City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-005"
        locationName = "桃園區"
    if location == "新竹市":
        displayLocation = "Hsinchu City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-053"
        locationName = "東區"
    if location == "台中市":
        displayLocation = "Taichung City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-073"
        locationName = "西區"
    if location == "台南市":
        displayLocation = "Tainan City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-077"
        locationName = "東區"
    if location == "高雄市":
        displayLocation = "Kaohsiung City"
        url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-065"
        locationName = "苓雅區"

    params = {
        "Authorization": "CWB-715EF7DE-990A-497E-9908-AA23A028213D",
        "elementName": ["WeatherDescription", "PoP6h"],
        "locationName": locationName
    }
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    
    description = location + "6小時內天氣概況如下:\n\n"
    description += data["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][0]["elementValue"][0]["value"]

    PoPs = []
    times = []
    for element in data["records"]["locations"][0]["location"][0]["weatherElement"][1]["time"]:
        if len(PoPs) >= 7:
            break
        PoPs.append(element["elementValue"][0]["value"])
        times.append(element["startTime"][5:10] + ' ' + element["startTime"][11:16])

    # print(PoPs)
    # print(times)

    PoP_img = matplotlib.image.imread("assets/PoP.png")
    fig, ax = plt.subplots(figsize=(7,3), dpi=80)
    plt.imshow(PoP_img)
    plt.title(displayLocation + ", probability of precipitation next two days" , fontsize = 12, color = "#575757")
    plt.xticks([])
    plt.yticks([])

    for i in range(7):
        ax.text(33 + 200*i, 75, times[i][0:5], fontsize = 12)
        ax.text(20 + 200*i, 145, times[i][5:], fontsize = 12)
        ax.text(45 + 200*i, 320, PoPs[i] + "%", fontsize = 16)

    plt.savefig("raining.png")

    return description

def get_air_condition(location):
    api_key = "81d875e6-6d74-4c4d-90a0-40b4f68e4fdd"
    if location == "台北市":
        County = "臺北市"
        SiteName = ["松山", "士林", "中山", "萬華", "大同"]
        url = "https://data.epa.gov.tw/api/v1/aqx_p_432?format=json&limit=1&api_key=" + api_key + "&filters=SiteName,EQ,士林&County,EQ,臺北市"

    if location == "新北市":
        County = "新北市"
        SiteName = ["板橋", "汐止", "新店", "新莊", "淡水"]
        url = "https://data.epa.gov.tw/api/v1/aqx_p_432?format=json&limit=1&api_key=" + api_key + "&filters=SiteName,EQ,汐止&County,EQ,新北市"

    if location == "桃園市":
        County = "桃園市"
        SiteName = ["桃園", "大園", "觀音", "平鎮", "龍潭"]
        url = "https://data.epa.gov.tw/api/v1/aqx_p_432?format=json&limit=1&api_key=" + api_key + "&filters=SiteName,EQ,桃園&County,EQ,桃園市"

    if location == "新竹市":
        County = "新竹市"
        SiteName = ["新竹", "竹東", "湖口"]
        url = "https://data.epa.gov.tw/api/v1/aqx_p_432?format=json&limit=1&api_key=" + api_key + "&filters=SiteName,EQ,竹東&County,EQ,新竹縣"

    if location == "台中市":
        County = "臺中市"
        SiteName = ["豐原", "沙鹿", "大里", "忠明", "西屯"]
        url = "https://data.epa.gov.tw/api/v1/aqx_p_432?format=json&limit=1&api_key=" + api_key + "&filters=SiteName,EQ,豐原&County,EQ,臺中市"

    if location == "台南市":
        County = "臺南市"
        SiteName = ["新營", "善化", "安南", "台南"]
        url = "https://data.epa.gov.tw/api/v1/aqx_p_432?format=json&limit=1&api_key=" + api_key + "&filters=SiteName,EQ,臺南&County,EQ,臺南市"

    if location == "高雄市":
        County = "高雄市"
        SiteName = ["左營", "前鎮", "小港", "楠梓", "鳳山"]
        url = "https://data.epa.gov.tw/api/v1/aqx_p_432?format=json&limit=1&api_key=" + api_key + "&filters=SiteName,EQ,左營&County,EQ,高雄市"

    response = requests.get(url)
    data = json.loads(response.text)

    # print(url)
    # print(data["records"])

    if len(data["records"]) <= 0:
        print("------------------")
        print("REQ:" + url)
        print(data)
        print("------------------")
        return "伺服器異常 請稍候再試"

    data = data["records"][0]
    # print("------------------")
    # print(data)
    # print("------------------")


    descriptions = data["County"] + " " + data["SiteName"] + "測站\n" 
    descriptions += "時間: " + data["PublishTime"] + "\n"
    descriptions += "------------------\n"
    descriptions += "空氣品質: \" " + data["Status"] + " \"\n"
    descriptions += "AQI指數:" + data["AQI"] + "\n"
    descriptions += "PM2.5: " + data["PM2.5"] + "(ug/m3)\n"
    descriptions += "PM10: " + data["PM10"] + "(ug/m3)\n"

    return descriptions

def send_image_url(replyToken, img_url, text):
    line_bot_api = LineBotApi(channel_access_token)
    image_message = ImageSendMessage(
        original_content_url=img_url,
        preview_image_url=img_url
    )
    line_bot_api.reply_message(replyToken, [TextSendMessage(text=text), image_message])

    return


def send_button_message(replyToken, text, buttons, title, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text = 'button template',
        template = ButtonsTemplate(
            title=title,
            text=text,
            thumbnail_image_url = url,
            actions = buttons
        )
    )
    line_bot_api.reply_message(replyToken, message)
    
    return

