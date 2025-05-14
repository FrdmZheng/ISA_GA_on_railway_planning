import random

def are_first_two_columns_equal(list1, list2):
    return len(list1) == len(list2) and all(r1[:2] == r2[:2] for r1, r2 in zip(list1, list2))

def eliten(better, worse, p=0.5):
    """
    精英学习操作
    :param better: 父代优秀个体
    :param worse: 父代较差个体
    :param p: 以p概率学习
    :return: [子代个体1, 子代个体2]
    """

    if len(better) != len(worse):
        print("染色体长度不等，不进行精英学习操作")
        return [better, worse]

    better = sorted(better, key=lambda x: (x[0], x[1]))
    worse = sorted(worse, key=lambda x: (x[0], x[1]))

    if not are_first_two_columns_equal(better, worse):
        print("染色体中基因不成对，不进行精英学习操作")
        return [better, worse]

    new_schedule = []
    for i in range(len(better)):
        if random.random() < p:
            new_schedule.append(better[i])
        else:
            new_schedule.append(worse[i])

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
    schedule1 = Create_Individual(graph, k_paths)
    schedule2 = Create_Individual(graph, k_paths)

    print(schedule1)
    print(schedule2)

    temp = eliten(schedule1, schedule2)
    print(temp)
