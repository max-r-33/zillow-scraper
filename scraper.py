import requests
import re
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

# generating user agent so we don't get blocked from requesting the site
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
site = requests.get('https://www.zillow.com/santa-cruz-ca/', timeout=5, headers=headers)

def sanitize(str):    
  return float(re.sub('[,$]', '', str))

if site.status_code is 200:
  content = BeautifulSoup(site.content, 'html.parser')
  prices = content.find_all(class_='zsg-photo-card-price')
  info = content.find_all(class_='zsg-photo-card-info');

  homePrices = [];
  homeStats = [];

  for price in prices :
    homePrice = sanitize(price.get_text())
    homePrices.append(homePrice)

  for i in info:
    i = i.get_text().split(' · ')
    beds = 1.0 if i[0] in ('Studio', '1 bd') else sanitize(i[0].split(' bds')[0])
    baths = sanitize(i[1].split(' ba')[0])
    sqft = sanitize(i[2].split(' sqft')[0])
    homeStats.append([beds, baths, sqft])
  
  result = [[x] + homeStats[i] for i,x in enumerate(homePrices)]
  for r in result:
    print(r)
else:
  print(site.status_code)

