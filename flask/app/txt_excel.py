import pandas as pd

# 指定TXT文件路径
txt_file_path = '\\flask\\flask_templates\\data_bmi.txt'

# 指定XLSX文件路径
xlsx_file_path = 'flask\\flask_templates\\bmi_data.xlsx'

# 读取TXT文件，假设文件是以制表符分隔的
# 如果是以逗号分隔的，可以将sep参数改为','
df = pd.read_csv(txt_file_path, sep='\t')

# 将DataFrame写入XLSX文件
df.to_excel(xlsx_file_path, index=False)

print(f'TXT文件已转换为XLSX文件，并保存到：{xlsx_file_path}')
