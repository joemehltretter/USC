from bs4 import BeautifulSoup as bs
import requests
import queue
import urllib.request
#import string

def main():
  #Declare seeds
  seedUrls = ['https://threatpost.com/blog', 'https://hackread.com/',\
  'http://ehackingnews.com/', 'https://us-cert.gov/ncas/current-activity']
  articles = {}
  relevantArticles = {}
  keywords = []
  keywordPath = "/home/mehltret/Desktop/USC/CSCI 572/Crawler/words.txt"
  file = open(keywordPath, 'r')
  for word in file:
    keywords.append(word.lower().strip())

  linkQueue = queue.Queue()
  session = requests.session()
  for seed in seedUrls:
    url = ''.join(seed)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    urlPage = urllib.request.urlopen(req)
    charset = urlPage.info().get_content_charset()
    pageContent = urlPage.read().decode(charset)
    soupObject = bs(pageContent, "html.parser")
    allLinks = soupObject.find_all('a')
    for pageLinks in allLinks:
      if pageLinks:
        if pageLinks.has_attr('href'):
          articleTitle = pageLinks.text.strip().lower()
          articleUrl = pageLinks['href']
          articles[articleTitle] = articleUrl

    for key in articles:
      relevant = False
      for word in keywords:
        if word in key and len(key.split()) > 3:
          if key not in relevantArticles:
            relevantArticles[key] = articles[key]
          break
        else:
          continue
    for key in relevantArticles:
      print("{title} + {url}".format(title = key, url = relevantArticles[key]))

if __name__ == "__main__":
    main()
