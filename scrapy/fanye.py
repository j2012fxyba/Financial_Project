

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.parse
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pandas import DataFrame

  #翻页 javascript 动态获取的 后台ajax 异步更新网页内容，而url不发生变换
  #ETF-174320 

def init_driver():


    url='https://fund.eastmoney.com/data/fundranking.html#tall;c0;r;s1nzf;pn50;ddesc;qsd20240518;qed20250518;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb'

    chrome_options=Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36')
    driver=webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    time.sleep(3)
    print(driver.title)
    print(driver.current_url)
    return driver

"""获取分页链接"""
def click_next_page(driver):

    try:
        print(driver.current_url)
        # 定位“下一页”的 label 元素
        next_page_label = driver.find_element(By.XPATH, '//label[text()="下一页"]')

        # 获取当前页码（用于判断是否已翻页成功）
        current_page = driver.find_element(By.XPATH, '//label[@class="cur"]').text

        # 点击“下一页”
        next_page_label.click()

        # 等待新页码出现，并且与之前不同（表示页面已刷新）
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.XPATH, '//label[@class="cur"]').text != current_page
        )

        print("成功翻到下一页！")
        return True

    except Exception as e:
        print("无法翻页或已到达最后一页:", e)
        return False
    

def spider_data(driver):
    try:
        thead_tr=driver.find_element(By.XPATH,'//table[@id="dbtable"]/thead/tr')
        row_data=[]
    
        ths=thead_tr.find_elements(By.TAG_NAME,'th')
        row_head=[]
        for th in ths:

            row_head.append(th.text )
        row_data.append(row_head)
       

        tbody_tr=driver.find_elements(By.XPATH,'//table[@id="dbtable"]/tbody/tr')
        for tr in tbody_tr:
            td_data=[]
            tds=tr.find_elements(By.TAG_NAME,'td')
            for td in tds:
            #print(td.text)
                td_data.append(td.text)
            row_data.append(td_data)

        #print(row_data)
        return row_data  # 确保返回row_data
    except Exception as e:
        print(e)

#主程序和翻页结合
def spider_with_pagination():
    driver = init_driver()
    all_data = []
    while True:
        # 循环 抓取当前页面的数据  这个while的循环会自动调用翻页
        row_data = spider_data(driver)
        if row_data: 
            # 在这里处理抓取到的数据（例如保存到文件、数据库等）
            print(row_data)
        if len(row_data) > 1: 
            all_data.extend(row_data[1:])  

       
        if not click_next_page(driver): 
            print("所有页面已抓取完毕")
            break
        
       
        df=DataFrame(all_data,columns=row_data[0])   # 使用第一页的列名作为表头
        
        #上涨：3002只 下跌：2187只
        outfile='D:\\tool\\PythonTest\\AutoTest\\seleniums\\ETF174320.xlsx'
        #写入excel文件里面
        df.to_excel(outfile,index=False)
        print(f"所有数据已写入 {outfile}")
        # 可选延迟，避免过快请求
        time.sleep(3)
    driver.quit()
    


spider_with_pagination()