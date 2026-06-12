"""
run_demo.py — Run a single demonstration of the SO101 SmolVLA policy.

Runs one episode without recording to HuggingFace.
Useful for quick testing and demonstration purposes.

Usage:
    python scripts/run_demo.py [options]

Example:
    python scripts/run_demo.py --color red
"""

import argparse
import subprocess
import sys


TASK_STRINGS = {
    "red":    "Disconnect the red alligator clip and place it in the red zone",
    "yellow": "Disconnect the yellow alligator clip and place it in the yellow zone",
    "green":  "Disconnect the green alligator clip and place it in the green zone",
}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for demo."""
    parser = argparse.ArgumentParser(
        description="Run a single SO101 SmolVLA demo episode."
    )
    parser.add_argument(
        "--color",
        type=str,
        choices=["red", "yellow", "green"],
        default="red",
        help="Target cable color.",
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
        help="Duration of demo episode in seconds.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda", "cpu"],
        help="Device for policy inference.",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for demo."""
    args = parse_args()
    task = TASK_STRINGS[args.color]

    print("=" * 60)
    print("SO101 SmolVLA Demo")
    print("=" * 60)
    print(f"Color:  {args.color}")
    print(f"Task:   {task}")
    print(f"Model:  {args.model_repo_id}")
    print("=" * 60)

    # Fix serial port permissions
    subprocess.run(["sudo", "chmod", "666", args.robot_port], check=False)

    camera_config = (
        '{"top": {"type": "opencv", "index_or_path": "/dev/video0",'
        ' "width": 640, "height": 480, "fps": 10},'
        ' "front": {"type": "opencv", "index_or_path": "/dev/video2",'
        ' "width": 640, "height": 480, "fps": 10}}'
    )

    cmd = [
        "lerobot-record",
        "--robot.type=so101_follower",
        f"--robot.port={args.robot_port}",
        "--robot.id=my_so101",
        f"--robot.cameras={camera_config}",
        "--policy.type=smolvla",
        f"--policy.pretrained_path={args.model_repo_id}",
        f"--policy.device={args.device}",
        f"--dataset.repo_id=Oscarcarrh/demo_{args.color}",
        f"--dataset.single_task={task}",
        "--dataset.num_episodes=1",
        f"--dataset.episode_time_s={args.episode_time_s}",
        "--dataset.reset_time_s=5",
        "--interpolation_multiplier=5",
        "--dataset.push_to_hub=false",
    ]

    print("Running demo... Press Ctrl+C to stop.")
    result = subprocess.run(cmd, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
