# import cvxpy as cp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
def plot_CAES(axes):
    # 设置全局字体，确保中文字符正确显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取 JSON 文件中的数据
    with open("database.json", "r") as json_file:
        data = json.load(json_file)
    #从数据库中读取数据 
    Pcaes_d = data.get("Pcaes_d") 
    Pcaes_g = data.get("Pcaes_g")
    Pcaes_d = np.array(Pcaes_d)     
    Pcaes_g = np.array(Pcaes_g)

    Total_CAES = - Pcaes_d - Pcaes_g
    x = np.arange(1, 25)  # x 从 1 到 24
    axes.plot(x, Total_CAES, 'b', linewidth=2, label='压缩空气储能',color = '#FFEB3B')  # 假设 Load_real 是 cvxpy 变量并已经求解

    # 设置图形属性
    axes.set_xlabel('时间(h)', fontsize=16, color='#FFFFFF')
    axes.set_xticks(np.arange(1, 25, 2))
    axes.set_yticks(np.arange(-100, 150, 50))
    axes.set_ylabel('功率(kW)', fontsize=16, color='#FFFFFF')
    axes.set_title('压缩空气储能出力', color='#FFFFFF')
    axes.legend(loc='upper left')  # 添加图例
    # 设置刻度线颜色
    axes.tick_params(axis='x', colors='white')  # 设置x轴刻度线为白色
    axes.tick_params(axis='y', colors='white')  # 设置y轴刻度线为白色
    # 获取绘图的Figure对象并设置透明背景
    figure = axes.get_figure()
    # 设置坐标轴颜色
    axes.spines['top'].set_color('#FFFFFF')  # 顶部坐标轴为白色
    axes.spines['right'].set_color('#FFFFFF')  # 右侧坐标轴为白色
    axes.spines['left'].set_color('#FFFFFF')  # 左侧坐标轴为白色
    axes.spines['bottom'].set_color('#FFFFFF')  # 底部坐标轴为白色
    # 设置Figure的背景透明
    figure.patch.set_facecolor('none')  # 设置背景透明
    # 设置Axes的背景透明
    axes.set_facecolor('none')  # 设置坐标轴区域的背景透明

def plot_Ppm(axes):
    # 设置全局字体，确保中文字符正确显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取 JSON 文件中的数据
    with open("database.json", "r") as json_file:
        data = json.load(json_file)
    #从数据库中读取数据  
    Pgen = data.get("Pgen")
    Ppm = data.get("Ppm")
    Ppm = np.array(Ppm)
    Pgen = np.array(Pgen) 

    Total_Ppm = - Ppm - Pgen
    x = np.arange(1, 25)  # x 从 1 到 24
    axes.plot(x, Total_Ppm, 'b', linewidth=2, label='抽水蓄能储能',color = '#ffc54f')  # 假设 Load_real 是 cvxpy 变量并已经求解

    # 设置图形属性
    axes.set_xlabel('时间(h)', fontsize=16, color='#FFFFFF')
    axes.set_xticks(np.arange(1, 25, 2))
    axes.set_yticks(np.arange(-100, 150, 50))
    axes.set_ylabel('功率(kW)', fontsize=16, color='#FFFFFF')
    axes.set_title('抽水蓄能出力', color='#FFFFFF')
    axes.legend(loc='upper left')  # 添加图例
    # 设置刻度线颜色
    axes.tick_params(axis='x', colors='white')  # 设置x轴刻度线为白色
    axes.tick_params(axis='y', colors='white')  # 设置y轴刻度线为白色
    # 获取绘图的Figure对象并设置透明背景
    figure = axes.get_figure()
    # 设置坐标轴颜色
    axes.spines['top'].set_color('#FFFFFF')  # 顶部坐标轴为白色
    axes.spines['right'].set_color('#FFFFFF')  # 右侧坐标轴为白色
    axes.spines['left'].set_color('#FFFFFF')  # 左侧坐标轴为白色
    axes.spines['bottom'].set_color('#FFFFFF')  # 底部坐标轴为白色
    # 设置Figure的背景透明
    figure.patch.set_facecolor('none')  # 设置背景透明
    # 设置Axes的背景透明
    axes.set_facecolor('none')  # 设置坐标轴区域的背景透明

def plot_H2(axes):
    # 设置全局字体，确保中文字符正确显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 读取 JSON 文件中的数据
    with open("database.json", "r") as json_file:
        data = json.load(json_file)

    #从数据库中读取数据   
    Pfc = data.get("Pfc")  
    Pel = data.get("Pel")
    Pfc = np.array(Pfc)
    Pel = np.array(Pel) 

    Total_H2 = - Pfc - Pel
    x = np.arange(1, 25)  # x 从 1 到 24
    axes.plot(x, Total_H2, 'b', linewidth=2, label='氢储能',color = '#5cbab3')  # 假设 Load_real 是 cvxpy 变量并已经求解

    # 设置图形属性
    axes.set_xlabel('时间(h)', fontsize=16, color='#FFFFFF')
    axes.set_xticks(np.arange(1, 25, 2))
    axes.set_yticks(np.arange(-100, 150, 50))
    axes.set_ylabel('功率(kW)', fontsize=16, color='#FFFFFF')
    axes.set_title('氢储能出力', color='#FFFFFF')
    axes.legend(loc='upper left')  # 添加图例  
    # 设置刻度线颜色
    axes.tick_params(axis='x', colors='white')  # 设置x轴刻度线为白色
    axes.tick_params(axis='y', colors='white')  # 设置y轴刻度线为白色
    # 获取绘图的Figure对象并设置透明背景
    figure = axes.get_figure()
    # 设置坐标轴颜色
    axes.spines['top'].set_color('#FFFFFF')  # 顶部坐标轴为白色
    axes.spines['right'].set_color('#FFFFFF')  # 右侧坐标轴为白色
    axes.spines['left'].set_color('#FFFFFF')  # 左侧坐标轴为白色
    axes.spines['bottom'].set_color('#FFFFFF')  # 底部坐标轴为白色
    # 设置Figure的背景透明
    figure.patch.set_facecolor('none')  # 设置背景透明
    # 设置Axes的背景透明
    axes.set_facecolor('none')  # 设置坐标轴区域的背景透明

def plot_bat(axes):
    # 设置全局字体，确保中文字符正确显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 读取 JSON 文件中的数据
    with open("database.json", "r") as json_file:
        data = json.load(json_file)
    #从数据库中读取数据
    Pdis = data.get("Pdis")     
    Pcha = data.get("Pcha")  
    Pdis = np.array(Pdis)
    Pcha = np.array(Pcha)

    Total_bat = - Pdis - Pcha
    x = np.arange(1, 25)  # x 从 1 到 24
    axes.plot(x, Total_bat, 'b', linewidth=2, label='电化学储能',color = '#9C27B0')  # 假设 Load_real 是 cvxpy 变量并已经求解

    # 设置图形属性
    axes.set_xlabel('时间(h)', fontsize=16, color='#FFFFFF')
    axes.set_xticks(np.arange(1, 25, 2))
    axes.set_yticks(np.arange(-100, 150, 50))
    axes.set_ylabel('功率(kW)', fontsize=16, color='#FFFFFF')
    axes.set_title('电化学储能出力', color='#FFFFFF')
    axes.legend(loc='upper left')  # 添加图例         
    # 设置刻度线颜色
    axes.tick_params(axis='x', colors='white')  # 设置x轴刻度线为白色
    axes.tick_params(axis='y', colors='white')  # 设置y轴刻度线为白色
    # 获取绘图的Figure对象并设置透明背景
    figure = axes.get_figure()
    # 设置坐标轴颜色
    axes.spines['top'].set_color('#FFFFFF')  # 顶部坐标轴为白色
    axes.spines['right'].set_color('#FFFFFF')  # 右侧坐标轴为白色
    axes.spines['left'].set_color('#FFFFFF')  # 左侧坐标轴为白色
    axes.spines['bottom'].set_color('#FFFFFF')  # 底部坐标轴为白色
    # 设置Figure的背景透明
    figure.patch.set_facecolor('none')  # 设置背景透明
    # 设置Axes的背景透明
    axes.set_facecolor('none')  # 设置坐标轴区域的背景透明