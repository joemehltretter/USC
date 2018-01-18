from bs4 import BeautifulSoup as bs
import requests
from collections import deque
import urllib.request

## Global Variables ##
linkQueue = deque()
path = '/home/mehltret/Desktop/USC/CSCI 572/Crawler/files/'
##

def crawl(url):
  url = ''.join(url)
  req = urllib.request.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0')
  urlPage = urllib.request.urlopen(req)
  pageContent = urlPage.read()
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

def relevance_check(articles, keywords):
  rel = {}
  for key in articles:
    for word in keywords:
      if word in key and len(key.split()) > 3:
        url = articles[key]
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
  title = title.replace(' ', '_')
  
  req = urllib.request.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0')
  urlPage = urllib.request.urlopen(req)
  pageContent = urlPage.read()
  soupObject = bs(pageContent, "html.parser")
  bodyText = soupObject.find_all('p')

  body = []
  for p in bodyText:
    body.append(p.text)
  
  body = ''.join(body)
  fullPath = path + title
  with open(fullPath, 'w') as newFile:
    newFile.write(body)

def main():
  #Declare seeds
  seedUrls = ['https://threatpost.com', 'https://hackread.com',\
  'http://ehackingnews.com', 'https://us-cert.gov/ncas/current-activity']
  articles = {}
  relevantArticles = {}
  keywords = []
  keywordPath = "/home/mehltret/Desktop/USC/CSCI 572/Crawler/words.txt"
  file = open(keywordPath, 'r')
  for word in file:
    keywords.append(word.lower().strip())

  for seed in seedUrls:
    foundLinks = crawl(seed)
    articles = extract(foundLinks)
    relevantArticles.update(relevance_check(articles, keywords))

  while len(linkQueue) > 0:
    print("Queue current length is: {size} \n".format(size = len(linkQueue)))
    url = linkQueue.popleft()
    foundLinks = crawl(url)
    articles = extract(foundLinks)
    relevantArticles.update(relevance_check(articles, keywords))
    print("Current length of relevant article dic : {size}".format(size = len(relevantArticles)))
#    if len(linkQueue) > 1000:
#      break

  for key in relevantArticles:
    print("{title} + {url}".format(title = key, url = relevantArticles[key]))

if __name__ == "__main__":
  main()
