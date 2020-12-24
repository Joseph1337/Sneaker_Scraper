import json
import requests
from bs4 import BeautifulSoup


#api call to retrieve sneaker details
url = 'https://2fwotdvm2o-3.algolianet.com/1/indexes/*/queries'

#data sent with POST request
form_data = {
    "requests": [{
    "indexName":"product_variants_v2",
    "params":"",
    "highlightPreTag" : "<ais-highlight-0000000000>",
    "highlightPostTag": "</ais-highlight-0000000000>",
    "distinct": "true",
    "facetFilters": '[["product_category:shoes"]]',
    "maxValuesPerFacet": "30",
    "page": "0",
    "facets": '["instant_ship_lowest_price_cents","single_gender","presentation_size","shoe_condition","product_category","brand_name","color","silhouette","designer","upper_material","midsole","category","release_date_name"]',
    "tagFilters":""
    }]
}

query_params = {
    'x-algolia-agent': 'Algolia for JavaScript (3.35.1); Browser (lite); JS Helper (3.2.2); react (16.13.1); react-instantsearch (6.8.2)',
    'x-algolia-application-id': '2FWOTDVM2O',
    'x-algolia-api-key': 'ac96de6fef0e02bb95d433d8d5c7038a'
}



sneakers_page = requests.post(url, data=json.dumps(form_data), params=query_params).json()
# print(sneakers_page)

for sneaker in sneakers_page['results'][0]['hits']:
    print(str(sneaker['name']) + ' || $' +  str((sneaker['lowest_price_cents'] / 100)))





# # url = "https://stockx.com/sneakers/most-popular"
# # page = requests.get(url)
# # with open("stockx.html", "w", encoding='utf-8') as f:
# #     f.write(page.text)
# # # soup = BS(open("stockx.html", "w", encoding='utf-8').read(),"html.parser")
# # # /print(soup.prettify())
# # # print(soup.text)

# url = 'https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia for vanilla JavaScript 3.25.1&x-algolia-application-id=2FWOTDVM2O&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a'
# data = {"params":"distinct=true&facetFilters=()&facets=%5B%22size%22%5D&hitsPerPage=20&numericFilters=%5B%5D&page=0&query="}
# r = requests.post(url, data=json.dumps(data))
# print(r.json()['hits'][0])