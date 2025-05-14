import random


def random_k_shortest_paths(graph, start, end, k, num_attempts=1000, verbose=False):
    """
    随机生成K条较短路径（不一定是最优解）

    参数:
        graph: 邻接表形式的图，如 {u: [(v, weight), ...]}
        start: 起点节点
        end: 终点节点
        k: 要返回的路径数量
        num_attempts: 尝试生成路径的最大次数
        verbose: 是否打印中间信息

    返回:
        list of (path_length, path)
    """
    # 去重存储路径
    unique_paths = set()
    # 存储完整路径及其长度
    all_path_info = []

    for attempt in range(num_attempts):
        current = start
        path = [current]
        visited = set([current])
        total_cost = 0

        while current != end:
            neighbors = graph.get(current, [])
            if not neighbors:
                if verbose:
                    print(f"Attempt {attempt + 1}: Dead end at node {current}.")
                break

            # 加权随机选择下一个节点
            weights = [w for _, w in neighbors]
            nodes = [n for n, _ in neighbors]

            # softmax 归一化权重（避免除零），偏向低权重方向
            inv_weights = [1 / (w + 1e-5) for w in weights]
            sum_inv_weights = sum(inv_weights)
            probabilities = [iw / sum_inv_weights for iw in inv_weights]

            next_node = random.choices(nodes, weights=probabilities, k=1)[0]

            if next_node in visited:
                # 避免循环
                if verbose:
                    print(f"Attempt {attempt + 1}: Cycle detected. Skipping.")
                break

            path.append(next_node)
            visited.add(next_node)

            idx = nodes.index(next_node)
            total_cost += weights[idx]
            current = next_node

        else:
            # 成功到达终点
            path_tuple = tuple(path)
            if path_tuple not in unique_paths:
                unique_paths.add(path_tuple)
                all_path_info.append((total_cost, path))
                if verbose:
                    print(f"Attempt {attempt + 1}: Found new path: {path} with cost {total_cost}")

        if len(all_path_info) >= k and len(unique_paths) >= k:
            if verbose:
                print("Enough paths found.")
            break

    # 按路径长度排序
    all_path_info.sort(key=lambda x: x[0])

    return all_path_info[:k]

if __name__ == "__main__":
    # 示例图：邻接表形式
    graph = {
        3: [(2, 4), (1, 2)],
        2: [(1, 5), (0, 10)],
        1: [(0, 3)],
        0: []
    }

    start_node = 2
    end_node = 3
    k_paths = 2
    attempts = 1000

    results = random_k_shortest_paths(graph, start_node, end_node, k=k_paths, num_attempts=attempts, verbose=False)
    print(results)

    print("\nTop K shortest paths:")
    for i, (cost, path) in enumerate(results, 1):
        print(f"{i}. Cost: {cost}, Path: {path}")