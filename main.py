# Code by:- Rohit Kavitake

# Imports
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

product_urls = []
datalist = [["ProductTitle","Manufacturer-Name(manufacturer-Website)","stockStatus","Product-Link"]]
# Getting sites url from txt file
with open("brownells.txt", 'r') as urlfile:
    products = urlfile.readlines()

for url in products:
    url = url.rstrip("\n")
    product_urls.append(url)
flag = 0
# print(product_urls)
# print(len(product_urls))
print("Starting the Script...")
for product in product_urls:
    productPage = requests.get(product)
    Soup = BeautifulSoup(productPage.content, 'html.parser')
    titleContainer = Soup.find('h1', class_="mbm")
    containerSpan = titleContainer.findAll('span')
    Website = containerSpan[0].find('a', href=True)
    project_href = Website['href']
    productTitle = (containerSpan[1].get_text()).strip()
    ManufacturerName = (containerSpan[0].get_text()).strip("\n")
    manufacturerWebsite  =  "https://www.brownells.com" + project_href
    # print(containerSpan[0].get_text())
    availibility = Soup.find_all("span", class_="mfr")
    for i in availibility:
        if(((i.text).strip()) == "In Stock") :
            flag = 1
    if(flag == 1):
        stockStatus = ("In Stock")
    else :
        stockStatus = ("Out of Stock")

    # print(productTitle, "\n", ManufacturerName, "\n", manufacturerWebsite, "\n", stockStatus, "\n", product, "\n \n \n"  )
    data = [productTitle,ManufacturerName+"("+manufacturerWebsite+")",stockStatus,product]
    datalist.append(data)
print("Data Scrape Succcess ... \nSaving the Data..")
if(os.path.exists("output.csv")):
    datalist.pop(0)
    df = pd.DataFrame(datalist)
    df.to_csv("output.csv",mode="a",header=False, index= False )
else:
    df = pd.DataFrame(datalist)
    df.to_csv("output.csv",mode="a",header=False, index= False ) 