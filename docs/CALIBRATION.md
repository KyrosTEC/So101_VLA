# SO101 Calibration

Follower:
```bash
lerobot-calibrate \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0
```

Leader:
```bash
lerobot-calibrate \
  --teleop.type=so101_leader \
  --teleop.port=/dev/ttyACM1
```

Si aparece el mensaje de calibracion existente, presionar ENTER para usarla.
Usar 'c' solo si se quiere recalibrar desde cero.
