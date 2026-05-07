import time
import threading
import multiprocessing as mp
from djitellopy import Tello
import cv2

def video_thread(tello):
    tello.streamon()
    fr = tello.get_frame_read()
    while True:
        if fr.frame is not None:
            cv2.imshow("Tello", fr.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    tello.streamoff()
    cv2.destroyAllWindows()

def drone_process(q):
    tello = Tello()
    tello.connect()
    print("[DRONE] Battery:", tello.get_battery(), "%")

    threading.Thread(target=video_thread, args=(tello,), daemon=True).start()

    tello.takeoff()
    time.sleep(1)

    lr = fb = ud = yaw = 0
    last_ctrl = time.time()

    try:
        while True:
            if not q.empty():
                lr, fb, ud, yaw, ult = q.get()
                last_ctrl = time.time()
                if ult:
                    print("[DRONE] Ultimate!")
                    tello.flip_forward()

            if time.time() - last_ctrl > 0.3:
                tello.send_rc_control(0,0,0,0)
            else:
                tello.send_rc_control(lr, fb, ud, yaw)

            time.sleep(0.05)

    finally:
        tello.send_rc_control(0,0,0,0)
        time.sleep(0.5)
        tello.land()

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    q = mp.Queue(maxsize=1)

    mp.Process(target=__import__("controllerRead").controller_process, args=(q,)).start()
    mp.Process(target=drone_process, args=(q,)).start()