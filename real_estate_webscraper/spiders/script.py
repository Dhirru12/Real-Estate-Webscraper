#Imports CrawlerProcess
from scrapy.crawler import CrawlerProcess

#Imports spider from house_info.py
from house_info import HouseInfoSpider

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
    country = input()
    #If given incorrect input, user is told their input is incorrect and to give valid input
    if (country != 'c' and country!='a'):
        print("--------------------------------------------------------------------------"+
        "I'm sorry, that's not a valid response"+
        '\nIs your location in Canada or America?'+
        "\nc - Canada"+
        "\na - America")

#User is asked for the city (functions as the location)
print('Enter the city')
city = input()

#All inputted info is written into text file for spider to read and use
file1 = open('info.txt', 'w')
file1.writelines(country+'\n'+city)
file1.close()

#Spider will create a csv file in the file path given to FEED URI
process = CrawlerProcess({
    'FEED_URI': 'file://CSV_PATH', 
})

#Begins spider crawl
process.crawl(HouseInfoSpider)
process.start()
