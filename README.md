# SO101 Robot — Manipulación Dextral con Vision-Language-Action (SmolVLA)

**Instituto Tecnológico de Estudios Superiores de Monterrey — Campus Monterrey**  
**Implementación de Robótica Inteligente**  
**Prof. Nezih N. — 2026**

---

## Equipo

| Nombre | Matrícula |
|--------|-----------|
| Rhett Nieto Ramírez | A01286100 |
| Ricardo Gaspar Ochoa | A00838841 |
| Valentina González Benedossi | A00839507 |
| Oscar Carranza Hernández | A00838649 |

---

## 1. Introducción

Este proyecto implementa un sistema de manipulación robótica dextral para el robot SO101 usando el modelo Vision-Language-Action **SmolVLA** (HuggingFace, 2025).

**Track seleccionado:** Track 2 — Vision-Language-Action  
**Opción seleccionada:** Opción 2 — Laboratory Setup with Clip Wires

El robot aprende a desconectar pinzas de cocodrilo de colores de una barra de conexiones y colocarlas en la zona Lego del color correspondiente, guiado por instrucciones en lenguaje natural como:

> *"Disconnect the red alligator clip and place it in the red zone"*

---

## 2. Formulación del Problema

La política VLA se formula como:

```
a_t = π_θ(o_t, l)
```

Donde:
- `o_t` — observación visual en tiempo t (2 cámaras RGB, 640×480, 10 FPS)
- `l` — instrucción de lenguaje natural (color objetivo)
- `a_t` — acción predicha (6 DOF: shoulder_pan, shoulder_lift, elbow_flex, wrist_flex, wrist_roll, gripper)

**Clases de objetos:** Rojo, Amarillo, Verde  
**Criterio de éxito:** El robot desconecta la pinza del color indicado y la deposita en la caja Lego correcta.

---

## 3. Dataset

| Propiedad | Valor |
|-----------|-------|
| Total de episodios | 453 (151 por color) |
| Clases | Rojo, Amarillo, Verde |
| Cámaras | 2 (frontal + lateral) |
| Resolución | 640×480 px |
| FPS | 10 |
| Formato | LeRobot v3.0 (parquet + video AV1) |
| Plataforma | HuggingFace |

### Links a los datasets

| Dataset | Link |
|---------|------|
| Rojo | [Oscarcarrh/cables_vla_red_v2](https://huggingface.co/datasets/Oscarcarrh/cables_vla_red_v2) |
| Amarillo | [Oscarcarrh/cables_vla_yellow_v2](https://huggingface.co/datasets/Oscarcarrh/cables_vla_yellow_v2) |
| Verde | [Oscarcarrh/cables_vla_green_v2](https://huggingface.co/datasets/Oscarcarrh/cables_vla_green_v2) |
| Unificado (todos) | [Oscarcarrh/cables_vla_all_v2](https://huggingface.co/datasets/Oscarcarrh/cables_vla_all_v2) |

### Modelo entrenado

[Oscarcarrh/so101-cables-smolvla-all-v2](https://huggingface.co/Oscarcarrh/so101-cables-smolvla-all-v2)

Cada demostración incluye:
- Imágenes RGB de ambas cámaras
- Estados articulares del robot (6 DOF)
- Acciones expertas del operador
- Instrucción de lenguaje natural
- Etiqueta de tarea (`task_index`)

---

## 4. Metodología

Usamos **SmolVLA** (HuggingFace, 2025) — un modelo Vision-Language-Action de 500M parámetros basado en SmolVLM2.

### Arquitectura

```
Cámaras (front + side) ──► SmolVLM2 Visual Encoder (congelado)
Instrucción de lenguaje ──►          ↓
                              tokens visuales + linguísticos
Estado articular (6 DOF) ──►         ↓
                              Action Expert (100M params, fine-tuned)
                                       ↓
                              Chunk de 50 acciones → Robot SO101
```

### Parámetros de entrenamiento

| Parámetro | Valor |
|-----------|-------|
| Steps | 50,000 |
| Batch size | 32 |
| Learning rate | 1e-4 |
| Scheduler | Cosine decay with warmup |
| GPU | NVIDIA RTX A4000 16GB |
| Tiempo de entrenamiento | ~11 horas |
| Parámetros entrenables | 100M / 450M |
| Loss final | 0.105 (rojo), 0.108 (unificado) |

---

## 5. Instalación

### Opción A — Instalación local

```bash
git clone https://github.com/TU_USUARIO/so101-intelligent-control.git
cd so101-intelligent-control
pip install -r requirements.txt
```

### Opción B — Docker (recomendado)

```bash
docker build -t so101-vla .
docker run --gpus all -v $(pwd)/results:/app/results so101-vla
```

### Requisitos del sistema

- Python 3.12
- CUDA 12.5+ (GPU NVIDIA recomendada)
- Ubuntu 20.04+ o WSL2
- Cámaras USB (front: /dev/video2, side: /dev/video4)
- Robot SO101 follower (/dev/ttyACM0) + leader (/dev/ttyACM1)

---

## 6. Grabación del Dataset

### Verificar cámaras

```bash
bash scripts/setup_cameras.sh
```

### Grabar episodios VLA

```bash
# Graba 151 episodios del color especificado
bash scripts/record_vla.sh red 151
bash scripts/record_vla.sh yellow 151
bash scripts/record_vla.sh green 151
```

### Grabar episodios IL (Imitation Learning)

```bash
bash scripts/record_il.sh both_bw 100
```

---

## 7. Entrenamiento

### Descargar dataset localmente

```bash
hf download Oscarcarrh/cables_vla_all_v2 \
  --repo-type dataset \
  --local-dir ./data/cables_vla_all_v2
```

### Entrenar modelo

```bash
python scripts/train.py \
  --dataset_repo_id Oscarcarrh/cables_vla_all_v2 \
  --dataset_root ./data/cables_vla_all_v2 \
  --output_dir outputs/train/so101-cables-all \
  --policy_repo_id Oscarcarrh/so101-cables-smolvla-all-v2 \
  --steps 50000 \
  --batch_size 32
```

O directamente con LeRobot:

```bash
lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --dataset.repo_id=Oscarcarrh/cables_vla_all_v2 \
  --dataset.root=./data/cables_vla_all_v2 \
  --batch_size=32 \
  --steps=50000 \
  --num_workers=8 \
  --output_dir=outputs/train/so101-cables-all \
  --policy.repo_id=Oscarcarrh/so101-cables-smolvla-all-v2 \
  --policy.device=cuda \
  --save_freq=5000 \
  --dataset.video_backend=pyav \
  --rename_map='{"observation.images.front": "observation.images.camera1", "observation.images.side": "observation.images.camera2"}'
```

---

## 8. Evaluación

```bash
python scripts/evaluate.py \
  --color red \
  --num_episodes 10
```

O directamente:

```bash
sudo chmod 666 /dev/ttyACM0

lerobot-record \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.cameras="{top: {type: opencv, index_or_path: /dev/video0, width: 640, height: 480, fps: 10}, front: {type: opencv, index_or_path: /dev/video2, width: 640, height: 480, fps: 10}}" \
  --policy.type=smolvla \
  --policy.pretrained_path=Oscarcarrh/so101-cables-smolvla-all-v2 \
  --policy.device=cuda \
  --dataset.repo_id=Oscarcarrh/eval_so101_red \
  --dataset.single_task="Disconnect the red alligator clip and place it in the red zone" \
  --dataset.num_episodes=10 \
  --dataset.episode_time_s=30 \
  --dataset.reset_time_s=30 \
  --interpolation_multiplier=5
```

---

## 9. Docker

### Build

```bash
docker build -t so101-intelligent-control .
```

### Entrenamiento

```bash
docker run --rm --gpus all \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/results:/app/results \
  so101-intelligent-control \
  python scripts/train.py
```

### Evaluación (sin hardware)

```bash
docker run --rm \
  -v $(pwd)/results:/app/results \
  so101-intelligent-control \
  python scripts/evaluate.py --offline
```

> **Nota:** La ejecución con robot físico y cámaras requiere privilegios adicionales. Ver sección de requisitos del sistema.

---

## 10. Resultados

### Tasa de éxito observada

| Color | Intentos | Éxito parcial | Observación |
|-------|----------|---------------|-------------|
| Rojo | 10 | ~60% | Alcanza el cable, gripper falla en último momento |
| Amarillo | 10 | ~55% | Comportamiento dirigido consistente |
| Verde | 10 | ~50% | Movimiento correcto, precisión insuficiente |

### Curva de pérdida (training loss)

![Loss curve](results/plots/loss_curve.png)

### Videos de demostración

| Color | Video |
|-------|-------|
| Modelo Rojo | [Ver video](results/videos/demo_red.mp4) |
| Modelo Amarillo | [Ver video](results/videos/demo_yellow.mp4) |
| Modelo Verde | [Ver video](results/videos/demo_green.mp4) |

---

## 11. Discusión y Limitaciones

- **Entorno de grabación ruidoso**: objetos extra en el entorno redujeron la calidad de las demostraciones
- **Brecha de frecuencia**: entrenamiento a 10 FPS vs inferencia a ~3 Hz (SmolVLA es un modelo de 500M params)
- **Fallo del gripper**: el robot alcanza el cable correctamente pero no logra el agarre fino en el último momento
- **Sin política de recuperación**: ante un fallo no hay mecanismo de reintento

---

## 12. Estructura del Repositorio

```
so101-intelligent-control/
├── README.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── scripts/
│   ├── record_vla.sh
│   ├── record_il.sh
│   ├── setup_cameras.sh
│   ├── train.py
│   ├── evaluate.py
│   └── run_demo.py
├── src/
│   ├── preprocessing/
│   ├── training/
│   ├── evaluation/
│   └── robot_execution/
├── data/
│   └── dataset_link.md
├── models/
├── results/
│   ├── metrics/
│   ├── plots/
│   ├── videos/
│   └── execution_demos/
├── report/
│   └── final_report.pdf
├── presentation/
│   └── SO101_VLA_Presentacion.pptx
├── tests/
│   └── test_core_modules.py
└── docs/
    └── additional_documentation.md
```

---

## 13. Presentación

La presentación final se encuentra en [`presentation/SO101_VLA_Presentacion.pptx`](presentation/SO101_VLA_Presentacion.pptx).

---

## 14. Referencias

- HuggingFace LeRobot Team. *SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics*. arXiv:2506.01844, 2025.
- Zhao et al. *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (ACT)*. arXiv:2304.13705, 2023.
- HuggingFace. *LeRobot Documentation*. https://huggingface.co/docs/lerobot
