import requests
import re
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

# generating user agent so we don't get blocked from requesting the site
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}

# returns array of urls to request
# takes in amount of pages to scrape
def getUrls(pagesToScrape):
  urls = [];
  currPage = 1;
  while(currPage <= pagesToScrape):
    baseUrl = 'https://www.zillow.com/homes/for_sale/Santa-Cruz-CA/fsba,fsbo_lt/13715_rid/globalrelevanceex_sort/37.187672,-121.807824,36.902136,-122.342034_rect/10_zm/' + str(currPage) + '_p/0_mmm/'
    urls.append(baseUrl)
    currPage = currPage + 1
  return urls;

# removes text from strings
def sanitize(str):    
  return float(re.sub('[,$K]', '', str))

# scrapes specified number of pages
def scrape(numPages):
    urls = getUrls(numPages);
    results = [];

    for url in urls:
      print("GETTING URL", url);
      site = requests.get(url, timeout=5, headers=headers)
      
      if site.status_code is 200:
        content = BeautifulSoup(site.content, 'html.parser')
        prices = content.find_all(class_='zsg-photo-card-price')
        info = content.find_all(class_='zsg-photo-card-info');
        homePrices = [];
        homeStats = [];

        # parses out price for each home
        for price in prices :
          homePrice = sanitize(price.get_text())
          homePrices.append(homePrice)

        for idx, propertyInfo in enumerate(info):
          # parses out beds, baths, sqft for each house
          try:
            parsedInfo = propertyInfo.get_text().split(' · ')
            beds = 1.0 if parsedInfo[0] in ('Studio', '1 bd') else sanitize(parsedInfo[0].split(' bds')[0]);
            baths = sanitize(parsedInfo[1].split(' ba')[0])
            sqft = sanitize(parsedInfo[2].split(' sqft')[0])
            homeStats.append([beds, baths, sqft])
          except:
            homeStats.append([0,0,0]);
            print("error parsing");
        
        # appending array of stats for all homes on a page
        results.append([[price] + homeStats[i] for i, price in enumerate(homePrices)])
      else:
        print("Error:")
        print(site.status_code)

    # return flatten(results);
    count = 0;
    for page in results:
      for home in page:
        count = count +1;
        print("----")
        print("Price: $", home[0]);
        print("Beds: ", home[1]);
        print("Baths: ", home[2]);
        print("Sqft: ", home[3]);
    print("Scraped results for " + str(count) + " properties")

scrape(10)