# this will be the main file for the scripting of the weather app

import sys
import os
import requests
from dotenv import load_dotenv
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
)
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QPixmap

# Load environment variables from .env file
load_dotenv()

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # declaring the elements we need
        self.city_label = QLabel("Enter city name", self)
        self.city_input = QLineEdit(self)
        self.submit_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("", self)
        self.emoji_label = QLabel("", self)
        self.description_label = QLabel("", self)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Weather App ☁️")
        self.setGeometry(600, 300, 550, 400)

        # setting up the layout
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.city_label)
        self.vbox.addWidget(self.city_input)
        self.vbox.addWidget(self.submit_button)
        self.vbox.addWidget(self.temperature_label)
        self.vbox.addWidget(self.emoji_label)
        self.vbox.addWidget(self.description_label)
        self.setLayout(self.vbox)
        
        # aligning them to center
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        # making object of each variable, this helps us to style each with using objectname
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.submit_button.setObjectName("submit_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        self.setStyleSheet(
        """
        QLabel, QPuhButton {
            font-family: calibri;
        }
        QLabel#city_label {
            font-size: 40px;
            font-style: italic;
        }
        QLineEdit#city_input {
            font-size: 30px;
            padding: 5px 10px;
            margin: 10px;
        }
        QPushButton#submit_button {
            font-size: 25px;
            font-weight: bold;
            padding: 6px 20px;
            margin: 10px;
        }
        QLabel#temperature_label {
            font-size: 50px;
        }
        QLabel#emoji_label {
            font-size: 60px;
        }
        QLabel#description_label {
            font-size: 40px;
        }
        """
        )
        
        self.submit_button.clicked.connect(self.get_weather)

    def get_weather(self):
        # Access the API key
        api_key = os.getenv("API_KEY")
        
        city = self.city_input.text()
        base_url= f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        if city:
            try:
                response = requests.get(base_url)
                response.raise_for_status()
                response = response.json()
                print(response)

                if response["cod"] == 200:
                    self.display_weather(response)
            
            except requests.exceptions.HTTPError as http_err:
                match response.status_code:
                    case 400:
                        message = "Bad Request:\nPlease check the city name."
                    case 401:
                        message = "Unauthorized:\nYour credentials aren't valid."
                    case 403:
                        message = "Forbidden:\nYou do not have access."
                    case 404:
                        message = "Not Found:\nCity does not exist."
                    case 500:
                        message = "Internal Server Error:\nPlease try again later."
                    case 502:
                        message = "Bad Gateway:\nInvalid response from the server."
                    case 503:
                        message = "Service Unavailable:\nThe server is temporarily down."
                    case 504:
                        message = "Servie Timeout:\nNo response from the server."
                    case _:
                        message = f"HTTP error occured:\n{http_err}"
                self.display_error(message)
                return
            except requests.exceptions.ConnectionError:
                self.display_error("Connection error:\nCheck your internet connection.")
            except requests.exceptions.Timeout:
                self.display_error("Request timed out:\nPlease try again later.")
            except requests.exceptions.TooManyRedirects:
                self.display_error("Too many redirects:\nPlease try later.")
            except requests.exceptions.RequestException as reqexec_err:
                self.display_error(f"Request exception:\n{reqexec_err}")
        else:
            self.description_label.setText("Please enter a city name")
    
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px; color: red;")
        self.temperature_label.setText(message)
        self.emoji_label.setText("")
        self.description_label.setText("")
    
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 50px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_id = data["weather"][0]["id"]
        description = data["weather"][0]["description"]
        
        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_emoji_method(weather_id))
        self.description_label.setText(description)

    # here we are going to define a function which will return emoji based on the code we get as argument of the weather in the data from the api
    @staticmethod
    def get_emoji_method(weather_code):
        if weather_code >= 200 and weather_code <= 232:
            return "⛈️"
        elif weather_code >= 300 and weather_code <= 321:
            return "🌦️"
        elif weather_code >= 500 and weather_code <= 531:
            return "🌧️"
        elif weather_code >= 600 and weather_code <= 622:
            return "❄️"
        elif weather_code >= 701 and weather_code <= 741:
            return "🌫️"
        elif weather_code == 762:
            return "🌋"
        elif weather_code == 771:
            return "💨"
        elif weather_code == 781:
            return "🌪️"
        elif weather_code == 800:
            return "🌞"
        elif weather_code >= 801 and weather_code <= 804:
            return "🌤️"
        else:
            return ""
    
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())