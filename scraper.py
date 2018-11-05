import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}

# zsg-photo-card-price
# zsg-photo-card-info

site = requests.get('https://www.zillow.com/santa-cruz-ca/', timeout=5, headers=headers)

if site.status_code is 200:
  content = BeautifulSoup(site.content, 'html.parser')
  
  prices = content.find_all(class_='zsg-photo-card-price')
  #comes back in form
  # <span class="zsg-photo-card-price">$949,000</span>
  
  info = content.find_all(class_='zsg-photo-card-info');
  # comes back in form 
  # <span class="zsg-photo-card-info">5 bds <span class="interpunct">·</span> 4 ba <span class="interpunct">·</span> 3,012 sqft</span>

  
  for price in prices :
    print(price);
  for i in info:
    print(i);