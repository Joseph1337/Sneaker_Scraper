import json
import requests
import pprint
from time import sleep
import random
# from bs4 import BeautifulSoup


#extracts all user-agents from the provided 'ua_file.txt' into a lst then randomly selects a user-agent
def getUserAgent():
    randomUserAgent = ""
    listOfUserAgents = []
    userAgentFile = 'ua_file.txt'
    with open('ua_file.txt') as file:
        listOfUserAgents = [line.rstrip("\n") for line in file]
    return random.choice(listOfUserAgents)

#function to get all sneakers from 'Shop All' page
def getAllSneakers():
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
        # 'x-algolia-agent': 'Algolia for JavaScript (3.35.1); Browser (lite); JS Helper (3.2.2); react (16.13.1); react-instantsearch (6.8.2)',
        'x-algolia-application-id': '2FWOTDVM2O',
        'x-algolia-api-key': 'ac96de6fef0e02bb95d433d8d5c7038a'
    }
    return requests.post(url, data=json.dumps(form_data), params=query_params).json()['results'][0]['hits']



class Sneaker:
    def __init__(self, name, query_id, retail_price):
        self.name = name
        self.query_id = query_id
        self.retail_price = retail_price
        self.sizeAndPrice = {}

    # #returns product info for each sneaker
    # def getSneakerInfo(self):
    #     info = {}

    #returns all sizes and their corresponding price for each sneaker
    def getSneakerSizesAndPrices(self):
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
            "productTemplateId": self.query_id
        }

        # while True:
        for i in range(0, 20):
            try:
                headers.update({"user-agent": getUserAgent()})
                response = requests.get(url, headers=headers, params=query_params)
                print(response.status_code)
                if(response.status_code >= 200 and response.status_code < 400):
                    page = response.json()
                    for i in range(0, len(page)):
                        #check ONLY for new shoes with boxes in good condition
                        if(page[i]['boxCondition'] == "good_condition" and page[i]['shoeCondition'] == "new_no_defects"):
                            self.sizeAndPrice.update({page[i]['size']: page[i]['lowestPriceCents']['amount']/100})
                        # print(str(page[i]['size']) + "||" + str(page[i]['lowestPriceCents']['amount'] / 100))
                else:
                    # print("Server did not return an 'OK' response. Content was: {!r}".format(response.content))
                    raise PermissionError

            except (PermissionError):#request got blocked by captcha
                print("Unable to retrieve sneaker info...Retrying...")
                # sleep(random.randrange(1,8)) #wait a while before retrying to avoid getting detected
                continue

            else:
                break

        else: # if not sizeAndPrice:
            self.sizeAndPrice.update({"Size_Timeout": "Price_Timeout"})

        return self.sizeAndPrice


if __name__ == "__main__":
    sneakersList = []
    sneakers_page = getAllSneakers()

    for sneaker in sneakers_page:
        sneakersList.append(Sneaker(sneaker['name'], sneaker['slug'], sneaker['retail_price_cents']/100))

    for sneaker in sneakersList:
        print("Name: " + sneaker.name)
        print("Retail Price: " + str(sneaker.retail_price))
        # print(sneaker.getSneakerSizesAndPrices())
        print(sneaker.getSneakerSizesAndPrices())
        sleepTime = random.randrange(1,4)

        print("Delaying for " + str(sleepTime) + "s..." )
        sleep(sleepTime)

    # pprint.pprint(sneakersList[0].getSneakerSizesAndPrices())
    # print(getUserAgent())

    # sneakers = getAllSneakers()
    # for sneaker in sneakers:
    #     print("Name: " + sneaker.name)
    #     print("Retail Price: " + str(sneaker.retail_price))
    #     print("Buy New: " + sneaker.sizeAndPrice)


