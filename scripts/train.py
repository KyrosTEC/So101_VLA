"""
train.py — Training script for SO101 SmolVLA policy.

Usage:
    python scripts/train.py [options]

Example:
    python scripts/train.py \\
        --dataset_repo_id Oscarcarrh/cables_vla_all_v2 \\
        --dataset_root ./data/cables_vla_all_v2 \\
        --output_dir outputs/train/so101-cables \\
        --policy_repo_id Oscarcarrh/so101-cables-smolvla-all-v2 \\
        --steps 50000 \\
        --batch_size 32
"""

import argparse
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for training."""
    parser = argparse.ArgumentParser(
        description="Train SmolVLA policy for SO101 cable manipulation task."
    )
    parser.add_argument(
        "--dataset_repo_id",
        type=str,
        default="Oscarcarrh/cables_vla_all_v2",
        help="HuggingFace dataset repository ID.",
    )
    parser.add_argument(
        "--dataset_root",
        type=str,
        default="./data/cables_vla_all_v2",
        help="Local path to the dataset.",
    )
    parser.add_argument(
        "--policy_base",
        type=str,
        default="lerobot/smolvla_base",
        help="Base SmolVLA model to fine-tune.",
    )
    parser.add_argument(
        "--policy_repo_id",
        type=str,
        default="Oscarcarrh/so101-cables-smolvla-all-v2",
        help="HuggingFace model repository ID for saving.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="outputs/train/so101-cables",
        help="Local output directory for checkpoints.",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=50000,
        help="Total training steps.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=32,
        help="Training batch size.",
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=8,
        help="Number of dataloader workers.",
    )
    parser.add_argument(
        "--save_freq",
        type=int,
        default=5000,
        help="Save checkpoint every N steps.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda", "cpu"],
        help="Device to train on.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume training from last checkpoint.",
    )
    return parser.parse_args()


def build_lerobot_command(args: argparse.Namespace) -> list:
    """Build the lerobot-train command from parsed arguments."""
    rename_map = (
        '{"observation.images.front": "observation.images.camera1",'
        ' "observation.images.side": "observation.images.camera2"}'
    )
    cmd = [
        "lerobot-train",
        f"--policy.path={args.policy_base}",
        f"--dataset.repo_id={args.dataset_repo_id}",
        f"--dataset.root={args.dataset_root}",
        f"--batch_size={args.batch_size}",
        f"--steps={args.steps}",
        f"--num_workers={args.num_workers}",
        f"--output_dir={args.output_dir}",
        f"--policy.repo_id={args.policy_repo_id}",
        f"--policy.device={args.device}",
        f"--save_freq={args.save_freq}",
        "--dataset.video_backend=pyav",
        f"--rename_map={rename_map}",
    ]
    if args.resume:
        cmd.append("--resume=true")
        cmd.append("--optimizer.type=adamw")
    return cmd


def main() -> None:
    """Main entry point for training."""
    args = parse_args()
    cmd = build_lerobot_command(args)

    print("=" * 60)
    print("SO101 SmolVLA Training")
    print("=" * 60)
    print(f"Dataset:    {args.dataset_repo_id}")
    print(f"Steps:      {args.steps}")
    print(f"Batch size: {args.batch_size}")
    print(f"Device:     {args.device}")
    print(f"Output:     {args.output_dir}")
    print("=" * 60)
    print("Running:", " ".join(cmd))
    print("=" * 60)

    result = subprocess.run(cmd, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
