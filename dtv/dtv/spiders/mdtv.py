import scrapy
from selenium.webdriver.common.by import By
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from time import sleep
from dtv.items import DtvItem
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MdtvSpider(CrawlSpider):
    name = "mdtv"
    # allowed_domains = ["www.xxx.com"]
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 防止被检测
    # 处理SSL证书错误问题
    opt.add_argument('--ignore-certificate-errors')
    opt.add_argument('--ignore-ssl-errors')

    # 忽略无用的日志
    # opt.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

    opt.page_load_strategy = 'none'  # 页面加载策略为none
    # 无头浏览器
    # opt.add_argument('--headless')
    # opt.add_argument('--disable-gpu')
    bro = webdriver.Chrome(executable_path='./chromedriver.exe',
                           options=opt)



    start_urls = ["https://www.bilibili.com/v/douga/mad"]
    Channel_allow_domains = []  # //*[@id="i_cecream"]/div/main/div/div[3]/div[2]/div[1]
    # Channel_Link = LinkExtractor(restrict_xpaths=r'//*[@id="i_cecream"]/div[2]/div[1]/div[3]/div[2]'
    #                                              r'/div[1]/a[position()>6 and position()<8]')  # 各频道分类链接
    Detailed_partition_link = []  # 单个频道进一步分区
    video_Link = LinkExtractor(restrict_xpaths=r'//*[@id="i_cecream"]/div/main/div/div[3]/div[2]/div/div[2]/a')
    rules = (Rule(video_Link, callback="parse_video", follow=False),
             )

    num = 0


    def parse_item(self, response):
        Channel_title = response.xpath('//*[@id="i_cecream"]/div/div[3]/div/div/div[1]/text()').extract_first()
        # print(Channel_title)
        self.bro.maximize_window()  # 窗口最大化
        self.bro.get(url=response.url)
        sleep(60)
        self.bro.implicitly_wait(3)
        partition_btns = self.bro.find_elements(By.XPATH, '//*[@id="i_cecream"]/div/div[3]/div/div/div[2]/button[position()>1 and position()<=last()]')
        for partition_btn in partition_btns:
            try:
                sleep(0.5)
                partition_btn.click()
                self.Detailed_partition_link.append(self.bro.current_url)
                yield scrapy.Request(url=self.bro.current_url, callback=self.parse_partition)
                # print(self.bro.current_url)
            except:
                print('点击失败!')


    def parse_partition(self, response):
        titles = response.xpath('//*[@id="i_cecream"]/div/main/div/div[3]/div[2]/div/div[2]/div/div/h3/a/text()').extract()
        video_Links = response.xpath('//*[@id="i_cecream"]/div/main/div/div[3]/div[2]/div/div[2]/a/@href').extract()
        for video_Link in video_Links:
            print(video_Link)
            yield scrapy.Request(url='https:'+video_Link, callback=self.parse_video)
            self.num += 1

    def parse_video(self, response):
        try:
            item = DtvItem()  # //*[@id="viewbox_report"]/div/div/span[1]
            item['title'] = response.xpath('//*[@id="viewbox_report"]/h1/@title').extract_first().strip()
            item['Likes'] = response.xpath('//*[@id="arc_toolbar_report"]/div[1]/div[1]/div/span/text()').extract_first().strip()
            item['Playback_volume'] = response.xpath('//*[@id="viewbox_report"]/div/div/span[1]/text()').extract_first().strip()
            item['Number_of_barrages'] = response.xpath('//*[@id="viewbox_report"]/div/div/span[2]/text()').extract_first().strip()
            item['Number_of_coins_invested'] = response.xpath('//*[@id="arc_toolbar_report"]/div[1]/div[2]/div/span/text()').extract_first().strip()
            item['Collection_volume'] = response.xpath('//*[@id="arc_toolbar_report"]/div[1]/div[3]/div/span/text()').extract_first().strip()
            item['Forwarding_volume'] = response.xpath('//*[@id="share-btn-outer"]/div/span/text()').extract_first().strip()
            # print(item['Likes'])
            # print(item['Playback_volume'])
            # print(item['Number_of_barrages'])
            # print(item['Number_of_coins_invested'])
            # print(item['Collection_volume'])
            # print(item['Forwarding_volume'])
            yield item
            print(item['title']+'相关数据已获取完毕！')
            self.num += 1
        except:
            print('解析出错！')

    def closed(self, spider):
        self.bro.quit()
        print(self.num)