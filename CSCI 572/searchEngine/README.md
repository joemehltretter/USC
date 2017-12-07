# searchEngine

We were tasked with creating a search engine that index documents from a solr core. The search engine must take provide autocomplete
functionality when search queries are input and spell checking. When a query is submitted the search engine must produce a title, url,
and snippet for each result.

## Getting Started

If used for custom purposes, the following must be changed:

- Change URL in [searchEngine/searchEngine/settings.py](https://github.com/joemehltretter/USC/blob/master/CSCI%20572/searchEngine/searchEngine/settings.py) to your solr core
```
HAYSTACK_CONNECTIONS = {
  'default': {
    'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
    'URL': 'http://127.0.0.1:8983/solr/core_name' 
  }
}
```

## Running

When in root searchEngine directory run:

```
python manage.py makemigrations
python manage.py build_solr_schema
python manage.py runserver
```

