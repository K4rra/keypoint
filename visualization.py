import open3d as o3d
import numpy as np
import sys
import os
import random


def load_point_cloud_with_labels(file_path):
    """
    从txt文件中读取包含标签的点云数据，并返回点的坐标和标签列表。
    每一行的格式: x y z label
    如果某些行中标签缺失，将用 None 代替。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"未找到文件: {file_path}")

    points = []
    labels = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # 忽略空行
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        x, y, z = map(float, parts[:3])
                        label = parts[3]  # 标签可以是数字或字符串
                        points.append([x, y, z])
                        labels.append(label)
                    except ValueError:
                        # 当无法转换为float时跳过这一行
                        continue
                elif len(parts) >= 3:
                    try:
                        x, y, z = map(float, parts[:3])
                        points.append([x, y, z])
                        labels.append(None)
                    except ValueError:
                        continue

    if not points:
        raise ValueError("文件中没有有效的点云数据")

    return np.array(points), labels


def generate_color_mapping(labels):
    """
    根据输入的标签列表生成颜色映射。
    对于所有不同的标签，随机生成一种颜色，颜色值为 [r, g, b]，范围均为0~1。
    如果某个点的标签为 None，则分配默认灰色。
    """
    unique_labels = set(labels)
    color_map = {}
    random.seed(42)  # 保证每次生成的颜色相同，便于调试
    for label in unique_labels:
        if label is None:
            color_map[label] = [0.5, 0.5, 0.5]  # 默认灰色
        else:
            # 随机生成颜色
            color_map[label] = [random.random(), random.random(), random.random()]
    return color_map


def load_colored_point_cloud(file_path):
    """
    根据文本文件构建一个带颜色的Open3D点云。
    点的颜色根据标签进行分配。
    """
    points, labels = load_point_cloud_with_labels(file_path)
    color_map = generate_color_mapping(labels)

    # 为每个点分配颜色
    colors = []
    for label in labels:
        colors.append(color_map[label])
    colors = np.array(colors)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    return pcd


def render_point_cloud(pcd):
    """
    使用Open3D的交互式窗口渲染点云
    """
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='点云渲染', width=800, height=600)
    vis.add_geometry(pcd)
    vis.run()
    vis.destroy_window()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python point_cloud_render_colored.py <point_cloud_with_labels.txt>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        pcd = load_colored_point_cloud(file_path)
    except Exception as e:
        print(e)
        sys.exit(1)

    render_point_cloud(pcd)


# python visualization.py /path/to/txt
