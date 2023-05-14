import random
import sys

import pygame as pg

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習１
    bb_img.set_colorkey((0, 0, 0))  # 練習１
    x, y = random.randint(0, 1600), random.randint(0, 900)  # 練習２
    # screen.blit(bb_img, [x, y])  # 練習２
    vx, vy = +1, +1  # 練習３
    bb_rct = bb_img.get_rect()  # 練習３
    bb_rct.center = (x, y)  # 練習３
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0

        tmr += 1
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, [900, 400])
        bb_rct.move_ip(vx, vy)  # 練習３
        screen.blit(bb_img, bb_rct)  # 練習３

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()