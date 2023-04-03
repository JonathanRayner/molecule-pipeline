# Data Loader Script

This Python script is used for loading data from a specified directory. It takes one required argument and two optional arguments:

## Required Argument

- `--data-dir`: Path to the data directory.

## Optional Arguments

- `--num-workers` (int): Number of subprocesses to use for data loading. 0 means that the data will be loaded in the main process. Default value is 0.

- `--batch-size` (int): How many samples per batch to load. Default value is 1.

Note: the `shuffle` option is always enabled for data loading.

Note: the seed option is set to the pytorch default value of 0.

Note: may need a `pin_memory` method for dataset?

## Usage

Run the script with the required and optional arguments as needed:

```bash
python data_loader.py --data-dir /path/to/data --num-workers 4 --batch-size 32
```
