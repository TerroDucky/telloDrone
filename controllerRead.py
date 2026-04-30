import pygame
import multiprocessing as mp

def controller_process(control_queue):
    pygame.init()
    pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Controller Input")

    clock = pygame.time.Clock()

    speed_xy = 100
    speed_ud = 100
    speed_yaw = 90

    running = True

    while running:
        lr = fb = ud = yaw = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Movement keys (same logic you already had)
        if keys[pygame.K_a]:
            lr = -speed_xy
        elif keys[pygame.K_d]:
            lr = speed_xy

        if keys[pygame.K_w]:
            fb = speed_xy
        elif keys[pygame.K_s]:
            fb = -speed_xy

        if keys[pygame.K_UP]:
            ud = speed_ud
        elif keys[pygame.K_DOWN]:
            ud = -speed_ud

        if keys[pygame.K_LEFT]:
            yaw = -speed_yaw
        elif keys[pygame.K_RIGHT]:
            yaw = speed_yaw

        # Send latest control values (non‑blocking)
        if not control_queue.full():
            control_queue.put((lr, fb, ud, yaw))

        clock.tick(20)

    pygame.quit()


if __name__ == "__main__":
    q = mp.Queue(maxsize=1)
    controller_process(q)