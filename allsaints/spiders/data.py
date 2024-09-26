import datetime
import json

import scrapy
from scrapy.cmdline import execute
from allsaints.db_config import DbConfig
from fake_useragent import UserAgent
from allsaints.items import dataItem
import os
import hashlib

ua = UserAgent()
obj = DbConfig()
today_date = datetime.datetime.now().strftime("%d_%m_%Y")
def create_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()
def page_write(pagesave_dir, file_name, data):
    if not os.path.exists(pagesave_dir):
        os.makedirs(pagesave_dir)
    file = open(file_name, "w", encoding='utf8')
    file.write(data)
    file.close()
    return "Page written successfully"

class DataSpider(scrapy.Spider):
    name = "data"
    handle_httpstatus_list = [403, 401]

    def start_requests(self):
        qr = f"select * from {obj.store_table} where status=0"
        obj.cur.execute(qr)
        rows = obj.cur.fetchall()
        for row in rows:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                # 'upgrade-insecure-requests': '1',
                'user-agent': ua.random,
                'Content-Type': 'text/plain'
            }
            yield scrapy.Request(url=row['store_link'], headers=headers, meta=row, callback=self.parse)

    def parse(self, response):
        hashid = create_md5_hash(response.meta['store_link'])
        pagesave_dir = rf"C:/Users/Actowiz/Desktop/pagesave/allsaints/{today_date}"
        file_name = fr"{pagesave_dir}/{hashid}.html"
        page_write(pagesave_dir, file_name, response.text)
        store_locator_div = response.xpath("//div[@class='l-storelocator-details_info']")
        store_name = store_locator_div.xpath(".//h1[@class='b-storelocator_result-name']/text()").get()
        store_name = store_name.strip()
        lat = store_locator_div.xpath(".//div/@data-latitude").get()
        lng = store_locator_div.xpath(".//div/@data-longitude").get()
        address = store_locator_div.xpath(".//div[@class='b-storelocator_result-address']//p/text()").getall()
        try:phone = store_locator_div.xpath(".//div[@class='b-storelocator_result-phone']/a/text()").get()
        except:phone = ""
        try:
            store_schedule = ""
            schedule_div = store_locator_div.xpath(".//div[@class='b-storelocator_result-schedule']/table//tr")
            list_schedule = list()
            for schedule in schedule_div:
                day = schedule.xpath("./td[1]/text()").get()
                timings = schedule.xpath("./td[2]/text()").get()
                day_timings = f"{day}: {timings}"
                if 'None' not in day_timings:
                    list_schedule.append(day_timings)
                store_schedule = " | ".join(list_schedule)
        except:
                store_schedule = ""
        try:map_url = store_locator_div.xpath(".//a[contains(@class, 'b-storelocator_result-get_directions')]/@href").get()
        except:map_url = ""
        script = response.xpath("//script[@type='application/ld+json']/text()").get()
        script_jsn = json.loads(script)
        postal_code = script_jsn["address"]["postalCode"]
        state = script_jsn["address"]["addressRegion"]
        city = script_jsn["address"]["addressLocality"]
        streetAddress = script_jsn["address"]["streetAddress"]
        country = script_jsn["address"]["addressCountry"]
        item = dataItem()
        item['store_no'] = ""
        item['name'] = store_name
        item['latitude'] = lat
        item['longitude'] = lng
        item['street'] = streetAddress
        item['city'] = city
        item['state'] = state
        item['zip_code'] = postal_code
        item['county'] = city
        item['phone'] = phone
        item['open_hours'] = store_schedule
        item['url'] = response.meta['store_link']
        item['provider'] = "Allsaints"
        item['category'] = "Apparel And Accessory Stores"
        item['updated_date'] = datetime.datetime.today().strftime("%d-%m-%Y")
        item['country'] = "US"
        item['status'] = ""
        item['direction_url'] = map_url
        item['pagesave_path'] = file_name
        item['id'] = response.meta['id']
        # all = store_locator_div.xpath(".//text()").getall()
        yield item











if __name__ == '__main__':
    execute("scrapy crawl data".split())