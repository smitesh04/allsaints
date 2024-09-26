import re
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from fake_useragent import UserAgent
from allsaints.items import storeLocatorItem
ua = UserAgent()


class StoreLocatorSpider(scrapy.Spider):
    name = "store_locator"
    handle_httpstatus_list = [403, 401]



    def start_requests(self):
        url = "https://www.allsaints.com/us/sitemap_us-stores.xml"
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': '__cf_bm=9t.gBSgmgRt7jngfUY.DgECWw3jm88vVPKwHjIUxYxg-1727088146-1.0.1.1-Lz1uM8q8X.cKOhTU9vyfmzSj7c2YlW4WrK_f7p0lunLdyKUswayJuUh_NCH2lQUgrsfAN00PPVOPzQ9A8m4ojg; as_session=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..11YM4NfhCpAFTLrv.FLcVlIv5IWK_5FIRk_OCpgr3rIdrgkt-j24iVV2J6bRc6zLm8T6CbwBDfcgAMSBWmvDMu5HoFqyAPxdKPN71KQCZHhdQ5l27sZCuTxrIOSaE4U_sIbC3dJ0ERU701ziVh-FiiZpJAuawtQ6zzEb88QqJAKuXUOiYSfQOvZy9clY8Xfi2mfOBe_ouGTc8JazK1pi0tr7ugWZNff8x3oj8wtkTtHP_X9t4XTp33jArxdB_y6U1KyExqlzqDT4kmdndxBum9qRSMQdOCGCsWrn9E1If2Z3r8k4mL3z7is0HrVq_.LaAxCkftqENcgI9XobXHzA; as_ctoken=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..m892-DhbBzaM0cfY.FgC81Cdecl2f6cV1weJTIXLTnbRy7ld3v1uoHbT0sUKrWlYtYWuHbjRkPjtu2IZYfl9IANfQvnYlu_Yy9aEQb7WmIW6thPcHIoQzJkAO9ea0Lz4CiA4e_qYlQw00QpOjoVvf5YeX6VcNSoS1ig.O09YNvmj-3mOc6PajsWxhg; _abck=FB3F21ECA16C06BD4487DD1D0E297DF1~-1~YAAQtphmUkkphP2RAQAAPELlCQx4Zw31C3soEkOO0tsxcc8U3exXZY0S/s1z+ASayFXzBcc0HBZB7lX9KLAMTfluXtiKWgATV4EF85Jd3IQMrPpn5A0DMgMcIal37R9+4oRRH6kCGCoYekDYE0iO++/T/XP04dSaqI6hpF/WL8Qf8aJPWgxKVc3Vx13/0lXS1XkUro8Amsk2hI0bzT19msPP14wNRwomAIafL3nA2oCm+n829TXuz39PrtMiNPRnNimDYeUstuCh3qiaoTjWyKOrNjBQXN8bbA8UO8ymNfvLo7UjqXgpFynH3vlr7arqEG5QzYsL93xZJce2K0RcCXzN+3qND5GadRSdP5gMTqg+Ty2leMQ+EWREpU7VK6zdvBSsv/VQsCPzoyPJsMY6G/U5KrH1GGNCaKFGE0iQdFV9VJpeoqJKtZfXWcG3cPgDddDAD6oXPtRWPW2CT3OUrRtDqQSduVMo1RBqFUNlZaTNf3PkJ/AzgXudNko0ZzQskCxcVs9oGLTs6W6OSDh4oTd7bqX0xLcJRp9u8EPPoHeY4+HoNHBNtyNYnM9d6dC/Q7y7lusII8c=~0~-1~1726740790',
            'priority': 'u=0, i',
            'referer': 'https://www.allsaints.com/us/sitemap_us-stores.xml',
            'upgrade-insecure-requests': '1',
            'user-agent': ua.random,
            'Content-Type': 'text/plain'
        }
        yield scrapy.Request(url, headers=headers, callback=self.parse)


    def parse(self, response):
        all_urls = re.findall('https.*?</loc>', response.text)
        for url in all_urls:
            url = url.replace('</loc>', '')
            if 'united-state' in url:
                item = storeLocatorItem()
                item['store_link'] = url
                item['country'] = 'US'
                item['state'] = url.split('/')[-2]
                yield item


if __name__ == "__main__":
    execute("scrapy crawl store_locator".split())