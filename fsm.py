import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import eventplot
from transitions.extensions import GraphMachine

from utils import send_text_message
from utils import send_image_url
from utils import send_button_message
from utils import get_weather_data_temperature
from utils import get_weather_discription
from utils import get_air_condition
from linebot.models import MessageTemplateAction
import pyimgur

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

        # default setting
        self.area = "南部"
        self.city = "台南市"

    def is_going_to_setting(self, event):
        return "setting" in event.postback.data

    def is_going_to_temperature(self, event):
        return "temperature" in event.postback.data

    def is_going_to_raining(self, event):
        return "raining" in event.postback.data

    def is_going_to_air(self, event):
        return "air" in event.postback.data

    ########## setting-area #########

    def on_enter_setting_area(self, event):
        # send a button message to the user, then the user can choose a area 

        text = "目前查詢地點: " + self.city
        text += "\n請選擇想查詢的區域"

        title = "Weather Bot"
        buttons = [
            MessageTemplateAction(
                label = "北部",
                text = "北部"
            ),
            MessageTemplateAction(
                label = "中部",
                text = "中部"
            ),
            MessageTemplateAction(
                label = "南部",
                text = "南部"
            ),
        ]
        url = "https://i.imgur.com/BdOJmjV.png"

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons, title, url)

    def on_exit_setting_area(self, event):
        pass


    ########## setting-city #########

    def on_enter_setting_city(self, event):
        # send a button message to the user according the area choosed, 
        # then the user can choose a city in that area 

        self.area = event.message.text

        text = "目前查詢地點: " + self.city
        text += "\n請選擇想查詢的城市"

        title = "Weather Bot"
        if self.area == "北部":
            buttons = [
                MessageTemplateAction(
                    label = "台北市",
                    text = "台北市"
                ),
                MessageTemplateAction(
                    label = "新北市",
                    text = "新北市"
                ),
                MessageTemplateAction(
                    label = "桃園市",
                    text = "桃園市"
                ),
                MessageTemplateAction(
                    label = "新竹市",
                    text = "新竹市"
                ),
            ]
        elif self.area == "中部":
            buttons = [
                MessageTemplateAction(
                    label = "台中市",
                    text = "台中市"
                ),
            ]
        elif self.area == "南部":
            buttons = [
                MessageTemplateAction(
                    label = "台南市",
                    text = "台南市"
                ),
                MessageTemplateAction(
                    label = "高雄市",
                    text = "高雄市"
                ),
            ]
        url = "https://i.imgur.com/BdOJmjV.png"

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons, title, url)

        
    def on_exit_setting_city(self, event):
        pass


    ########## change-city #########
    
    def on_enter_change_city(self, event):
        # change the city

        self.city = event.message.text
        reply_token = event.reply_token
        send_text_message(reply_token, "成功設置查詢地點: " + self.city)
        self.go_back()

    def on_exit_change_city(self):
        pass


    ########## temperature #########

    def on_enter_temperature(self, event):
        # draw the temperature chart
        get_weather_data_temperature(self.city)

        # upload the chart to imgur platform
        im = pyimgur.Imgur("e68af9d49ba23bb")
        upload_image = im.upload_image("temperature.png", title="TOC_FSM_temperature")

        # send the image message to the user
        reply_token = event.reply_token
        send_image_url(reply_token, upload_image.link, self.city + "一周氣溫圖:")
        self.go_back()

    def on_exit_temperature(self):
        pass


    ########## raining #########

    def on_enter_raining(self, event):
        # get the weather discription and draw the PoP chart
        description = get_weather_discription(self.city)
        reply_token = event.reply_token

        # upload the chart to imgur platform
        im = pyimgur.Imgur("e68af9d49ba23bb")
        upload_image = im.upload_image("raining.png", title="TOC_FSM_raining")

        # send the image message to the user
        reply_token = event.reply_token
        send_image_url(reply_token, upload_image.link, description + "\n\n降雨機率表:")

        self.go_back()

    def on_exit_raining(self):
        pass


    ########## air #########

    def on_enter_air(self, event):
        # get the air condition discription
        description = get_air_condition(self.city)

        # send the discription to the user
        reply_token = event.reply_token
        send_text_message(reply_token, description)
        self.go_back()

    def on_exit_air(self):
        pass

