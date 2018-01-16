from bs4 import BeautifulSoup as bs
import requests
import queue
import urllib.request
import string

def main():
  #Declare seeds
  seedUrls = ['https://threatpost.com/blog', 'https://hackread.com/',\
  'http://ehackingnews.com/', 'https://us-cert.gov/ncas/current-activity']
  relevantArticles = {}
  keywords = []
  keywordPath = "/Users/jmehl/Documents/Github/USC/CSCI 572/Crawler/words.txt"
  file = open(keywordPath, 'r')
  for word in file:
    keywords.append(word)

  linkQueue = queue.Queue()
  session = requests.session()
  for seed in seedUrls:
    url = ''.join(seed)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    urlPage = urllib.request.urlopen(req)
    charset = urlPage.info().get_content_charset()
    print(charset)
    pageContent = urlPage.read().decode(charset)
    soupObject = bs(pageContent, "html.parser")
    #pageLinks = soupObject.find_all('a')
    for pageLinks in soupObject.find_all('a'):
      #print(type(pageLinks))
      if pageLinks:
        #for link in pageLinks:
        if pageLinks.has_attr('href'):
          articleTitle = pageLinks.text.strip()
          print(articleTitle.encode('utf-8', 'ignore').decode('utf-8'))
          articleUrl = pageLinks['href']
          relevant = False
          for word in keywords:
            if word in articleTitle:
              relevant = True
              print("True")
              #relevantArticles[articleTitle] = articleUrl
              print(word)
              break
            
            else:
              continue
            #print(articleTitle.encode("utf-8"))
    for url in relevantArticles:
      print("{url} : {title}".format(url = url, title = relevantArticles['url']))
if __name__ == "__main__":
    main()
