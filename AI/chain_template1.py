from langchain_core.prompts import ChatPromptTemplate
 
# 定义模板
template_content="""请告诉我{date}在{location}的天气情况。"""

 
# 使用模板
 
prompt_template = ChatPromptTemplate.from_template(template_content)
 
# 打印原始模板
print("原始模板:", prompt_template.messages[0].prompt)
 
date = '今天'
location = '北京'
 
# 注意：这里修正了参数名为 location
user_content=prompt_template.format_messages(
    date=date,
    location=location  # 修正了拼写错误：从 local 改为 location
)

 
# 打印格式化后的模板
print("格式化后的模板:", prompt_template.messages[0].prompt)



# 虚构的天气数据获取函数
def get_weather_data(date, location):
    # 这里应该调用一个天气API或访问一个天气数据库来获取实际数据
    # 但为了演示，我们返回一个虚构的天气对象
    return WeatherData(
        date=date,
        location=location,
        description="阴转晴",
        temperature_high="8℃",
        temperature_low="0℃",
        # 添加其他天气信息，如风力、湿度等（如果需要）
    )
 

class WeatherData:
    def __init__(self, date, location, description, temperature_high, temperature_low, **kwargs):
        self.date = date
        self.location = location
        self.description = description
        self.temperature_high = temperature_high
        self.temperature_low = temperature_low
        # 存储其他天气信息（如果需要）
 
    # 可以添加一个方法来格式化天气信息为字符串（可选）
    def __str__(self):
        return (f"{self.date}在{self.location}的天气情况：{self.description}，最高气温{self.temperature_high}，最低气温{self.temperature_low}。"
                # 添加其他天气信息的格式化字符串（如果需要）
                )
    
# 获取天气数据（这里使用虚构的函数）
weather_data = get_weather_data(date, location)
formatted_prompt = prompt_template.messages[0].prompt  # 获取格式化后的模板字符串
print("格式化后的模板及天气数据:", formatted_prompt.strip() + " " + str(weather_data))
#通过某种方式获取实际的天气数据，并将其与格式化后的模板结合起来。这通常涉及到调用一个天气API，或者使用某个能够获取天气数据的库    