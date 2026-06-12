"""
evaluate.py — Evaluation script for SO101 SmolVLA policy.

Runs the trained policy on the physical robot and records
evaluation episodes to HuggingFace.

Usage:
    python scripts/evaluate.py [options]

Example:
    python scripts/evaluate.py --color red --num_episodes 10
"""

import argparse
import subprocess
import sys


TASK_STRINGS = {
    "red":    "Disconnect the red alligator clip and place it in the red zone",
    "yellow": "Disconnect the yellow alligator clip and place it in the yellow zone",
    "green":  "Disconnect the green alligator clip and place it in the green zone",
}

CAMERA_CONFIG = (
    '{"top": {"type": "opencv", "index_or_path": "/dev/video0",'
    ' "width": 640, "height": 480, "fps": 10},'
    ' "front": {"type": "opencv", "index_or_path": "/dev/video2",'
    ' "width": 640, "height": 480, "fps": 10}}'
)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for evaluation."""
    parser = argparse.ArgumentParser(
        description="Evaluate SmolVLA policy on SO101 robot."
    )
    parser.add_argument(
        "--color",
        type=str,
        choices=["red", "yellow", "green"],
        default="red",
        help="Target cable color to evaluate.",
    )
    parser.add_argument(
        "--num_episodes",
        type=int,
        default=10,
        help="Number of evaluation episodes to record.",
    )
    parser.add_argument(
        "--model_repo_id",
        type=str,
        default="Oscarcarrh/so101-cables-smolvla-all-v2",
        help="HuggingFace model repository ID.",
    )
    parser.add_argument(
        "--robot_port",
        type=str,
        default="/dev/ttyACM0",
        help="Serial port for SO101 follower robot.",
    )
    parser.add_argument(
        "--episode_time_s",
        type=int,
        default=30,
        help="Duration of each episode in seconds.",
    )
    parser.add_argument(
        "--reset_time_s",
        type=int,
        default=30,
        help="Reset time between episodes in seconds.",
    )
    parser.add_argument(
        "--interpolation_multiplier",
        type=int,
        default=5,
        help="Action interpolation multiplier for smoother motion.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda", "cpu"],
        help="Device for policy inference.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Run in offline mode (no robot connection, for testing).",
    )
    return parser.parse_args()


def build_eval_command(args: argparse.Namespace) -> list:
    """Build the lerobot-record command for evaluation."""
    dataset_repo = f"Oscarcarrh/eval_so101_{args.color}"
    task_string = TASK_STRINGS[args.color]

    cmd = [
        "lerobot-record",
        "--robot.type=so101_follower",
        f"--robot.port={args.robot_port}",
        "--robot.id=my_so101",
        f"--robot.cameras={CAMERA_CONFIG}",
        "--policy.type=smolvla",
        f"--policy.pretrained_path={args.model_repo_id}",
        f"--policy.device={args.device}",
        f"--dataset.repo_id={dataset_repo}",
        f"--dataset.single_task={task_string}",
        f"--dataset.num_episodes={args.num_episodes}",
        f"--dataset.episode_time_s={args.episode_time_s}",
        f"--dataset.reset_time_s={args.reset_time_s}",
        f"--interpolation_multiplier={args.interpolation_multiplier}",
    ]
    return cmd


def main() -> None:
    """Main entry point for evaluation."""
    args = parse_args()

    print("=" * 60)
    print("SO101 SmolVLA Evaluation")
    print("=" * 60)
    print(f"Color:    {args.color}")
    print(f"Task:     {TASK_STRINGS[args.color]}")
    print(f"Episodes: {args.num_episodes}")
    print(f"Model:    {args.model_repo_id}")
    print("=" * 60)

    if args.offline:
        print("[OFFLINE MODE] Skipping robot connection.")
        print("Use --offline=False to run on physical robot.")
        return

    # Fix serial port permissions
    fix_permissions = subprocess.run(
        ["sudo", "chmod", "666", args.robot_port],
        check=False
    )
    if fix_permissions.returncode != 0:
        print(f"Warning: Could not set permissions on {args.robot_port}")

    cmd = build_eval_command(args)
    print("Running:", " ".join(cmd))
    print("=" * 60)

    result = subprocess.run(cmd, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
