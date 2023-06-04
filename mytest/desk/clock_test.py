import pygame
import time
import math

import sys
def clock():

    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))

        # 绘制时针
        t = time.localtime()
        hour = t.tm_hour % 12
        hour_angle = (hour / 12) * 360
        hour_x = 200 + 75 * math.sin(math.radians(hour_angle))
        hour_y = 200 - 75 * math.cos(math.radians(hour_angle))
        pygame.draw.line(screen, (0, 0, 0), (200, 200), (hour_x, hour_y), 7)

        # 绘制分针
        minute = t.tm_min
        minute_angle = (minute / 60) * 360
        minute_x = 200 + 100 * math.sin(math.radians(minute_angle))
        minute_y = 200 - 100 * math.cos(math.radians(minute_angle))
        pygame.draw.line(screen, (0, 0, 0), (200, 200), (minute_x, minute_y), 5)

        # 绘制秒针
        second = t.tm_sec
        second_angle = (second / 60) * 360
        second_x = 200 + 125 * math.sin(math.radians(second_angle))
        second_y = 200 - 125 * math.cos(math.radians(second_angle))
        pygame.draw.line(screen, (255, 0, 0), (200, 200), (second_x, second_y), 3)

        pygame.display.flip()

        clock.tick(30)
def teest():
    import pygame
    import time

    # 初始化 Pygame
    pygame.init()

    # 设置窗口大小和标题
    window_size = (600, 300)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pixel Style Date & Time Display")

    # 加载字体
    font = pygame.font.Font(None, 36)

    # 设置白色背景
    white = (255, 255, 255)
    window.fill(white)

    # 循环渲染文本
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 获取当前日期和时间
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 将文本渲染为图像
        text_image = font.render(current_time, True, (0, 0, 0))

        # 将图像绘制到窗口中
        window.blit(text_image, (50, 50))

        # 刷新屏幕
        pygame.display.update()
if __name__ == '__main__':
    teest()