


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains 
import unittest
from  openpyxl import load_workbook



class test_BMI():
    def login_BMI(self):
        self.driver=webdriver.Chrome()
        url='http://127.0.0.1:5000/'
        self.driver.get(url)
        time.sleep(1)
        print(self.driver.current_url)
        print(self.driver.title)
        time.sleep(2)
        return self.driver

    
    #send_key  click()button
    def spider_key(self):
        
        a=self.driver.find_element(By.XPATH,'//div[@class="calculator"]')
        z=a.find_element(By.XPATH,'//input[@id="height"]')
        ActionChains(self.driver).move_to_element(z).click().perform()
        time.sleep(2)
        z.send_keys('160')
        
        w= a.find_element(By.XPATH,'//input[@id="weight"]')
        time.sleep(2)
        w.send_keys('45')

        button=self.driver.find_element_by_tag_name('button')
        time.sleep(1)
        button.click()
        time.sleep(3)


    #获取title th td
    def get_html_parame(self):
        
        title=self.driver.find_element(By.XPATH,'//head/title')
        print(title.get_attribute('text'))

        a=self.driver.find_element(By.XPATH,'//div[@class="calculator"]')
        print(a.get_attribute('outerHTML'))
        tr_list=a.find_elements(By.XPATH,'.//div[@class="bmi-info"]//table//tr')
        for row in tr_list:
            tds=row.find_elements(By.TAG_NAME,'td')
            ths=row.find_elements(By.TAG_NAME,'th')
            if ths:
                for th in ths:
                    table_title=th.text
                    print(table_title)
            elif tds:
                for td in tds:
                    table_data=td.text
                    print(table_data)
        return table_title,table_data
   



T=test_BMI()
T.login_BMI()
T.spider_key()
T.get_html_parame()