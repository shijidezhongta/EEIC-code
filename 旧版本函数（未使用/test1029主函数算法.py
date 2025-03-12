import numpy as np
import pandas as pd

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

# ---------------------------------
# 1. 参数和常数定义
# ---------------------------------

# 电池参数
BATTERY_CAPACITY = 500  # 电池容量 (kWh)
CHARGE_RATE = 100       # 最大充电速率 (kW)
DISCHARGE_RATE = 100    # 最大放电速率 (kW)
EFFICIENCY = 0.9        # 电池充放电效率

# 遗传算法参数
POPULATION_SIZE = 100     # 种群规模
GENERATIONS = 300        # 代数
CROSSOVER_RATE = 0.8     # 交叉概率
MUTATION_RATE = 0.1      # 变异概率

# 优化时间段和数据矩阵
TIME_PERIODS = 24
load_demand = np.random.randint(300, 600, TIME_PERIODS)  # 负荷需求 (kW)
price_matrix = np.random.uniform(0.1, 0.5, TIME_PERIODS)  # 电价矩阵 (每kWh价格)

# ------------------------变量定义-----------------------%
Pmt = np.random.uniform(50, 200, (1, 24))  # 燃气轮机出力
PP = np.random.uniform(0, 1, (1, 24)) #蓄电池SOC
Pel = np.random.uniform(0, 100, (1, 24))  # 电解槽耗电功率
Pfc = np.random.uniform(0, 100, (1, 24))  # 燃料电池耗电功率（实际为放电，所以是负值）
Pcha = np.random.uniform(0, 100, (1, 24))  # 电解槽耗电功率
Pdis = np.random.uniform(0, 100, (1, 24))  # 蓄电池放电功率
Temp_ps_pm = np.random.uniform(0, 1, (1, 24))  # 抽水蓄能抽水标志
Temp_ps_gen = np.random.uniform(0, 1, (1, 24))  # 抽水蓄能放电标志
Pgen = np.random.uniform(0, 100, (1, 24))  # 抽蓄放电
Ppm = np.random.uniform(0, 100, (1, 24))  # 抽蓄抽水
Vps = np.random.uniform(0, 100, (1, 24))  # 水库容量变化
need_to_stop_in = np.random.uniform(0, 1, (1, 24))  # 是否需要停机标志
need_to_stop_out = np.random.uniform(0, 1, (1, 24))  # 是否需要停机标志

# CAES部分
Pcaes_g = np.random.uniform(0, 100, (1, 24))  # CAES充电功率变量
Pcaes_d = np.random.uniform(0, 100, (1, 24))  # CAES放电功率变量
P_pv = np.random.uniform(0, 200, (1, 24))  # 光伏出力
P_w = np.random.uniform(0, 100, (1, 24))  # 风机出力

k1 = 1.4  # 绝热指数
Rg = 0.297  # 气体常数，单位是KJ/(kg·K)
rho = 1
tao_am = 15  # 环境温度，单位是摄氏度
tao_K = 273.15  # 绝对零度
tao_am = tao_am + tao_K  # 转换为绝对温度
tao_str = 40  # 热网出口温度
tao_str = tao_str + tao_K  # 转换为绝对温度
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
threshold = 1

# 软件中可改变的参数
Price_Pmt = 0.3  # 火力发电单价
Price_pv = 0.24  # 光伏单价
Price_w = 0.28   # 风能单价
Price_Pump_change = 0.5  # 抽水蓄能开停机价格
Price_CAES = 0.1  # 压缩空气储能单价
Price_H2 = 0.15  # 氢储能单价
Price_bat = 0.1  # 蓄电池储能单价
Price_CO2 = 1.5  # 碳交易机制碳成本系数

Demand_re = 1  # 是否考虑需求响应，考虑为1，不考虑为0
Carbon_Tra = 0  # 是否考虑碳约束，考虑为1，不考虑为0

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

# ---------------------------------
# 2. 约束条件函数
# ---------------------------------

def apply_constraints(schedule):
    
    for k in range(24):   #功率平衡约束
        if np.abs(P_pv[k] + P_w[k] + Pmt[k] - Pfc[k] - Pdis[k] - Pgen[k] - Pcaes_d[k] - Load_real[k] + Pel[k] + Pcha[k] + Ppm[k] + Pcaes_g[k]) <= threshold:
    
    # soc = 0  # 初始化电池的SOC (State of Charge, kWh)
    for t in range(TIME_PERIODS):
        # 限制单个时间段内的充电和放电功率
        if schedule[t] > CHARGE_RATE:
            schedule[t] = CHARGE_RATE
        elif schedule[t] < -DISCHARGE_RATE:
            schedule[t] = -DISCHARGE_RATE

        # 计算电池能量，应用电池效率
        energy_change = schedule[t] * EFFICIENCY if schedule[t] > 0 else schedule[t] / EFFICIENCY
        soc += energy_change

        # 保证SOC在0和电池容量之间
        if soc > BATTERY_CAPACITY:
            energy_excess = soc - BATTERY_CAPACITY
            schedule[t] -= energy_excess / EFFICIENCY if schedule[t] > 0 else energy_excess * EFFICIENCY
            soc = BATTERY_CAPACITY
        elif soc < 0:
            energy_shortage = -soc
            schedule[t] += energy_shortage / EFFICIENCY if schedule[t] < 0 else energy_shortage * EFFICIENCY
            soc = 0
    return schedule

# ---------------------------------
# 3. 遗传算法函数
# ---------------------------------

# 初始化种群
def initialize_population():
    return [np.random.uniform(-DISCHARGE_RATE, CHARGE_RATE, TIME_PERIODS) for _ in range(POPULATION_SIZE)]

# 适应度函数：计算成本
def fitness(schedule):
    adjusted_schedule = apply_constraints(schedule)
    cost = np.sum(adjusted_schedule * price_matrix)  # 充放电成本
    penalty = np.sum(np.maximum(load_demand + adjusted_schedule, 0))  # 负荷满足度
    return cost + penalty

# 选择：轮盘赌选择法
def selection(population, fitness_scores):
    total_fitness = np.sum(fitness_scores)
    pick = np.random.rand() * total_fitness
    current = 0
    for individual, score in zip(population, fitness_scores):
        current += score
        if current > pick:
            return individual

# 交叉：单点交叉
def crossover(parent1, parent2):
    if np.random.rand() < CROSSOVER_RATE:
        point = np.random.randint(1, TIME_PERIODS - 1)
        child1 = np.concatenate((parent1[:point], parent2[point:]))
        child2 = np.concatenate((parent2[:point], parent1[point:]))
        return child1, child2
    return parent1, parent2

# 变异
def mutate(schedule):
    for i in range(TIME_PERIODS):
        if np.random.rand() < MUTATION_RATE:
            schedule[i] += np.random.uniform(-10, 10)
    return schedule

# 主遗传算法过程
def genetic_algorithm():
    population = initialize_population()
    
    for generation in range(GENERATIONS):
        fitness_scores = np.array([fitness(ind) for ind in population])
        next_population = []
        
        # 选择、交叉和变异
        for _ in range(POPULATION_SIZE // 2):
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            next_population.extend([mutate(child1), mutate(child2)])
        
        population = next_population
        
        # 输出当前代的最佳个体
        best_fitness = np.min(fitness_scores)
        best_schedule = population[np.argmin(fitness_scores)]
        # print(f"Generation {generation + 1}: Best Cost = {best_fitness}")
    
    # 最终的最佳结果
    best_fitness = np.min(fitness_scores)
    best_schedule = population[np.argmin(fitness_scores)]
    return best_schedule, best_fitness

# 执行遗传算法
best_schedule, best_fitness = genetic_algorithm()
print("最佳调度策略：", best_schedule)
print("最低成本：", best_fitness)
