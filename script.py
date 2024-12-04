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
        self.temperature_label = QLabel("23°C", self)
        self.emoji_label = QLabel("🌞", self)
        self.description_label = QLabel("Sunny", self)
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
            pass
        else:
            self.description_label.setText("Please enter a city name")
    
    def display_error(self):
        pass
    
    def display_weather(self):
        pass
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())