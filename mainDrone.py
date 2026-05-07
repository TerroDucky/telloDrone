import time
import multiprocessing as mp
from djitellopy import Tello

def drone_process(control_queue):
    tello = Tello()
    tello.connect()
    print("Battery:", tello.get_battery())

    tello.takeoff()
    time.sleep(1)

    try:
        lr = fb = ud = yaw = 0

        while True:
            # Get latest control values
            if not control_queue.empty():
                lr, fb, ud, yaw = control_queue.get()

            tello.send_rc_control(lr, fb, ud, yaw)
            time.sleep(0.05)  # ~20 Hz

    finally:
        tello.send_rc_control(0, 0, 0, 0)
        tello.land()


if __name__ == "__main__":
    q = mp.Queue(maxsize=1)

    controller = mp.Process(
        target=__import__("controllerRead").controller_process,
        args=(q,)
    )
    drone = mp.Process(target=drone_process, args=(q,))
    video = mp.Process(
        target=__import__("video_stream").video_process
    )

    controller.start()
    drone.start()
    video.start()

    controller.join()
    drone.join()
    video.join()