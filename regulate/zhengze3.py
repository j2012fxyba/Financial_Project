import re

s='testing search'

reg=r'[A-Za-z]+\b'    #    + 表示匹配前面的模式 1次或多次（至少一个字母）

str=re.search(reg,s)
print(str)

while str!=None:
    start=str.start()   #新字符串起始位置
    end=str.end()      #新字符串结束位置
    print(s[start:end],end=' ')   
    s=s[end:]   #从结束位置开始匹配，也就是剩余字符串search ，保存在s1里面
    str=re.search(reg,s)    #重新搜索s1

    #str = None，循环条件 str != None 不成立，退出循环。

# r'\w+@(\w+\.)+\w+'   username@sub.domain.com
 

 
# 输入	匹配结果
# user@example.com	✅ 匹配
# john.doe@gmail.com	❌ 不匹配（因为 . 不在 \w 中）
# admin@sub.domain.org	✅ 匹配
