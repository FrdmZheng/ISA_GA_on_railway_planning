import random

def are_first_two_columns_equal(list1, list2):
    return len(list1) == len(list2) and all(r1[:2] == r2[:2] for r1, r2 in zip(list1, list2))

def chiasma(schedule1, schedule2, p=0.5):
    """
    交叉操作
    :param schedule1: 父代个体1
    :param schedule2: 父代个体2
    :param p: 以p概率交叉
    :return: [子代个体1, 子代个体2]
    """

    if len(schedule1) != len(schedule2):
        print("染色体长度不等，不进行交叉操作")
        return [schedule1, schedule2]

    schedule1 = sorted(schedule1, key=lambda x: (x[0], x[1]))
    schedule2 = sorted(schedule2, key=lambda x: (x[0], x[1]))

    if not are_first_two_columns_equal(schedule1, schedule2):
        print("染色体中基因不成对，不进行交叉操作")
        return [schedule1, schedule2]

    new_schedule1 = []
    new_schedule2 = []

    for i in range(len(schedule1)):
        if random.random() < p:
            new_schedule1.append(schedule2[i])
            new_schedule2.append(schedule1[i])
        else:
            new_schedule1.append(schedule1[i])
            new_schedule2.append(schedule2[i])

    return [new_schedule1, new_schedule2]

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

    temp = chiasma(schedule1, schedule2)
    print(temp[0])
    print(temp[1])
