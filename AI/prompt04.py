import openai
import os

# 初始化 OpenAI 客户端
client = openai.OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 国内稳定访问
    api_key=os.getenv("DASHSCOPE_API_KEY")           # 替换为你的 API 密钥
)


#引导推理的模型

message=[
     {"role": "user", "content": "又到了周日，小明像以往一样去爷爷奶奶家玩，小明于早上八点整步行出发，已知小明每分钟行走50米，"\
"走了12分钟后，小明的父亲发现小明忘记带作业了，于是便骑车去追小明，已知小明的爸爸每分钟骑行200米，"\
"等到追上小明后，爸爸决定骑车带上小明，已知小明坐自行车的路程是走路路程的5倍，"\
#目的
"小明什么时候到爷爷家？"\
#任务步骤

"1. 先计算小明被爸爸追上时的时间和移动的距离。"\
"2. 再计算小明去爷爷家剩余的距离和需要的时间。"\
"3. 最后计算小明到爷爷家的时间。"\
        }
]
# 定义生成文本的函数
def generate_text():
    response = client.chat.completions.create(
        #qwen-long  qwen-turbo
        model="qwen-plus",  # 使用最新版本的 GPT 模型
        messages=message,
        #max_tokens=50
    )
    print(response.choices[0].message.content)

generate_text()

