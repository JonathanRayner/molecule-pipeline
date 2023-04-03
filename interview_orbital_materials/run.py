import argparse
from ase.io.sdf import read_sdf
from pathlib import Path
from torch.utils.data import DataLoader, Dataset
import torch
import torch.nn.functional as F
from itertools import cycle


class MoleculeDataset3D(Dataset):
    """

    Use the ASE package to read the SDF files.
    See https://wiki.fysik.dtu.dk/ase/ase/io/io.html and https://wiki.fysik.dtu.dk/ase/ase/io/formatoptions.html#sdf

    Args:
        data_dir: Path to the directory containing the SDF files.
        coord_jitter_std: Std of gaussian noise added to coordinate positions for data augmentation.
        max_num_atoms: Sequences of atomic numbers and coordinate positions are padded with zeros to this length for batching.

    Returns:
        A dictionary with keys "atomic_numbers" and "positions" containing the atomic numbers and positions of the atoms in the molecule.
    """

    def __init__(
        self,
        data_dir: str,
        coord_jitter_std: float,
        max_num_atoms: int = 50,
    ):
        self.data_dir = data_dir
        self.paths = list(Path.cwd().joinpath(data_dir).glob("*.sdf"))
        self.coord_jitter_std = coord_jitter_std
        self.max_num_atoms = max_num_atoms

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        atoms = read_sdf(self.paths[idx])
        atomic_numbers = torch.tensor(atoms.get_atomic_numbers())
        positions = torch.tensor(atoms.get_positions())

        # data augmentation
        if self.coord_jitter_std > 0.0:
            positions = self.augment_coordinates_with_jitter(
                positions, self.coord_jitter_std
            )

        # pad with zeros so all molecule tensors are of length self.max_num_atoms
        atomic_numbers = self.pad_first_dim_with_zeros(
            atomic_numbers, self.max_num_atoms
        )
        positions = self.pad_first_dim_with_zeros(positions, self.max_num_atoms)

        return {"atomic_numbers": atomic_numbers, "positions": positions}

    def augment_coordinates_with_jitter(
        self, positions: torch.Tensor, std: float
    ) -> torch.Tensor:
        """Add zero-mean gaussian noise to the coordinates of the atoms in a molecule."""
        return positions + torch.randn_like(positions) * std

    def pad_first_dim_with_zeros(
        self, tensor: torch.Tensor, length: int
    ) -> torch.Tensor:
        """Pad the first dimension of a tensor with zeros to the specified length."""
        num_dims = len(tensor.shape)
        pad = [0] * 2 * (num_dims - 1)  # do nothing to the other dimensions, if any
        pad.extend([0, length - tensor.shape[0]])  # pad the first dimension
        return F.pad(tensor, pad=pad, mode="constant", value=0)


def main(
    data_dir: str, num_workers: int, batch_size: int, coord_jitter_std: float
) -> DataLoader:
    """
    Load the data, print the batch size, and print the shape of the atomic_numbers and positions tensors for 100 batches.
    The dataloader has shuffle=True, drops_last=True, and a fixed random seed.
    """
    dataset = MoleculeDataset3D(data_dir, coord_jitter_std=coord_jitter_std)

    # Create a generator with a fixed seed
    seed = 42
    generator = torch.Generator()
    generator.manual_seed(seed)

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        drop_last=True,
        generator=generator,
    )

    print(f"Batch size: {batch_size}")

    BATCHES_TO_PRINT = 100
    i = 0
    for batch in cycle(dataloader):
        atomic_numbers = batch["atomic_numbers"]
        positions = batch["positions"]
        print(f"Shape of atomic_numbers tensor: {atomic_numbers.shape}")
        print(f"Shape of positions tensor: {positions.shape}")
        i += 1
        if i == BATCHES_TO_PRINT:
            break


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

    parser.add_argument(
        "--coord-jitter-std",
        type=float,
        default=0.0,
        help="Std of gaussian noise added to coordinate positions for data augmentation (default: 0.0).",
    )

    args = parser.parse_args()

    main(args.data_dir, args.num_workers, args.batch_size, args.coord_jitter_std)
