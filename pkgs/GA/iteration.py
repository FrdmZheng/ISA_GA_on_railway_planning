from pkgs.CalculateEnergy import Calculate_Energy
from pkgs.GA.eliten import eliten
from pkgs.GA.chiasma import chiasma
from pkgs.GA.variation import variation

import math
import random


def roulette_wheel_selection(fitness):
    # 计算适应度总和
    sum_fitness = sum(fitness)
    # 计算选择概率
    probabilities = [f / sum_fitness for f in fitness]
    # 构造累积概率分布
    cumulative_probabilities = []
    cumulative_sum = 0
    for p in probabilities:
        cumulative_sum += p
        cumulative_probabilities.append(cumulative_sum)
    # 选择两个个体（例如）
    parents_index = []
    for _ in range(2):  # 假设我们需要选择两个父母
        r = random.random()
        for index, cp in enumerate(cumulative_probabilities):
            if r <= cp:
                parents_index.append(index)
                break
    return parents_index

def genetic_iter(energylst, demands, limitations, ts, Cms, graph, miu1, miu2, miu3, p1, p2, p3, k_paths=3, times=50):
    """
    遗传算法迭代
    :param energylst: [[schedule, energy], ...]
    :param demands: 运输需求
    :param limitations: 改变限制
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
    :return: 新的energylst
    """

    n = len(energylst)
    m = math.ceil(n / 2)
    '''
    n = len(schedule_lst)
    m = math.ceil(n / 2)
    energylst = []
    for schedule in schedule_lst:
        energy = Calculate_Energy(schedule, demands, limitations, ts, Cms, graph, miu1, miu2, miu3)[1]
        energylst.append([schedule, energy])

    energylst = sorted(energylst, key=lambda x: x[1])
    '''

    # 精英学习
    for i in range(n - m):
        for j in range(times):
            result = eliten(energylst[random.randint(0, m - 1)][0], energylst[i][0], p1)
            energy = Calculate_Energy(result, demands, limitations, ts, Cms, graph, miu1, miu2, miu3)
            if energy[0]:
                energylst[i+m] = [result, energy[1]]
                break

    # 交叉
    new_energylst = []
    fitness = [1/x[1] for x in energylst]
    for i in range(times):
        parents_index = roulette_wheel_selection(fitness)
        results = chiasma(energylst[parents_index[0]][0], energylst[parents_index[1]][0], p2)
        for result in results:
            energy = Calculate_Energy(result, demands, limitations, ts, Cms, graph, miu1, miu2, miu3)
            if energy[0]:
                new_energylst.append([result, energy[1]])
        if len(new_energylst) >= n:
            break
    if len(new_energylst) > n:
        new_energylst = new_energylst[:n-1]
    if len(new_energylst) < n:
        for i in range(n - len(new_energylst)):
            new_energylst.append(energylst[i])

    # 变异
    for i in range(len(new_energylst)):
        result = variation(new_energylst[i][0], graph, p=p3, k_paths=k_paths)
        energy = Calculate_Energy(result, demands, limitations, ts, Cms, graph, miu1, miu2, miu3)
        if energy[0]:
            new_energylst[i] = [result, energy[1]]
        else:
            new_energylst[i] = [result, energy[1]]

    return new_energylst

if __name__ == '__main__':
    import copy
    from pkgs.CreateIndividual import Create_Individual

    # 编组计划
    graph = {
        3: [(2, 4), (1, 2)],
        2: [(1, 5), (0, 10)],
        1: [(0, 3)],
        0: []
    }
    k_paths = 2

    # 运输需求
    demands = [[1, 0, 100],
               [2, 0, 50],
               [2, 1, 150],
               [3, 0, 80],
               [3, 1, 120],
               [3, 2, 100]]
    # 解编限制
    limitations = {3: 300,
                   2: 400,
                   1: 200,
                   0: 250}

    # 车站改编节省时间
    ts = {3: 3,
          2: 3,
          1: 3,
          0: 3}

    # 车站集结车小时
    Cms = {3: 600,
           2: 600,
           1: 600,
           0: 600, }

    energylst = []
    for i in range(10):
        schedule = Create_Individual(graph, k_paths)
        energy = Calculate_Energy(schedule, demands, limitations, ts, Cms, graph, 1, 1, 1)
        if energy[0]:
            energylst.append([schedule, energy[1]])
    print(energylst)
    print(genetic_iter(copy.deepcopy(energylst), demands, limitations, ts, Cms, graph, 1, 1, 1, 0.5, 0.5, 0.5, k_paths=2, times=50))
