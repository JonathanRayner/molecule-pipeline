# 3D Molecular Data Pipeline

## Overview

This script `run.py` provides a way to load a dataset of molecular structures stored as SDF files, perform data augmentation, and output tensor shapes of atomic numbers and positions for the first 100 batches.

The script uses the ASE package to read the SDF files and the [PyTorch cpu-only version](https://download.pytorch.org/whl/cpu) for tensor manipulation and data batching.

## Usage

You can run the script from a docker container as follows (you will need to include the data directory as a volume):

```bash
docker pull jonathanrayner/molecule-pipeline:latest
docker run -v /path/to/your/data/dir:/app/data jonathanrayner/molecule-pipeline:latest --data-dir data
```

You can run the script from the command line as follows:

```bash
cd interview_orbital_materials
python run.py --data-dir /path/to/your/data/dir
```

You can also use optional arguments:

- `--num-workers`: Number of subprocesses to use for data loading. 0 means that the data will be loaded in the main process. (default: 0)
- `--batch-size`: How many samples per batch to load (default: 1)
- `--coord-jitter-std`: Std of gaussian noise added to coordinate positions for data augmentation (default: 0.0)

For example:

TODO

```bash
docker run -v /path/to/your/data/dir:/app/data molecule-pipeline:latest --data-dir data --num-workers 4 --batch-size 10 --coord-jitter-std 0.1
```

## Documentation

### MoleculeDataset3D

`MoleculeDataset3D` is a custom PyTorch `Dataset` class that reads molecular structures from SDF files using the ASE package.

Arguments:

- `data_dir`: Path to the directory containing the SDF files
- `coord_jitter_std`: Std of gaussian noise added to coordinate positions for data augmentation
- `max_num_atoms`: Sequences of atomic numbers and coordinate positions are padded with zeros to this length for batching (default: 50)

Methods:

- `augment_coordinates_with_jitter()`: Add zero-mean gaussian noise to the coordinates of the atoms in a molecule
- `pad_first_dim_with_zeros()`: Pad the first dimension of a tensor with zeros to the specified length

### main()

The `main()` function loads the data, prints the batch size, and prints the shape of the atomic_numbers and positions tensors for 100 batches. The dataloader has shuffle=True, drops_last=True, and a fixed random seed.

Arguments:

- `data_dir`: Path to the data directory
- `num_workers`: Number of subprocesses to use for data loading (default: 0)
- `batch_size`: How many samples per batch to load (default: 1)
- `coord_jitter_std`: Std of gaussian noise added to coordinate positions for data augmentation (default: 0.0)
