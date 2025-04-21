import os
import re

class_name = "b"  # b,t
# class_name = "t"  # b,t
data_num = 700
rff_path = f'/mnt/sdb2/work/dr/Projects/profeta/key_point_segmentation/PC/{class_name}'  # rename files in folder
mfn_path = f'/mnt/sdb2/work/dr/Projects/profeta/key_point_segmentation/PC/{class_name}'  # modify file name
mtc_path = f'/mnt/sdb2/work/dr/Projects/profeta/key_point_segmentation/PC/'  # modify txt content


# data merging path
src_folder_b = '/mnt/sdb2/work/dr/Projects/profeta/key_point_segmentation/PC/b'  # 替换为b文件夹的路径
src_folder_t = '/mnt/sdb2/work/dr/Projects/profeta/key_point_segmentation/PC/t'  # 替换为t文件夹的路径
dest_folder_h = '/mnt/sdb2/work/dr/Projects/profeta/key_point_segmentation/shapenetcore_partanno_segmentation_benchmark_v0_normal/0'  # 替换为h文件夹的路径

split_path = "/mnt/sdb2/work/dr/Projects/profeta/key_point_segmentation/shapenetcore_partanno_segmentation_benchmark_v0_normal/train_test_split"

# seg_path = "/mnt/sdb2/work/dr/Projects/profeta/key_point_segmentation/PC/p"
seg_path = "/mnt/sdb2/work/dr/Projects/profeta/key_point_segmentation/shapenetcore_partanno_segmentation_benchmark_v0_normal/0"

def rename_files_in_folder(folder_path):
    # 获取文件夹中所有文件的列表
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 对文件列表进行排序，确保重命名的顺序是正确的
    files.sort()

    # 定义起始的数字
    start_number = 1

    # 遍历文件列表，进行重命名
    for file_name in files:
        # 获取文件的扩展名
        file_extension = os.path.splitext(file_name)[1]
        zero_num = 4 - len(str(start_number))
        # 构造新的文件名
        new_file_name = f"{class_name}_{zero_num * '0'}{start_number}{file_extension}"
        # new_file_name = f"{zero_num * '0'}{start_number}{file_extension}"

        # 获取完整的旧文件路径和新文件路径
        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_file_name)

        # 重命名文件
        os.rename(old_file_path, new_file_path)

        # 打印出旧文件名和新文件名
        print(f"Renamed '{file_name}' to '{new_file_name}'")

        # 增加数字，用于下一个文件
        start_number += 1


def modify_filename(directory):
    # 遍历目录中的所有 txt 文件
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)

            # 读取原始文件内容
            with open(filepath, 'r') as file:
                lines = file.readlines()

            # 修改内容，将每个空档替换为一个逗号
            modified_lines = [re.sub(r'\s+', ', ', line.strip()) + '\n' for line in lines]

            # 写回新的内容
            with open(filepath, 'w') as file:
                file.writelines(modified_lines)

    print('所有文件处理完成。')


def modify_txt_content(direction, data_num):
    test_file = "profeta_test.txt"
    train_file = "profeta_train.txt"

    test_num = int(data_num * 0.2) + 1

    test_dir = os.path.join(direction, test_file)
    train_dir = os.path.join(direction, train_file)

    with open(test_dir, 'w', encoding='utf-8') as file:
        for i in range(1, test_num):
            zero_num = 4 - len(str(i))
            line = f"b_{zero_num * '0'}{i}\n"
            file.write(line)

        for j in range(1, test_num):
            zero_num = 4 - len(str(j))
            line = f"p_{zero_num * '0'}{j}\n"
            file.write(line)

    with open(train_dir, 'w', encoding='utf-8') as file:
        for i in range(test_num, data_num + 1):
            zero_num = 4 - len(str(i))
            line = f"b_{zero_num * '0'}{i}\n"
            file.write(line)

        for j in range(test_num, data_num + 1):
            zero_num = 4 - len(str(j))
            line = f"p_{zero_num * '0'}{j}\n"
            file.write(line)

    print(f"Successfully writing {data_num} b & t in {direction}")


def seg_label(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.startswith(f'{class_name}_') and filename.endswith('.txt'):
            # 构建完整的文件路径
            file_path = os.path.join(folder_path, filename)
            print(file_path)
            # 读取文件内容
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # 在每一行末尾添加字符串", 1.000000"，并写回文件
            with open(file_path, 'w') as file:
                for line in lines:
                    file.write(line.strip() + '.000000\n')

    print("完成所有文件的处理。")


def merge_files(src_folder_b, src_folder_t, dest_folder_h, start, end):
    for i in range(start, end + 1):
        # 构建源文件和目标文件的路径
        filename_b = f"b_{i:04}.txt"  # 如b_0001.txt
        filename_t = f"t_{i:04}.txt"  # 如t_0001.txt
        filename_h = f"{i:04}.txt"  # 如0001.txt

        src_path_b = os.path.join(src_folder_b, filename_b)
        src_path_t = os.path.join(src_folder_t, filename_t)
        dest_path_h = os.path.join(dest_folder_h, filename_h)

        # 读取两个源文件的内容
        with open(src_path_b, 'r') as file_b, open(src_path_t, 'r') as file_t:
            content_b = file_b.readlines()
            content_t = file_t.readlines()

        # 在content_b后添加一个换行符，然后合并content_p
        # merged_content = content_b + ['\n'] + content_t
        merged_content = content_b + content_t
        # merged_content = content_t + content_b

        # 确保目标文件夹存在
        os.makedirs(dest_folder_h, exist_ok=True)

        # 将合并后的内容保存到目标文件
        with open(dest_path_h, 'w') as file_h:
            file_h.writelines(merged_content)

    print("所有文件合并并保存完成。")


def sort_seg(path):
    import random
    import json
    import os

    # 设置数据总数
    total_files = data_num

    # 设置训练集、验证集、测试集的比例
    train_ratio = 0.8
    val_ratio = 0.1
    test_ratio = 0.1

    # 指定输出路径
    output_path = path  # 替换为您想要保存JSON文件的目录

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 生成文件名列表
    file_list = [f"{i:04}" for i in range(1, total_files + 1)]

    # 随机打乱文件名列表
    random.shuffle(file_list)

    # 计算训练集、验证集、测试集的文件数量
    train_size = int(total_files * train_ratio)
    val_size = int(total_files * val_ratio)
    test_size = total_files - train_size - val_size

    # 分割数据集
    train_files = file_list[:train_size]
    val_files = file_list[train_size:train_size + val_size]
    test_files = file_list[train_size + val_size:]

    # 准备JSON数据
    train_data = [f"shape_data/0/{file}" for file in train_files]
    val_data = [f"shape_data/0/{file}" for file in val_files]
    test_data = [f"shape_data/0/{file}" for file in test_files]

    # 写入JSON文件
    json_files = {
        'shuffled_train_file_list.json': train_data,
        'shuffled_test_file_list.json': test_data,
        'shuffled_val_file_list.json': val_data
    }

    for filename, data in json_files.items():
        with open(os.path.join(output_path, filename), 'w') as json_file:
            json.dump(data, json_file)

    print(f"数据集已成功划分并保存为JSON文件到 {output_path}")


def modify_seg_filename(directory):
    # 遍历目录中的所有 txt 文件
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)

            # 读取原始文件内容
            with open(filepath, 'r') as file:
                lines = file.readlines()

            # 修改内容
            modified_lines = [line.replace(', ', ' ') for line in lines]

            # 写回新的内容
            with open(filepath, 'w') as file:
                file.writelines(modified_lines)
        print(f"file content modified: {filename}")


def clean_BOM(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            cleaned_content = content.replace('\ufeff', '')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"file BOM cleaned: {file_name}")


# # 1. sort data file name into "b_0001.txt"  # check b, t
# rename_files_in_folder(rff_path)
# # # 2. convert "int int int int int int" to "int, int, int, int, int, int"  # check b, t ###
# # modify_filename(mfn_path)
# # 3. labeling the points  # check b,t
# seg_label(mfn_path)
# # 4. clean file BOM  # check b,t
# clean_BOM(mfn_path)
# # # 5. convert  "int, int, int, int, int, int" to "int int int int int int"  # check b,t
# # modify_seg_filename(mfn_path)

# 对b降采样

# 6. divide training and testing dataset
modify_txt_content(mtc_path, data_num)
# 7. 调用函数，合并文件
merge_files(src_folder_b, src_folder_t, dest_folder_h, 1, data_num)
# 8. splitting datasets
sort_seg(split_path)


