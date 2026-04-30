from djitellopy import Tello
import pygame
import time

tello = Tello()
tello.connect()
print("Battery:", tello.get_battery())


pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Tello Control")
clock = pygame.time.Clock()

speed = 100
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

# Control keys
        if keys[pygame.K_TAB]: # takeoff
            tello.takeoff()

        if keys[pygame.K_o]: # turn off motors
            tello.turn_motor_off()
        if keys[pygame.K_p]: # turn on motors
            tello.turn_motor_on()

# Movement keys
        if keys[pygame.K_a]: # move left
            lr = -speed
        elif keys[pygame.K_d]: # move right
            lr = speed

        if keys[pygame.K_w]: # move forwards
            fb = speed
        elif keys[pygame.K_s]: # move back
            fb = -speed

        if keys[pygame.K_SPACE]: # go up
            ud = speed
        elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]: # go down
            ud = -speed

        if keys[pygame.K_q]: # turn left
            yaw = -speed
        elif keys[pygame.K_e]: #turn right
            yaw = speed

        tello.send_rc_control(lr, fb, ud, yaw)
        clock.tick(20)
finally:
    tello.send_rc_control(0, 0, 0, 0)
    tello.land()
    pygame.quit()