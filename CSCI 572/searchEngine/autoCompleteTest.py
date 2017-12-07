import pysolr
import nltk
from bs4 import BeautifulSoup as bs
from nltk import word_tokenize
from nltk.util import ngrams

#Search and store all indexed documents in result variable.
solr = pysolr.Solr('http://localhost:8983/solr/assign4/')
#Results variable is a dictionary
results = solr.search('*:*', **{'rows': 10000000})

count = 0
allKeywords = []
#Iterate through all results and store words from keyword, title, 
# and description keys into keywords variable and create n-grams.
for result in results:
  if 'keywords' in result.keys():
    print("in keywords")
    keywords = result['keywords']

    keywords = ",".join(keywords)
    keywordsAsString = str(keywords)
    keywords = ' '.join(keywordsAsString.split(','))
    keywords = keywords.lower()
    #Iterate through all keywords and remove characters.
    for keyword in keywords.split(' '):
      keywords = keywords.replace(",", '')
      keywords = keywords.replace(".", '')
      keywords = keywords.replace("'", '')
      keywords = keywords.replace(']', '')
      keywords = keywords.replace('[', '')
      keywords = keywords.lower()

    #Create token(unigram), bigram and tri-gram from keyword variable.
    tokens = nltk.word_tokenize(keywords)
    bigrams = ngrams(tokens, 2)
    trigrams = ngrams(tokens, 3)
    #Store n-grams into allkeywords variable.
    allKeywords.extend([' '.join(gram) for gram in bigrams])
    allKeywords.extend([' '.join(gram) for gram in bigrams])
    allKeywords.extend([' '.join(gram) for gram in trigrams])
    allKeywords.extend([' '.join(token.split(' ')) for token in tokens])

  if 'title' in result.keys():
    print("In title")
    keywords = result['title']
    keywords = ' '.join(keywordsAsString.split(','))
    for keyword in keywords.split(' '):
      keywords = keywords.replace(",", '')
      keywords = keywords.replace(".", '')
      keywords = keywords.replace("'", '')
      keywords = keywords.replace(']', '')
      keywords = keywords.replace('[', '')
      keywords = keywords.lower()

    tokens = nltk.word_tokenize(keywords)
    bigrams = ngrams(tokens, 2)
    trigrams = ngrams(tokens, 3)
    allKeywords.extend([' '.join(gram) for gram in bigrams])
    allKeywords.extend([' '.join(token.split(' ')) for token in tokens])
    allKeywords.extend([' '.join(gram) for gram in bigrams])
    allKeywords.extend([' '.join(gram) for gram in trigrams])


  if 'description' in result.keys():
    print("description")
    keywords = result['description']
    keywordsAsString = str(keywords)
    keywords = ' '.join(keywordsAsString.split(','))
    for keyword in keywords.split(' '):
      keywords = keywords.replace(",", '')
      keywords = keywords.replace(".", '')
      keywords = keywords.replace("'", '')
      keywords = keywords.replace(']', '')
      keywords = keywords.replace('[', '')
      keywords = keywords.lower()

    tokens = nltk.word_tokenize(keywords)
    bigrams = ngrams(tokens, 2)
    trigrams = ngrams(tokens, 3)
    allKeywords.extend([' '.join(gram) for gram in bigrams])
    allKeywords.extend([' '.join(token.split(' ')) for token in tokens])
    allKeywords.extend([' '.join(gram) for gram in bigrams])
    allKeywords.extend([' '.join(gram) for gram in trigrams])

#Open file and write keywords to the file.
with open("/home/mehltret/Desktop/autoWords2.txt", mode = "wt") as testFile: 
  for item in allKeywords:
    print(item)
    testFile.write("%s\n" % item)

testFile.close()
