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

        self.city = "台南市"
        self.area = "南區"

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
        text = "目前查詢地點: " + self.city
        text += "\n請選擇想查詢的區域"

        title = "Weather Bot"
        buttons = [
            MessageTemplateAction(
                label = "北區",
                text = "北區"
            ),
            MessageTemplateAction(
                label = "中區",
                text = "中區"
            ),
            MessageTemplateAction(
                label = "南區",
                text = "南區"
            ),
        ]
        url = "https://i.imgur.com/BdOJmjV.png"

        reply_token = event.reply_token
        send_button_message(reply_token, text, buttons, title, url)


    def on_exit_setting_area(self, event):
        pass


    ########## setting-city #########

    def on_enter_setting_city(self, event):
        self.area = event.message.text


        text = "目前查詢地點: " + self.city
        text += "\n請選擇想查詢的城市"

        title = "Weather Bot"
        if self.area == "北區":
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
        elif self.area == "中區":
            buttons = [
                MessageTemplateAction(
                    label = "台中市",
                    text = "台中市"
                ),
            ]
        elif self.area == "南區":
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
        self.city = event.message.text
        reply_token = event.reply_token
        send_text_message(reply_token, "成功設置查詢地點: " + self.city)
        self.go_back()

    def on_exit_change_city(self):
        pass


    ########## temperature #########

    def on_enter_temperature(self, event):
        
        get_weather_data_temperature(self.city)

        im = pyimgur.Imgur("e68af9d49ba23bb")
        upload_image = im.upload_image("temperature.png", title="TOC_FSM_temperature")
        print("----------")
        print(upload_image.link)
        print("----------")

        reply_token = event.reply_token
        # send_text_message(reply_token, upload_image.link)
        send_image_url(reply_token, upload_image.link, self.city + "一周氣溫圖:")
        self.go_back()

    def on_exit_temperature(self):
        print("Leaving temperature")


    ########## raining #########

    def on_enter_raining(self, event):

        description = get_weather_discription(self.city)
        reply_token = event.reply_token

        im = pyimgur.Imgur("e68af9d49ba23bb")
        upload_image = im.upload_image("raining.png", title="TOC_FSM_raining")
        print("----------")
        print(upload_image.link)
        print("----------")

        reply_token = event.reply_token
        send_image_url(reply_token, upload_image.link, description + "\n\n降雨機率表:")

        self.go_back()

    def on_exit_raining(self):
        print("Leaving raining")


    ########## air #########

    def on_enter_air(self, event):
        description = get_air_condition(self.city)

        reply_token = event.reply_token
        send_text_message(reply_token, description)
        self.go_back()

    def on_exit_air(self):
        print("Leaving air")

