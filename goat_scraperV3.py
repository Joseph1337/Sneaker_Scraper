import json
import requests
import pprint
from time import sleep
import random
from bs4 import BeautifulSoup as bs
import pandas as pd
import proxyFinder
import csv


#extracts all user-agents from the provided 'ua_file.txt' into a list then randomly selects a user-agent
def getUserAgent():
    randomUserAgent = ""
    listOfUserAgents = []
    userAgentFile = 'ua_file.txt'
    with open('ua_file.txt') as file:
        listOfUserAgents = [line.rstrip("\n") for line in file]
    return random.choice(listOfUserAgents)


class Sneaker:
    def __init__(self, name, query_id, retail_price, displayed_size, price, image_url):
        self.name = name
        self.query_id = query_id
        self.retail_price = retail_price
        self.displayed_size = displayed_size
        self.price = price
        self.image_url = image_url
        # self.sizeAndPrice = sizeAndPrice


#function to get all sneakers from 'Shop All' page
def getAllSneakers():
    sneakersList = []
    #api call to retrieve sneaker details
    url = 'https://2fwotdvm2o-3.algolianet.com/1/indexes/*/queries'
    #size you want to look for:
    shoe_size = 8
    #data sent with POST request
    for page in range(0,5):
        form_data = {
            "requests": [{
            "indexName":"product_variants_v2",
            "params":"",
            "highlightPreTag" : "<ais-highlight-0000000000>",
            "highlightPostTag": "</ais-highlight-0000000000>",
            "distinct": "true",
            "facetFilters": [["presentation_size:" + str(shoe_size)],["product_category:shoes"]],
            "maxValuesPerFacet": 30,
            "page": page,
            "facets": ["instant_ship_lowest_price_cents","single_gender","presentation_size","shoe_condition","product_category","brand_name","color","silhouette","designer","upper_material","midsole","category","release_date_name"],
            "tagFilters":""
            }]
        }
        query_params = {
            'x-algolia-agent': 'Algolia for JavaScript (3.35.1); Browser (lite); JS Helper (3.2.2); react (16.13.1); react-instantsearch (6.8.2)',
            'x-algolia-application-id': '2FWOTDVM2O',
            'x-algolia-api-key': 'ac96de6fef0e02bb95d433d8d5c7038a'
        }
        response = requests.post(url, data=json.dumps(form_data), params=query_params).json()['results'][0]['hits']
        for sneaker in response:
            sneakersList.append(Sneaker(sneaker['name'], sneaker['slug'], sneaker['retail_price_cents']/100, sneaker['size'], sneaker['lowest_price_cents']/100, sneaker['original_picture_url']))  # setSneakerSizesAndPrices(sneaker['slug'])))
            # sleep(random.randrange(1,3))

    return sneakersList


def setSneakerSizesAndPrices(query_id):
        sizeAndPrice = {}
        url = 'https://www.goat.com/web-api/v1/product_variants'
        user_agent = getUserAgent()
        headers = {
            "user-agent": user_agent,
            "accept" : "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language" : "en-US,en;q=0.9",
            "referer": 'https://www.google.com/'
        }

        query_params = {
            "productTemplateId": query_id
        }
        # proxy = proxyFinder.get_random_proxy()
        # proxies = {
        #     "http": "http://" + proxy,
        #     "https": "https://" + proxy
        # }

        # while True:
        for i in range(0, 10):
            try:
                headers.update({"user-agent": getUserAgent()})
                # proxies.update({"http": "http://" + proxyFinder.get_random_proxy(), "https": "https://" + proxyFinder.get_random_proxy()})
                # print("getting page with ip: " + proxies['https'])
                response = requests.get(url, headers=headers, params=query_params, timeout=10)
                print(response.status_code)

                if(response.status_code >= 200 and response.status_code < 400):
                    page = response.json()
                    for i in range(0, len(page)):
                        #check ONLY for new shoes with boxes in good condition
                        if(page[i]['boxCondition'] == "good_condition" and page[i]['shoeCondition'] == "new_no_defects"):
                            sizeAndPrice.update({page[i]['size']: page[i]['lowestPriceCents']['amount']/100})
                elif (response.json()['success'] == False): #catches if query_id invalid
                    sizeAndPrice.update({"message": "Invaid product id."})
                    break
                else:
                    raise PermissionError

            except (PermissionError):#request got blocked by captcha
                print("Unable to retrieve sneaker info...Retrying...")
                # sleep(random.randrange(1,3)) #wait a while before retrying to avoid getting detected
                continue

            except requests.exceptions.Timeout as err:
                print("Request timed out...Retrying...")
                continue

            else:
                break

        else: # if not sizeAndPrice:
            sizeAndPrice.update({"Size_Timeout": "Price_Timeout"})

        return sizeAndPrice


if __name__ == "__main__":
    sneakers = getAllSneakers()
    sneakerData = {}
    nameList = []
    retailPriceList = []
    displayed_size = []
    price = []
    image_urls = []

    for sneaker in sneakers:
        nameList.append(sneaker.name)
        retailPriceList.append(sneaker.retail_price)
        displayed_size.append(sneaker.displayed_size)
        price.append(sneaker.price)
        image_urls.append(sneaker.image_url)
        # sizesAndPrices = sneaker.sizeAndPrice
        sneakerData.update({"Name": nameList, "Retail Price": retailPriceList, "Display Size": displayed_size, "Price":price})

    dataFrame = pd.DataFrame(sneakerData)
    dataFrame.to_csv("sneakers.csv", index=False, header=True)
    print(dataFrame)

    # for sneaker in sneakers:
    #     print("Name: " + sneaker.name)
    #     print("Retail Price: " + str(sneaker.retail_price))
    #     print(sneaker.sizeAndPrice)

