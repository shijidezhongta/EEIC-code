'''
    本函数用于模型求解
    使用python docplex库进行求解
    需要python3.7版本（我用的是3.7.16，其他版本未测试）
    docplex库安装参考：https://zhuanlan.zhihu.com/p/655434273
    在调试时，将画图部分代码取消注释，可查看结果图；使用主函数调用run_solving函数时，最好将画图部分代码注释掉
'''

def run_solving():
    import numpy as np
    import json
    from docplex.mp.model import Model
    import os
    from pyecharts import options as opts
    from pyecharts.charts import Bar, Line, Grid
    # # 获取当前脚本所在的目录
    # script_dir = os.path.dirname(os.path.realpath(__file__))

    # # 生成图表并保存到当前脚本所在的文件夹下
    # output_total1 = os.path.join(script_dir, "total_1.html")
    # output_total2 = os.path.join(script_dir, "total_2.html")
    # output_total3 = os.path.join(script_dir, "total_3.html")
    # ------------------------变量定义-----------------------%
    # 初始化模型
    model = Model(  )

    # 时间范围（假设为24小时）
    time_steps = 24

    # ========== 发电设备变量 ==========
    # 将模块1和模块2的同类型变量合并为二维结构
    P_pv = [[model.continuous_var(lb=0, name=f"PV_{k}_{m}") for m in range(2)] for k in range(time_steps)]  # m=0模块1, m=1模块2
    P_w = [[model.continuous_var(lb=0, name=f"Wind_{k}_{m}") for m in range(3)] for k in range(time_steps)]
    Pmt = [[model.continuous_var(lb=40, ub=170, name=f"Pmt_{k}_{m}") for m in range(3)] for k in range(time_steps)]

    # ========== 储能系统变量 ==========
    # 蓄电池
    PP = [[model.continuous_var(lb=0, ub=300, name=f"SOC_{k}_{m}") for m in range(2)] for k in range(time_steps)]   # 电池容量
    Pcha = [[model.continuous_var(lb=0, ub=40, name=f"Charge_{k}_{m}")for m in range(2)] for k in range(time_steps)]  # 充电功率
    Pdis = [[model.continuous_var(lb=-40, ub=0, name=f"Discharge_{k}_{m}") for m in range(2)] for k in range(time_steps)]  # 放电功率

    # 氢能系统
    Pel = [model.continuous_var(lb=0, ub=300, name=f"Electrolysis_{k}") for k in range(time_steps)]  # 电解槽
    Pfc = [model.continuous_var(lb=-300, ub=0, name=f"FuelCell_{k}") for k in range(time_steps)]  # 燃料电池（负值表示放电）
    L_H2 = [model.continuous_var(lb=0, ub=500, name=f"L_H2_{t}") for t in range(time_steps)]  # 储氢罐容量
    p_H2 = [model.continuous_var(lb=0, ub=3000, name=f"p_H2_{t}") for t in range(time_steps)]  # 储氢罐压力

    # 抽水蓄能系统
    Ppm = [model.continuous_var(lb=0, ub=50, name=f"Pump_charge_{k}") for k in range(time_steps)] # 充电
    Pgen = [model.continuous_var(lb=-50, ub=0, name=f"Pump_discharge_{k}") for k in range(time_steps)] # 放电
    Temp_ps_pm = [model.binary_var(name=f"PumpMode_{k}") for k in range(time_steps)]  # 抽水模式标志
    Temp_ps_gen = [model.binary_var(name=f"GenMode_{k}") for k in range(time_steps)]   # 发电模式标志
    Temp_ps_Hstatic = [model.binary_var(name=f"IdleMode_{k}") for k in range(time_steps)]  # 静置模式标志

    # 水库容量变化
    Vps = [model.continuous_var(name=f"Vps_{k}") for k in range(time_steps)]

    # 机组启停标志
    need_to_stop_in = [model.binary_var(name=f"StopIn_{k}") for k in range(time_steps)]  # 进水停机标志
    need_to_stop_out = [model.binary_var(name=f"StopOut_{k}") for k in range(time_steps)]  # 出水停机标志

    # 压缩空气储能
    Pcaes_g = [model.continuous_var(lb=0, ub=50, name=f"CAES_charge_{k}") for k in range(time_steps)]  # 充电
    Pcaes_d = [model.continuous_var(lb=-50, ub=0, name=f"CAES_discharge_{k}") for k in range(time_steps)]  # 放电
    CAES_p = [model.continuous_var(lb=0, ub=10000, name=f"p_CAES_{k}") for k in range(time_steps)]  # 储气罐压力
    CAES_k = [model.continuous_var(lb=0.001, ub=0.01, name=f"k_CAES_{k}") for k in range(time_steps)]  # 渗透率（新增）

    # ========== 电力交易 ==========
    ele_buy = [[model.continuous_var(lb=0, ub=100, name=f"Buy_{k}_{m}") for m in range(3)] for k in range(time_steps)]    # 购电
    ele_sell = [[model.continuous_var(lb=0, ub=100, name=f"Sell_{k}_{m}")for m in range(3)] for k in range(time_steps)]  # 售电


    # 创建二元变量
    b_ele = [[model.binary_var(name=f'buy_ele_{k}_{m}')for m in range(3)] for k in range(time_steps)]

    # 碳约束部分
    Ecfp = [[model.continuous_var(lb=0, name=f"Ecfp_{k}_{m}") for m in range(3)] for k in range(time_steps)] # 碳排放配额
    Emt = [[model.continuous_var(lb=0, name=f"Emt_{k}_{m}") for m in range(3)] for k in range(time_steps)] # 火力机组实际碳排放
    Ecet = [[model.continuous_var(lb=-1000,name=f"Ecet_{k}_{m}") for m in range(3)] for k in range(time_steps)] # 参与碳市场交易的碳额
    Ccar = [[model.continuous_var(lb=-10000,name=f"Ccar_{k}_{m}") for m in range(3)] for k in range(time_steps)] # 碳交易成本

    # -------------------------常量定义-----------------------%

    # 光伏和风机出力
    random_Ppv = np.array([0, 0, 0, 0, 0, 50.37, 17.13, 29.40, 291.70, 240.07, 216.66, 250.34, 267.96, 327.72, 276.47, 206.05, 27.83, 0, 0, 0, 0, 0, 0, 0])
    random_Pw = np.array([56.10, 60, 18.14, 38.19, 31.28, 37.64, 35.97, 34.99, 57.96, 79.56, 67.68, 50.73, 46.61, 33.35, 45.27, 61.85, 43.55, 38.99, 25.81, 12.02, 12.25, 11.95, 14.06, 13.23])

    random_Ppv_1 = np.array([0, 0, 0, 0, 0, 40.37, 7.13, 19.40, 191.70, 200.07, 196.66, 200.34, 217.96, 287.72, 246.47, 186.05, 7.83, 0, 0, 0, 0, 0, 0, 0])
    random_Pw_1 = np.array([36.10, 40, 8.14, 28.19, 21.28, 27.64, 25.97, 24.99, 47.96, 69.56, 57.68, 40.73, 36.61, 23.35, 35.27, 51.85, 33.55, 28.99, 15.81, 2.02, 2.25, 1.95, 4.06, 3.23])

    random_Pw_2 = [56.10, 60.00, 23.14, 43.19, 36.28, 42.64, 40.97,40.99, 72.96, 94.56, 
                82.68, 65.73, 61.61, 38.35, 50.27, 66.85, 48.55, 43.99, 35.81, 17.02, 
                20.25, 16.95, 19.06, 18.23]
    
    # 氢储能参数定义
    R = 8.314               # 理想气体常数 (J/mol·K)
    T = 298.15              # 温度 (K)
    V_H2 = 100                 # 储氢罐体积 (m³)
    p_safe = 20             # 安全压力变化阈值 (Pa/h)
    k_leak = 0.001          # 泄漏系数 (m³/(Pa·h))
    initial_L = 50          # 初始储氢量 (mol)

    # CAES储能参数定义
    V_CAES = 1000                  # 储气罐体积 (m³)
    R = 8.314                 # 理想气体常数 (J/mol·K)
    T = 298.15                # 温度 (K)
    initial_p = 3000        # 初始压力 (Pa)
    alpha = 0.95     # 地质影响系数

    # 电化学储能常量定义（常量值待定）
    Ebattery = 300          # 电池容量
    soc0 = 0.5              # 初始SOC
    η_charge = 0.95         # 充电效率
    η_discharge = 0.95      # 放电效率
    a1 = 50                # 老化系数1
    a2 = 100               # 老化系数2
    a3 = 1.5                # 老化系数3
    a4 = 2                  # 温度系数
    a5 = 50                 # C-rate系数
    N_max = 2000            # 总循环次数
    Cost_replace = 100      # 更换成本（元）
    T = 25                  # 温度（℃）
    C_rate = 1.0            # 充放电速率（C）
    Replace_cost = model.continuous_var(name="Replace_cost")

    # 抽水蓄能参数定义
    Vpsmax = 100  # 最大容量变化
    Vpmax = 500  # 最大容量
    Vmin = 0.1  # 最低容量系数限制
    Vmax = 0.9  # 最大容量系数限制
    np1 = 0.55  # 容量系数
    C_number = 4  # 转换次数上限

    B = 50

    # 碳排放参数定义
    Epsilon_0 = 0.6  # 碳排放系数
    Epsilon_Pmt = 0.9  # 火力发电碳排放系数
    d = 10
    cc = 0.25
    aa = 0.25

    # 读取 JSON 文件中的数据
    with open("database.json", "r") as json_file:
        data = json.load(json_file)

    Price_Pmt = float(data.get("value_Pmt", 0.3))  # 火力发电单价，默认值为 0.3
    Price_pv = float(data.get("value_pv", 0.24))   # 光伏单价，默认值为 0.24
    Price_w = float(data.get("value_w", 0.2))      # 风能单价，默认值为 0.2
    Price_Pump_change = float(data.get("value_Pump", 0.5))  # 抽水蓄能开停机价格，默认值为 0.5
    Price_CAES = float(data.get("value_CAES", 0.4))  # 压缩空气储能单价，默认值为 0.4
    Price_H2 = float(data.get("value_H2", 0.6))     # 氢储能单价，默认值为 0.6
    Price_bat = float(data.get("value_bat", 0.25))  # 蓄电池储能单价，默认值为 0.25
    Price_CO2 = float(data.get("value_CO2", 0.05))  # 碳交易机制碳成本系数，默认值为 0.05
    Demand_re = float(data.get("value_if_demand", 1))  # 是否考虑需求响应，默认值为 1
    Carbon_Tra = float(data.get("value_if_carbon", 1))  # 是否考虑碳约束，默认值为 1

    # Load: 假设你已经有这个负荷数据
    Load = np.array([188.24, 183.01, 180.15, 179.01, 176.07, 178.39, 189.95, 228.85, 255.45, 276.35, 
                    293.71, 282.57, 279.64, 266.31, 264.61, 264.61, 274.48, 303.93, 318.99, 338.11, 
                    316.14, 273.87, 231.07, 194.04])
    Load1 = np.array([139.42, 134.71, 131.13, 130.15, 127.46, 129.55, 140.95, 168.97, 194.91, 214.72, 231.89, 221.31, 218.68, 206.68, 205.15, 205.15, 214.03, 241.53, 256.64, 275.90, 264.52, 224.48, 184.96, 150.64])
    Load2 = np.array([73.83, 60.86, 55.64, 53.58, 50.77, 53.97, 65.45, 98.91, 125.18, 155.54, 
            172.80, 161.94, 159.16, 146.50, 144.88, 154.88, 164.26, 192.73, 217.82, 220.01, 
            200.33, 189.18, 158.02, 132.34])
    Load_real = Load
    Load_real1 = Load1
    Load_real2 = Load2

    value_sell = np.array([0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.52,0.52,0.52,0.52,0.72,0.72,0.72,0.72,0.72,0.72,0.52,0.52,0.52,0.52,0.52,0.25])
    value_buy = np.array([0.46,0.46,0.46,0.46,0.46,0.46,0.46,0.46,0.35,0.35,0.35,0.35,0.27,0.27,0.27,0.27,0.27,0.27,0.35,0.35,0.35,0.35,0.35,0.46])

    F_expr = model.sum( 
        Price_Pmt * (Pmt[k][0] + Pmt[k][1] + Pmt[k][2]) + # 火力发电成本
        Price_pv * (P_pv[k][0] + P_pv[k][1]) + # 光伏发电成本
        Price_w * (P_w[k][0] + P_w[k][1] + P_w[k][2]) + # 风能发电成本
        Price_H2 * (Pel[k] - Pfc[k]) +  # 氢储能成本
        Price_bat * (Pcha[k][0] + Pcha[k][1] - Pdis[k][0] - Pdis[k][1]) + # 电化学储能成本
        Price_Pump_change * (need_to_stop_in[k] + need_to_stop_out[k]) +  # 抽水蓄能成本
        Price_CAES * (Pcaes_g[k] - Pcaes_d[k]) + # 压缩空气储能成本
        (value_buy[k] * (ele_buy[k][0] + ele_buy[k][1] + ele_buy[k][2]) - 
        value_sell[k] * (ele_sell[k][0] + ele_sell[k][1] + ele_sell[k][2])) +   # 电力市场成本
        Price_CO2 * (Ccar[k][0] + Ccar[k][1])  # 碳交易成本
        for k in range(time_steps)
    )

    # # 设置目标
    # model.minimize(F_expr)

    # ----------------------约束条件----------------------%
    # 功率平衡约束
    for k in range(time_steps):
        # 模块1功率平衡
        model.add_constraint(
            P_pv[k][0] + P_w[k][0] + Pmt[k][0] - Pgen[k] - Pcaes_d[k] + ele_buy[k][0] 
            == Load_real[k] + Ppm[k] + Pcaes_g[k] + ele_sell[k][0],
            ctname=f"power_balance1_{k}"
        )
        
        # 模块2功率平衡
        model.add_constraint(
            P_pv[k][1] + P_w[k][1] + Pmt[k][1] - Pfc[k] - Pdis[k][0] + ele_buy[k][1] 
            == Load_real1[k] + Pel[k] + Pcha[k][0] + ele_sell[k][1],
            ctname=f"power_balance2_{k}"
        )

        # 模块3功率平衡
        model.add_constraint(
            P_w[k][2] + Pmt[k][2]  - Pdis[k][1] + ele_buy[k][2] 
            == Load_real2[k]  + Pcha[k][1] + ele_sell[k][2],
            ctname=f"power_balance3_{k}"
        )

        # 电力市场交易平衡
        model.add_constraint(
            ele_buy[k][0] + ele_buy[k][1] + ele_buy[k][2]== ele_sell[k][0] + ele_sell[k][1] + ele_sell[k][2],
            ctname=f"market_balance_{k}"
        )

    # 电源侧约束
    for k in range(time_steps):
        # 可再生能源出力上限
        model.add_constraint(P_pv[k][0] <= random_Ppv[k], ctname=f"pv_limit_{k}")
        model.add_constraint(P_pv[k][1] <= random_Ppv_1[k], ctname=f"pv1_limit_{k}")
        model.add_constraint(P_w[k][0] <= random_Pw[k], ctname=f"wind_limit_{k}")
        model.add_constraint(P_w[k][1] <= random_Pw_1[k], ctname=f"wind1_limit_{k}")
        model.add_constraint(P_w[k][2] <= random_Pw_2[k], ctname=f"wind2_limit_{k}")

        # # 电力交易互斥约束
        model.add_constraint(ele_buy[k][0] <= 100 * b_ele[k][0])
        model.add_constraint(ele_sell[k][0] <= 100 * (1 - b_ele[k][0]))
        model.add_constraint(ele_buy[k][1] <= 100 * b_ele[k][1])
        model.add_constraint(ele_sell[k][1] <= 100 * (1 - b_ele[k][1]))
        model.add_constraint(ele_buy[k][2] <= 100 * b_ele[k][2])
        model.add_constraint(ele_sell[k][2] <= 100 * (1 - b_ele[k][2]))

    # ========== 储能系统约束 ==========
    # 氢能系统能量平衡
    model.add_constraint(model.sum(Pfc) == -model.sum(Pel), ctname="h2_balance")
    # 储氢罐压力与容量关系
    for t in range(time_steps):
        model.add_constraint(p_H2[t] == L_H2[t] * R * T / V_H2)
        # 储氢量平衡方程（含泄漏）
        if t == 0:
            model.add_constraint(L_H2[t] == initial_L + (Pel[t] + Pfc[t] - k_leak * p_H2[t]) )
        else:
            model.add_constraint(L_H2[t] == L_H2[t-1] + (Pel[t] + Pfc[t] - k_leak * p_H2[t]) )

    # 压力变化率安全约束
    for t in range(1, time_steps):
        model.add_constraint(p_H2[t] - p_H2[t-1] <= p_safe)

    # 压缩空气储能
    model.add_constraint(model.sum(Pcaes_g) == -model.sum(Pcaes_d), ctname="CAES_balance")
    # 压缩空气储能模型优化
    for t in range(time_steps):        
        # 储气罐压力动态方程（新增渗透率影响）
        if t == 0:
            model.add_constraint(CAES_p[t] == initial_p + (Pcaes_g[t] + Pcaes_d[t]) * R * T / V_CAES )
        else:
            model.add_constraint(CAES_p[t] == CAES_p[t-1] + (Pcaes_g[t] + Pcaes_d[t]) * R * T / V_CAES )
        
        # 地质稳定性约束（新增）
        model.add_constraint(CAES_k[t] <= alpha * CAES_k[t-1] if t > 0 else True)
        
        # # 压力变化率约束
        # if t > 0:
        #     model.add_constraint(CAES_p[t] - CAES_p[t-1] <= max_p_change)
        #     model.add_constraint(CAES_p[t-1] - CAES_p[t] <= max_p_change)

    # # 蓄电池约束 
    # PP[0][0] = soc0 * Ebattery
    # PP[0][1] = soc0 * Ebattery
    # η_charge = 0.95  # 充电效率
    # η_discharge = 0.95  # 放电效率
    # for k in range(24):
    #     for m in range(2):
    #         # 充放电功率限制
    #         model.add_constraint(PP[k][m] == PP[k-1][m] + η_charge*Pcha[k][m] - (1/η_discharge)*Pdis[k][m])
    # 储能SOC约束
    PP[0][0] = soc0 * Ebattery
    PP[0][1] = soc0 * Ebattery
    for t in range(1, time_steps):
        for m in range(2):
            model.add_constraint(
                PP[t][m] == PP[t-1][m] + η_charge*Pcha[t][m] - (1/η_discharge)*Pdis[t][m],
                ctname=f"soc_constraint_{t}_{1}"
            )
    # 蓄电池SOC全局约束
    model.add_constraint(model.sum(Pcha[k][0] for k in range(24)) == -model.sum(Pdis[k][0] for k in range(24)), ctname="bat_balance")
    model.add_constraint(model.sum(Pcha[k][1] for k in range(24)) == -model.sum(Pdis[k][1] for k in range(24)), ctname="bat_balance1")

    # 电化学储能老化模型
    aging_cost = []
    for t in range(time_steps):
        # 计算放电深度
        D_N = 1 - PP[t][0]/Ebattery
        
        # 多因素老化模型
        # N = a1 + a2 * np.exp(a3 * D_N) + a4 * T + a5 * C_rate
        N = a1 + a2 * (1 + (a3 * D_N) + 0.5 * (a3 * D_N) * (a3 * D_N)) + a4 * (T - 25) + a5 * (C_rate - 1)
        
        # 寿命损耗成本
        Replace_cost = Cost_replace * (N / N_max)
        aging_cost.append(Replace_cost)
        
        # 约束：确保成本非负
        # model.add_constraint(Replace_cost >= 0)

    # 加入老化成本到目标函数
    F_expr += model.sum(aging_cost)
    model.minimize(F_expr)

    #  抽水蓄能约束
    for k in range(time_steps):
        # 运行模式逻辑
        model.add_constraint(Ppm[k] <= B * Temp_ps_pm[k], ctname=f"pump_mode_{k}")
        model.add_constraint(Pgen[k] >= -B * Temp_ps_gen[k], ctname=f"gen_mode_{k}")
        model.add_constraint(Temp_ps_pm[k] + Temp_ps_gen[k] <= 1)
        
        # 启停逻辑
        if k > 0:
            model.add_constraint(Temp_ps_pm[k-1] + Temp_ps_gen[k] <= 1, ctname=f"mode_trans1_{k}")
            model.add_constraint(need_to_stop_in[k] >= Temp_ps_pm[k-1] - Temp_ps_pm[k], ctname=f"stop_in_{k}")

    # 抽蓄能量平衡
    model.add_constraint(model.sum(Ppm) == -model.sum(Pgen), ctname="pump_storage_balance")
    s1 = 0.5 * Vpmax  # 初始库容
    for p in range(time_steps):
        s1 += np1 * (Pgen[p] + Ppm[p])  # np1为转换效率系数
        model.add_range(Vmin*Vpmax, s1, Vmax*Vpmax, f"reservoir_capacity_{p}")
    # 机组启停次数约束
    model.add_constraint(model.sum(need_to_stop_in) + model.sum(need_to_stop_out) <= C_number,
                        ctname="operation_change_limit")

    # ----------------------碳约束---------------------- #
    # 基础约束
    for k in range(time_steps):
        for m in range(3):
            if m == 2:
                model.add_constraint(Ecfp[k][m] == Epsilon_0 * (Pmt[k][m]  + P_w[k][m]))  # 配额计算
            else:
                model.add_constraint(Ecfp[k][m] == Epsilon_0 * (Pmt[k][m] + P_pv[k][m] + P_w[k][m]))  # 配额计算
            model.add_constraint(Emt[k][m] == Epsilon_Pmt * Pmt[k][m])                   # 实际排放
            model.add_constraint(Ecet[k][m] == Emt[k][m] - Ecfp[k][m])             # 交易量计算

    # 动态碳交易成本变化
    beta = 0.2 # 动态调节系数
    gamma = 0.2 # 经济补偿系数
    GDP_index = 0.8 #地区经济值

    for k in range(time_steps):
        for m in range(3):
            # 动态调整碳交易价格
            P_renewable = np.sum(random_Ppv + random_Pw + random_Ppv_1 + random_Pw_1 + random_Pw_2)
            P_total = np.sum(Load_real + Load_real1 + Load_real2)
            cc = cc * (1 + beta * (P_renewable/P_total))
            ecet = Ecet[k][m]
            
            # 定义6个二进制变量对应6个区间
            z = [model.binary_var(name=f"z_{k}_{m}_{i}") for i in range(6)]
            
            # 区间互斥约束
            model.add_constraint(sum(z) == 1)
            
            # 各区间边界约束
            # 1. Ecet <= -2d
            model.add_indicator(z[0], ecet <= -2*d)
            model.add_indicator(z[0], Ccar[k][m] == -cc*(1+aa)*d - cc*(1+2*aa)*d + cc*(1+3*aa)*(ecet + 2*d))
            
            # 2. -2d < Ecet <= -d
            model.add_indicator(z[1], ecet >= -2*d + 1e-6)  # 避免边界重叠
            model.add_indicator(z[1], ecet <= -d)
            model.add_indicator(z[1], Ccar[k][m] == -cc*(1+aa)*d + cc*(1+2*aa)*(ecet + d))
            
            # 3. -d < Ecet <= 0
            model.add_indicator(z[2], ecet >= -d + 1e-6)
            model.add_indicator(z[2], ecet <= 0)
            model.add_indicator(z[2], Ccar[k][m] == cc*(1+aa)*ecet)
            
            # 4. 0 < Ecet <= d
            model.add_indicator(z[3], ecet >= 1e-6)
            model.add_indicator(z[3], ecet <= d)
            model.add_indicator(z[3], Ccar[k][m] == cc*ecet)
            
            # 5. d < Ecet <= 2d
            model.add_indicator(z[4], ecet >= d + 1e-6)
            model.add_indicator(z[4], ecet <= 2*d)
            model.add_indicator(z[4], Ccar[k][m] == cc*d + cc*(1+aa)*(ecet - d))
            
            # 6. Ecet > 2d
            model.add_indicator(z[5], ecet >= 2*d + 1e-6)
            model.add_indicator(z[5], Ccar[k][m] == cc*(2+aa)*d + cc*(1+2*aa)*(ecet - 2*d))
    # ----------------------储能占比----------------------
    # Total_Charge_Discharge_Abs = cp.Variable(24)
    # Hydrogen_Storage_Total_Abs = cp.Variable(24)
    # Pumped_Storage_Total_Abs = cp.Variable(24)
    # Battery_Total_Abs = cp.Variable(24)
    # CAES_Total_Abs = cp.Variable(24)

    # # 计算各储能系统充电和放电量的绝对值之和
    # for k in range(24):
    #     constraints.append(Total_Charge_Discharge_Abs[k] == Pel[k] - Pfc[k] + Pcha[k] - Pdis[k] - Pcaes_d[k] + Pcaes_g[k] + Ppm[k] - Pgen[k])
    # # 计算抽水蓄能充电和放电量的绝对值之和
    # for k in range(24):
    #     constraints.append(Pumped_Storage_Total_Abs[k] == Ppm[k] -Pgen[k] )
    # # 蓄电池充放电量的绝对值之和
    # for k in range(24):
    #     constraints.append(Battery_Total_Abs[k] == Pcha[k] - Pdis[k])
    # # 氢储能系统充放电量的绝对值之和
    # for k in range(24):
    #     constraints.append(Hydrogen_Storage_Total_Abs[k] ==  Pel[k] - Pfc[k])
    # # 压缩空气储能系统（CAES）充放电量的绝对值之和
    # for k in range(24):
    #     constraints.append(CAES_Total_Abs[k] == Pcaes_g[k] - Pcaes_d[k])
    # # 添加约束：抽水蓄能占总充电量和放电量的比例不超过47%
    # constraints.append(cp.sum(Pumped_Storage_Total_Abs) <= 0.47 * cp.sum(Total_Charge_Discharge_Abs))
    # # 添加约束：蓄电池占总充电量和放电量的比例不超过24%
    # constraints.append(cp.sum(Battery_Total_Abs) <= 0.3 * cp.sum(Total_Charge_Discharge_Abs))
    # # 添加约束：氢储能占总充电量和放电量的比例不超过17%
    # constraints.append(cp.sum(Hydrogen_Storage_Total_Abs) <= 0.27 * cp.sum(Total_Charge_Discharge_Abs))
    # # 添加约束：压缩空气储能占总充电量和放电量的比例不超过12%
    # constraints.append(cp.sum(CAES_Total_Abs) <= 0.2 * cp.sum(Total_Charge_Discharge_Abs))

    # # ----------------------充放电约束----------------------
    # # 1. 定义储能系统的判断变量
    # CAES_Status = cp.Variable(24, boolean=True)  # CAES状态变量
    # CAES_Status1 = cp.Variable(24, boolean=True)  # CAES状态变量2

    # # 2. 施加状态判断约束
    # for k in range(24):
    #     if Pcaes_d[k]:
    #         constraints += [CAES_Status[k] == 1]
    #     if Pcaes_g[k]:
    #         constraints += [CAES_Status1[k] == 1]  

    # # 3. 施加基于放电状态的充电约束
    # for k in range(24):
    #     # 如果蓄电池在放电，则其他储能设备不能充电
    #     if Temp_dis[k]:
    #         constraints += [Pcha[k] == 0, Pel[k] == 0, Pcaes_g[k] == 0, Ppm[k] == 0]
        
    #     # 如果抽水蓄能在放电，则其他储能设备不能充电
    #     if Temp_ps_gen[k]:
    #         constraints += [Pcha[k] == 0, Pel[k] == 0, Pcaes_g[k] == 0, Ppm[k] == 0]
        
    #     # 如果压缩空气在放电，则其他储能设备不能充电
    #     if CAES_Status[k]:
    #         constraints += [Pcha[k] == 0, Pel[k] == 0, Pcaes_g[k] == 0, Ppm[k] == 0]
        
    #     # 如果氢储能在放电，则其他储能设备不能充电
    #     if Temp_fc[k]:
    #         constraints += [Pcha[k] == 0, Pel[k] == 0, Pcaes_g[k] == 0, Ppm[k] == 0]

    # # 4. 施加基于充电状态的放电约束
    # for k in range(24):
    #     # 如果蓄电池在充电，则其他储能设备不能放电
    #     if Temp_cha[k]:
    #         constraints += [Pdis[k] == 0, Pfc[k] == 0, Pcaes_d[k] == 0, Pgen[k] == 0]
        
    #     # 如果抽水蓄能在充电，则其他储能设备不能放电
    #     if Temp_ps_pm[k]:
    #         constraints += [Pdis[k] == 0, Pfc[k] == 0, Pcaes_d[k] == 0, Pgen[k] == 0]
        
    #     # 如果压缩空气在充电，则其他储能设备不能放电
    #     if CAES_Status1[k]:
    #         constraints += [Pdis[k] == 0, Pfc[k] == 0, Pcaes_d[k] == 0, Pgen[k] == 0]
        
    #     # 如果氢储能在充电，则其他储能设备不能放电
    #     if Temp_el[k]:
    #         constraints += [Pdis[k] == 0, Pfc[k] == 0, Pcaes_d[k] == 0, Pgen[k] == 0]

    model.parameters.timelimit=20  # 设置求解时间上限
    model.parameters.mip.tolerances.mipgap=0.01  # 设置最优解的容忍度
    model.print_information()  # 输出变量/约束统计
    # 调用求解器
    solution = model.solve(log_output=True)  # log_output显示求解过程

    # 输出结果
    if solution:
        print(f"最优成本: {model.objective_value:.2f} 万元") 
        print("求解状态:", model.solve_details.status)
    else:
        print("模型不可行，请检查约束条件")

    value = round(model.objective_value,2)

    # ##--------------------------------------------结果数据处理----------------------------------
    # # 数据数值化处理
    # Pfc_value = np.zeros(24)
    # Pel_value = np.zeros(24)
    # Pmt_value = np.zeros(24)
    # Pcaes_d_value = np.zeros(24)
    # Pcaes_g_value = np.zeros(24)
    # Pdis_value = np.zeros(24)
    # Pcha_value = np.zeros(24)
    # Pdis_value1 = np.zeros(24)
    # Pcha_value1 = np.zeros(24)
    # Pgen_value = np.zeros(24)
    # Ppm_value = np.zeros(24)
    # Ps_Pw = np.zeros(24)
    # Ps_Ppv = np.zeros(24)
    # Pmt_value1 = np.zeros(24)
    # Pmt_value2 = np.zeros(24)
    # Ps_Ppv1 = np.zeros(24)
    # Ps_Pw1 = np.zeros(24)
    # Ps_Pw2 = np.zeros(24)
    # ele_buy_value = np.zeros(24)
    # ele_sell_value = np.zeros(24)
    # ele_buy_value1 = np.zeros(24)
    # ele_sell_value1 = np.zeros(24) 
    # ele_buy_value2 = np.zeros(24)
    # ele_sell_value2 = np.zeros(24) 

    # for k in range(24):
    #     # 发电设备出力
    #     Pmt_value[k] = Pmt[k][0].solution_value
    #     Pmt_value1[k] = Pmt[k][1].solution_value
    #     Pmt_value2[k] = Pmt[k][2].solution_value

    #     # 储能系统
    #     Pcaes_d_value[k] = -Pcaes_d[k].solution_value  # 放电为正
    #     Pcaes_g_value[k] = -Pcaes_g[k].solution_value    # 充电为负
        
    #     # 抽水蓄能
    #     Pgen_value[k] = -Pgen[k].solution_value  # 发电量取正
    #     Ppm_value[k] = -Ppm[k].solution_value
        
    #     # 氢能系统
    #     Pfc_value[k] = -Pfc[k].solution_value  # 燃料电池放电为正
    #     Pel_value[k] = -Pel[k].solution_value  # 电解槽电量为正

    #     # 蓄电池
    #     Pcha_value[k] = -Pcha[k][0].solution_value  # 充电为正
    #     Pdis_value[k] = -Pdis[k][0].solution_value  # 放电为正

    #     Pcha_value1[k] = -Pcha[k][1].solution_value  # 充电为正
    #     Pdis_value1[k] = -Pdis[k][1].solution_value  # 放电为正

    #     # 可再生能源
    #     Ps_Pw[k] = P_w[k][0].solution_value
    #     Ps_Pw1[k] = P_w[k][1].solution_value
    #     Ps_Pw2[k] = P_w[k][2].solution_value
    #     Ps_Ppv[k] = P_pv[k][0].solution_value
    #     Ps_Ppv1[k] = P_pv[k][1].solution_value
        
    #     # 电力交易
    #     ele_buy_value[k] = ele_buy[k][0].solution_value
    #     ele_sell_value[k] = -ele_sell[k][0].solution_value  # 售电量为正
    #     ele_buy_value1[k] = ele_buy[k][1].solution_value
    #     ele_sell_value1[k] = -ele_sell[k][1].solution_value  # 售电量为正
    #     ele_buy_value2[k] = ele_buy[k][2].solution_value
    #     ele_sell_value2[k] = -ele_sell[k][2].solution_value  # 售电量为正
        
    # ## ------------------------------------模块一绘图------------------------------------ ##
    # # 定义 X 轴数据（假设为时间或其他分类变量）
    # x_data = [str(i) for i in range(1, len(Pmt_value) + 1)]

    # # 创建堆积柱状图
    # bar = (
    #     Bar()
    #     .add_xaxis(x_data)  # 添加 X 轴数据
    #     .add_yaxis("火电", Pmt_value.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pmt
    #     .add_yaxis("风电", Ps_Pw.tolist(), stack="stack1")  # 添加 Y 轴数据系列 P_w
    #     .add_yaxis("太阳能", Ps_Ppv.tolist(), stack="stack1")  # 添加 Y 轴数据系列 P_pv
    #     .add_yaxis("抽蓄放电", Pgen_value.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pgen
    #     .add_yaxis("抽蓄充电", Ppm_value.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Ppm
    #     .add_yaxis("CAES放电", Pcaes_d_value.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pcaes_d
    #     .add_yaxis("CAES充电", Pcaes_g_value.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pcaes_g
    #     .add_yaxis("电网购电", ele_buy_value.tolist(), stack="stack1")
    #     .add_yaxis("电网售电", ele_sell_value.tolist(), stack="stack1") 
    #     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 隐藏数据标签
    #     .set_global_opts(
    #         title_opts=opts.TitleOpts(is_show=False),  # 隐藏标题
    #         legend_opts=opts.LegendOpts(is_show=True,textstyle_opts=opts.TextStyleOpts(font_size=16)),  # 隐藏图例
    #         yaxis_opts=opts.AxisOpts(
    #             min_=-200,  # 设置 Y 轴最小值
    #             max_=500,  # 设置 Y 轴最大值
    #             interval=50,  # 设置 Y 轴刻度间隔
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#5BA5E7")  # 设置 Y 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#5BA5E7",
    #                                         font_size = 16),  # 设置 Y 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=True,
    #                 linestyle_opts=opts.LineStyleOpts(
    #                     color="#5BA5E7",
    #                     opacity=0.2,  # 设置网格线透明度为 0.2
    #                 )
    #             ),
    #         ),
    #         xaxis_opts=opts.AxisOpts(
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#5BA5E7")  # 设置 X 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#5BA5E7",
    #                                         font_size = 16),  # 设置 X 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=False  # 隐藏 X 轴网格线
    #             ),
    #         ),
    #     )
    # )

    # # 创建折线图，并将其样式与柱状图保持一致
    # line = (
    #     Line()
    #     .add_xaxis(x_data)  # 使用相同的 X 轴数据
    #     .add_yaxis(
    #         "负荷量",
    #         Load_real.tolist(),
    #         is_smooth=True,
    #         z_level = 1,
    #         color="#E12F13",  # 使用与柱状图一致的颜色
    #     )  # 添加负荷量折线图
    #     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 隐藏数据标签
    #     .set_global_opts(
    #         yaxis_opts=opts.AxisOpts(
    #             min_=-200,  # 设置 Y 轴最小值，与柱状图一致
    #             max_=500,  # 设置 Y 轴最大值，与柱状图一致
    #             interval=50,  # 设置 Y 轴刻度间隔，与柱状图一致
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # 设置 Y 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # 设置 Y 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=True,
    #                 linestyle_opts=opts.LineStyleOpts(
    #                     color="#CCEDFF",
    #                     opacity=0.2,  # 设置网格线透明度为 0.2
    #                 )
    #             ),
    #         ),
    #         xaxis_opts=opts.AxisOpts(
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # 设置 X 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # 设置 X 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=False  # 隐藏 X 轴网格线
    #             ),
    #         ),
    #         legend_opts=opts.LegendOpts(is_show=False),  # 隐藏图例
    #     )
    # )

    # # 使用 Grid 将两个图表叠加
    # grid = (
    #     Grid(init_opts=opts.InitOpts(width="1180px", height="820px"))
    #     .add(line, grid_opts=opts.GridOpts())  # 添加折线图
    #     .add(bar, grid_opts=opts.GridOpts())  # 添加堆积柱状图
    # )

    # # 渲染图表并保存为 HTML 文件
    # grid.render(output_total1)

    # ## --------------------------------------------模块二绘图---------------------------------- ##
    # # 创建堆积柱状图
    # bar = (
    #     Bar()
    #     .add_xaxis(x_data)  # 添加 X 轴数据
    #     .add_yaxis("火电", Pmt_value1.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pmt
    #     .add_yaxis("风电", Ps_Pw1.tolist(), stack="stack1")  # 添加 Y 轴数据系列 P_w
    #     .add_yaxis("太阳能", Ps_Ppv1.tolist(), stack="stack1")  # 添加 Y 轴数据系列 P_pv
    #     .add_yaxis("氢储放电", Pfc_value.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pgen
    #     .add_yaxis("氢储充电", Pel_value.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Ppm
    #     .add_yaxis("蓄电池充电", Pcha_value.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pcaes_d
    #     .add_yaxis("蓄电池放电", Pdis_value.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pcaes_g
    #     .add_yaxis("电网购电", ele_buy_value1.tolist(), stack="stack1")
    #     .add_yaxis("电网售电", ele_sell_value1.tolist(), stack="stack1") 
    #     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 隐藏数据标签
    #     .set_global_opts(
    #         title_opts=opts.TitleOpts(is_show=False),  # 隐藏标题
    #         legend_opts=opts.LegendOpts(is_show=True,textstyle_opts=opts.TextStyleOpts(font_size=16)),  # 隐藏图例
    #         yaxis_opts=opts.AxisOpts(
    #             min_=-200,  # 设置 Y 轴最小值
    #             max_=500,  # 设置 Y 轴最大值
    #             interval=50,  # 设置 Y 轴刻度间隔
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#5BA5E7")  # 设置 Y 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#5BA5E7",font_size=16),  # 设置 Y 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=True,
    #                 linestyle_opts=opts.LineStyleOpts(
    #                     color="#5BA5E7",
    #                     opacity=0.2,  # 设置网格线透明度为 0.2
    #                 )
    #             ),
    #         ),
    #         xaxis_opts=opts.AxisOpts(
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#5BA5E7")  # 设置 X 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#5BA5E7",font_size=16),  # 设置 X 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=False  # 隐藏 X 轴网格线
    #             ),
    #         ),
    #     )
    # )

    # # 创建折线图，并将其样式与柱状图保持一致
    # line = (
    #     Line()
    #     .add_xaxis(x_data)  # 使用相同的 X 轴数据
    #     .add_yaxis(
    #         "负荷量",
    #         Load_real1.tolist(),
    #         is_smooth=True,
    #         z_level = 1,
    #         color="#E12F13",  # 使用与柱状图一致的颜色
    #     )  # 添加负荷量折线图
    #     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 隐藏数据标签
    #     .set_global_opts(
    #         yaxis_opts=opts.AxisOpts(
    #             min_=-200,  # 设置 Y 轴最小值，与柱状图一致
    #             max_=500,  # 设置 Y 轴最大值，与柱状图一致
    #             interval=50,  # 设置 Y 轴刻度间隔，与柱状图一致
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # 设置 Y 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # 设置 Y 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=True,
    #                 linestyle_opts=opts.LineStyleOpts(
    #                     color="#CCEDFF",
    #                     opacity=0.2,  # 设置网格线透明度为 0.2
    #                 )
    #             ),
    #         ),
    #         xaxis_opts=opts.AxisOpts(
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # 设置 X 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # 设置 X 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=False  # 隐藏 X 轴网格线
    #             ),
    #         ),
    #         legend_opts=opts.LegendOpts(is_show=False),  # 隐藏图例
    #     )
    # )

    # # 使用 Grid 将两个图表叠加
    # grid = (
    #     Grid(init_opts=opts.InitOpts(width="1180px", height="820px"))
    #     .add(line, grid_opts=opts.GridOpts())  # 添加折线图
    #     .add(bar, grid_opts=opts.GridOpts())  # 添加堆积柱状图
    # )

    # # 渲染图表并保存为 HTML 文件
    # grid.render(output_total2)


    # ## --------------------------------------------模块三绘图---------------------------------- ##
    # # 创建堆积柱状图
    # bar = (
    #     Bar()
    #     .add_xaxis(x_data)  # 添加 X 轴数据
    #     .add_yaxis("火电", Pmt_value2.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pmt
    #     .add_yaxis("风电", Ps_Pw2.tolist(), stack="stack1")  # 添加 Y 轴数据系列 P_w
    #     .add_yaxis("蓄电池充电", Pcha_value1.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pcaes_d
    #     .add_yaxis("蓄电池放电", Pdis_value1.tolist(), stack="stack1")  # 添加 Y 轴数据系列 Pcaes_g
    #     .add_yaxis("电网购电", ele_buy_value2.tolist(), stack="stack1")
    #     .add_yaxis("电网售电", ele_sell_value2.tolist(), stack="stack1") 
    #     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 隐藏数据标签
    #     .set_global_opts(
    #         title_opts=opts.TitleOpts(is_show=False),  # 隐藏标题
    #         legend_opts=opts.LegendOpts(is_show=True,textstyle_opts=opts.TextStyleOpts(font_size=16)),  # 隐藏图例
    #         yaxis_opts=opts.AxisOpts(
    #             min_=-200,  # 设置 Y 轴最小值
    #             max_=500,  # 设置 Y 轴最大值
    #             interval=50,  # 设置 Y 轴刻度间隔
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#5BA5E7")  # 设置 Y 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#5BA5E7",font_size=16),  # 设置 Y 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=True,
    #                 linestyle_opts=opts.LineStyleOpts(
    #                     color="#5BA5E7",
    #                     opacity=0.2,  # 设置网格线透明度为 0.2
    #                 )
    #             ),
    #         ),
    #         xaxis_opts=opts.AxisOpts(
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#5BA5E7")  # 设置 X 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#5BA5E7",font_size=16),  # 设置 X 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=False  # 隐藏 X 轴网格线
    #             ),
    #         ),
    #     )
    # )

    # # 创建折线图，并将其样式与柱状图保持一致
    # line = (
    #     Line()
    #     .add_xaxis(x_data)  # 使用相同的 X 轴数据
    #     .add_yaxis(
    #         "负荷量",
    #         Load_real2.tolist(),
    #         is_smooth=True,
    #         z_level = 1,
    #         color="#E12F13",  # 使用与柱状图一致的颜色
    #     )  # 添加负荷量折线图
    #     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 隐藏数据标签
    #     .set_global_opts(
    #         yaxis_opts=opts.AxisOpts(
    #             min_=-200,  # 设置 Y 轴最小值，与柱状图一致
    #             max_=500,  # 设置 Y 轴最大值，与柱状图一致
    #             interval=50,  # 设置 Y 轴刻度间隔，与柱状图一致
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # 设置 Y 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # 设置 Y 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=True,
    #                 linestyle_opts=opts.LineStyleOpts(
    #                     color="#CCEDFF",
    #                     opacity=0.2,  # 设置网格线透明度为 0.2
    #                 )
    #             ),
    #         ),
    #         xaxis_opts=opts.AxisOpts(
    #             axisline_opts=opts.AxisLineOpts(
    #                 linestyle_opts=opts.LineStyleOpts(color="#CCEDFF")  # 设置 X 轴线条颜色为白色
    #             ),
    #             axislabel_opts=opts.LabelOpts(color="#CCEDFF"),  # 设置 X 轴标签颜色为白色
    #             splitline_opts=opts.SplitLineOpts(
    #                 is_show=False  # 隐藏 X 轴网格线
    #             ),
    #         ),
    #         legend_opts=opts.LegendOpts(is_show=False),  # 隐藏图例
    #     )
    # )

    # # 使用 Grid 将两个图表叠加
    # grid = (
    #     Grid(init_opts=opts.InitOpts(width="1180px", height="820px"))
    #     .add(line, grid_opts=opts.GridOpts())  # 添加折线图
    #     .add(bar, grid_opts=opts.GridOpts())  # 添加堆积柱状图
    # )

    # # 渲染图表并保存为 HTML 文件
    # grid.render(output_total3)

    ##--------------------------------------------结果数据处理----------------------------------
    # 数据数值化处理（保留两位小数）
    # 火电（3×24）
    Pmt_value = [
        [round(Pmt[k][0].solution_value, 2) for k in range(24)],
        [round(Pmt[k][1].solution_value, 2) for k in range(24)],
        [round(Pmt[k][2].solution_value, 2) for k in range(24)]
    ]

    # 储能系统（1×24）
    Pcaes_d_value = [round(-Pcaes_d[k].solution_value, 2) for k in range(24)]  # 放电为正
    Pcaes_g_value = [round(-Pcaes_g[k].solution_value, 2) for k in range(24)]  # 充电为负

    # 抽水蓄能（1×24）
    Pgen_value = [round(-Pgen[k].solution_value, 2) for k in range(24)]  # 发电量取正
    Ppm_value = [round(-Ppm[k].solution_value, 2) for k in range(24)]

    # 氢能系统（1×24）
    Pfc_value = [round(-Pfc[k].solution_value, 2) for k in range(24)]  # 燃料电池放电为正
    Pel_value = [round(-Pel[k].solution_value, 2) for k in range(24)]  # 电解槽电量为正

    # 蓄电池（2×24）
    Pcha_value = [
        [round(-Pcha[k][0].solution_value, 2) for k in range(24)],  # 充电为正
        [round(-Pcha[k][1].solution_value, 2) for k in range(24)]
    ]
    Pdis_value = [
        [round(-Pdis[k][0].solution_value, 2) for k in range(24)],  # 放电为正
        [round(-Pdis[k][1].solution_value, 2) for k in range(24)]
    ]

    # 可再生能源（风电3×24，光伏2×24）
    Ps_Pw = [
        [round(P_w[k][0].solution_value, 2) for k in range(24)],
        [round(P_w[k][1].solution_value, 2) for k in range(24)],
        [round(P_w[k][2].solution_value, 2) for k in range(24)]
    ]
    Ps_Ppv = [
        [round(P_pv[k][0].solution_value, 2) for k in range(24)],
        [round(P_pv[k][1].solution_value, 2) for k in range(24)]
    ]

    # 电力交易（3×24）
    ele_buy_value = [
        [round(ele_buy[k][0].solution_value, 2) for k in range(24)],
        [round(ele_buy[k][1].solution_value, 2) for k in range(24)],
        [round(ele_buy[k][2].solution_value, 2) for k in range(24)]
    ]
    ele_sell_value = [
        [round(-ele_sell[k][0].solution_value, 2) for k in range(24)],  # 售电量为正
        [round(-ele_sell[k][1].solution_value, 2) for k in range(24)],
        [round(-ele_sell[k][2].solution_value, 2) for k in range(24)]
    ]

    Load_value = [
        [round(Load_real[k], 2) for k in range(24)],
        [round(Load_real1[k], 2) for k in range(24)],
        [round(Load_real2[k], 2) for k in range(24)]
    ]

    # 读取并更新JSON文件（其余部分保持不变）
    with open("database.json", "r") as json_file:
        data = json.load(json_file)

    # 更新JSON数据结构（修正键值对应关系）
    data.update({
        "Pmt": Pmt_value,          # 火电出力（3×24）
        "Pcaes_d": Pcaes_d_value,  # CAES放电（1×24）
        "Pcaes_g": Pcaes_g_value,  # CAES充电（1×24）
        "Pgen": Pgen_value,        # 抽水蓄能发电（1×24）
        "Ppm": Ppm_value,          # 抽水蓄能抽水（1×24）
        "Pfc": Pfc_value,          # 氢燃料电池出力（1×24）
        "Pel": Pel_value,          # 电解槽用电（1×24）
        "Pcha": Pcha_value,        # 蓄电池充电（2×24）
        "Pdis": Pdis_value,        # 蓄电池放电（2×24）
        "P_w": Ps_Pw,              # 风电出力（3×24）
        "P_pv": Ps_Ppv,            # 光伏出力（2×24）
        "Pgrid_buy": ele_buy_value,  # 电网购电（3×24）
        "Pgrid_sell": ele_sell_value,# 电网售电（3×24）
        'total_value': value       ,# 最优成本
        'Load_real': Load_value     # 实际负荷
    })

    # 将更新后的数据写回JSON文件
    with open("database.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


# 如果直接运行这个脚本，调用子函数
if __name__ == "__main__":
    run_solving()