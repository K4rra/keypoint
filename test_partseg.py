import hydra
import torch
import importlib
import numpy as np
import os
from dataset import PartNormalDataset
from torch.utils.data import DataLoader
from omegaconf import OmegaConf


@hydra.main(config_path='config', config_name='partseg', version_base="1.2.0")
def main(args):
    # ===== 解除结构化模式限制 ===== #
    OmegaConf.set_struct(args, False)  # 允许动态添加字段

    # ===== 维度配置 ===== #
    args.num_class = int(args.num_class)
    args.input_dim = int(args.input_dim)
    args.batch_size = int(args.batch_size)
    args.num_point = 1024
    args.normal = True
    num_category = 1
    args.input_dim = (6 if args.normal else 3) + num_category  # 动态添加input_dim

    # ===== 恢复结构化模式（可选） ===== #
    OmegaConf.set_struct(args, True)

    # ===== 模型加载 ===== #
    model = getattr(importlib.import_module(f'models.{args.model.name}.model'), 'PointTransformerSeg')(args).cuda()
    checkpoint = torch.load('log/partseg/Hengshuang/best_model.pth', weights_only=False)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    print("模型加载成功")

    # ===== 数据加载 ===== #
    root_path = hydra.utils.to_absolute_path(
        '/mnt/sdb2/work/dr/Projects/profeta/key_point_segmentation/shapenetcore_partanno_segmentation_benchmark_v0_normal'
    )
    print(f"数据集路径: {root_path}")
    if not os.path.exists(root_path):
        print(f"路径不存在: {root_path}")
        return

    test_dataset = PartNormalDataset(
        root=root_path,
        npoints=args.num_point,
        split='test',
        normal_channel=args.normal
    )
    print(f"数据集大小: {len(test_dataset)}")
    if len(test_dataset) == 0:
        print("数据集为空，请检查数据集文件或重新生成数据集。")
        return

    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)

    # ===== 预测保存 ===== #
    save_dir = 'predictions'
    os.makedirs(save_dir, exist_ok=True)
    print(f"保存路径: {os.path.abspath(save_dir)}")

    def to_categorical(y, num_classes):
        return torch.ones((y.shape[0], 1)).cuda()  # 单类别全1向量

    with torch.no_grad():
        for batch_idx, (points, labels, _) in enumerate(test_loader):
            points = points.float().cuda()
            labels = labels.long().cuda()

            # ===== 特征拼接 ===== #
            one_hot = to_categorical(labels, num_category)
            one_hot_expanded = one_hot.unsqueeze(1).expand(-1, points.size(1), -1)
            points_with_label = torch.cat([points, one_hot_expanded], dim=-1)

            # ===== 推理 ===== #
            seg_pred = model(points_with_label)
            pred_labels = seg_pred.argmax(dim=-1).cpu().numpy()

            print(f"批次 {batch_idx} 推理完成，预测标签形状: {pred_labels.shape}")

            # ===== 保存结果 ===== #
            for i in range(points.size(0)):
                idx = batch_idx * args.batch_size + i
                if idx >= len(test_dataset):
                    break

                original_path = test_dataset.datapath[idx][1]
                filename = os.path.basename(original_path).replace('.txt', '_pred.txt')
                save_path = os.path.join(save_dir, filename)

                xyz = points[i].cpu().numpy()[:, :3]
                labels = pred_labels[i].reshape(-1, 1)
                np.savetxt(save_path, np.hstack([xyz, labels]), fmt='%.6f %.6f %.6f %d')

                print(f"保存文件: {save_path}")

    print(f"预测保存至：{os.path.abspath(save_dir)}")


if __name__ == '__main__':
    main()