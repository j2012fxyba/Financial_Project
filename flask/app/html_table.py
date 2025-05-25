

#如果 数据在html 表格里面，需要通过selenium.webdriver(tr,td)的方式获取值  其实和爬虫是类似的

from selenium import webdriver
from selenium.webdriver.common.by import By

def get_web_table_column(driver, table_locator, row_index, column_index=None, column_title=None):
    """
    通过行索引获取 HTML 表格的列数据或标题
    :param driver: WebDriver 实例
    :param table_locator: 表格定位方式（如 By.ID, By.XPATH）
    :param row_index: 行索引（从 0 开始）
    :param column_index: 列索引（从 0 开始），与 column_title 二选一
    :param column_title: 列标题文本，用于动态确定列索引
    :return: 列值或列标题
    """
    table = driver.find_element(*table_locator)
    rows = table.find_elements(By.TAG_NAME, "tr")  # 获取所有行
    
    # 如果指定列标题，先根据标题行找到列索引
    if column_title:
        header_row = rows[0]  # 假设第一行是标题行
        headers = header_row.find_elements(By.TAG_NAME, "th") or header_row.find_elements(By.TAG_NAME, "td")
        column_index = next((i for i, elem in enumerate(headers) if elem.text == column_title), None)
        if column_index is None:
            raise ValueError(f"列标题 '{column_title}' 不存在")
    
    # 获取指定行的列数据
    target_row = rows[row_index]
    columns = target_row.find_elements(By.TAG_NAME, "td")
    
    if column_index is not None:
        return columns[column_index].text
    else:
        return [col.text for col in columns]  # 返回整行数据

# 示例调用
driver = webdriver.Chrome()
driver.get("https://example.com/table.html")

# 方式1：通过列索引获取数据
print(get_web_table_column(
    driver, 
    table_locator=(By.ID, "myTable"), 
    row_index=2, 
    column_index=1
))  # 获取第3行第2列的数据

# 方式2：通过列标题获取数据
print(get_web_table_column(
    driver,
    table_locator=(By.XPATH, "//table[@class='data']"),
    row_index=1,
    column_title="Price"
))  # 获取第2行中标题为 "Price" 的列数据