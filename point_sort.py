import os
import glob
import numpy as np
import networkx as nx
from collections import deque

# 参数设置
input_dir = "predictions"  # 输入文件夹路径
output_dir = "sorted_points"  # 输出文件夹路径
distance_threshold = 0.3  # 距离阈值

# 如果输出文件夹不存在，则创建该文件夹
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取输入文件夹下所有 txt 文件
input_file_list = glob.glob(os.path.join(input_dir, "*.txt"))


# 定义欧氏距离计算函数
def euclidean_distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


# 遍历每个输入文件进行处理
for file_path in input_file_list:
    try:
        # 读取数据，假设每行格式为：x y z label
        data = np.loadtxt(file_path)
    except Exception as e:
        print(f"文件 {file_path} 读取失败：{e}")
        continue

    # 检查数据是否为空及是否含有4列
    if data.size == 0 or data.ndim != 2 or data.shape[1] < 4:
        print(f"文件 {file_path} 格式不符合要求，跳过。")
        continue

    # 提取所有点的坐标和标签
    points = data[:, :3]  # 提取所有点的坐标
    labels = data[:, 3]  # 提取所有点的标签

    # --- 关键点提取逻辑修改 ---
    # 初始化一个空的关键点列表
    key_points = []

    # 遍历所有点，检查其与其他关键点的距离
    for i in range(len(points)):
        # 如果点的标签不是1，则跳过
        if labels[i] != 1:
            continue

        # 检查该点是否与已有的关键点距离小于阈值
        is_keypoint = True
        for kp in key_points:
            if euclidean_distance(points[i], kp) < distance_threshold:
                is_keypoint = False
                break

        # 如果该点可以作为关键点，则添加到列表中
        if is_keypoint:
            key_points.append(tuple(points[i]))

    if not key_points:
        print(f"文件 {file_path} 中无符合条件的关键点数据，跳过。")
        continue

    # --- 构建图模型 ---
    G = nx.Graph()
    for idx, pt in enumerate(key_points):
        G.add_node(idx, coord=pt)

    # 对所有节点之间计算欧氏距离，满足条件则添加边
    n_points = len(key_points)
    for i in range(n_points):
        for j in range(i + 1, n_points):
            if euclidean_distance(key_points[i], key_points[j]) < distance_threshold:
                G.add_edge(i, j)

    # --- BFS 遍历并赋予顺序标签 ---
    start_node = 0
    visited = set()
    bfs_order = []
    queue = deque([start_node])
    visited.add(start_node)

    while queue:
        current = queue.popleft()
        bfs_order.append(current)
        neighbors = sorted(G.neighbors(current))
        for nb in neighbors:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)

    # 根据 BFS 遍历顺序为每个节点赋予标签（从1开始）
    node_label = {node: idx + 1 for idx, node in enumerate(bfs_order)}

    # --- 保存结果 ---
    base_name = os.path.basename(file_path)
    output_file = os.path.join(output_dir, base_name)
    with open(output_file, 'w') as f_out:
        for node in bfs_order:
            x, y, z = G.nodes[node]['coord']
            label = node_label[node]
            f_out.write(f"{x} {y} {z} {label}\n")

    print(f"已处理文件 {file_path}，结果保存到 {output_file}")