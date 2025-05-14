from collections import defaultdict

def merge_rows_by_first_two_columns(data):
    # 使用 defaultdict 来按前两列分组
    merged = defaultdict(int)

    for row in data:
        key = (row[0], row[1])  # 前两列作为键
        merged[key] += row[2]   # 第三列累加

    # 转换回二维列表格式
    result = [[key[0], key[1], value] for key, value in merged.items()]
    return result

def merge_lists_by_first_two_columns(list1, list2):
    # 构建字典：key 是前两列，value 是整行
    dict1 = {tuple(row[:2]): row for row in list1}
    dict2 = {tuple(row[:2]): row[2:] for row in list2}

    # 合并结果
    merged = []
    for key in dict1:
        if key in dict2:
            merged_row = dict1[key] + dict2[key]
            merged.append(merged_row)
        else:
            # 可选：处理没有匹配的情况
            merged.append(dict1[key])

    return merged

def Is_Available(schedule, demands, limitations):
    '''
    判断编组计划是否可行
    :param schedule: 编组计划
    :param demands: 运输需求
    :param limitations: 车站改编车数限制
    :return: 布尔值
    '''
    s_d = merge_lists_by_first_two_columns(schedule, demands)
    s_d = sorted(s_d, key=lambda x: x[0], reverse=True)
    demands_lim = dict.fromkeys(limitations, 0) # 每个站需要改编的车数
    for lst in s_d:
        path = lst[2]
        if lst[3] != path[-1]:
            demands_lim[lst[3]] = demands_lim[lst[3]] + lst[4]
            for i in range(len(s_d)):
                if (s_d[i][0] == lst[3]) and (s_d[i][1] == lst[1]):
                    s_d[i][4] = s_d[i][4] + lst[4]
    for i in demands_lim.keys():
        if demands_lim[i] > limitations[i]:
            return False

    return True

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

    print(Is_Available(schedule, demands, limitations))
