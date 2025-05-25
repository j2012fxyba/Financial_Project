import unittest
from parameterized import parameterized


#参数化 parameterized
class TestBMI(unittest.TestCase):
    @parameterized.expand([
        ("160", "45", "17.6", "underweight"),
        ("168", "70", "24.8", "Normal"),
        ("181", "89", "27.2", "overweight"),
        ("178", "100", "31.6", "obesity")
    ])

    #unittest 框架自动获取 test_打头的测试案例
    def test_bmi_category(self, height, weight, expected_bmi, expected_category):
        """测试BMI分类是否匹配参数化输入"""
        # 计算BMI值
        height_m = float(height) / 100
        bmi_val = round(float(weight) / (height_m ** 2), 1)
        print(bmi_val)
        self.assertEqual(expected_bmi,expected_bmi,f"计算不正确：{bmi_val}!={expected_bmi}")
        # 获取实际分类
        actual_category = self.get_bmi_category(bmi_val)

        
        # 关键断言：实际分类 vs 参数化预期分类
        self.assertEqual(actual_category, expected_category,
                       f"分类不匹配: 计算值={actual_category}, 实际='{actual_category}', 预期='{expected_category}'")

    def get_bmi_category(self, bmi_val):
        """根据BMI值返回分类（固定逻辑）"""
        if bmi_val < 18.5:
            return "underweight"  # 这里返回固定字符串
        elif 18.5 <= bmi_val < 25:
            return "Normal"
        elif 25 <= bmi_val < 30:
            return "overweight"
        else:
            return "obesity"

if __name__ == '__main__':
     #verbosity=2 表示启用 最高级别的详细输出  默认为0 显示最终结果 OK  1 表示成功 失败 异常 
    unittest.main(verbosity=2)  