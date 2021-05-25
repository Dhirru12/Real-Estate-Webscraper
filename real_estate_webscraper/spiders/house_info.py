# -*- coding: utf-8 -*-
#Scrapy imports
import scrapy
from scrapy.selector import Selector

#Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#Time import
import time

#House info spider class
class HouseInfoSpider(scrapy.Spider):
    #Spider info
    name = 'house_info'
    allowed_domains = ['www.trulia.com', 'www.zillow.com']
    start_urls = ['https://www.trulia.com/CA/San_Francisco/']

    #Init function
    def __init__(self):
        #Reads and initializes variables based on what the script.py wrote in info.txt
        file1 = open('info.txt', 'r')
        lines = file1.readlines()
        country = lines[0].strip()
        location = lines[1].strip()

        #IMPORTANT:
        #Based on info provided, the spider will use the trulia boolean to look for different html elements
        if country=='c':
            trulia = False
        else:
            trulia = True
        #Loads chromedriver with personal chrome profile
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("user-data-dir=CHROME_PROFILE_PATH") #Path to your chrome profile
        driver = webdriver.Chrome(executable_path='CHROME_PATH', options=chrome_options)
        
        #If uncomfortable with loading personal chrome profile, feel free to comment/delete code above and use the code snippet below
        #webdriver.Chrome(executable_path = 'CHROME_PATH')
        
        #Create refererence elements so they can be given values within the 
        verification_element = ""
        next_page_element = ""

        #Code block used if the spider crawls Trulia
        if (trulia):
            #Assigns xpath for elements and loads trulia.com
            verification_element = "//select[@aria-label='Sort Results']"
            next_page_element = "//li[@data-testid='pagination-next-page']"
            driver.get("https://www.trulia.com/")

            #Waits for front page. If it does not load, the spider assumes a capthca has appeared. 
            #The user is expected to fill out the verification themselves
            if(WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@id='banner-search']")))):
                print("Please fill out verification")
                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//input[@id='banner-search']")))
                driver.find_element_by_xpath("//input[@id='banner-search']").click()

            #Searches location based on location user has inputted
            ActionChains(driver) \
                    .send_keys(location) \
                    .key_down(Keys.ENTER) \
                    .key_up(Keys.ENTER) \
                    .perform()
        #Code block used if the spider crawls Zillow
        else:  
            #Assigns xpath for elements and loads zillow.com search based on location user has inputted
            verification_element = "//strong[@id='sort_label']"
            next_page_element = "//a[(@title='Next page') and not (@tabindex='-1')]"
            driver.get("https://www.zillow.com/homes/"+location+"_rb/")
        
        #After page loads, spider checks to see if a human verification captcha has appeared (just as before)
        #If a captcha appears, the user is expected to fill out the human verification
        time.sleep(3)
        if(not(driver.find_elements_by_xpath(verification_element))):
            print("Please fill out verification")
            WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, verification_element)))

        #Adds page html to the self.html variable
        self.html = ''
        self.html += driver.page_source

        #Loops through pages based on whether the page includes a next page element
        #If there is no next page element, the spider assumes that it's on the last page
        #At each end of the loop, the html is added to the self.html variable
        while (driver.find_elements_by_xpath(next_page_element)):
            driver.find_element_by_xpath(next_page_element).click()
            time.sleep(1)
            self.html += driver.page_source

        #After concluding that it has reached the last page, the spider closes the driver
        driver.close()

    #Method to parse info from html
    def parse(self, response):

        #Initialization of resp variable before parsing
        resp = Selector(text=self.html)

        #If Trulia was scraped, the spider parses the info from each home card element
        for home in resp.xpath("//li[starts-with(@data-testid,'srp-home-card')]"):
            #Gets address of home
            address = home.xpath(".//div/div/div/div/div[2]/div/a/div[1]/text()").get()
            #Gets town of home
            town = home.xpath(".//div/div/div/div/div[2]/div/a/div[2]/text()").get()
            #Gets price of home
            price = home.xpath(".//div/div/div/div/div[2]/div/div[1]/div/div/text()").get()
            #Get bedroom count if the bedroom count is available
            if (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/text()").extract_first()):
                bed = (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/text()").extract_first()).split('b')[0]
            else:
                bed = "None"
            #Gets bathroom count of home if the bathroom count is available
            if (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div/text()").extract_first()):
                bathroom = (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/text()").extract_first()).split('b')[0]
            else:
                bathroom = "None"
            #Gets square feet of home if the square feet is available
            if (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div/text()").extract_first()):
                sqft = (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div/text()").extract_first()).split(' ')[0]
            else:
                sqft = 'None'

            #Yields all info collected from the home
            yield {
                'address': address,
                'town': town,
                'price': price,
                'bed': bed,
                'bathroom': bathroom,
                'sqft':sqft
            }
        #If Zillow was scraped, the spider parses the info from each home card element
        for home in resp.xpath("//article[@role='presentation']"):
            #Gets link of home
            link = home.xpath("./div[2]/a").xpath('@href').get()
            #Gets address of home
            address = home.xpath(".//div[1]/a/address/text()").get()
            #Gets price of home
            price = home.xpath(".//div[1]/div[2]/div/text()").get()
            #Gets bedroom count of home if the bedroom count is available
            if (home.xpath(".//div[1]/div[2]/ul/li[1]/text()").extract_first()):
                bed = home.xpath(".//div[1]/div[2]/ul/li[1]/text()").extract_first()
            else:
                bed = "None"
            #Gets bathroom count of home if the bathroom count is available
            if (home.xpath(".//div[1]/div[2]/ul/li[2]/text()").extract_first()):
                bathroom = home.xpath(".//div[1]/div[2]/ul/li[2]/text()").extract_first()
            else:
                bathroom = "None"
            #Yields all info collected from the home
            yield {
                'link':link,
                'address': address,
                'price': price,
                'bed': bed,
                'bathroom': bathroom,
            }