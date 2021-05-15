# -*- coding: utf-8 -*-
import scrapy
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
"""
cd projects/real_estate_webscraper/real-estate-webscraper
scrapy crawl house_info -o house_info.csv

"""
class HouseInfoSpider(scrapy.Spider):
    name = 'house_info'
    allowed_domains = ['www.trulia.com', 'www.zillow.com']
    start_urls = ['https://www.trulia.com/CA/San_Francisco/']
    def scrape(self, location, trulia):

        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("user-data-dir=C:\\Users\\thana\\AppData\Local\\Google\\Chrome\\User Data\\Default") #Path to your chrome profile
        #driver = webdriver.Chrome(executable_path=PATH, chrome_options=options)
        #chrome_options = Options()
        #chrome_options.add_argument("--headless")

        #chrome_path = which("chromedriver")

        driver = webdriver.Chrome(executable_path='C:/Users/thana/Documents/DS/Dababy/chromedriver.exe', options=chrome_options)

        
        verification_element = ""
        next_page_element = ""
        if (trulia):
            verification_element = "//select[@aria-label='Sort Results']"
            next_page_element = "//li[@data-testid='pagination-next-page']"
            driver.get("https://www.trulia.com/")

            if(WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@id='banner-search']")))):
                print("Please fill out verification")
                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//input[@id='banner-search']")))
                driver.find_element_by_xpath("//input[@id='banner-search']").click()


            ActionChains(driver) \
                    .send_keys(location) \
                    .key_down(Keys.ENTER) \
                    .key_up(Keys.ENTER) \
                    .perform()
        else:  
            verification_element = "//strong[@id='sort_label']"
            next_page_element = "//a[(@title='Next page') and not (@tabindex='-1')]"
            driver.get("https://www.zillow.com/homes/"+location+"_rb/")
        
        time.sleep(3)

        if(not(driver.find_elements_by_xpath(verification_element))):
            print("Please fill out verification")
            WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, verification_element)))

        self.html = ''
        self.html += driver.page_source

        while (driver.find_elements_by_xpath(next_page_element)):
            driver.find_element_by_xpath(next_page_element).click()
            time.sleep(1)
            self.html += driver.page_source

        driver.close()

    def __init__(self):
        file1 = open('info.txt', 'r')
        lines = file1.readlines()
        country = lines[0].strip()
        city = lines[1].strip()
        if country=='c':
            self.scrape(
            location = city,
            trulia = False
            )
        else:
            self.scrape(
            location = city,
            trulia = True
            )



    def parse(self, response):
        resp = Selector(text=self.html)
        #homes = response.xpath("//li[starts-with(@data-testid,'srp-home-card')]")
        #//li[starts-with(@data-testid,'srp-home-card')]/div/div/div/div/div[2]/div/div[1]/div/div
        for home in resp.xpath("//li[starts-with(@data-testid,'srp-home-card')]"):
            address = home.xpath(".//div/div/div/div/div[2]/div/a/div[1]/text()").get()
            town = home.xpath(".//div/div/div/div/div[2]/div/a/div[2]/text()").get()
            price = home.xpath(".//div/div/div/div/div[2]/div/div[1]/div/div/text()").get()
            if (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/text()").extract_first()):
                bed = (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/text()").extract_first()).split('b')[0]
            else:
                bed = "None"
            if (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div/text()").extract_first()):
                bathroom = (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/text()").extract_first()).split('b')[0]
            else:
                bathroom = "None"
            if (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div/text()").extract_first()):
                sqft = (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div/text()").extract_first()).split(' ')[0]
            else:
                sqft = 'None'
            yield {
                'address': address,
                'town': town,
                'price': price,
                'bed': bed,
                'bathroom': bathroom,
                'sqft':sqft
            }

        for home in resp.xpath("//article[@role='presentation']"):
            link = home.xpath("./div[2]/a").xpath('@href').get()
            address = home.xpath(".//div[1]/a/address/text()").get()
            #town = home.xpath(".//article[@role='presentation']/div[1]/div[2]/div/text()").get()
            price = home.xpath(".//div[1]/div[2]/div/text()").get()
            if (home.xpath(".//div[1]/div[2]/ul/li[1]/text()").extract_first()):
                bed = home.xpath(".//div[1]/div[2]/ul/li[1]/text()").extract_first()
            else:
                bed = "None"
            if (home.xpath(".//div[1]/div[2]/ul/li[2]/text()").extract_first()):
                bathroom = home.xpath(".//div[1]/div[2]/ul/li[2]/text()").extract_first()
            else:
                bathroom = "None"
            """
            if (home.xpath(".//article[@role='presentation']/div[1]/div[2]/div/text()").extract_first()):
                sqft = (home.xpath(".//div/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div/text()").extract_first()).split(' ')[0]
            else:
                sqft = 'None'
            """
            yield {
                'link':link,
                'address': address,
                'price': price,
                'bed': bed,
                'bathroom': bathroom,
            }