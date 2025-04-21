# This repository is based on [this repo](https://github.com/yanx27/Pointnet_Pointnet2_pytorch)

## Classification
### Data Preparation
Download alignment **ModelNet** [here](https://shapenet.cs.stanford.edu/media/modelnet40_normal_resampled.zip) and save in `modelnet40_normal_resampled`.

### Run
Change which method to use in `config/cls.yaml` and run
```
python train_cls.py
```

## Part Segmentation
### Data Preparation
Download alignment **ShapeNet** [here](https://shapenet.cs.stanford.edu/media/shapenetcore_partanno_segmentation_benchmark_v0_normal.zip) and save in `data/shapenetcore_partanno_segmentation_benchmark_v0_normal`.

### Run
Change which method to use in `config/partseg.yaml` and run
```
python train_partseg.py
```
### Results
Currently only Hengshuang's method is implemented.

