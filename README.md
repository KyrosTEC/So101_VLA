# SO101 Intelligent Control - Final Project

Proyecto de control inteligente con robot SO-101 para ordenar cables de colores.

- IL / Imitation Learning: aprendizaje por demostracion basado en estados visuales.
- VLA: control con instrucciones de lenguaje.

## Task
Laboratory Setup with Clip Wires.
El robot manipula cables tipo caiman y los coloca en cajas correspondientes.
Colores principales (IL): rojo, amarillo, verde.
Distractores: blanco, negro.

## Quick Start
    git clone https://github.com/carloAdr1/so101-intelligent-control.git
    cd so101-intelligent-control
    python -m venv venv
    source venv/bin/activate
    pip install lerobot

## Hardware Configuration
    /dev/ttyACM0 = SO101 follower / robot
    /dev/ttyACM1 = SO101 leader / teleop
    /dev/video0  = front camera
    /dev/video2  = side camera

## Docs (read in order)
1. docs/SETUP_WSL_USB.md
2. docs/CAMERA_TESTS.md
3. docs/TELEOPERATION.md
4. docs/CALIBRATION.md
5. docs/DATASET_PLAN.md

## Recording IL Dataset
    bash scripts/record_il.sh both_bw 100
    bash scripts/record_il.sh only_black 100
    bash scripts/record_il.sh only_white 100

## Recording VLA Dataset
    bash scripts/record_vla.sh red 100
    bash scripts/record_vla.sh yellow 100
    bash scripts/record_vla.sh green 100

## Data Policy
Datasets, videos, checkpoints y modelos NO van a GitHub.
Carpetas ignoradas: data/, outputs/, venv/
Cada miembro graba su propia data local.

## Repository Structure
    so101-intelligent-control/
    scripts/
        setup_cameras.sh
        record_il.sh
        record_vla.sh
    src/
        preprocessing/
        perception/
        training/
        evaluation/
        robot_execution/
    docs/
        SETUP_WSL_USB.md
        CAMERA_TESTS.md
        TELEOPERATION.md
        CALIBRATION.md
        DATASET_PLAN.md
    results/
        metrics/
        plots/
        videos/
    README.md
