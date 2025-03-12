import json  

# 定义ConnectDB类，用于与本地JSON文件进行交互
class ConnectDB:
    def __init__(self):
        # 初始化函数，设置存储聊天数据的JSON文件路径
        self.chat_db_path = "data.json"  # 设定JSON文件路径

    def get_chat_data(self):
        """
        读取JSON文件并返回聊天数据。
        :return: 聊天数据(Python对象,通常是列表或字典)
        """
        # 打开JSON文件并加载数据
        with open(self.chat_db_path, "r") as f:
            chat_db = json.load(f)  # 使用json.load()读取文件内容并解析为Python对象

        return chat_db  # 返回聊天数据

    def get_chat_title_list(self):
        """
        获取所有聊天记录的标题。
        :return: 包含所有标题的列表
        """
        chat_list = []  # 用于存储标题的列表
        chat_db = self.get_chat_data()  # 获取所有聊天数据
        
        # 遍历所有聊天记录，提取并添加标题到列表中
        for chat in chat_db:
            title = chat.get("title")  # 获取每条记录中的"title"字段
            chat_list.append(title)  # 将标题添加到列表

        return chat_list  # 返回标题列表

    def save_chat_data(self, new_chat_data):
        """
        将新的聊天数据保存到JSON文件中。
        :param new_chat_data: 新的聊天数据(Python对象)
        """
        # 打开JSON文件，并将新的数据写入文件
        with open(self.chat_db_path, "w") as f:
            f.write(json.dumps(new_chat_data))  # 将Python对象转为JSON字符串并写入文件

    def delete_all_data(self):
        """
        删除所有聊天记录。
        """
        chat_db = self.get_chat_data()  # 获取当前的聊天数据
        chat_db.clear()  # 清空聊天数据
        self.save_chat_data(chat_db)  # 保存空的数据到JSON文件，达到删除所有记录的目的

    def delete_chat_data(self, index):
        """
        删除指定索引的聊天记录。
        :param index: 要删除记录的索引
        """
        # 读取JSON文件内容
        with open(self.chat_db_path, "r") as f:
            chat_db = json.load(f)  # 加载聊天数据

        # 使用pop()方法删除指定索引的聊天记录
        chat_db.pop(index)

        # 保存删除后的数据回JSON文件
        self.save_chat_data(chat_db)
