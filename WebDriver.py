from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import random
from selenium.webdriver.support import expected_conditions as ec


class SponsoredClick(object):
    def __init__(self, url, next_limit, asin, driver):
        self.next_page = 0
        self.click_flag = 0
        self.url = url
        self.next_limit = next_limit
        self.asin = asin
        self.driver = driver
        self.driver.maximize_window()
        self.driver.get(url)

    def sponsored_click(self):
        search_box = driver.find_elements_by_xpath('//*[@data-component-type="sp-sponsored-result"]//*\
        [@class="a-link-normal a-text-normal"]')
        for i in range(0, len(search_box)):
            links = driver.find_elements_by_xpath('//*[@data-component-type="sp-sponsored-result"]//*\
            [@class="a-link-normal a-text-normal"]')
            asin_list = driver.find_elements_by_xpath('//*[contains(@class,"AdHolder")]')
            if asin == asin_list[i].get_attribute('data-asin'):
                self.onclick(links[i])
                break
            else:
                continue
        if self.click_flag == 1 or self.next_page > self.next_limit:
            self.driver.quit()
        else:
            self.driver.find_element_by_xpath('//*[@class="a-last"]/a').click()
            self.next_page += 1
            self.sponsored_click()

    def onclick(self, link):
        link.click()
        for button in driver.find_elements_by_xpath('//*[@id="variation_color_name"]/ul/li/span\
                        /div/span/span/span/button'):
            try:
                button.click()
                time.sleep(1 + random.random())
            except:
                continue
        for j in range(0, 3):
            driver.execute_script("window.scrollBy(0,{num})".format(num=random.randint(500, 1000)))
            time.sleep(1 + random.random())

        time.sleep(3)
        self.click_flag = 1
        self.driver.back()


if __name__ == '__main__':
    url = 'https://www.amazon.com/s?k=iphone+x+case&ref=nb_sb_noss_1'
    driver = webdriver.Chrome('G:\\迅雷下载\\chromedriver.exe')
    asin = 'B07GBJ9ZYM'
    next_limit = 10
    SC = SponsoredClick(url, next_limit, asin, driver)
    SC.sponsored_click()
    driver.quit()
