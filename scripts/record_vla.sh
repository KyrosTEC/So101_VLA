#!/bin/bash
# Usage: bash scripts/record_vla.sh <color> <num_episodes>
# Colors: red | yellow | green
COLOR=${1:-red}
NUM_EPISODES=${2:-200}

sudo chmod 666 /dev/video0 /dev/video2 /dev/video4

lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
--robot.cameras='{"front":{"type":"opencv","index_or_path":2,"width":640,"height":480,"fps":10,"fourcc":"MJPG"},"side":{"type":"opencv","index_or_path":4,"width":640,"height":480,"fps":10,"fourcc":"MJPG"}}' \
  --teleop.type=so101_leader \
  --teleop.port=/dev/ttyACM1 \
  --dataset.repo_id=Oscarcarrh/cables_vla_${COLOR}_v2 \
  --dataset.root=./data/cables_vla_${COLOR}_v2 \
  --dataset.single_task="remove the ${COLOR} cable and place it in the ${COLOR} box" \
  --dataset.num_episodes=${NUM_EPISODES} \
  --dataset.episode_time_s=40 \
  --dataset.reset_time_s=5 \
  --dataset.fps=10 \
  --dataset.push_to_hub=true \
  --resume=true \
  --play_sounds=false
