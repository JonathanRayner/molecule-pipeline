import argparse


def main(data_dir: str, num_workers: int, batch_size: int):
    print(f"Data directory: {data_dir}")
    print(f"Number of workers: {num_workers}")
    print(f"Batch size: {batch_size}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script that requires the --data-dir argument and accepts optional arguments."
    )
    parser.add_argument(
        "--data-dir", type=str, required=True, help="Path to the data directory."
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=0,
        help="Number of subprocesses to use for data loading. 0 means that the data will be loaded in the main process. (default: 0)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="How many samples per batch to load (default: 1).",
    )

    args = parser.parse_args()

    main(args.data_dir, args.num_workers, args.batch_size)
