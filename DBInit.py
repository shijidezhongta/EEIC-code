import json
import numpy as np

def database_init():
    # 打开文件并清空内容
    with open("database.json", "w") as json_file:
        json.dump({}, json_file, indent=4)  # 使用空字典清空文件

    # 数据初始化
    data = {
        "value_Pmt": 0.3,         # 假设为火电成本系数
        "value_pv": 0.24,         # 光伏成本系数
        "value_CAES": 0.4,        # 压缩空气储能成本系数
        "value_Pump": 0.5,        # 抽水蓄能成本系数
        "value_H2": 0.35,         # 氢储能成本系数
        "value_bat": 0.25,        # 电池储能成本系数
        "value_w": 0.25,          # 风电成本系数
        "value_CO2": 0.65,        # 碳排放成本系数
        "value_if_demand": 0,     # 是否考虑需求标志
        "value_if_carbon": 0,     # 是否考虑碳排放标志
        "Pel": np.zeros(24).tolist(),              # 未调整，仍为1×24（假设为总电力）
        "Pfc": np.zeros((3, 24)).tolist(),         # 火电出力，3个微电网，3×24
        "Ppm": np.zeros(24).tolist(),              # 未调整，仍为1×24（假设为抽水蓄能相关）
        "Pgen": np.zeros(24).tolist(),             # 未调整，仍为1×24（假设为总发电）
        "Pdis": np.zeros((2, 24)).tolist(),        # 放电功率，2个微电网，2×24
        "Pcha": np.zeros((2, 24)).tolist(),        # 充电功率，2个微电网，2×24
        "Pcaes_d": np.zeros(24).tolist(),          # 未调整，仍为1×24（假设为CAES放电）
        "Pcaes_g": np.zeros(24).tolist(),          # 未调整，仍为1×24（假设为CAES发电）
        "Pmt": np.zeros(24).tolist(),              # 未调整，仍为1×24（假设为火电相关）
        "P_pv": np.zeros((2, 24)).tolist(),        # 光伏出力，2个微电网，2×24
        "P_w": np.zeros((3, 24)).tolist(),         # 风电出力，3个微电网，3×24
        "Load_real": np.zeros((3, 24)).tolist(),   # 实际负荷，3个微电网，3×24
        "Pgrid_buy": np.zeros((3, 24)).tolist(),   # 电网购电，3个微电网，3×24
        "Pgrid_sell": np.zeros((3, 24)).tolist(),  # 电网售电，3个微电网，3×24
        "total_value": None,                       # 总成本或目标值
        "calculate": 0                             # 计算标识，0表示不计算，1表示计算
    }

    # 将数据写入 JSON 文件
    with open("database.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

database_init()