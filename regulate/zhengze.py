import re

''' python 的正则表达式要先进入re模块，正则表达式以 r 作为引导 
如果搜索到返回值，如果无搜索到，则默认返回None
r 表示使用原始字符串 r'C:\Users\Example\file.txt' ， 这样python就不会以为反斜杠为转义字符
windows 使用的是反斜杠 ，linux使用的是正斜杠
'''

reg=r'\w+'     #匹配包括下划线在内的单词字符，等价于 '[a-zA-Z0-9_]'
str='Python is easy'
ma=re.search(reg,str)
print(ma)     # 结果返回python  +代表匹配前面一个单词1次或多次 python后面是空格 因此就一次


reg=r'\w+'     #匹配包括下划线在内的单词字符，等价于 '[a-zA-Z0-9_]'
str='PythonPython is easy'
ma=re.search(reg,str)
print(ma)    #返回 span=(0, 12), match='PythonPython'  

reg=r'\d+'    #匹配连续多个数  \d=[0~9]    \w=[A-Z  a-z 0-9]
m1=re.search(reg,'abc1234cd')
print(m1)   #返回1234


reg=r'\d+'
mt='abc12mn34'
print(mt)   # 返回12  因为 34 数字不连续


reg=r'\d+'
str='ab12cd234'
val=re.search(reg,str)
print(val)    #返回第一个连续的字符  12
print(val.start(),val.end())   #搜索匹配的起止位置 c是第4个字符不是数字，因此结束搜索




reg1=r'\d'    #匹配0~9之间的一个数值   返回1 
m2=re.search(reg1,'abc1234cde')
print(m2)
 

reg2=r'b\d+'    # 第一个字符要匹配b开始， \d+  匹配+前面的连续数值 123
m3=re.search(reg2,'a123b123c123d1234b11')
print(m3)   #返回 span=(4, 8), match='b123'


reg3=r'ab*'   #   *重复前面一个匹配字符0次或多次  即 *前面的b可以不出现
m4=re.search(reg3,'acabc')
print(m4)  #返回   span=(0, 1), match='a'


reg4=r'ab+'       #   ab+ abb abbb   a开始 b的重复一次以上
m5=re.search(reg4,'acabc')
print(m5)   #  span=(2, 4), match='ab'


reg=r'^ab'    #匹配开头位置的ab,因为cab开头并不是ab 所以搜索结果返回None
mt='cabcab'
mr=re.search(reg,mt)
print(mr)   #返回空

reg5=r'ab?'    # 从a开始匹配  b 可以出现0次或者1次，因为?前面的字符匹配1次或0次就是b
m6=re.search(reg5,'acbbcabc')
print(m6)     #返回结果 a



reg5=r'ab?'    # 从a开始匹配  b 可以出现0次或者1次，因为?前面的字符匹配1次或0次就是b
m6=re.search(reg5,'abbcabc')
print(m6)     #返回结果 ab


reg=r'ab$'
str='abcaba'  # 找到字符串中结尾位置的ab，不是第一个abc
mm=re.search(reg,str)
print(mm)


reg=r'ab$'
str='abcab'  # 找到字符串中结尾位置的ab，不是第一个abc
mm=re.search(reg,str)
print(mm)   #返回ab



#使用() 可以把()看作一个整体，经常与 +  * ？ 连用 表对对（）部分的重复
reg=r'(ab)+'     #  匹配多个字符串ab
str='ababcdab'
m6=re.search(reg,str)
print(m6)    # span=(0, 4), match='abab'


reg=r'\d(ab)+\d'   #\d 代表开头数字  （ab）+代表重复  \d结尾数字
str='x123abababab4c5ab'
y=re.search(reg,str)
print(y)    #返回 match='3abababab4'


x='axbxy'
reg6=r'a.b'    # 匹配 a 和 b 中间任意字符   axb
m7=re.search(reg6,x)
print(m7)


s='xaabababy'
m8=re.search(r'ab|ba',s)    #把字符串分割左右2边  2边任意一个匹配都可以
print(m8)


e=r"PYABC"
ae=re.search(r'[^PY]{0,10}',e)   #  ^匹配字符串开头
print(ae)

'''


+ 匹配前面一个字符一次或者多次
$ 匹配字符结尾
. 表示任何单个字符
[^abc] 表示 非 a /b /c 的单个字符
\r 回车  return - go back, re-enter
\n 换行  newline - line , line feed
 \t 制表符   \\  反斜杠
 \b  单词结尾
 \d 匹配0-9之间的一个数值
 [] ascii 中连续的一组  例如[0-9]   [A-Z]
 ? 重复前面一个字符0次或者1 次
'''

#匹配英文句子中的所有单词

s='i am testing search funtion'
reg11='r[A-Za-z]+\b'    # 前面可以是任意字符，\b表示单词的结尾
m=re.search(reg11,s)
print(m)


reg=r'a\sb'        #\s匹配任意空白字符， 等价于 '[\r\n\x20\t\f\v]' 
str='1a ba \tbxy'
m=re.search(reg,str)
print(m)      #结果返回a b

reg=r'a\sb'
str='1aba\tbxy'
ma=re.search(reg,str)
print(ma)    #返回 a\tb


reg=r'^ab'  # 匹配字符串开头位置 ^
str='cabcab'
mk=re.search(reg,str)
print(mk)    #结果返回为None  因为 cab开头并不是ab



 # 字符^ 出现在[]第一个位置，代表取反。 例如： [^ab0-9]表示不是a、b 也不是0-9的数字
reg=r'x[^ab0-9]y'    
ee=str='xayx2yxcy'    #xay  x2y  xcy 只能是xcy
re.search(reg,ee)
print(ee)

'''

[]中的字符是任意一个，如果字符是ASCII编码中连续一组，可以用'-'符号连接
例如[0-9]表示0-9的其中一个数字，[A-Z]的其中一个大写字符，[0-9A-Z]表示0-9的
其中一个数字或者A-Z的其中一个大写字符'''

reg=r'x[0-9]y'
str='xyz2y'
m11=re.search(reg,str)
print(m11)     #返回x2y   从x开始 匹配 0-9 之间任意数字，y结束


#  匹配单词结尾  包含单词尾部空格字符
reg=r'\b'     
str='the car is black'
uo=re.search(reg,str)
print(uo)     #span=(0, 0), match=''


reg=r'car\b'      #因为car后面是空格，因此只展示car
str='the car is black'
uo=re.search(reg,str)
print(uo)     #span=(0, 0), match=car


reg=r'er\b'
str='Her Paper'
hg=re.search(reg,str)
print(hg)    #span=(1, 3), match='er'

reg=r'er\b'
str='His Paper'
hgr=re.search(reg,str)
print(hgr)   #span=(7, 9), match='er'


#特殊字符 \  例如：\n  \r   \t   \\分别表示回车 换行  制表符 与反斜杠本身

reg=r'a\nb?'    #代表字符串本身 对于长字符串可以截取
str='ca\nbcabc'
gh=re.search(reg,str)
print(gh)    #结果返回 a\nb




str='i am a testing search function'
reg=r'[A-Za-z]+\b'
m=re.search(reg,str)
print(m)



str='i am a testing search function'
reg=r'[A-Za-z]+\b'
m=re.search(reg,str)
while m !=None:
    start=m.start()
    end=m.end()
    print(str[start:end])
    str=str[end:]
    m=re.search(reg,str)#将原字符串起止位置标出 形成新的str字符串，开始从头查找，遍历输出

  


