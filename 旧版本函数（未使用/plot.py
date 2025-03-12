import cvxpy as cp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
def plot_matplotlib(axes):
    # 设置全局字体，确保中文字符正确显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取 JSON 文件中的数据
    with open("database.json", "r") as json_file:
        data = json.load(json_file)

    # 从数据库中读取数据
    Pmt = data.get("Pmt")  
    P_w = data.get("P_w")   
    P_pv = data.get("P_pv")      
    Pfc = data.get("Pfc")  
    Pel = data.get("Pel")
    Pdis = data.get("Pdis")     
    Pcha = data.get("Pcha")  
    Pgen = data.get("Pgen")
    Ppm = data.get("Ppm") 
    Pcaes_d = data.get("Pcaes_d") 
    Pcaes_g = data.get("Pcaes_g")
    Load_real = data.get("Load_real")

    Pcaes_d = np.array(Pcaes_d)     
    Pcaes_g = np.array(Pcaes_g)
    Pmt = np.array(Pmt)
    P_w = np.array(P_w)
    P_pv = np.array(P_pv)
    Pfc = np.array(Pfc)
    Pel = np.array(Pel)
    Pdis = np.array(Pdis)
    Pcha = np.array(Pcha)
    Pgen = np.array(Pgen)
    Ppm = np.array(Ppm)
    Load_real = np.array(Load_real)
    
    # 数据准备
    labels = ['火电', '风电', '光伏', '氢储能放电', '氢储能充电', '蓄电池放电', '蓄电池充电', '抽水蓄能放电', '抽水蓄能充电', '压缩空气放电', '压缩空气充电']
    data = np.array([Pmt, P_w, P_pv, -Pfc, -Pel, -Pdis, -Pcha, -Pgen, -Ppm, -Pcaes_d, -Pcaes_g])

    # 确定数据形状
    data_shape = data.shape

    # 分开正负数据并进行累积
    def get_cumulated_array(data, **kwargs):
        cum = data.clip(**kwargs)  # 取出正值
        cum = np.cumsum(cum, axis=0)  # 对正值进行累积
        d = np.zeros(data.shape)
        d[1:] = cum[:-1]  # 累积值往后移一位
        return d  

    # 处理数据
    cumulated_data = get_cumulated_array(data, min=0)
    cumulated_data_neg = get_cumulated_array(data, max=0)

    # 合并负值和正值
    row_mask = (data < 0)
    cumulated_data[row_mask] = cumulated_data_neg[row_mask]
    data_stack = cumulated_data

    # 绘制堆叠条形图
    x = np.arange(1, 25)  # x 从 1 到 24
    width = 0.35  # 条形宽度

    # 绘制堆叠条形图
    for i in range(data_shape[0]):
        axes.bar(x, data[i], width, bottom=data_stack[i], label=labels[i], color=plt.cm.tab10(i))

    # 绘制负荷曲线
    axes.plot(x, Load_real, 'r', linewidth=2, label='负荷')  # 假设 Load_real 是 cvxpy 变量并已经求解
    axes.axhline(0, color='white', linewidth=1)  # 设置横线为白色

    # 设置图形属性
    axes.set_xlabel('时间(h)', fontsize=16, color='#FFFFFF')  # x轴标签为白色
    axes.set_xticks(np.arange(1, 25, 2))  # 设置x轴刻度
    axes.set_yticks(np.arange(-100, 301, 50))  # 设置y轴刻度
    axes.set_ylabel('功率(kW)', fontsize=16, color='#FFFFFF')  # y轴标签为白色
    axes.set_title('源荷储整体功率', color='#FFFFFF')  # 图表标题为白色

    # 设置坐标轴颜色
    axes.spines['top'].set_color('#FFFFFF')  # 顶部坐标轴为白色
    axes.spines['right'].set_color('#FFFFFF')  # 右侧坐标轴为白色
    axes.spines['left'].set_color('#FFFFFF')  # 左侧坐标轴为白色
    axes.spines['bottom'].set_color('#FFFFFF')  # 底部坐标轴为白色

    # 设置刻度线颜色
    axes.tick_params(axis='x', colors='white')  # 设置x轴刻度线为白色
    axes.tick_params(axis='y', colors='white')  # 设置y轴刻度线为白色

    axes.legend(loc='upper left')  # 添加图例
    # 获取绘图的Figure对象并设置透明背景
    figure = axes.get_figure()
    axes.spines['top'].set_color('#FFFFFF')  # 顶部坐标轴为白色
    axes.spines['right'].set_color('#FFFFFF')  # 右侧坐标轴为白色
    axes.spines['left'].set_color('#FFFFFF')  # 左侧坐标轴为白色
    axes.spines['bottom'].set_color('#FFFFFF')  # 底部坐标轴为白色
    # 设置Figure的背景透明
    figure.patch.set_facecolor('none')  # 设置背景透明
    # 设置Axes的背景透明
    axes.set_facecolor('none')  # 设置坐标轴区域的背景透明
