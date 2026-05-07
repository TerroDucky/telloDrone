import cv2
from djitellopy import Tello

def video_process():
    tello = Tello()
    tello.connect()

    tello.streamon()
    frame_reader = tello.get_frame_read()

    while True:
        frame = frame_reader.frame
        if frame is not None:
            cv2.imshow("Tello Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    tello.streamoff()
    cv2.destroyAllWindows()