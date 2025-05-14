import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import math
import random
import copy
from pkgs.GA.iteration import genetic_iter
from pkgs.CreateIndividual import Create_Individual
from pkgs.CalculateEnergy import Calculate_Energy

def ISA(T, minT, demands, limitations, ts, Cms, graph, miu1, miu2, miu3, p1, p2, p3, k_paths=2, times=50, n_individuals=20):
    """
    模拟退火算法
    :param T: 初始温度
    :param minT: 结束温度
    :param demands: 运输需求
    :param limitations: 改编限制
    :param ts: 改编节省时间
    :param Cms: 集结时间
    :param graph: 线网图
    :param miu1: 单位集结车小时成本
    :param miu2: 单位改编车数成本
    :param miu3: 单位路径消耗成本
    :param p1: 每个染色体精英学习概率
    :param p2: 每个染色体交叉概率
    :param p3: 每个染色体变异概率
    :param k_path: 生成的k个最小路径
    :param times: 最大尝试次数
    :param n_individuals: 每代中有多少个个体
    :return: [schedule, energy]
    """

    # 生成初始解
    energylst = []
    while True:
        schedule = Create_Individual(graph, k_paths)
        energy = Calculate_Energy(schedule, demands, limitations, ts, Cms, graph, 1, 1, 1)
        if energy[0]:
            energylst.append([schedule, energy[1]])
        if len(energylst) >= n_individuals :
            break

    # 目标函数列表
    fs = []
    mins = []
    i = 0
    while True:
        i += 1
        father_f = (sum([row[1] for row in energylst]) / len([row[1] for row in energylst]) + min(row[1] for row in energylst)) / 2
        new_energylst = genetic_iter(copy.deepcopy(energylst), demands, limitations, ts, Cms, graph, miu1, miu2, miu3, p1, p2, p3, k_paths=k_paths, times=times)
        son_f = (sum([row[1] for row in new_energylst]) / len([row[1] for row in new_energylst]) + min(row[1] for row in new_energylst)) / 2
        if son_f <= father_f:
            energylst = copy.deepcopy(new_energylst)
            fs.append(son_f)
            mins.append(min(row[1] for row in new_energylst))
        elif math.exp(father_f - son_f)/T > random.random():
            energylst = copy.deepcopy(new_energylst)
            fs.append(son_f)
            mins.append(min(row[1] for row in new_energylst))
        else:
            fs.append(father_f)
            mins.append(min(row[1] for row in energylst))
        print(f"第{i}次迭代的目标函数值为：{fs[-1]}")
        T = 0.998 * T
        if T < minT:
            break

    print(f"一共跑了{i}次")
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, i + 1), fs, color='blue', linestyle='-', linewidth=2, label='平均成本和最小成本的均值')
    plt.title("目标函数")
    plt.xlabel("迭代次数")
    plt.ylabel("成本")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(8, 4))
    plt.plot(range(1, i + 1), mins, color='blue', linestyle='-', linewidth=2, label='最小成本')
    plt.title("最小成本")
    plt.xlabel("迭代次数")
    plt.ylabel("成本")
    plt.legend()
    plt.grid(True)
    plt.show()

    schedule_energy = min(energylst, key=lambda row: row[1])

    return schedule_energy

if __name__ == '__main__':
    # 初始温度及结束温度
    T, minT = 500, 10
    # 成本系数及概率系数
    miu1, miu2, miu3 = 1, 1, 1
    p1, p2, p3 = 0.8, 0.5, 0.2
    # 线网图
    graph = {
        4: [(3, 2), (2, 5)],
        3: [(2, 2), (1, 4)],
        2: [(1, 5), (0, 10)],
        1: [(0, 3)],
        0: []
    }

    # 运输需求
    demands = [[1, 0, 100],
               [2, 0, 50],
               [2, 1, 150],
               [3, 0, 80],
               [3, 1, 120],
               [3, 2, 100],
               [4, 3, 60],
               [4, 2, 80],
               [4, 1, 100],
               [4, 0, 120]]
    # 解编限制
    limitations = {4: 250,
                   3: 300,
                   2: 400,
                   1: 200,
                   0: 250}

    # 车站改编节省时间
    ts = {4: 3,
          3: 4,
          2: 3,
          1: 2,
          0: 3}

    # 车站集结车小时
    Cms = {4: 500,
           3: 600,
           2: 700,
           1: 650,
           0: 600, }

    print(ISA(T, minT, demands, limitations, ts, Cms, graph, miu1, miu2, miu3, p1, p2, p3, k_paths=5, times=50, n_individuals=20))