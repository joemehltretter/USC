from bs4 import BeautifulSoup as bs
from lxml import etree
from io import StringIO
import codecs
from nltk import tokenize

keyWord = "HighTower confederation"

path = '/home/mehltret/Desktop/WSJSub/'
file0 = 'test.html'
testList = []
fileList = [file0]

for fileName in fileList:
  filePath = path + fileName
  html_file = codecs.open(filePath, 'r', 'utf-8')
  html_content = html_file.read()

  soup = bs(html_content, 'lxml')

  for script in soup(['script', 'style', 'span', 'class']):
    script.extract()

  for p in soup.findAll('p'):
    if 'class' in p.attrs:
      p.decompose()

  pText = "".join([p.text for p in soup.findAll('p')])
  testList.append(pText)

for listText in testList:
  snippet = []
  sentences = tokenize.sent_tokenize(listText)  
  for sentence in sentences:
    print(sentence)
    for word in keyWord.split(' '):
      if word in sentence:
        if sentence not in snippet:
          if(len(snippet) < 256):
            snippet.append(sentence) 

snippet = " ".join(snippet)
snippet = snippet.replace("\n", ' ')
print(snippet)
