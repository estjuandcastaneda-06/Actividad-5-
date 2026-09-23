# Actividad 5 — Control de Brazo Robótico (ESP32 + PyBullet)

## Descripción general

Este proyecto implementa la teleoperación de un brazo robótico simulado en **PyBullet** a partir de 3 potenciómetros físicos conectados a un **ESP32**. El microcontrolador lee las posiciones de los potenciómetros, las mapea a los rangos articulares definidos en el archivo `brazo.urdf`, y las envía por comunicación serial (UART) a un script de Python que actualiza las articulaciones del robot en tiempo real.

## Funcionamiento

1. El ESP32 lee continuamente 3 entradas analógicas (potenciómetros).
2. Cada lectura (0–4095) se convierte a un valor en radianes dentro del límite articular correspondiente definido en el URDF.
3. Los tres valores se envían por Serial a 115200 baudios, en el formato:
   ```
   j1:<valor>,j2:<valor>,grip:<valor>
   ```
4. El script de Python (`control_brazo.py`) abre el puerto serial, lee cada línea, la interpreta (parseo por clave:valor) y aplica los valores a las articulaciones del robot cargado en PyBullet mediante `setJointMotorControl2` en modo `POSITION_CONTROL`.
5. El resultado es un control en vivo: al mover cualquier potenciómetro físico, la articulación correspondiente se mueve inmediatamente en la simulación 3D.

## Hardware y conexión

| Potenciómetro | Controla | Terminal A | Wiper (señal) | Terminal B |
|---|---|---|---|---|
| Pot 1 | Rotación de la base (`joint_1`) | 3V3 | **GPIO34** | GND |
| Pot 2 | Movimiento del hombro (`joint_2`) | 3V3 | **GPIO35** | GND |
| Pot 3 | Apertura/cierre de la pinza (`joint_dedo_izq` y `joint_dedo_der`) | 3V3 | **GPIO32** | GND |

Se usan pines ADC1 (34, 35, 32) porque son de solo entrada y no interfieren con el WiFi/Bluetooth del ESP32. El valor de resistencia del potenciómetro (1kΩ, 10kΩ, 50kΩ, etc.) no afecta la lectura, ya que el ESP32 solo mide la posición relativa del cursor como divisor de voltaje.

## Límites articulares (tomados de `brazo.urdf`)

| Articulación | Rango |
|---|---|
| `joint_1` (base) | -2.5 a 2.5 rad |
| `joint_2` (hombro) | -2.0 a 2.0 rad |
| `joint_dedo_izq` / `joint_dedo_der` (pinza) | 0.0 a 0.05 m |

## Archivos del repositorio

- **`control_brazo.ino`** — Código del ESP32: lectura de los 3 potenciómetros y envío por Serial.
- **`control_brazo.py`** — Script de Python: recibe los datos por Serial y controla el robot en PyBullet.
- **`brazo.urdf`** — Definición del modelo del brazo robótico (eslabones, articulaciones, límites).
- **Video** — Demostración de los 3 movimientos (base, hombro, pinza) respondiendo en tiempo real a los potenciómetros.
- **Capturas** — Código en Arduino IDE, Monitor Serial con datos en vivo, y el brazo en PyBullet en distintas posiciones.

## Requisitos para ejecutar

- Arduino IDE con soporte para ESP32 instalado.
- Python 3.11 (via entorno conda, recomendado por incompatibilidad de `pybullet` con versiones más nuevas en Windows).
- Librerías: `pybullet`, `pyserial`.

```
conda create -n brazo python=3.11 pybullet pyserial -c conda-forge
conda activate brazo
```

## Pasos de ejecución

1. Subir `control_brazo.ino` al ESP32 desde Arduino IDE.
2. Verificar en el Monitor Serial (115200 baudios) que los 3 valores cambian al mover cada potenciómetro, y luego **cerrar el Monitor Serial**.
3. En `control_brazo.py`, ajustar la variable `PUERTO` con el puerto COM real del ESP32.
4. Asegurarse de que `brazo.urdf` esté en la misma carpeta que `control_brazo.py`.
5. Ejecutar:
   ```
   conda activate brazo
   python control_brazo.py
   ```
6. Se abrirá la ventana de PyBullet con el brazo respondiendo en tiempo real a los potenciómetros.


