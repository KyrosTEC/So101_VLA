# Setup WSL + USBIPD

## 1. PowerShell como administrador

Ver dispositivos:
```powershell
usbipd list
```

Compartir y conectar camaras/brazos:
```powershell
usbipd bind --busid <BUSID>
usbipd attach --wsl --busid <BUSID>
```

Ejemplo para este proyecto:
```powershell
usbipd attach --wsl --busid 1-1
usbipd attach --wsl --busid 2-2
```

## 2. En Ubuntu/WSL
```bash
cd ~/so101_project
source venv/bin/activate
ls /dev/video*
ls /dev/ttyACM*

sudo chmod 666 /dev/video0 /dev/video2
sudo chmod 666 /dev/ttyACM0 /dev/ttyACM1
```
