import openai
import os
import json

# 初始化 OpenAI 客户端
client = openai.OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 国内稳定访问
    api_key=os.getenv("DASHSCOPE_API_KEY")           # 替换为你的 API 密钥
)

# message_3=[
#     {"role": "user", "content": "软件测试开发工程师转LLM的技术路线"},
#     {"role": "user", "content": "解释一下量子计算机的基本原理"},
#     {"role": "user", "content": "LLM学习路径和开发岗位要求"},
# ]

# questions=["软件测试开发工程师转LLM的技术路线","解释一下量子计算机的基本原理","LLM学习路径和开发岗位要求"]

#定义生成文本的函数
def generate_text():
    for question in questions:

        response = client.chat.completions.create(
        
        model="deepseek-r1",  # 使用最新版本的 GPT 模型
        #等于是 question 遍历一次，调一次循环
        messages=[{'role':'user','content':question}],
                  
        max_tokens=500,
        temperature=0.7,  #创造性 平衡 0--2之间
        #stream=True  #流式输出  格式输出冲突，建议优化修改
    )
        
    #标准输出 方式
    #{}引用 定义questions  字段
    print(f'\n请回答：{questions}')  
    print('回答如下',response.choices[0].message.content)

    #使用函数functions调用 推理
def get_reasoning_answer(question):

        response=client.chat.completions.create(
            #model="chatgpt-4o-latest",
            #model="o3-mini-2025-01-31",
            model='qwen-plus',
            
            messages=[{'role':"user","content":f"{question} 请分步骤解释"}],
            #用户发出的请求 functions 
            functions=[{
                "name":'format_response',
                
                'parameters':{
                    "type":'object',
                    "properties":{
                        "reasoning":{"type":"string"},
                        "answer":{"type":"string"}}
                }
            }],
            #openAI 调用AI模型后，返回的function_call响应 ，然后返回原始的 json 
        function_call={"name":"format_response"}
        )
    
        args=json.loads(response.choices[0].message.function_call.arguments)
        #从 arguments 字典获取的 reasoning answer   
        #在 functions 参数中定义了规范，要求AI返回包含这2个字段的json
        return args['reasoning'],args['answer']
    

generate_text()
questions=["软件测试开发工程师转LLM的技术路线","解释一下量子计算机的基本原理","LLM学习路径和开发岗位要求"]
for ques in questions:
     
    get_reasoning_answer(ques)



