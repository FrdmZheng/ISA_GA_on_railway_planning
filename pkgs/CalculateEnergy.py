from pkgs.IsAvailable import merge_lists_by_first_two_columns
from pkgs.IsAvailable import merge_rows_by_first_two_columns

def Calculate_Energy(schedule, demands, limitations, ts, Cms, graph, miu1, miu2, miu3):
    """
    计算能量，即目标函数
    :param schedule: 编组计划
    :param demands: 运输需求
    :param limitations: 车站改编辆数限制
    :param ts: 车站改编一辆节省时间
    :param Cms: 车站集结车小时
    :param graph: 线网图
    :param miu1: 单位集结车小时成本
    :param miu2: 单位改编车数成本
    :param miu3: 单位路径消耗成本
    :return: [是否满足约束条件, 总成本]
    """

    s_d = merge_lists_by_first_two_columns(schedule, demands)
    s_d = sorted(s_d, key=lambda x: x[0], reverse=True)

    # 计算该方案的路径消耗
    sum3 = 0
    for lst in s_d:
        path = lst[2]
        for i in range(len(path) - 1):
            sum3 += [v for k, v in graph[path[i]] if k==path[i+1]][0] * miu3 * lst[4]

    # 计算该方案集结消耗
    sum1 = 0
    templst = [[row[0], row[3], row[4]] for row in s_d]
    templst = merge_rows_by_first_two_columns(templst)
    for i in Cms.keys():
        sum1 += sum(1 for row in templst if row[0] == i) * Cms[i] * miu1

    # 判断方案是否可行
    demands_lim = dict.fromkeys(limitations, 0)  # 每个站需要改编的车数
    for lst in s_d:
        path = lst[2]
        if lst[3] != path[-1]:
            demands_lim[lst[3]] = demands_lim[lst[3]] + lst[4]
            for i in range(len(s_d)):
                if (s_d[i][0] == lst[3]) and (s_d[i][1] == lst[1]):
                    s_d[i][4] = s_d[i][4] + lst[4]

    for i in demands_lim.keys():
        if demands_lim[i] > limitations[i]:
            return [False, float('inf')]

    # 计算该方案改编消耗
    sum2 = 0
    for i in demands_lim.keys():
        sum2 += demands_lim[i] * ts[i] * miu2

    return [True, sum3 + sum2 + sum1]

if __name__ == '__main__':
    from pkgs.CreateIndividual import Create_Individual
    # 编组计划
    graph = {
        3: [(2, 4), (1, 2)],
        2: [(1, 5), (0, 10)],
        1: [(0, 3)],
        0: []
    }
    k_paths = 2
    schedule = Create_Individual(graph, k_paths)
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
           0: 600,}


    print(Calculate_Energy(schedule, demands, limitations, ts, Cms, graph, 1, 1, 1))
