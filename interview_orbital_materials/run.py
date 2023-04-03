import argparse


def main(data_dir):
    print(f"Data directory: {data_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script that requires the --data-dir argument."
    )
    parser.add_argument(
        "--data-dir", type=str, required=True, help="Path to the data directory."
    )

    args = parser.parse_args()

    main(args.data_dir)
