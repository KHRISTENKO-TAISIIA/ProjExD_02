import random
import sys

import pygame as pg


# 練習４
delta = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
        }


def check_bound(scr_rct: pg.Rect, obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数１：画面SurfaceのRect
    引数２：こうかとん，または，爆弾SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct =kk_img.get_rect()  # 練習４
    kk_rct.center = 900, 400  # 練習４

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

        # 練習４
        key_lst = pg.key.get_pressed()
        for k, mv in delta.items():
           if key_lst[k]:
               kk_rct.move_ip(mv)
        if check_bound(screen.get_rect(), kk_rct) != (True, True):
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rct.move_ip(-mv[0], -mv[1])
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)  # 練習４
        bb_rct.move_ip(vx, vy)  # 練習３
        yoko, tate = check_bound(screen.get_rect(), bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 練習３
        if kk_rct.colliderect(bb_rct):  # 練習６
            return 

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()