# -*- coding: utf-8 -*-
import scrapy
import logging


class HouseInfoSpider(scrapy.Spider):
    name = 'house_info'
    allowed_domains = ['www.trulia.com']
    start_urls = ['https://www.trulia.com/CA/San_Francisco/']

    def parse(self, response):
        homes = response.xpath("//li[starts-with(@data-testid,'srp-home-card')]")
        #//li[starts-with(@data-testid,'srp-home-card')]/div/div/div/div/div[2]/div/div[1]/div/div
        for home in homes:
            price = home.xpath(".//div/div/div/div/div[2]/div/div[1]/div/div/text()").get()
            yield {
                'price': price
            }