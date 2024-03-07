# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DtvDownloaderMiddleware:
    sum = 1

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):


        bro = spider.bro
        bro.maximize_window()  # 窗口最大化
        bro.get(url=request.url)
        sleep(random.uniform(2.5, 3.5))
        bro.implicitly_wait(3)
        if self.sum == 1:
            self.sum += 1
            js = "window.scrollTo(0,1000);"
            login_btn = bro.find_element(By.XPATH, '//*[@id="i_cecream"]/div/div[1]/div/div[1]/ul[2]/li[1]/li/div')  # 实现登录
            sleep(0.5)
            wait = WebDriverWait(bro, 1200, 0.5)  # 设置等待
            login_btn.click()
            try:
                wait.until(EC.staleness_of(login_btn))  # 判断是否登录成功,设置等待时间直至登录成功
            except:
                print('登录超时！')
            try:
                for i in range(1, 20, 10):
                    sleep(random.uniform(1.5, 2.5))
                    target = bro.find_element(By.XPATH, f'//*[@id="i_cecream"]/div/main/div/div[3]/div[2]/div[{i}]')
                    bro.execute_script("arguments[0].scrollIntoView();", target)
            except :
                pass
            # target = bro.find_element(By.XPATH, f'//*[@id="comment"]/div/div/div/div[2]/div[2]/div[{i}]')
            # bro.execute_script("arguments[0].scrollIntoView();", target)
        # js = "window.scrollTo(0,1000);"
        # bro.execute_script(js)  # 调动滑轮往下滑
        # bro.execute_script(js)
        page_text = bro.page_source
        new_resp = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
        return new_resp


    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass


