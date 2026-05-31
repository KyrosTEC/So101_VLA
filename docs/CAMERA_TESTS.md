# Camera Tests

Este proyecto usa dos camaras:
- /dev/video0 = camara frontal
- /dev/video2 = camara lateral

Ver camaras disponibles:
```bash
v4l2-ctl --list-devices
```

Probar ambas simultaneamente:
```bash
python -c "
import cv2
cap0 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)
ret0, _ = cap0.read()
ret2, _ = cap2.read()
print('cam0 (front):', ret0)
print('cam2 (side): ', ret2)
cap0.release()
cap2.release()
print('OK - ready to record' if ret0 and ret2 else 'ERROR - check USB attach')
"
```
