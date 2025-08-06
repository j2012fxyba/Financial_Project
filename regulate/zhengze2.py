
import re
import urllib

#当http 连接中‘’ 之间出现不规则的情况，reg正则表达式需要调整搜索表达式
#比方 出现空格或者单''引号的情况
#  \s

html='''
<div><img width="600" src =  "/static/20250123.png"></div>
<div><img width="600" src='/static/download.png'></div>
'''

reg=r'<img.+src\s*=\s*'  # \s 代表src 后面的空格 ，*代表重复，因为有可能空格是多个， 在= 前后各出现一次
a=re.search(reg,html)
print(a)   #返回 '<img width="600" src =  "'> 然后从"后面开始截取

#另外如果src=后面是单引号'' 则怎么匹配呢

'''
表达式的结构如下：
r""：表示原始字符串（raw string），避免转义字符的问题。
[\",\']：匹配一个双引号 " 或单引号 '。
.+：匹配一个或多个任意字符（除换行符外）。
[\",\']：匹配一个双引号 " 或单引号 '。
r'\w+@(\w+\.)+\w+'： 邮箱验证的复杂性较高，建议优先使用现成的库。 Python 的 email-validator 库更可靠：
r'\d+-\d+'   由两个数字序列组成，中间用连字符 - 连接的字符串
r'\w+\b'  匹配由字母、数字、下划线组成的单词，直到单词边界
r'\w+\s'  匹配单词+后面的空格
'''

html1='''
<div><img width="600" src='/static/download.png'>
</div>'''

reg=r'<img.+?src=(["\'])(.+?)\1'
danyinhao=re.search(reg,html1)
print(danyinhao)

'''
python中使用字符串表示正则表达式   reg='https:\/\/' 
javascript 使用 // 包裹正则表达式  reg=/https:\/\// 
windows 使用的是反斜杠 \  ，linux使用的是正斜杠  /
跨平台路径 拼接时 ，不能使用硬编码，否则可能导致路径不一致
os.path 或pathlib 模块处理路径，确保跨平台的兼容性，避免硬编码路径分隔符，使用原始字符串或双反斜杠处理windows路径

'''
str='https://'
reg='https:\/\/'   #\代表转义匹配/   连续用2次  开头的/ /   代表括起来
a=re.search(reg,str)
print(a)
