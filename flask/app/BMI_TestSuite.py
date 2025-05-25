


import unittest
from  openpyxl import load_workbook
from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium import webdriver


'''
#cls 是类方法 类似于self（@classmethod）中的一个约定命名参数，代表类本身（class itself）
#self 指向实例对象，实例对象是 单个 实例的  而 cls指向类方法 ，类方法是和类绑定的
'''

'''
写代码之前先 设计好 调用的框架和 每个类的方法里面怎么走，现在的问题是  比较混乱

没有遵从几个原则：首先页面和参数化分开，其次 数据excel加载可以单独封装一个方法，
其次 对于测试类，这里面是不需要参数化循环的 selenium的页面元素爬取的

所以：现在存在几个问题  1  先封装一个页面元素爬取的方法 
2 封装一个参数化的方法，可以是 excel和 元组 字典 或者数据库驱动  ，可以是 junit and  unittest 
3 封装个 计算bmi的方法,给出计算的公式
4 封装一个 计算bmi_category ,根据实际计算的 bmi 判断属于哪一类
5 封装一个 测试 用于校验计算的bmi 和category的值是否正确
6 构造一个 输出的report报告
7 现在犯的问题是 设计思路比较混乱 然后页面的元素爬取的xpath 不是很熟悉，导致有些元素爬取不到
8 click的点击无效
9 参数化的excle 加载和csv加载 以及 元素 或者字典 格式 以及 列表和  集合的 数据格式不太熟悉，所以操作起来比较man
10 对于之前的问题，这里需要继续验证的是否 方法存在问
11 如果下次设计一个类似的项目，是不是可以沿用这个办法，先抽象出项目的结构性框架，然后将框架形成惯性，直接套用 
12  需要操作的步骤游侠： 先 找到合适的项目，然后找到页面元素的相似性（需要练习 点击 单击  双击 拖拽 send_keys ），数据的相似性，参数集合脚本的相似性
13 项目的化，类似

14  页面的封装： 包括 登录  查询  从业务模块来拆分，或者单从页面来拆分
15 业务流程包括：登录  注册  修改密码  充值  转账  个人信息中心  设置  支付结算  
16 从页面角度封装： 每一个页面的从首页开始，跳转到下一页，然后再跳转到下一页  
比方：请登录  用户名密码登录 验证码登录 登录页面的用户名密码输入  登录成功的 产品展示  产品详情  产品加入购物车  购物车产品信息展示
17  实际上 页面元素的封装和  从业务角度考虑的封装是类似的
19  做到页面元素的封装和 数据参数化分离，这样如果测试案例需要调整，也只是 调节参数化的案例 
20  页面元素的案例是不需要动的
21 如果页面元素，比方技术改造或者 业务改造，修改了前端的页面的加载方式或者样式，javascript的化，可以单独 update 该页面的案例
22 数据参数化，单一来说只是  测试角度 对于数据变动的案例改造


23  selenium元素定位的方法：
by.css 
另一个例子：如果你想设计 table的多行操作，可以通过 row in for row_number 来循环excel里面的每一行



'''
driver=webdriver.Chrome()
userName=driver.findElement(By.CSS_SELECTOR('html>body>div>div>form>input'))
userName=driver.find_element(By.CSS_SELECTOR('input'))
driver.elememnt(By.CLASS_NAME())
driver.element(By.CSS_SELECTOR('input.login')) # yem de calss 的login的元素的封装

login=driver.element(By.CSS_SELECTOR('.login'))

driver.find_element(By.CSS_SELECTOR('input#username'))
userName id
driver.find_element(By.CSS_SELECTOR('username'))

        
    
    #封装页面元素，不需要数据参数化，只是封装获取页面元素的逻辑
    #后面真正 calcuator计算值的时候，才需要参数化
    # def test_selenium_bmi(self):   
    #     url='http://127.0.0.1:5000/'
    #     #driver=cls.driver()
    #     driver=self.driver()  #这里 cls.driver是类的driver 而 self.driver是每个方法单独的 
    #     driver.get(url)
    #     print(driver.current_url)






#从excel 中读取数据 参数化 然后 selenium传入到抓取的元素中
class test_BMI(unittest.TestCase):
    @classmethod
    def setUpclass(cls):

        print('测试类开始执行')
        #在类方法内部，不能直接访问实例属性（因为还没有实例化） 将dirver与类绑定
        #所以不能是 self.driver
        
        cls.driver=webdriver.Chrome()
        #driver1=webdriver.Chrome()   #区别， driver1只在此方法中有效，而在类别的方法无法访问
        cls.driver.implicitly_wait(10)  #隐士等待 10s

    def tearDownClass(cls):

        cls.driver.quit()  # 每个测试方法后清理

    parameterized.expand([
        ('正常体重','1.75','70','23.5','Normal'),
        ('体重过轻',"180", "50", "22.7", "underweight"),
        ('超重',"170", "80", "24.8", "voerweight"),
        ('肥胖',"170", "80", "27.2", "obesity"),
        ('边界测试',"0.01", "1", "100", "体重过轻")
    ])
    
    @parameterized
    def test_data():
        pass
        
    

    @classmethod
    def teardownclass():
        print('测试类运行结束')


    #计算低于18.5 偏瘦
    def test_calcuator_18(self):
        
        
        for i in range(len(self.test_data)):
            height_m = float(self.height[i]) / 100  # 厘米转米
            print('身高'+str(height_m))
            
            calculated_bmi = round(float(self.weight[i]) / (height_m ** 2), 1)
            print('bmi'+str(calculated_bmi))
            self.assertEqual(str(calculated_bmi), self.bmi[i])
            print('fenlei'+str(calculated_bmi))
        
        height_m = float(self.height[i]) / 100  # 厘米转米
        calculated_bmi = float(self.weight) / (height_m ** 2)
        self.assertEqual(self.height_m + self.weight, self.bmi,f'不相等')  # 断言

    #计算正常值
    def test_calcuate_23(self):
        self.assertNotEqual(self.height_m+self.weight, self.bmi,f'nonno')
    #计算超重
    def test_calculate_27(self):
        self.assertCountEqual(self.assertCountEqual)

    def test_calcu_fat28(self):
        self.assertEqual('计算肥胖')  #分别传入肥胖的数据
    # 在每个测试方法后执行（类似JUnit的@After）
    def tearDown(self):
        #driver.close()
        pass

    #创建一个测试集合，逐个添加测试案例
    def suit1():
        test_suit=unittest.TestSuite()
        #添加测试案例 test_BMI类名来引用
        test_suit.addTests(test_BMI('test_calcu_fat28'))
        test_suit.addTest(test_BMI('test_BMI.test_calcuate_23'))
        test_suit.addTest(test_BMI('test_BMI.test_calcuator_18'))
        test_suit.addTest(test_BMI('test_BMI.test_calculate_27'))
        return test_suit
    
    #批量添加，直接添加 类名  不是方法名
    def suite2():
        suite2 = unittest.TestSuite()
        # load=unittest.TestLoader()
        # load.loadTestsFromTestCase()
        # 添加整个测试类的所有测试方法
        suite2.addTest(unittest.TestLoader().loadTestsFromTestCase(test_BMI.test_calcu_fat28)) #加载类单一方法
        suite2.addTest(unittest.TestLoader.loadTestsFromModule(test_BMI))  #加载整个类
        #suite2.addTest(unittest.makeSuite(TestString)) #废弃
        
         
def run_main():
    #实例化
    run=unittest.TextTestRunner()
    #运行测试集合
    run.run(test_BMI.suit1())
    run.run(test_BMI.suite2())
    testRunner=xmlrunner.XMLTestRunner(output='test-reports')
    print(testRunner)


if __name__ == '__main__':
    unittest.main()