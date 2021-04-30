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
#cd projects/real_estate_webscraper/real_estate_webscraper
#scrapy crawl house_info -o house_info.csv
class HouseInfoSpider(scrapy.Spider):
    name = 'house_info'
    allowed_domains = ['www.trulia.com']
    start_urls = ['https://www.trulia.com/CA/San_Francisco/']

    def __init__(self):

        #chrome_options = Options()
        #chrome_options.add_argument("--headless")

        #chrome_path = which("chromedriver")

        #driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver = webdriver.Chrome(executable_path = 'C:/Users/thana/Documents/DS/Dababy/chromedriver.exe')
        #driver.set_window_size(1920, 1080)
        driver.get("https://www.trulia.com/CA/San_Francisco/")


        #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[@class = 'xWeGp']")))
        #homes = []

        self.html = ''
        c = 0
        f = open("rec.txt", "w")


        while (driver.find_elements_by_xpath("//li[@data-testid='pagination-next-page']")):
            c+=1
            f.write(str(c)+'\n')
            self.html += driver.page_source
            driver.find_element_by_xpath("//li[@data-testid='pagination-next-page']").click()
            time.sleep(1)
        f.close()
        driver.close()

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