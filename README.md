# Weather Bot

## 介紹
提供查詢 天氣 氣溫 空氣品質 的line bot
即時擷取氣象局最新資料並採用圖表方式呈現

## 功能
### 主選單
![](https://i.imgur.com/MrVC5Ur.png)

#### 設定城市
左上為設定，按下後進入設定模式，可以選擇想要查詢的地區和城市
![](https://i.imgur.com/Tn8MJfT.png)
選擇想要查詢的區域
![](https://i.imgur.com/VnDeCX8.png)


#### 氣溫查詢
右上為氣溫查詢 可查詢最近一周每日的最高溫和最低溫
![](https://i.imgur.com/cPfIkWt.png)
![](https://i.imgur.com/wnozPi9.png)


#### 降雨機率查詢
左下為降雨機率查詢 可查詢兩天內降雨機率以及現在的天氣概況
![](https://i.imgur.com/9X4s4oj.png)
![](https://i.imgur.com/sKen1in.png)


#### 空氣品質查詢
右下為空氣品質查詢 可以查到當前空氣狀況
![](https://i.imgur.com/NvedJzK.png)
其中AQI指數為空氣品質指數
0-50:良好
51-100:普通
101-150:對敏感族群不良
151-200:對所有族群不良
201-300:非常不良
301-500:危害


## 環境設置
```
# python 3.6
$ conda install -c conda-forge pygraphviz
$ pip install python-dotenv pygraphviz transitions line-bot-sdk flask colorama
$ python app.py
$ ./ngrok.exe http 8000
# 更新Channel Webhook 網址: https://...ngrok.io/webhook
```

## FSM graph
![](https://i.imgur.com/XTe7Wc5.png)

