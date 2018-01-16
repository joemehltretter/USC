from bs4 import BeautifulSoup as bs
import requests
import queue
import urllib.request

def main():
  #Declare seeds
  seedUrls = ['https://threatpost.com/blog', 'https://hackread.com/',\
  'http://ehackingnews.com/', 'https://us-cert.gov/ncas/current-activity']
  linkQueue = queue.Queue()
  session = requests.session()
  for seed in seedUrls:
    url = ''.join(seed)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.encoding = "utf-8"
    urlPage = urllib.request.urlopen(req).read()
    soupObject = bs(urlPage, "lxml")
    pageLinks = soupObject.find_all('a')
    print("Printing for {url}".format(url = url))
    if pageLinks:
      for link in pageLinks:
        if link.has_attr('href'):
          #print(link['href'].encode("utf-8"))
          #Analyze link if relevant store in queue
          continue
    
if __name__ == "__main__":
    main()
