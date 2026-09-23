import pybullet as p
import pybullet_data
import serial
import time


PUERTO = "COM7"      # Cambia por el puerto real de tu ESP32
BAUDRATE = 115200

ser = serial.Serial(PUERTO, BAUDRATE, timeout=1)
time.sleep(2)

physics_client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

robot_id = p.loadURDF("brazo.urdf", [0, 0, 0.15], useFixedBase=True)

num_joints = p.getNumJoints(robot_id)
joint_index = {}
for i in range(num_joints):
    info = p.getJointInfo(robot_id, i)
    name = info[1].decode("utf-8")
    joint_index[name] = i
    print(f"Joint {i}: {name} (tipo: {info[2]})")

def parse_linea(linea):
    
    datos = {}
    try:
        for par in linea.strip().split(","):
            clave, valor = par.split(":")
            datos[clave] = float(valor)
    except ValueError:
        return None
    return datos

print("Iniciando teleoperacion... (Ctrl+C para salir)")

try:
    while True:
        if ser.in_waiting > 0:
            linea = ser.readline().decode("utf-8", errors="ignore")
            datos = parse_linea(linea)
            if datos and all(k in datos for k in ("j1", "j2", "grip")):
                p.setJointMotorControl2(robot_id, joint_index["joint_1"],
                                         p.POSITION_CONTROL, targetPosition=datos["j1"])
                p.setJointMotorControl2(robot_id, joint_index["joint_2"],
                                         p.POSITION_CONTROL, targetPosition=datos["j2"])
                p.setJointMotorControl2(robot_id, joint_index["joint_dedo_izq"],
                                         p.POSITION_CONTROL, targetPosition=datos["grip"])
                p.setJointMotorControl2(robot_id, joint_index["joint_dedo_der"],
                                         p.POSITION_CONTROL, targetPosition=datos["grip"])

        p.stepSimulation()
        time.sleep(1.0 / 240.0)

except KeyboardInterrupt:
    print("Cerrando conexion...")
finally:
    ser.close()
    p.disconnect()
