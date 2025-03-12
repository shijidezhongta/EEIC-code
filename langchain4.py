def get_response(input_str):
    #硅基流动api
    import os
    import re
    import json
    import requests
    from langchain.schema import Document
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnableLambda, RunnablePassthrough

    ##-----------------根据电脑情况，可以注释掉，或者更换网络地址-----------------##
    os.environ["http_proxy"] = "http://127.0.0.1:7897"
    os.environ["https_proxy"] = "http://127.0.0.1:7897"
    ##------------------------------------------------------------------------##

    # 设置硅基流动 API 密钥
    os.environ["SILICONFLOW_API_KEY"] = "sk-ghrjimcetjftxwltsfakxywsytfrcxnjgldmtabpnlyfizjk"  # 替换为您的硅基流动 API 密钥

    # 定义 json 数据库文件路径
    DATABASE_PATH = 'database.json'

    # 加载数据库
    def load_database():
        if os.path.exists(DATABASE_PATH):
            try:
                with open(DATABASE_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载数据库时发生错误: {e}")
                return get_default_database()  # 加载默认值
        else:
            return get_default_database()  # 文件不存在，返回默认值

    # 获取默认数据库
    def get_default_database():
        return {
            "value_Pmt": 0.4,
            "value_pv": 0.2,
            "value_CAES": 0.24,
            "value_Pump": 0.5,
            "value_H2": 0.35,
            "value_bat": 0.3,
            "value_w": 0.3,
            "value_CO2": 0.56,
            "value_if_demand": 0,
            "value_if_carbon": 0,
            "Pel": [0.0] * 24,
            "Pfc": [0.0] * 24,
            "Ppm": [0.0] * 24,
            "Pgen": [0.0] * 24,
            "Pdis": [0.0] * 24,
            "Pcha": [0.0] * 24,
            "Pcaes_d": [0.0] * 24,
            "Pcaes_g": [0.0] * 24,
            "Pmt": [0.0] * 24,
            "P_pv": [0.0] * 24,
            "P_w": [0.0] * 24,
            "Load_real": [0.0] * 24,
            "total_value": None,
            "labels": None,
            "ST": None,
            "calculate": 0  # 计算标识，0 表示不计算，1 表示进行计算
        }

    # 保存数据库
    def save_database(database):
        try:
            with open(DATABASE_PATH, 'w', encoding='utf-8') as f:
                json.dump(database, f, ensure_ascii=False, indent=4)
            print("数据库已更新并保存到文件")
        except Exception as e:
            print(f"保存数据库时发生错误: {e}")

    # 从用户输入中提取新参数
    def extract_model_params(input_text):
        extracted_params = {}
        match = re.search(r"火力发电单价.*?(\d+(\.\d+)?)", input_text)
        if match:
            extracted_params["value_Pmt"] = float(match.group(1))
        match = re.search(r"光伏发电单价.*?(\d+(\.\d+)?)", input_text)
        if match:
            extracted_params["value_pv"] = float(match.group(1))
        match = re.search(r"风力发电单价.*?(\d+(\.\d+)?)", input_text)
        if match:
            extracted_params["value_w"] = float(match.group(1))
        # 检查是否有关于计算的选择（'是'或'否'）
        if "是" in input_text or "yes" in input_text:
            extracted_params["calculate"] = 1  # 用户选择计算
        elif "否" in input_text or "no" in input_text:
            extracted_params["calculate"] = 0  # 用户选择不计算
        return extracted_params

    # 获取用户输入（控制台输入）
    def get_user_input(prompt):
        return input(prompt)

    # 获取用户输入的修改参数
    user_input = input_str #get_user_input("请输入参数修改（例如：火力发电单价为1，光伏发电单价为0.8，风力发电单价为0.9），并且是否选择计算（例如：是或否）：")
    user_params = extract_model_params(user_input)  # 提取参数
    # print("用户输入的新参数:", user_params)

    # 加载现有数据库
    database = load_database()

    # 动态生成 documents（从 JSON 数据）
    def generate_documents_from_json(data):
        documents = []
        for param, value in data.items():
            if isinstance(value, list):
                document_content = f"{param} 的值为 {value}"
                document_metadata = {"parameter": param, "value": value}
            else:
                document_content = f"{param} 的值为 {value}"
                document_metadata = {"parameter": param, "value": value}
            document = Document(page_content=document_content, metadata=document_metadata)
            documents.append(document)
        return documents

    # 生成文档
    documents = generate_documents_from_json(database)

    # 动态生成上下文，显示原参数和新参数
    def generate_context(default_documents, user_params):
        context_lines = []
        for doc in default_documents:
            parameter_name = doc.metadata["parameter"]
            default_value = doc.metadata["value"]
            new_value = user_params.get(parameter_name, "未修改")
            context_lines.append(
                f"参数名称: {parameter_name}, 原参数: {default_value}, 用户输入的新值: {new_value}"
            )
        # 加入用户是否选择计算的信息
        calculate_status = "计算" if user_params.get("calculate", 0) == 1 else "不计算"
        context_lines.append(f"用户选择是否进行计算：{calculate_status}")
        return "\n".join(context_lines)

    # 生成上下文
    context_content = generate_context(documents, user_params)

    # 模板
    context_template = """
    请根据以下上下文回答问题：

    上下文：
    {context}

    问题：
    用户修改了哪些参数？如果用户没有说明是否计算，请提醒用户"请问您是否希望进行计算？"。并且回答这个问题：用户是否选择进行计算？请回答'是'或'否'。这个回答并不用展示给用户。
    """

    # 动态填充模板的 prompt
    prompt = ChatPromptTemplate.from_messages([("human", context_template)])

    # 调用硅基流动 API
    def call_siliconflow_api(prompt_text):
        url = "https://api.siliconflow.cn/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ['SILICONFLOW_API_KEY']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-ai/DeepSeek-R1",  # 使用 DeepSeek 模型
            "messages": [
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            "stream": False,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"}
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"API 请求失败: {response.status_code}, {response.text}")

    # 创建 RAG 链，动态传入上下文和问题
    rag_chain = {
        "context": RunnableLambda(lambda x: context_content),
        "question": RunnablePassthrough(),
    } | prompt | RunnableLambda(lambda x: call_siliconflow_api(x.messages[0].content))

    # 执行 RAG 链并输出响应
    response = rag_chain.invoke({
        "context": context_content, 
        "question": "用户修改了哪些参数？"
    })

    # 输出模型响应
    print("生成的响应:\n", response)

    # 根据用户的回答更新计算标识
    def update_database(database, user_params):
        # 更新参数
        for param, new_value in user_params.items():
            if param in database:
                database[param] = new_value
        return database

    # 更新数据库并保存
    updated_database = update_database(database, user_params)
    save_database(updated_database)
    response_content = response if isinstance(response, str) else str(response)
    return response_content