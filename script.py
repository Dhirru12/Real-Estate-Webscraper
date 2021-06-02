# -*- coding: utf-8 -*-
#Imports CrawlerProcess
from scrapy.crawler import CrawlerProcess

#Imports spider from house_info.py
from real_estate_webscraper.spiders.house_info import HouseInfoSpider


#Initializes country variable
country = ''

#Prompts user to enter whether their location is in Canada or America
print("--------------------------------------------------------------------------"+
    "\n(⌐■_■) Welcome to the Real Estate Webscraper (⌐■_■)"+
    "\nGive us a location and we'll scrape info about the houses in the area"
    '\nIs your location in Canada or America?'+
    "\nc - Canada"+
    "\na - America")

#Loops every time user does not give either an 'c' or 'a' input
while (country != 'c' and country!='a'):
    #Assigns input to country variable
    #country = input()
    country = "a"
    #If given incorrect input, user is told their input is incorrect and to give valid input
    if (country != 'c' and country!='a'):
        print("--------------------------------------------------------------------------"+
        "\nI'm sorry, that's not a valid response"+
        '\nIs your location in Canada or America?'+
        "\nc - Canada"+
        "\na - America")

#All inputted info is written into text file for spider to read and use
file1 = open('info.txt', 'w')
file1.writelines(country+'\n'+city)
file1.close()


#Spider will create a csv  and log file in the file path given to FEED_URI and LOG_FILE
process = CrawlerProcess()

#Begins spider crawl
process.crawl(HouseInfoSpider)
process.start()
