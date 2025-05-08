# 参考https://api-docs.deepseek.com/guides/function_calling
from openai import OpenAI
import random

client = OpenAI(api_key="sk-rbqagklfjzbcqgibwpxahpvroizcutlckfbxzjkewoycqlvs", base_url="https://api.siliconflow.cn/v1")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取一个位置的天气，用户应该先提供一个位置",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

def get_weather():
    weather_list = ["天晴", "多云", "下雨", "下雪", "阴天"]
    return random.choice(weather_list)

# 1. 用户询问广州的天气如何？
messages = [{"role": "user", "content": "广州的天气如何?"}]
message = send_messages(messages)
print(f"User>\t {messages[0]['content']}")

print(f"message>\t {message}")
# 2. 模型需要调用tool工具函数
tool = message.tool_calls[0]
messages.append(message)

# 3. 调用函数，并将结果返回给模型
function_mapper = {
    "get_weather": get_weather
}
print(f"tool>\t {tool}")
messages.append({"role": "tool", "tool_call_id": tool.id, "content":function_mapper[tool.function.name]() })
# 4. 模型根据函数返回结果，生成最终回复
message = send_messages(messages)
print(f"Model>\t {message.content}")