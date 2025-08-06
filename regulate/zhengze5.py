

import re
import time


'''
re.compile()
用于将正则表达式字符串编译成一个正则表达式对象（Pattern 对象），
这样可以提高正则表达式的执行效率，特别是在需要多次使用同一个正则表达式时。
'''

pattern = re.compile(r'正则表达式模式', flags=0)


# 不使用compile
start = time.time()
for i in range(100000):
    re.match(r'\d+', '123abc')
print(f"不使用compile: {time.time()-start:.4f}秒")

# 使用compile
pattern = re.compile(r'\d+')
start = time.time()
for i in range(100000):
    pattern.match('123abc')
print(f"使用compile: {time.time()-start:.4f}秒")