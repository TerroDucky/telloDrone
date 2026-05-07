import serial
import time

def controller_process(control_queue):
    ser = serial.Serial("COM8", 9600, timeout=0.05)
    time.sleep(2)
    print("[CONTROLLER] Connected")

    CENTER = 512
    DEADZONE = 25
    SCALE = 90

    lr = fb = ud = yaw = 0
    yaw_btn = 0
    ult = False
    last_serial = time.time()

    def zero(v): return 0 if abs(v) < 5 else v

    while True:
        line = ser.readline().decode(errors="ignore").strip()
        now = time.time()

        if line:
            last_serial = now

            if line == "BTN:R:DOWN": yaw_btn = 30
            elif line == "BTN:R:UP": yaw_btn = 0
            elif line == "BTN:L:DOWN": yaw_btn = -30
            elif line == "BTN:L:UP": yaw_btn = 0
            elif line == "BTN:U:DOWN": ult = True

            elif line.startswith("JOY:"):
                _, data = line.split(":")
                axis, val = data.split(",")
                val = int(val)
                d = val - CENTER
                if abs(d) < DEADZONE: d = 0
                s = int((d / 512) * SCALE)

                if axis == "VX": yaw = s
                if axis == "VY": ud  = -s
                if axis == "MX": lr  = s
                if axis == "MY": fb  = -s

        # SERIAL FAILSAFE
        if now - last_serial > 0.2:
            lr = fb = ud = yaw = yaw_btn = 0

        yaw_f = zero(yaw + yaw_btn)
        lr, fb, ud = map(zero, (lr, fb, ud))

        while not control_queue.empty():
            control_queue.get()
        control_queue.put((lr, fb, ud, yaw_f, ult))
        ult = False