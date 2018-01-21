from bs4 import BeautifulSoup as bs
import urllib.request
import datetime
url = 'https://threatpost.com/oneplus-confirms-credit-card-breach-impacted-up-to-40000-customers/129569/'

req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0')
urlPage = urllib.request.urlopen(req)
pageContent = urlPage.read()
soupObject = bs(pageContent, 'html.parser')

time = soupObject.find('time')
print(time['datetime'])
newTime = time['datetime']
print(datetime.date.today())
print(newTime < str(datetime.date.today()))
