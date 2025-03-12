def Model_solving():
    import cvxpy as cp
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import json
    import main

    # #新增加的两行
    # import matplotlib
    # matplotlib.rc("font",family='DengXian')

    def ElasticityMatrix(P):
        """
        构造需求弹性矩阵，基于电价分布（P）
        数据来源：《需求侧响应理论模型与应用研究_曾鸣》
        
        参数：
        P - 24小时的电价数组
        
        返回：
        Z - 需求弹性矩阵 (24x24)
        """
        Z = np.zeros((24, 24))  # 初始化24x24的需求弹性矩阵

        for i in range(23):
            if P[i] == np.min(P):  # 谷时段
                for j in range(23):
                    if P[j] == np.min(P):
                        Z[i, j] = -0.1
                    elif P[j] == np.max(P):
                        Z[i, j] = 0.012
                    else:
                        Z[i, j] = 0.01
            elif P[i] == np.max(P):  # 峰时段
                for j in range(23):
                    if P[j] == np.min(P):
                        Z[i, j] = 0.012
                    elif P[j] == np.max(P):
                        Z[i, j] = -0.1
                    else:
                        Z[i, j] = 0.016
            else:  # 平时段
                for j in range(23):
                    if P[j] == np.min(P):
                        Z[i, j] = 0.01
                    elif P[j] == np.max(P):
                        Z[i, j] = 0.016
                    else:
                        Z[i, j] = -0.1

        return Z

    def IBDR(Z_SL, Z_CL, load, p_a, p_b, W2, W3):
        """
        价格型需求响应优化函数
        
        参数：
        Z_SL - 转移负荷弹性矩阵
        Z_CL - 消减负荷弹性矩阵
        load - 负荷数据 (24小时)
        p_a - 需求响应后电价
        p_b - 需求响应前电价
        W2 - 可转移负荷占比
        W3 - 可消减负荷占比
        
        返回：
        Psl - 转移负荷量
        Pcl - 消减负荷量
        """
        
        Psl = np.zeros(24)  # 初始化转移负荷量
        Pcl = np.zeros(24)  # 初始化消减负荷量
        
        # 计算转移负荷量
        for i in range(23):
            sum1 = 0
            for j in range(23):
                sum1 += Z_SL[i, j] * ((p_a[j] - p_b[j]) / p_b[j])  # 可转移系数
            Psl[i] = W2 * load[i] * sum1
        
        # 计算消减负荷量
        for i in range(23):
            sum2 = 0
            for j in range(23):
                sum2 += Z_CL[i, j] * ((p_a[j] - p_b[j]) / p_b[j])  # 可消减系数
            
            if sum2 > 0:  # 消减发生在价格上涨时
                sum2 = 0
            else:
                Pcl[i] = W3 * load[i] * sum2
        
        return Psl, Pcl

    # ------------------------变量定义-----------------------%
    Pmt = cp.Variable(24)  # 燃气轮机出力
    Phss = cp.Variable(24)  # 氢储能出力
    Pbat = cp.Variable(24)  # 蓄电池出力
    Temp_el = cp.Variable(24, boolean=True)  # 氢储能充电标志（电解槽工作标志）
    Temp_fc = cp.Variable(24, boolean=True)  # 氢储能放电标志（燃料电池工作标志）
    Temp_Hstatic = cp.Variable(24, boolean=True)  # 氢储能系统静置标志
    Temp_cha = cp.Variable(24, boolean=True)  # 蓄电池充电标志
    Temp_dis = cp.Variable(24, boolean=True)  # 蓄电池放电标志
    Temp_static = cp.Variable(24, boolean=True)  # 蓄电池静置标志
    PP = cp.Variable(24) #蓄电池SOC
    Pel = cp.Variable(24)  # 电解槽耗电功率
    Pfc = cp.Variable(24)  # 燃料电池耗电功率（实际为放电，所以是负值）
    Pcha = cp.Variable(24)  # 电解槽耗电功率
    Pdis = cp.Variable(24)  # 蓄电池放电功率
    Pps = cp.Variable(24)  # 抽水蓄能出力
    Temp_ps_pm = cp.Variable(24, boolean=True)  # 抽水蓄能抽水标志
    Temp_ps_gen = cp.Variable(24, boolean=True)  # 抽水蓄能放电标志
    Temp_ps_Hstatic = cp.Variable(24, boolean=True)  # 抽水蓄能系统静置标志
    Pgen = cp.Variable(24)  # 抽蓄放电
    Ppm = cp.Variable(24)  # 抽蓄抽水
    Vps = cp.Variable(24)  # 水库容量变化
    need_to_stop_in = cp.Variable(24, boolean=True)  # 是否需要停机标志
    need_to_stop_out = cp.Variable(24, boolean=True)  # 是否需要停机标志

    # CAES部分
    Pcaes_g = cp.Variable(24)  # CAES充电功率变量
    Pcaes_d = cp.Variable(24)  # CAES放电功率变量
    H_str = cp.Variable(24)  # 储热系统的储能状态（SOC）

    pr_st = cp.Variable(24)  # 储气罐的压力
    pr_st0 = cp.Variable(1)  # 初始压力
    y1 = cp.Variable(24)  # 线性化储气室压强约束
    h1 = cp.Variable(24)  # 线性化储热系统的储能状态（SOC）
    on_comp = cp.Variable(24, boolean=True)  # CAES压缩机的启停状态
    on_turb = cp.Variable(24, boolean=True)  # CAES涡轮机的启停状态
    qm_comp = cp.Variable(24)  # 压缩机的空气质量流量
    qm_turb = cp.Variable(24)  # 涡轮机的空气质量流量

    # 碳约束部分
    Ecfp = cp.Variable(24)  # 碳排放配额
    Emt = cp.Variable(24)  # 火力机组实际碳排放
    Ecet = cp.Variable(24)  # 参与碳市场交易的碳额
    Ccar = cp.Variable(24)  # 碳交易成本

    P_pv = cp.Variable(24)  # 光伏出力
    P_w = cp.Variable(24)  # 风机出力

    # -------------------------常量定义-----------------------%
    # 碳约束部分参数定义
    Be = 0.8159
    F1 = 1
    Fr = 0.934
    Ff = 1.087
    BB = 0.8
    kc = 1
    aa = 0.25
    cc = 0.25
    d = 30


    # CAES储能参数定义
    H_str0 = 0
    Vst = 2000  # 蓄气库的体积，单位是立方米
    k1 = 1.4  # 绝热指数
    Rg = 0.297  # 气体常数，单位是KJ/(kg·K)
    rho = 1
    tao_am = 15  # 环境温度，单位是摄氏度
    tao_K = 273.15  # 绝对零度
    tao_am = tao_am + tao_K  # 转换为绝对温度
    tao_str = 40  # 热网出口温度
    tao_str = tao_str + tao_K  # 转换为绝对温度
    tao_comp_in1 = tao_am * np.ones(24)  # 将环境温度乘以ones生成NT个相同值的温度向量，作为压缩机进口1的温度
    pr_am = 0.101 * 1e3  # 环境压力，单位是Kpa
    pr_st_min = 8.4 * 1e3  # 蓄气库最小压力，单位是Kpa
    pr_st_max = 9.0 * 1e3  # 蓄气库最大压力，单位是Kpa
    qm_comp_min = 0  # 压缩机最小空气质量流量
    qm_comp_max = 2.306 / 3.6  # 压缩机最大空气质量流量，单位是kg/s，相当于1MW CAES
    qm_turb_min = 0  # 涡轮机最小空气质量流量
    qm_turb_max = 8.869 / 3.6  # 涡轮机最大空气质量流量，单位是kg/s，相当于1MW CAES
    yita_comp = 0.80  # 压缩机效率
    yita_turb = 0.86  # 涡轮机效率
    Pcomp_min = np.zeros(1)  # 压缩机最小功率，Nc是压缩机阶段的数量
    Pcomp_max = 500 * np.ones(1)  # 压缩机最大功率，这里是500kW
    Pturb_min = np.zeros(1)  # 涡轮机最小功率，Ne是涡轮机的数量
    Pturb_max = 1000 * np.ones(1)  # 涡轮机最大功率，这里是1000kW
    pi_turb = [8.9, 8.9]
    beta_comp = [11.6, 8.15]
    y_comp1 = (beta_comp[0]) ** ((k1 - 1) / k1)  # 压缩机效率系数
    y_turb1 = (pi_turb[0]) ** (-(k1 - 1) / k1)
    tao_turb_in1 = (280 + tao_K) * np.ones(24)  # 将固定的280℃加上绝对零度转换为绝对温度，作为涡轮机进口1的温度

    # 常量
    Load = np.array([188.24, 183.01, 180.15, 179.01, 176.07, 178.39, 189.95, 228.85, 255.45, 276.35, 293.71, 282.57, 279.64, 266.31, 264.61, 264.61, 274.48, 303.93, 318.99, 338.11, 316.14, 273.87, 231.07, 194.04])

    # 光伏和风机出力
    random_Ppv = np.array([0, 0, 0, 0, 0, 50.37, 17.13, 29.40, 291.70, 240.07, 216.66, 250.34, 267.96, 327.72, 276.47, 206.05, 27.83, 0, 0, 0, 0, 0, 0, 0])
    random_Pw = np.array([56.10, 60, 18.14, 38.19, 31.28, 37.64, 35.97, 34.99, 57.96, 79.56, 67.68, 50.73, 46.61, 33.35, 45.27, 61.85, 43.55, 38.99, 25.81, 12.02, 12.25, 11.95, 14.06, 13.23])

    # 氢储能参数定义
    V = 100  # L
    R = 8.314  # J/(mol·K)
    T = 293  # K，即20℃
    n0 = 0.8  # mol
    M = 2  # g/mol
    pmin = 4  # Mpa
    pmax = 1000  # Mpa
    Pn = 300  # kW

    # 蓄电池参数定义
    Ebattery = 300
    soc0 = 0.5
    socmin = 0.3
    socmax = 0.95
    Pcs = 40
    POWER = 160

    # 抽水蓄能参数定义
    Ppsmax = 50  # kW
    Vpsmax = 100  # 最大容量变化
    Vpmax = 500  # 最大容量
    Vmin = 0.1  # 最低容量系数限制
    Vmax = 0.9  # 最大容量系数限制
    np1 = 0.55  # 容量系数
    start_ps = 0.5  # 启动成本
    stop_ps = 0.5  # 停机成本
    num_stops = 0  # 抽蓄停机次数
    C_number = 4  # 转换次数上限

    B = 1000

    # 读取 JSON 文件中的数据
    with open("database.json", "r") as json_file:
        data = json.load(json_file)

    # 从读取的数据中提取相应的参数值
    Price_Pmt = data.get("value_Pmt",0.3)  # 火力发电单价，默认值为 0.3
    Price_pv = data.get("value_pv", 0.24)   # 光伏单价，默认值为 0.24
    Price_w = data.get("value_w", 0.2)      # 风能单价，默认值为 0.2
    Price_Pump_change = data.get("value_Pump", 0.5)  # 抽水蓄能开停机价格，默认值为 0.5
    Price_CAES = data.get("value_CAES", 0.4)  # 压缩空气储能单价，默认值为 0.4
    Price_H2 = data.get("value_H2", 0.6)     # 氢储能单价，默认值为 0.6
    Price_bat = data.get("value_bat", 0.25)  # 蓄电池储能单价，默认值为 0.25
    Price_CO2 = data.get("value_CO2", 0.05)  # 碳交易机制碳成本系数，默认值为 0.05

    Demand_re = data.get("value_if_demand", 1)  # 是否考虑需求响应，默认值为 1
    Carbon_Tra = data.get("value_if_carbon", 1)  # 是否考虑碳约束，默认值为 1

    # 读取需求响应数据
    shuju = pd.read_excel('carbon+DR数据.xlsx').values  # 把一天划分为24小时
    pe_b = shuju[5, 1:24]  # 需求响应前电价
    pe_a = shuju[6, 1:24]  # 需求响应电价

    Z = np.zeros((24, 24))  # 需求弹性矩阵

    # 约束：固定、可转移、可消减、可替代负荷占比50%，30%，20%
    e_W1, e_W2, e_W3 = 0.5, 0.3, 0.2

    # 初始化电负荷量
    Psl_e = np.zeros(24)  # 转移电负荷量
    Pcl_e = np.zeros(24)  # 消减电负荷量
    OP_Load = np.zeros(24)  # 优化后的电负荷

    # Load: 假设你已经有这个负荷数据
    Load = np.array([188.24, 183.01, 180.15, 179.01, 176.07, 178.39, 189.95, 228.85, 255.45, 276.35, 
                    293.71, 282.57, 279.64, 266.31, 264.61, 264.61, 274.48, 303.93, 318.99, 338.11, 
                    316.14, 273.87, 231.07, 194.04])

    # DR-需求侧响应优化
    Z_e = ElasticityMatrix(pe_a)  # 电价需求弹性矩阵
    Z_e_CL = np.diag(np.diag(Z_e))  # 消减电负荷弹性矩阵, 对角阵
    Z_e_SL = Z_e - Z_e_CL  # 转移电负荷弹性矩阵

    # 价格型需求响应
    Psl_e, Pcl_e = IBDR(Z_e_SL, Z_e_CL, Load, pe_a, pe_b, e_W2, e_W3)

    # 优化后的电负荷
    OP_Load = Load + Psl_e + Pcl_e

    # 选择负荷
    if Demand_re == 1:
        Load_real = OP_Load
    else:
        Load_real = Load


    # 定义优化变量
    F_expr = cp.Variable()

    # ------------------------------主函数-------------------------#
    F_expr = cp.sum([
        Price_Pmt * Pmt[k] + Price_pv * P_pv[k] + Price_w * P_w[k] +
        Price_H2 * (cp.abs(Pel[k]) + cp.abs(Pfc[k])) +
        Price_bat * (cp.abs(Pcha[k]) + cp.abs(Pdis[k])) +
        Price_Pump_change * need_to_stop_in[k] +
        Price_Pump_change * need_to_stop_out[k] +
        Price_CAES * (cp.abs(Pcaes_g[k]) + cp.abs(Pcaes_d[k]))
        for k in range(24)
    ])

    # 约束条件列表
    constraints = []

    # 功率平衡约束
    for k in range(24):
        constraints.append(P_pv[k] + P_w[k] + Pmt[k] - Pfc[k] - Pdis[k] - Pgen[k] - Pcaes_d[k] == Load_real[k] + Pel[k] + Pcha[k] + Ppm[k] + Pcaes_g[k])

    # 电源侧约束
    for k in range(24):
        constraints.append(Pmt[k] >= 40)
        constraints.append(Pmt[k] <= 180)
        constraints.append(P_pv[k]>=0)
        constraints.append(P_w[k] >= 0)
        constraints.append(P_pv[k] <= random_Ppv[k])
        constraints.append(P_w[k] <= random_Pw[k])

    for k in range(24):  # 假设k的范围是0到22
        # 电解槽、燃料电池及静置情况的约束
        # constraints.append(-Pn <= Phss[k]) 
        constraints.append(0 <= Pel[k])
        constraints.append(-Pn <= Pfc[k]) # 基础功率约束
        # constraints.append(Phss[k] <= Pn)
        constraints.append(Pel[k] <= Pn)
        constraints.append( Pfc[k] <= 0) # 基础功率约束


    #压强（物质的量）上下限约束
    # constraints.append(pmin * V / (R * T) <= (n0 + cp.sum([0.8 * Pel[j] / 3.03 + 0.8 * Pfc[j] / 22.28 for j in range(k+1)])) / M)
    # constraints.append((n0 + cp.sum([0.8 * Pel[j] / 3.03 + 0.8 * Pfc[j] / 22.28 for j in range(k+1)])) / M <= pmax * V / (R * T))
    constraints.append(cp.sum(Pfc) == -cp.sum(Pel))


    # ----------------------压缩空气储能----------------------
    for kt in range(24):
        constraints.append(Pcaes_d <= 0)
        constraints.append(Pcaes_d >= -50)
        constraints.append(Pcaes_g <= 50)
        constraints.append(Pcaes_g >= 0)


    constraints.append(cp.sum(Pcaes_g) == -cp.sum(Pcaes_d))



    # ----------------------蓄电池储能----------------------
    for k in range(24):
        # constraints.append(-Pcs <= Pbat[k])
        constraints.append(0 <= Pcha[k])
        constraints.append(-Pcs <= Pdis[k])  # 蓄电池充放电约束, PCS功率是40kW
        # constraints.append (Pbat[k] <= Pcs)
        constraints.append (Pcha[k] <= Pcs)
        constraints.append ( Pdis[k] <= 0)  # 蓄电池充放电约束, PCS功率是40kW

        # 计算SOC
        for k in range(24):
            constraints.append(PP[k] == Pdis[k] + Pcha[k])
            constraints.append(Ebattery * (socmin - soc0) <= PP)  # SOC约束
            constraints.append(PP <= Ebattery * (socmax - soc0))  # SOC约束
    constraints.append(cp.sum(Pcha) == -cp.sum(Pdis))



    # ----------------------抽水蓄能约束----------------------
    for k in range(24):
        constraints.append(Ppm[k] >= 0)
        constraints.append(Pgen[k] <= 0)
        constraints.append(Pgen[k] >= -50)
        constraints.append(Ppm <= 50)
        constraints.append(0 <= Vps[k])  # 库容变化约束
        constraints.append(Vps[k] <= Vpsmax)  # 库容变化约束
        # if k > 0:
        #     constraints.append(Pgen[k-1] * Ppm[k] >= 0)
        #     constraints.append(Pgen[k] * Ppm[k-1] >= 0)
        constraints.append(Ppm[k] <= B * Temp_ps_pm[k])  # 如果充电，则 is_pumping[k] == 1
        constraints.append(Ppm[k] >=  1 - B * (1 - Temp_ps_pm[k]))  # 防止浮点误差，使用一个小正数   

        constraints.append(Pgen[k] >= - B * Temp_ps_gen[k])  # 如果放电
        constraints.append(Pgen[k] <=  1 + B * (1 - Temp_ps_gen[k]))  # 防止浮点误差，使用一个小正数 

    for k in range(24):
        if k > 0:
                constraints.append(Temp_ps_pm[k-1] + Temp_ps_gen[k] <= 1)
                constraints.append(Temp_ps_pm[k] + Temp_ps_gen[k-1] <= 1)
                constraints.append(need_to_stop_in[k] >= Temp_ps_pm[k-1] - Temp_ps_pm[k])
                constraints.append(need_to_stop_out[k] >= Temp_ps_gen[k-1] - Temp_ps_gen[k])
    constraints.append(cp.sum(Ppm) == -cp.sum(Pgen))


    # 总容量限制
    s1 = 0.5 * Vpmax
    for p in range(24):
        s1 += np1 * (Pgen[p] + Ppm[p])
        constraints.append(Vmin * Vpmax <= s1)
        constraints.append( s1 <= Vmax * Vpmax)

    constraints.append(sum(need_to_stop_in) + sum(need_to_stop_out) <= C_number)  # 转化次数小于指定次数

    # ----------------------储能占比----------------------
    Total_Charge_Discharge_Abs = cp.Variable(24)
    Hydrogen_Storage_Total_Abs = cp.Variable(24)
    Pumped_Storage_Total_Abs = cp.Variable(24)
    Battery_Total_Abs = cp.Variable(24)
    CAES_Total_Abs = cp.Variable(24)

    # 计算各储能系统充电和放电量的绝对值之和
    for k in range(24):
        constraints.append(Total_Charge_Discharge_Abs[k] == Pel[k] - Pfc[k] + Pcha[k] - Pdis[k] - Pcaes_d[k] + Pcaes_g[k] + Ppm[k] - Pgen[k])
    # 计算抽水蓄能充电和放电量的绝对值之和
    for k in range(24):
        constraints.append(Pumped_Storage_Total_Abs[k] == Ppm[k] -Pgen[k] )
    # 蓄电池充放电量的绝对值之和
    for k in range(24):
        constraints.append(Battery_Total_Abs[k] == Pcha[k] - Pdis[k])
    # 氢储能系统充放电量的绝对值之和
    for k in range(24):
        constraints.append(Hydrogen_Storage_Total_Abs[k] ==  Pel[k] - Pfc[k])
    # 压缩空气储能系统（CAES）充放电量的绝对值之和
    for k in range(24):
        constraints.append(CAES_Total_Abs[k] == Pcaes_g[k] - Pcaes_d[k])
    # 添加约束：抽水蓄能占总充电量和放电量的比例不超过47%
    constraints.append(cp.sum(Pumped_Storage_Total_Abs) <= 0.47 * cp.sum(Total_Charge_Discharge_Abs))
    # 添加约束：蓄电池占总充电量和放电量的比例不超过24%
    constraints.append(cp.sum(Battery_Total_Abs) <= 0.3 * cp.sum(Total_Charge_Discharge_Abs))
    # 添加约束：氢储能占总充电量和放电量的比例不超过17%
    constraints.append(cp.sum(Hydrogen_Storage_Total_Abs) <= 0.27 * cp.sum(Total_Charge_Discharge_Abs))
    # 添加约束：压缩空气储能占总充电量和放电量的比例不超过12%
    constraints.append(cp.sum(CAES_Total_Abs) <= 0.2 * cp.sum(Total_Charge_Discharge_Abs))

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


    # 定义优化问题
    problem = cp.Problem(cp.Minimize(F_expr), constraints)

    # 求解问题
    problem.solve(solver=cp.SCIP)

    # 输出结果
    print("Optimal cost:", F_expr.value)

    ##--------------------------------------------结果数据处理----------------------------------
    # 数据数值化处理
    Pfc_value = np.zeros(24)
    Pel_value = np.zeros(24)
    Pmt_value = np.zeros(24)
    Pcaes_d_value = np.zeros(24)
    Pcaes_g_value = np.zeros(24)
    Pdis_value = np.zeros(24)
    Pcha_value = np.zeros(24)
    Pgen_value = np.zeros(24)
    Ppm_value = np.zeros(24)
    Ps_Pw = np.zeros(24)
    Ps_Ppv = np.zeros(24)

    for i in range(24):
        Pfc_value[i] = Pfc[i].value
        Pel_value[i] = Pel[i].value
        Pmt_value[i] = Pmt[i].value
        Pcaes_d_value[i] = Pcaes_d[i].value
        Pcaes_g_value[i] = Pcaes_g[i].value
        Pdis_value[i] = Pdis[i].value
        Pcha_value[i] = Pcha[i].value
        Pgen_value[i] = Pgen[i].value
        Ppm_value[i] = Ppm[i].value
        Ps_Pw[i] = P_w[i].value
        Ps_Ppv[i] = P_pv[i].value

    # 数据准备
    labels = ['火电', '风电', '光伏', '氢储能放电', '氢储能充电', '蓄电池放电', '蓄电池充电', '抽水蓄能放电', '抽水蓄能充电', '压缩空气放电', '压缩空气充电']
    ST = np.array([Pmt_value, Ps_Pw, Ps_Ppv, -Pfc_value, -Pel_value, -Pdis_value, -Pcha_value, -Pgen_value, -Ppm_value, -Pcaes_d_value, -Pcaes_g_value])

    data_Load = np.zeros((24, 2))
    for i in range(24):
        data_Load[i][:] = [i, Load_real[i]]

    # 替换 JSON 数据中的值，并保留两位小数（固定格式）
    data['Pfc'] = [float(f"{x:.2f}") for x in Pfc_value]
    data['Pel'] = [float(f"{x:.2f}") for x in Pel_value]
    data['Pmt'] = [float(f"{x:.2f}") for x in Pmt_value]
    data['Pcaes_d'] = [float(f"{x:.2f}") for x in Pcaes_d_value]
    data['Pcaes_g'] = [float(f"{x:.2f}") for x in Pcaes_g_value]
    data['Pdis'] = [float(f"{x:.2f}") for x in Pdis_value]
    data['Pcha'] = [float(f"{x:.2f}") for x in Pcha_value]
    data['Pgen'] = [float(f"{x:.2f}") for x in Pgen_value]
    data['Ppm'] = [float(f"{x:.2f}") for x in Ppm_value]
    data['P_w'] = [float(f"{x:.2f}") for x in Ps_Pw]
    data['P_pv'] = [float(f"{x:.2f}") for x in Ps_Ppv]
    data['Load_real'] = [float(f"{x:.2f}") for x in Load_real]

    # 替换 total_value
    if isinstance(F_expr.value, (list, np.ndarray)):
        data['total_value'] = [float(f"{x:.2f}") for x in F_expr.value]
    else:
        data['total_value'] = float(f"{F_expr.value:.2f}")

    # 保存修改后的 JSON 数据
    with open("database.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

def Translate_plot(axes):
    import plot
    plot.plot_matplotlib(axes)

