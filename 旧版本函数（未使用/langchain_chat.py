def get_response(input_str):
    import os
    import re
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OpenAIEmbeddings
    from langchain.schema import Document
    from langchain_core.runnables import RunnableLambda, RunnablePassthrough
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate

    ##-----------------根据电脑情况，可以注释掉，或者更换网络地址-----------------##
    os.environ["http_proxy"] = "http://127.0.0.1:7897"
    os.environ["https_proxy"] = "http://127.0.0.1:7897"
    ##------------------------------------------------------------------------##

    # 设置 OpenAI API 密钥
    os.environ["OPENAI_API_KEY"] = "sk-RGrPu5pMJpoSbb5LBpghjjemoANmpxpGPUH6Q4lt4uT3BlbkFJtzzF0Oxtj20KOCt3v20cqqWimjp7jq7BPO7rUM-F4A"

    # 数据库中的原始参数（保持不变）
    documents = [
        Document(page_content="发电机的输出功率应设置为output_power=500", metadata={"parameter": "output_power", "default_value": 500}),
        Document(page_content="发电机的效率参数应设置为efficiency=90", metadata={"parameter": "efficiency", "default_value": 90}),
        Document(page_content="冷却系统的温度参数应设置为temperature=40", metadata={"parameter": "temperature", "default_value": 40}),
    ]

    # 初始化嵌入和向量存储
    embedding = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embedding)

    # 向量检索
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})

    # 用户输入
    user_input = input_str
    # user_input = "我想让发电机的输出功率为400kW，效率为95%"

    # 提取用户输入的新参数（不更新数据库中的默认值）
    def extract_model_params(input_text):
        """
        从用户输入中提取新参数。
        """
        extracted_params = {}
        for doc in documents:
            parameter_name = doc.metadata["parameter"]
            # 根据数据库中的参数名称匹配用户输入中的值
            if parameter_name == "output_power":
                match = re.search(r"输出功率.*?(\d+)\s*kW", input_text)
                if match:
                    extracted_params[parameter_name] = int(match.group(1))
            elif parameter_name == "efficiency":
                match = re.search(r"效率.*?(\d+)", input_text)
                if match:
                    extracted_params[parameter_name] = int(match.group(1))
            elif parameter_name == "temperature":
                match = re.search(r"温度.*?(\d+)", input_text)
                if match:
                    extracted_params[parameter_name] = int(match.group(1))
        return extracted_params

    # 获取用户输入的参数
    user_params = extract_model_params(user_input)
    print("用户输入的新参数:", user_params)

    # 动态生成上下文，显示原参数和新参数
    def generate_context(default_documents, user_params):
        """
        生成上下文内容，包含原参数和用户输入的新参数。
        """
        context_lines = []
        for doc in default_documents:
            parameter_name = doc.metadata["parameter"]
            default_value = doc.metadata["default_value"]
            new_value = user_params.get(parameter_name, "未修改")
            context_lines.append(
                f"参数名称: {parameter_name}, 默认值: {default_value}, 用户输入的新值: {new_value}"
            )
        return "\n".join(context_lines)

    # 生成上下文
    context_content = generate_context(documents, user_params)
    print("生成的上下文内容:\n", context_content)

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
    # choice_list = [choice.get("text").lstrip("\n") for choice in response.content]
    response_content = response.content if isinstance(response.content, str) else str(response.content)
    return response_content
