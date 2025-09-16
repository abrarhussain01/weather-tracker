import requests
import sys
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout,QHBoxLayout,QPushButton,QLineEdit,QMainWindow
from PyQt5.QtCore import Qt
from urllib3 import request
#https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={api_key}
class weather_report(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WEATHER_REPORT")
        self.enter_city=QLabel("Enter The City :",self)
        self.city=QLineEdit(self)
        self.button=QPushButton("Get Weather",self)
        self.temp=QLabel(self)
        self.desc=QLabel(self)
        self.emoji=QLabel(self)
       # self.widget=QWidget(self)
        self.vbox=QVBoxLayout(self)
        self.guint()

    def guint(self):
        self.vbox.addWidget(self.enter_city)
        self.vbox.addWidget(self.city)
        self.vbox.addWidget(self.button)
        self.vbox.addWidget(self.temp)
        self.vbox.addWidget(self.emoji)
        self.vbox.addWidget(self.desc)
       # self.widget.setLayout(self.vbox)

        self.enter_city.setAlignment(Qt.AlignCenter)
        self.city.setAlignment(Qt.AlignCenter)
        self.temp.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.desc.setAlignment(Qt.AlignCenter)

        self.enter_city.setObjectName("enter_city")
        self.city.setObjectName("city")
        self.temp.setObjectName("temp")
        self.emoji.setObjectName("emoji")
        self.desc.setObjectName("desc")
        self.button.setObjectName("button")

        self.setStyleSheet("""
        QLabel,QPushButton{
            font-family:calibri;
        }
        QLabel#enter_city{
            font-size:40px;
            font-style: italic;
            }
        QLineEdit#city{
            font-size:40px;
            }
        QPushButton{
            font-size:30px;
            font-weight:bold;
            }       
        QLabel#temp{
            font-size:75px;
            }
        QLabel#emoji{
            font-size:100px;
            font-family:segoe ui emoji; 
            }
        QLabel#desc{
            font-size:50px;
            }        
        """)
        self.button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key="4f7e3942c976bb04147e4025a2ad3f41"
        city=self.city.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response=requests.get(url)
            response.raise_for_status()

            data=response.json()

            if(data["cod"]==200):
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nCheck the input")
                case 401:
                    self.display_error("Unauthorised:\nInvalid api key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal server error:\nTry again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from server")
                case 503:
                    self.display_error("Service unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway timeout:\nNo response from server")
                case _:
                    self.display_error(f"HTTP ERROR OCCURED\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe Request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self,message):
        self.temp.setStyleSheet("font-size:40px")
        self.temp.setText(message)
        self.emoji.clear()
        self.desc.clear()

    def display_weather(self,data):
        temp_k=data["main"]["temp"]
        temp_c=temp_k-273.15
        temp_f = (temp_k*9/5)-459.67
        self.temp.setText(f"{temp_c:.0f}°C")
        weather_id=data["weather"][0]["id"]
        self.emoji.setText(self.get_emoji(weather_id))
        weather_desc=data["weather"][0]["description"]
        self.desc.setText(weather_desc)


    @staticmethod
    def get_emoji(weather_id):
        if(weather_id>=200 and weather_id<=232):
            return"⛈️"
        elif(weather_id>=300 and weather_id<=321):
            return "⛅"
        elif(weather_id>=500 and weather_id<=531):
            return "🌧️"
        elif(weather_id>=600 and weather_id<=622):
            return "❄️"
        elif(weather_id>=701 and weather_id<=741):
            return "🌫️"
        elif weather_id==762:
            return "🌋"
        elif weather_id==771:
            return "💨"
        elif weather_id==781:
            return "🌪️"
        elif weather_id==800:
            return "☀️"
        elif (weather_id>=801 and weather_id<=804):
            return "☁️"
        else:
            return ""
#main code
if __name__=="__main__":
    app=QApplication(sys.argv)
    main_window=weather_report()
    main_window.show()
    sys.exit(app.exec_())