import os                                   #робота з папкою
import requests                             #парсинг
from bs4 import BeautifulSoup               #
from geopy.geocoders import Nominatim       #повернення країни (для парсингу)
import matplotlib.pyplot as plt             #графіки
import json                                 #збереження в файл
from datetime import date                   #для сьогоднішньої дати


class sinoptik():
    """Клас синоптика"""
    def __init__(self, city):
        self.city = city
        self.data = [[],[]]
        self.temp_now = None
        self.humidity_now = None
        self.date = date.today().strftime('%d-%m-%Y')

        self.container = [self.city, self.data, self.temp_now, self.humidity_now,self.data]

    def parce_weather(self):
        """
        Парсинг погоди з сайту
        """
        geolocator = Nominatim(user_agent="geo_lookup")
        location = geolocator.geocode(self.city, language="en")
        country = location.address.split(",")[-1].strip()
        if country == "United States":country = "usa"
        elif country == "United Kingdom":country="uk"


        #Адреса сторінки з погодою
        url = f"https://www.timeanddate.com/weather/{country}/{self.city}"      
        #Заголовки
        headers = {"User-Agent": "Mozilla/5.0"}

        #html код сторінки
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return response.status_code     #Якщо 200 - успіх
        
        #Парсинг
        soup = BeautifulSoup(response.text, "html.parser")

        temp_tag = soup.find("div", class_="h2")
        
        temp = soup.find_all('tr')
        for i in temp:
            if "Humidity: " in str(i): humidity_tag = i.find_next("td")
            if "Temperature<" in str(i): self.data[0] = i.find_all("td")
            if "Humidity<" in str(i): self.data[1] = i.find_all("td")

        #виокремлення данних з тегів для графіків
        for i in range(len(self.data[0])): self.data[0][i] = ''.join(filter(str.isdigit, str(self.data[0][i]))); self.data[0][i] = int(self.data[0][i])
        for i in range(len(self.data[1])): self.data[1][i] = ''.join(filter(str.isdigit, str(self.data[1][i]))); self.data[1][i] = int(self.data[1][i])

        #виокремлення данних з тегів для того що зараз
        if temp_tag and humidity_tag:
            self.temp_now = int(temp_tag.text.strip().replace("°C", ""))
            self.humidity_now = int(humidity_tag.text.strip().replace("%", ""))
            return self.temp_now, self.humidity_now
        else:
            return 0
        
    def make_graph(self):
        """Створення графіків"""
        try:
            plt.plot(["6","12","18","24","30","36","42"], self.data[0], 'ro-')
            plt.savefig(f'{os.path.dirname(os.path.realpath(__file__))}/temp.png', dpi=200)
            plt.cla()
            plt.plot(["6","12","18","24","30","36","42"], self.data[1], 'bs-')
            plt.savefig(f'{os.path.dirname(os.path.realpath(__file__))}/humidity.png', dpi=200)
            plt.close()
        except:
            plt.close()

    #Зберігати як JSON
    def export(self,name):
        """Збереження даних в JSON"""
        f = open(f"{name}.json", "w")
        self.container = [self.city, self.data, self.temp_now, self.humidity_now,self.data]
        json.dump(self.container, f, indent=4)
    
    def load(self,name):
        """Завантаження даних з JSON"""
        try:
            f = open(f"{name}", "r")
            self.container = json.load(f)
            self.city, self.data, self.temp_now, self.humidity_now,self.data = self.container
        except:
            print("Error, the file is invalid, or wrong format")


        



    
city = sinoptik(None)
