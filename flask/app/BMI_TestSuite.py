


import unittest
from  openpyxl import load_workbook
from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium import webdriver


#另一个例子：如果你想设计 table的多行操作，可以通过 row in for row_number 来循环excel里面的每一行



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

        
    

    # def test_selenium_bmi(self):   
    #     url='http://127.0.0.1:5000/'
    #     #driver=cls.driver()
    #     driver=self.driver()  #这里 cls.driver是类的driver 而 self.driver是每个方法单独的 
    #     driver.get(url)
    #     print(driver.current_url)
          return driver


#从excel 中读取数据 参数化 然后 selenium传入到抓取的元素中
class test_BMI(unittest.TestCase):
    @classmethod
    def setUpclass(cls):

        print('测试类开始执行')
        #在类方法内部，不能直接访问实例属性（因为还没有实例化） 将dirver与类绑定
        #所以不能是 self.driver
        
        cls.driver=webdriver.Chrome()
        #driver1=webdriver.Chrome()   #区别， driver1只在此方法中有效，而在类别的方法无法访问
        cls.driver.implicitly_wait(10)  

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
