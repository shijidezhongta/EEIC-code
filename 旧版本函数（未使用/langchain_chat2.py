def get_response(input_str):
    import os 
    import re
    import json
    from langchain.schema import Document
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnableLambda, RunnablePassthrough

    ##-----------------根据电脑情况，可以注释掉，或者更换网络地址-----------------##
    os.environ["http_proxy"] = "http://127.0.0.1:7897"
    os.environ["https_proxy"] = "http://127.0.0.1:7897"
    ##------------------------------------------------------------------------##

    # 设置 OpenAI API 密钥
    os.environ["OPENAI_API_KEY"] = "sk-RGrPu5pMJpoSbb5LBpghjjemoANmpxpGPUH6Q4lt4uT3BlbkFJtzzF0Oxtj20KOCt3v20cqqWimjp7jq7BPO7rUM-F4A"

    # 定义 json 数据库文件路径
    DATABASE_PATH = 'database.json'

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

    def get_default_database():
        return {
            "value_Pmt": 1,
            "value_pv": 1,
            "value_CAES": 1,
            "value_Pump": 1,
            "value_H2": 1,
            "value_bat": 1,
            "value_w": 1,
            "value_CO2": 1,
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
            "ST": None
        }

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
        return extracted_params

    # 获取用户输入的参数
    # user_input = "我想让火力发电单价为2，光伏发电单价为2，风力发电单价为1"
    user_input = input_str
    user_params = extract_model_params(user_input)
    print("用户输入的新参数:", user_params)

    # 加载现有数据库
    database = load_database()

    # 动态生成 documents（从 JSON 数据）
    def generate_documents_from_json(data):
        documents = []
        for param, value in data.items():
            if isinstance(value, list):
                # 对于列表类型的值，生成文档
                document_content = f"{param} 的值为 {value}"
                document_metadata = {"parameter": param, "value": value}
            else:
                # 对于整数类型的值，生成文档
                document_content = f"{param} 的值为 {value}"
                document_metadata = {"parameter": param, "value": value}
            
            document = Document(page_content=document_content, metadata=document_metadata)
            documents.append(document)
        return documents

    # 生成文档
    documents = generate_documents_from_json(database)

    # 动态生成上下文，显示原参数和新参数
    def generate_context(default_documents, user_params):
        """
        生成上下文内容，包含原参数和用户输入的新参数。
        """
        context_lines = []
        for doc in default_documents:
            parameter_name = doc.metadata["parameter"]
            default_value = doc.metadata["value"]
            new_value = user_params.get(parameter_name, "未修改")
            context_lines.append(
                f"参数名称: {parameter_name}, 原参数: {default_value}, 用户输入的新值: {new_value}"
            )
        return "\n".join(context_lines)


    # 生成上下文
    context_content = generate_context(documents, user_params)

    # 更新数据库中的参数
    def update_database(database, user_params):
        for param, new_value in user_params.items():
            if param in database:
                database[param] = new_value
        return database

    # 更新数据库并保存
    updated_database = update_database(database, user_params)
    save_database(updated_database)

    # 输出生成的documents内容
    for doc in documents:
        print(f"参数: {doc.metadata['parameter']}, 默认值: {doc.metadata['value']}")  # 这里显示的是更新前的默认值
        print(f"文档内容: {doc.page_content}")
        print("-" * 50)

    # 模板
    context_template = """
    请根据以下上下文回答问题：

    上下文：
    {context}

    问题：
    {question}
    """

    # 动态填充模板的 prompt
    prompt = ChatPromptTemplate.from_messages([("human", context_template)])

    # 设置 LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # 创建 RAG 链，动态传入上下文和问题
    rag_chain = {
        "context": RunnableLambda(lambda x: context_content),
        "question": RunnablePassthrough(),
    } | prompt | llm

    # 执行 RAG 链并输出响应
    response = rag_chain.invoke("请告诉我关于用户修改参数的信息")
    print("生成的响应:\n", response.content)
    response_content = response.content if isinstance(response.content, str) else str(response.content)
    return response_content