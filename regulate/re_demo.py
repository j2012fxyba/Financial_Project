import re



#
# re.findall()
# re.search()
# re.finditer()
# re.match()
# re.Match()



mt='sfmdfsdfewfsfse'
a=re.search('m.*w',mt)
print(a)

# 非贪婪匹配：.*? 遇到第一个数字就停止


text = "abc123def456ghi"
non_greedy_match = re.search(r'a.*?\d', text)
print(non_greedy_match.group())  # 输出: abc1

import re
text = "abc123def456ghi"

# 贪婪匹配：.* 会匹配到最后一个数字
greedy_match = re.search(r'a.*\d', text)
print(greedy_match.group())  # 输出: abc123def456