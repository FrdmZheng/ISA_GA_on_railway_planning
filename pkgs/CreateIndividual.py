from pkgs.Kpath import random_k_shortest_paths
import random

def Create_Individual(graph, k):
    """
    生成一个个体（即一个编组计划）
    :param graph: 线网图
    :param k: 生成路径，去最短的k个，随机选取一个作为初始路径
    :return: [[i, j, path, plan], ...]
    """

    starts = []
    ends = []
    paths = []
    plans = []

    keys = sorted(graph.keys())
    for idx_i, i in enumerate(keys):
        for j in keys[:idx_i]:  # 只取比当前i小的j
            pathlist = random_k_shortest_paths(graph, i, j, k, num_attempts=100, verbose=False)
            if (len(pathlist) != 0):
                starts.append(i)
                ends.append(j)
                path = pathlist[random.randint(0, len(pathlist)-1)][1]
                paths.append(path)
                plan = path[random.randint(1, len(path)-1)]
                plans.append(plan)

    results = []
    for i in range(len(starts)):
        results.append([starts[i], ends[i], paths[i], plans[i]])

    return results

if __name__ == "__main__":
    # 示例图：邻接表形式
    graph = {
        3: [(2, 4), (1, 2)],
        2: [(1, 5), (0, 10)],
        1: [(0, 3)],
        0: []
    }

    k_paths = 2

    results = Create_Individual(graph, k_paths)
    print(results)

