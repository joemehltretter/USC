from bs4 import BeautifulSoup as bs
import requests
from collections import deque
import urllib.request
import string
import datetime

## Global Variables ##
linkQueue = deque()
htmlPath = '/home/mehltret/Desktop/USC/CSCI 572/Crawler/htmlFiles/'
path = '/home/mehltret/Desktop/USC/CSCI 572/Crawler/files/'
##

def crawl(url):
  url = ''.join(url)
  req = urllib.request.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0')
  try:
    urlPage = urllib.request.urlopen(req)
    pageContent = urlPage.read()

  except urllib.error.URLERROR as e:
    pass

  soupObject = bs(pageContent, "html.parser")
  allLinks = soupObject.find_all('a')
  return(allLinks)

def extract(extractUrls):
  articles = {}
  for pageLinks in extractUrls:
    if pageLinks:
      if pageLinks.has_attr('href'):
        articleTitle = pageLinks.text.strip().lower()
        articleUrl = pageLinks['href']
        if 'http' in articleUrl:
          articles[articleTitle] = articleUrl
  return(articles)

def relevance_check(articles, keywords, urls):
  rel = {}
  for key in articles:
    for word in keywords:
      if word in key and len(key.split()) > 3:
        url = articles[key]
        if url not in urls:
          rel[key] = url
          get_body_and_save(key, url)
          linkQueue.append(articles[key])
          print("# of relevant articles found: {num}".format(num = len(linkQueue)))
        break

      else:
        continue

  return(rel)

def get_body_and_save(title, url):
  title = title.replace(',', '')
  title = title.replace('.', '')
  title = title.replace("'", "")
  title = title.replace('...', '')
  translator = str.maketrans('', '', string.punctuation)
  title = title.translate(translator)
  if len(title) > 50:
    title = title[:50]
  title = title.replace(' ', '_')
  txtTitle = title + ".txt"
  htmlTitle = title + ".html"
  print(title)
  
  req = urllib.request.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0')
  try:
    urlPage = urllib.request.urlopen(req)
    pageContent = urlPage.read()
    soupObject = bs(pageContent, "html.parser")
    bodyText = soupObject.find_all('p')
    body = []

    for p in bodyText:
      body.append(p.text)
 
    body = ''.join(body)
    fullPath = path + txtTitle
    fullHtmlPath = htmlPath + htmlTitle

    with open(fullPath, 'w') as newFile:
      newFile.write(body)
 
    with open(fullHtmlPath, 'w') as newFile:
      newFile.write(str(soupObject))

  except urllib.error.URLError as e:
    pass

def writeCache(articles, path2Cache):
  cacheFile = open(path2Cache, 'a')
  for key in articles:
    cacheFile.write(articles[key] + '\n')
  cacheFile.close()

def main():
  #Declare seeds
  seedUrls = ['https://threatpost.com', 'https://hackread.com',\
  'http://ehackingnews.com', 'https://us-cert.gov/ncas/current-activity']
  articles = {}
  relevantArticles = {}
  keywords = []
  urlSeen = []
  keywordPath = "/home/mehltret/Desktop/USC/CSCI 572/Crawler/words.txt"
  cachePath = "/home/mehltret/Desktop/USC/CSCI 572/Crawler/cache.txt"

  fileOpen = open(keywordPath, 'r')
  for word in fileOpen:
    keywords.append(word.lower().strip())
  fileOpen.close()

  cacheFile = open(cachePath, 'r')
  for url in cacheFile:
    urlSeen.append(url.lower().strip())
  cacheFile.close()

  for seed in seedUrls:
    foundLinks = crawl(seed)
    articles = extract(foundLinks)
    relevantArticles.update(relevance_check(articles, keywords, urlSeen))

  while len(linkQueue) > 0:
    print("Queue current length is: {size} \n".format(size = len(linkQueue)))
    url = linkQueue.popleft()
    foundLinks = crawl(url)
    articles = extract(foundLinks)
    relevantArticles.update(relevance_check(articles, keywords, urlSeen))
    print("Current length of relevant article dic : {size}".format(size = len(relevantArticles)))
    if len(linkQueue) > 5000:
      break

  writeCache(relevantArticles, cachePath)

if __name__ == "__main__":
  main()
