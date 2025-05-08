from openai import OpenAI

# 硅基流动key,解决deepseek key 账户没钱问题
client = OpenAI(api_key="sk-rbqagklfjzbcqgibwpxahpvroizcutlckfbxzjkewoycqlvs", base_url="https://api.siliconflow.cn/v1")

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "你是？"},
    ],
    stream=False
)

print(response.choices[0].message.content)
