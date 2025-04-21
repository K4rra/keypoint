# This repository is based on [this repo](https://github.com/yanx27/Pointnet_Pointnet2_pytorch)

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
The segmentation results are saved under `predictions`, and run
```
python point_sort.py
```

The sorted points are saved under `sorted_points`.
