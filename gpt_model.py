from openai import OpenAI
import openai
import os
# Set the proxy URL and port
# API_BASE = "https://api.lingyiwanwu.com/v1"
API_KEY = "sk-proj-VU0oDU3tBYzJQE5up5BYT3BlbkFJdBjqgbDy0PRd5BlctAGY"

os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ["HTTP_PROXY"] = 'http://127.0.0.1:7890'
def send_openai_request(user_input):
    """
    与 OpenAI API 交互的函数，接受用户输入并返回生成的回答。
    
    参数:
        user_input (str): 用户的提问内容。
        
    返回:
        tuple: (用户提问内容, 生成的回答)
    """
    # client = OpenAI(api_key="sk-proj-VU0oDU3tBYzJQE5up5BYT3BlbkFJdBjqgbDy0PRd5BlctAGY")
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=API_KEY,
    # base_url=API_BASE
    )
    try:
        # 创建对话请求
        # completion = client.chat.completions.create(
        #         model="yi-34b-chat-0205",
        #         messages=[{"role": "user", "content": "Hi, who are you?"}]
        #     )
        response = client.chat.completions.create(
            model="gpt-3.5",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that provides insights on energy storage optimization. Use technical terms accurately and ensure responses are concise."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.3,  # 设置随机性
            max_tokens=150,   # 设置回答的最大 token 数
            top_p=1           # 设置 nucleus 采样参数
        )

        # 提取响应文本
        answer = response['choices'][0]['message']['content']
        return user_input, answer

    # except openai.error.APIConnectionError as e:
    #     print(f"API Connection Error: {e}")
    #     return user_input, "Unable to connect to OpenAI API."
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return user_input, "An error occurred while fetching the response."
    
user_input = "你好"
question, answer = send_openai_request(user_input)
print(f"User: {question}\nAI: {answer}")
