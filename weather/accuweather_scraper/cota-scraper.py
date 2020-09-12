import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://www.accuweather.com/en/us/del-valle/78719/current-weather/2144521'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
headers = {'User-Agent': user_agent}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, features="html.parser")
current-weather-card card-module content-module
temp_block = soup.find('span', attrs={'class': 'large-temp'})
stats_block = soup.find('ul', attrs={'class': 'stats'})
sunrise_block = soup.find('ul', attrs={'class': 'time-period'})

temp = temp_block.text.strip()
stats = stats_block.text.strip()
sunrise= sunrise_block.text.strip()

print ("Temperature:" + temp)
print ("\nStats:\n\n" + stats)
print ("\nSunrise:\n\n" + sunrise)
