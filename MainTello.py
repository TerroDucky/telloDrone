import time

from djitellopy import Tello
import pygame

tello = Tello()
tello.connect()
print("Battery:", tello.get_battery())

tello.takeoff()
time.sleep(1)

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Tello Control")
clock = pygame.time.Clock()


speed_xy = 100    # left / right / forward / back
speed_ud = 100    # up / down
speed_yaw = 90   # rotation


running = True

try:
    while running:
        lr = fb = ud = yaw = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        keys = pygame.key.get_pressed()

        # Movement keys

        if keys[pygame.K_a]:        # move left
            lr = -speed_xy
        elif keys[pygame.K_d]:      # move right
            lr = speed_xy

        if keys[pygame.K_w]:        # move forwards
            fb = speed_xy
        elif keys[pygame.K_s]:      # move back
            fb = -speed_xy

        if keys[pygame.K_UP]:       # go up
            ud = speed_ud
        elif keys[pygame.K_DOWN]:   # go down
            ud = -speed_ud

        if keys[pygame.K_LEFT]:     # turn left
            yaw = -speed_yaw
        elif keys[pygame.K_RIGHT]:  # turn right
            yaw = speed_yaw

        tello.send_rc_control(lr, fb, ud, yaw)
        clock.tick(20)
finally:
    tello.send_rc_control(0, 0, 0, 0)
    tello.land()
    pygame.quit()