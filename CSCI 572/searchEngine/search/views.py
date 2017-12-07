# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from search.models import Item
from haystack.query import SearchQuerySet
from bs4 import BeautifulSoup as bs
from nltk import tokenize
from enchant import DictWithPWL
from enchant.checker import SpellChecker
import pysolr
import enchant
import codecs
import sys

#newQuery = ""
custWordList = enchant.request_pwl_dict("/home/mehltret/Desktop/autoWords2.txt")
#custWordList = DictWithPWL("en_US", "/home/mehltret/Desktop/autoWords.txt")
def home_page(request):
  newQuery = ""
  #custWordList = enchant.request_pwl_dict("/home/mehltret/Desktop/autoWords.txt")
  #If a new query is being made, set method to POST.
  if request.method == 'GET':
    #Save item that was input in browser to variable
    query = request.GET.get('item_text')
    suggestWord = ""    
    if not custWordList.check(str(query)):
      suggestWord = custWordList.suggest(str(query))
      if(len(suggestWord) > 0):
        newQuery = suggestWord[0]
 
    action = request.GET.get('action')
    suggestTerms = []
    #return HttpResponse(action)
    if action == 'Solr':

      solr = pysolr.Solr('http://localhost:8983/solr/assign4/')

      if newQuery:
        results = solr.search(newQuery)
        totalRes = len(results)

      elif not suggestWord:
        results = solr.search(query)
        totalRes = len(results)

      for result in results:
        result['title'] = ' '.join(result['title'])
        if 'og_url' in result.keys():
          result['og_url'] = ' '.join(result['og_url'])
        result['description'] = ' '.join(result['description'])
        #Snippet Generation
        filePath = "".join(result['resourcename'])
        html_file = codecs.open(filePath, 'r', 'utf-8')
        html_content = html_file.read()
        soup = bs(html_content, 'lxml')

        #clean file
        for script in soup(['script', 'style', 'span', 'class']):
          script.extract()

        for pObject in soup.findAll('p'):
          if 'class' in pObject.attrs:
            pObject.decompose()

        #Get body
        bodyText = "".join([pObject.text for pObject in soup.findAll('p')])
        testlist = []
        testlist.append(bodyText.lower())
        result['snippet'] = []
        #develop snippet
        for text in testlist:
          #sentences = text.split('. ')
          sentences = tokenize.sent_tokenize(text)
          for sentence in sentences:
            if newQuery:
              if newQuery in sentence:
                if(len(result['snippet']) < 3):
                  result['snippet'].append(sentence)
              else:
                for word in newQuery.split(' '):
                  if word in sentence:
                    if sentence not in result['snippet']:
                      if(len(result['snippet']) < 3):
                        result['snippet'].append(sentence)


            elif not newQuery:
              if query in sentence:
                if(len(result['snippet']) < 3):
                  result['snippet'].append(sentence)
            #if query not in sentence:
              else:
                for word in query.split(' '):
                  if word in sentence:
                    if sentence not in result['snippet']:
                      if(len(result['snippet']) < 3):
                        result['snippet'].append(sentence)

          result['snippet'] = ' '.join(result['snippet'])

      return render(request, 'search/solr.html', {'query':query, 'newQuery':newQuery, 'suggestWord': suggestWord, 'results':results, 'total':totalRes})

    elif action == 'Netx':
      solr = pysolr.Solr('http://localhost:8983/solr/assign4/')
      results = solr.search(query, **{
        'sort': 'pageRankFile desc',
       })
      totalRes = len(results)
      for result in results:
        result['title'] = ' '.join(result['title'])
        if 'og_url' in result.keys():
          result['og_url'] = ' '.join(result['og_url'])
        result['description'] = ' '.join(result['description'])

      return render(request, 'search/netx.html', {'query':query, 'results':results, 'total':totalRes})
    
    else:
      return render(request, 'search/home.html')
  
def solr_results(request):
  solr = pysolr.Solr('http://localhost:8983/solr/assign4')
  results = solr.search('elon musk')
  totalRes = len(results)
  return render(request, 'search/solr.html', {'results': results, 'totalRes':totalRes})

def netX_results(request):
  return render(request, 'search/netx.html')

def del_query_history(request):
  queries = Item.objects.all().delete()
  return redirect('/', {'queries':queries})
