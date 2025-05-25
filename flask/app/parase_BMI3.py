import unittest

from parameterized import parameterized


#使用excel参数化
class TestBMI(unittest.TestCase):
    @parameterized.expand(
        [
            ('160', '45', '17.6', 'underweight'),
            ('168', '70', '24.8', 'Normal'),
            ('181', '89', '27.2', 'overweight'),
            ('178', '100', '31.6', 'obesity')
        ]
    )
    def test_calculate_bmi(self,height,weight,expected_bmi,expected_Category):
        calculated_bmi=self.calculate_bmi(weight,height)
        self.assertEqual(expected_bmi,calculated_bmi,f"BMI计算错误:{calculated_bmi}!={expected_bmi}")

        #比较分类 偏瘦  正常  超重 肥胖
        True_fenlei=self.get_bmi_category(calculated_bmi)
        #
        self.assertEqual(expected_Category,True_fenlei,f"BMI分类错误:{True_fenlei}!={expected_Category}")
        
    #思路是错误的，计算方法上不需要循环，而在传入参数化的时候，可以for循环
    def calculate_bmi(self,weight,height):
        # 厘米转米
        height_m = float(height) / 100  
        calculated_bmi = float(weight) / (height_m ** 2)
        #print('bmi '+float(calculated_bmi))
        return f"{calculated_bmi:.1f}"  #保留1位小数

           
    #根据 BMI返回分类
    def get_bmi_category(self,calculated_bmi):
        calculated_bmi = float(calculated_bmi) 
        if 0<calculated_bmi <18.5:
            return 'underweight'
        elif 18.5<calculated_bmi<25:
            return 'Normal'
        elif 25<calculated_bmi<30:
            return 'overweight'
        else:
            return  'obesity'




if __name__ == '__main__':
    unittest.main()