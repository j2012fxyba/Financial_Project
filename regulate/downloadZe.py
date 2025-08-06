

import re



#  匹配单词结尾  包含单词尾部空格字符
reg=r'\b'     
str='the car is black'
uo=re.search(reg,str)
print(uo)     #返回kongge

reg=r'er\b'
str='Her Paper'
hg=re.search(reg,str)
print(hg)

reg=r'er\b'
str='His Paper'
hgr=re.search(reg,str)
print(hgr)


reg=r'\w+'     #匹配包括下划线在内的单词字符，等价于 '[a-zA-Z0-9_]'
str='PythonPython is easy'
ma=re.search(reg,str)
print(ma)

reg=r'ab$'
str='abcab'  # 找到字符串中结尾位置的ab，不是第一个abc
mm=re.search(reg,str)
print(mm)


reg=r'(ab)+'     #  匹配多个字符串ab
str='ababcdab'
m6=re.search(reg,str)
print(m6)


reg=r'\d(ab)+\d'   #\d 代表开头数字  （ab）+代表重复  \d结尾数字
str='x123abababab4c5ab'
y=re.search(reg,str)
print(y)  


s='i am testing search funtion'
reg11=r'[A-Za-z]+\b'    # 前面可以是任意字符，\b表示单词的结尾
m=re.search(reg11,s) 
print(m)    #返回  i



str='i am a testing search function'
reg=r'[A-Za-z]+\b'
m=re.search(reg,str)
while m !=None:
    start=m.start()  #将i  字符位置找出
    end=m.end()      #将n  字符位置超出
    print(str[start:end])   #形成新的字符串数组str 打印出来
    str=str[end:]  #然后从后往前找
    m=re.search(reg,str)   #重新匹配心的字符串数据