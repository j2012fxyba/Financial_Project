
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By




#selenium模拟用户登录

chrome_option=Options()
driver=webdriver.Chrome(chrome_options=chrome_option)
chrome_option.add_argument('--headless')   #无头模式，浏览器在后台运行
#chrome_option.add_argument('disable-gpu')   禁用gpu模式
url='http://127.0.0.1:5000/login'
driver.get(url)

def login():

    try:
        user=driver.find_element_by_name('user')
        password=driver.find_element_by_name('pwd')
        login=driver.find_element_by_name('login')
        time.sleep(2)
        
        user.send_keys('admin')
        time.sleep(0.2)
        password.send_keys('123')
    
        login.click()
        time.sleep(0.5)
    except Exception as e:
        print(e)


#爬取/show页码的手机信息
def spider_phone():
    print(driver.current_url)
    
    html=driver.find_element(By.XPATH,'//form[@id="frm"]//*')
    print(html.get_attribute('outerHTML'))
   
    #获取tr> th
    trs=driver.find_elements(By.TAG_NAME,'tr')
    for tr in trs:
        ths=tr.find_elements(By.TAG_NAME,'th')
        
        if len(ths)==3:
            a=ths[0].text
            b=ths[1].text
            c=ths[2].text
            print("%-16s%-16s%-16s" %(a,b,c))
            
    # #获取tr >td
    trs=driver.find_elements(By.TAG_NAME,'tr')
    for tr in trs:
    
        tds=tr.find_elements(By.TAG_NAME,'td')

        if len(tds)==3:
            marks=tds[0].text
            model=tds[1].text
            price=tds[2].text
            print("%-16s%-16s%-16s" %(marks,model,price))


        
        


login()
spider_phone()