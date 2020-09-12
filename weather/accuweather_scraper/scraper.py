from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json

<<<<<<< Updated upstream

#function returns a dictionary where the keys relate to weather attributes
#keys: chances, status, visibility, UV_index, pressure, humidity, wind, now, sun_rise, and temp

#makes connection to website for weather data
weather = {}
url = 'https://weather.com/weather/today/l/a9e8362791a8366662d2f306c08fc5496d43c98ec529f1044339f09454cc23a9'
req = Request(url ,headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read() # need this line to overrun mod security
soup = BeautifulSoup(page, 'html.parser')


# Loads data from Json file to request properly
def load_data():
    with open("req_data.json") as f:  #opens json file template
        json_data = json.load(f)
    for tag in json_data["tags"]:
        html_tag = tag["html_tag"]     #iterates through and selects all data to be parsed
        for attr in tag["attr_tags"]:
            for attr_data in tag["attr_tags"][attr]:
                class_data = tag["attr_tags"][attr][attr_data] 
                return_data(attr_data, html_tag, attr, class_data)
    print(weather)


'''
name (name) = soup.find("span" (type), attrs={'class' (classification): "_-_-components-src-atom-WeatherData-Wind-Wind--windWrapper--3Ly7c undefined" (classname)})
weather['wind'] = wind
'''

#finds data based on inputted tag and returns relevant weather results or a message saying that the weather data could not be found
def return_data(name, tag_type, classification, classname):
    data = soup.find(tag_type, attrs={classification: classname})
    if data is not None:
        data = data.text.strip()
        weather[name] = data
    else:
        print(f"{name} from the tag {tag_type} did not pull up any data. Ignoring.")


load_data()
=======
url = 'https://www.accuweather.com/en/us/austin-tx/78701/hourly-weather-forecast/351193'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
headers = {'User-Agent': user_agent}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, features="html.parser")
dataStr = ''
#print(soup)
for a in soup.findAll('div', {'class': 'accordion-item hourly-card-nfl hour non-ad'}):
    dataStr += a.text
data = dataStr.split()
labelStr = ['RealFeel', 'Wind', 'mph', 'Gusts:', 'Humidity',
            'Dew', 'Point', 'Max', 'UV', 'Index', '(', ')',
            'Cover', 'Rain', 'in', 'Snow', 'Ice', 'Visibility',
            'mi', 'Ceiling', 'Cloud', 'ft']
fData = []
for s in data:
    makeNew = False
    canAdd = True
    for s1 in labelStr:
        if (s1 in s):
            if (labelStr[0] in s):
                makeNew = True
            canAdd = False
    if (makeNew):
         fData.append([])
    if (canAdd):
         fData[-1].append(s)
print(fData)
>>>>>>> Stashed changes
