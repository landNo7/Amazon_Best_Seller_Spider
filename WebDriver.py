from selenium import webdriver
import time
import random


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
        search_box = self.driver.find_elements_by_xpath('//*[@data-component-type="sp-sponsored-result"]//*\
        [@class="a-link-normal a-text-normal"]')
        for i in range(0, len(search_box)):
            links = self.driver.find_elements_by_xpath('//*[@data-component-type="sp-sponsored-result"]//*\
            [@class="a-link-normal a-text-normal"]')
            asin_list = self.driver.find_elements_by_xpath('//*[contains(@class,"AdHolder")]')
            if self.asin == asin_list[i].get_attribute('data-asin'):
                links[i].click()
                self.random_click()
                break
            else:
                continue
        if self.click_flag == 1 or self.next_page > self.next_limit:
            self.driver.quit()
        else:
            self.driver.find_element_by_xpath('//*[@class="a-last"]/a').click()
            self.next_page += 1
            self.sponsored_click()

    def random_click(self):
        mode = random.randint(1, 4)
        if mode == 1:
            self.click_mode_1()
        elif mode == 2:
            self.click_mode_2()
        elif mode == 3:
            self.click_mode_3()
        else:
            self.click_mode_4()

    def click_mode_1(self):
        for button in self.driver.find_elements_by_xpath('//*[@id="variation_color_name"]/ul/li/span\
                        /div/span/span/span/button'):
            try:
                button.click()
                time.sleep(1 + random.random())
            except:
                continue
        for j in range(0, 3):
            self.driver.execute_script("window.scrollBy(0,{num})".format(num=random.randint(500, 1000)))
            time.sleep(1 + random.random())

        time.sleep(3)
        self.click_flag = 1
        self.driver.back()

    def click_mode_2(self):
        return

    def click_mode_3(self):
        return

    def click_mode_4(self):
        return


if __name__ == '__main__':
    _url = 'https://www.amazon.com/s?k=iphone+x+case&ref=nb_sb_noss_1'
    _driver = webdriver.Chrome('G:\\迅雷下载\\chromedriver.exe')
    _asin = 'B07GBJ9ZYM'
    _next_limit = 10
    SC = SponsoredClick(_url, _next_limit, _asin, _driver)
    SC.sponsored_click()
    _driver.quit()
