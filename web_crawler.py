# coding: utf-8
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import time
import re

class vieclam24h_Crawler(scrapy.Spider):
    name = "vieclam24h_crawler"
    start_urls = ['https://vieclam24h.vn/tim-kiem-viec-lam-nhanh/?hdn_nganh_nghe_cap1=&hdn_dia_diem=&hdn_tu_khoa=&hdn_hinh_thuc=&hdn_cap_bac=']
    
    vieclam24h_df = pd.DataFrame(columns=['title', 'company', 'salary'])

    def parse(self, response):
        XPATH = '//div[@class="detail-link pos_relative"]'
        links = response.xpath(XPATH)
        for index, link in enumerate(links):
            salary = link.xpath('div[@class="pos_absolute list_note_icon"]/div[@title="Mức lương"]/br/following::text()').get()
            print(salary)
            processed_salary = salary.replace('\n','')
            processed_salary = processed_salary.strip()
            processed_salary = re.sub(' +', ' ', processed_salary)
            title = link.xpath('div[@class="content_list_item_line w_100"]//a[@title and @class="text_grey2"]/text()').get()
            company = link.xpath('div[@class="content_list_item_line w_100"]//a[@href and @class="text_grey"]/text()').get()
            #print(title, company, processed_salary)
            self.vieclam24h_df = self.vieclam24h_df.append({'title': title \
                , 'company':company, 'salary':processed_salary}, ignore_index=True)
            self.vieclam24h_df.to_csv("vieclam24h.csv", encoding='utf-8')


class aliexpress_Crawler(scrapy.Spider):
    name="aliexpress_crawler"
    start_urls=['https://www.aliexpress.com/category/7/computer-office.html?spm=2114.11010108.104.1.650c649bV9UZCj']

    aliexpress_df = pd.DataFrame(columns=['product', 'company', 'price'])

    def parse(self, response):
        XPATH = '//*[@id="list-items"]//li'
        links = response.xpath(XPATH)
        for index, link in enumerate(links):
            company = link.xpath('div[1]/div/div[1]/div/span/a/text()').get()
            product = link.xpath('div[1]/div/div[1]/h3/a/span/text()').get()
            price = link.xpath('div[1]/div/div[2]/span/span[1]/text()').get()
            #print(title, company, processed_salary)
            self.aliexpress_df = self.aliexpress_df.append({'product': product \
                , 'company':company, 'price':price}, ignore_index=True)
            self.aliexpress_df.to_csv("aliexpress.csv", encoding='utf-8')

class vnexpress_Crawler(scrapy.Spider):
    name="vnexpress_crawler"
    start_urls=['https://vnexpress.net/kinh-doanh']

    articles = []
    vnexpress_df = pd.DataFrame(columns=['title','description'])

    csv_filename = 'vnexpress.csv'

    def parse(self, response):
        article_xpath = '//article[@class="list_news"]'
        links = response.xpath(article_xpath)
        for index, article in enumerate(links):
            # an_article = {
            #     'title': '',
            #     'description': ''
            # }
            # an_article['title'] = article.xpath('h4/a[@title]/text()').get()
            # an_article['description'] = article.xpath('p/text()').get()
            # self.vnexpress_df.append(an_article)
            title = article.xpath('h4/a[@title]/text()').get()
            description = article.xpath('p/text()').get()
            print(title, description)
            self.vnexpress_df = self.vnexpress_df.append({'title':title, 'description':description}, ignore_index=True)
            #print(an_article)
        print(self.vnexpress_df)
        self.vnexpress_df.to_csv(self.csv_filename, sep='\t', encoding='utf-8')
process = CrawlerProcess()
process.crawl(vieclam24h_Crawler)
process.crawl(vnexpress_Crawler)
process.crawl(aliexpress_Crawler)

process.start()