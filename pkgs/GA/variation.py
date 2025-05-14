import random
from pkgs.Kpath import random_k_shortest_paths

def variation(schedule, graph, p=0.5, k_paths=1):
    """
    变异操作
    :param schedule: 父代编组计划
    :param p: 变异概率
    :param graph: 线网图
    :param k_paths: 最小线路
    :return: 子代编组计划
    """
    new_schedule = []
    for lst in schedule:
        new_lst = []
        if random.random() < p:
            new_lst.append(lst[0])
            new_lst.append(lst[1])
            k_shortest_paths = random_k_shortest_paths(graph, lst[0], lst[1], k=k_paths)
            new_lst.append(k_shortest_paths[random.randint(0, len(k_shortest_paths)-1)][1])
            new_lst.append(new_lst[2][random.randint(1, len(new_lst[2])-1)])
            new_schedule.append(new_lst)
        else:
            new_schedule.append(lst)

    return new_schedule

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

    print(schedule)
    temp = variation(schedule, graph, k_paths=2)
    print(temp)
