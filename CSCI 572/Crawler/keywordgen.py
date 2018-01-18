from bs4 import BeautifulSoup as bs
import requests
import queue
import urllib.request

url = 'https://motherboard.vice.com/en_us/article/mg79v4/hacking-glossary'
filePath = "~/Desktop/USC/CSCI 572/Crawler/words.txt"

req = urllib.request.Request(url)
html = urllib.request.urlopen(req).read()
soupObject = bs(html, "lxml")
file = open(filePath, 'w')
for word in soupObject.find_all('b'):
	newWord = word.text
	file.write(newWord)
	file.write('\n')

	
