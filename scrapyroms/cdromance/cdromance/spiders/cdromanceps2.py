# -*- coding: utf-8 -*-
import scrapy
import requests

class Cdromanceps2Spider(scrapy.Spider):
    name = 'cdromanceps2'
    start_urls = ['https://cdromance.com/ps2-iso/']

    def parse(self, response):
        for article in response.css('section.cards article'):
          link = article.css('.game-box-layout a::attr(href)').extract_first()
          yield response.follow(link, self.parse_rom)

    def parse_rom(self, response):
      for fa in response.css('div.fa'):
        id = fa.xpath('@data-id').getall()[0]
        filename = fa.xpath('@data-filename').getall()[0]
        server = fa.xpath('@data-server').getall()[0]
        
        params = {
            'post_id': id,
            'file_name': filename,
	    'server_id': server
        }
          
        print(params)

        req = requests.post('https://cdromance.com/wp-content/plugins/cdromance/public/direct.php', data = params)
        yield {url: req.json}
        


