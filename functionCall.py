from openai import OpenAI
import json
from datetime import datetime


# 1. 外部工具函数调用定义
def get_current_time():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return f"现在是：{formatted_datetime}"

# 2. 创建tools数组，传递给LLM的知识库之一
functions=[
    {
       "type": "function",
       "function": {
           "name": "get_current_time",
           "description": "当你想知道现在的时间时非常有用",
       }
    }
]

 # 步骤3:发起 function calling 请求
client = OpenAI(api_key="sk-rbqagklfjzbcqgibwpxahpvroizcutlckfbxzjkewoycqlvs", base_url="https://api.siliconflow.cn/v1")

def chat_completion_request(messages, tools):
    print(f"正在像LLM发起API请求...")
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=messages,
        tools=tools
    )
    print("返回对象：")
    print(completion.choices[0].message.model_dump_json())
    print("\n")
    return completion

def main_loop():
    print("欢迎使用智能助手！输入内容开始对话（输入 exit 退出）")
    while True:
        try:
            # 获取用户输入
            user_input = input("\n用户输入: ")
            if user_input.lower() in ("exit", "quit"):
                break

            # 创建messages数组
            messages = [
                {"role": "system", "content": "",},
                {"role": "user", "content": user_input}
            ]

            completion = chat_completion_request(messages, functions)
            if not completion:
                continue

            if completion.choices[0].message.tool_calls:
                function_name = completion.choices[0].message.tool_calls[0].function.name
                arguments_string = completion.choices[0].message.tool_calls[0].function.arguments

                arguments = json.loads(arguments_string)
                # 创建一个函数映射表
                function_mapper = {
                    "get_current_time": get_current_time
                }

                # 获取函数实体
                function = function_mapper[function_name]
                if arguments == {}:
                    function_output = function()
                else:
                    function_output = function(arguments)
                print(f"AI:{function_output}\n")
            else:
                print(f"AI:{completion.choices[0].message.content}\n")
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main_loop()

