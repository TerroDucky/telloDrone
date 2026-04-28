from djitellopy import tello
t = tello.Tello()
t.connect()

# height = tello.get_height()

def fly():

    t.takeoff()
    t.move_up(40)
    t.land()



fly()