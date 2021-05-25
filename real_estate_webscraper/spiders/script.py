#Imports CrawlerProcess
from scrapy.crawler import CrawlerProcess

#Imports spider from house_info.py
from house_info import HouseInfoSpider

country = ''
print("--------------------------------------------------------------------------"+
    "\n(⌐■_■) Welcome to the Real Estate Webscraper (⌐■_■)"+
    "\nGive us a location and we'll scrape info about the houses in the area"
    '\nIs your location in Canada or America?'+
    "\nc - Canada"+
    "\na - America")
while (country != 'c' and country!='a'):
    country = input()
    if (country != 'c' and country!='a'):
        print("I'm sorry, that's not a valid response\n"
        '\nIs your location in Canada or America?'+
        "\nc - Canada"+
        "\na - America")
print('Enter the city')
city = input()

file1 = open('info.txt', 'w')
file1.writelines(country+'\n'+city)
file1.close()

process = CrawlerProcess({
    'FEED_URI': 'file://C:/Users/thana/projects/real_estate_webscraper/real-estate-webscraper/house_info.csv', 
})

process.crawl(HouseInfoSpider)
process.start()
