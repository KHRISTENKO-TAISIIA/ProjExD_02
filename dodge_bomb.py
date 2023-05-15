import random
import sys

import pygame as pg

# 押下キーに対する移動量の辞書
delta = {
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, +1),
    pg.K_LEFT: (-1, 0),
    pg.K_RIGHT: (+1, 0),
}


def check_bound(area: pg.Rect, obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数１：画面SurfaceのRect
    引数２：こうかとん，または，爆弾SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < area.left or area.right < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < area.top or area.bottom < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img_load = pg.image.load("ex02/fig/3.png")
    kk_img_1 = pg.transform.rotozoom(kk_img_load, 0, 2.0)  # こうかとんのベース画像
    kk_img_2 = pg.transform.flip(kk_img_1, True, False)  # rotozoomするためのflipしたこうかとんの画像
    # こうかとんの画像方向の辞書
    kk_imgs = {
        (+1, 0): kk_img_2,  # 右方向こうかとんの画像
        (+1, -1): pg.transform.rotozoom(kk_img_2, 45, 1.0),  # 右上方向こうかとんの画像
        (0, -1): pg.transform.rotozoom(kk_img_2, 90, 1.0),  # 上方向こうかとんの画像
        (-1, -1): pg.transform.rotozoom(kk_img_1, -45, 1.0),  # 左上方向こうかとんの画像
        (-1, 0): kk_img_1,  # 左方向こうかとんの画像
        (-1, +1): pg.transform.rotozoom(kk_img_1, 45, 1.0),  # 左下方向こうかとんの画像
        (0, +1): pg.transform.rotozoom(kk_img_2, -90, 1.0),  # 下方向こうかとんの画像
        (+1, +1): pg.transform.rotozoom(kk_img_2, -45, 1.0),  # 右下方向こうかとんの画像
        }
    kk_img = kk_imgs[+1, 0]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    # 爆弾の画像サイズの辞書
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    x, y = random.randint(0, 1600), random.randint(0, 900)
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = (x, y)
    vx, vy = +1, +1
    accs = [a for a in range(1, 11)]  # 加速度のリスト

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        tmr += 1
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):  # 着弾するとこうかとん画像が切り替わる
            kk_img_lose_load = pg.image.load("ex02/fig/9.png")
            kk_img_lose = pg.transform.rotozoom(kk_img_lose_load, 0, 2.0)
            kk_img = kk_img_lose
            screen.blit(kk_img, kk_rct)
            pg.display.update()
            return

        key_lst = pg.key.get_pressed()
        # こうかとんの画像方向を選ぶための変数
        kk_0 = 0
        kk_1 = 0
        for k, mv in delta.items():
            if key_lst[k]:
                kk_rct.move_ip(mv)
                kk_0 = kk_0 + mv[0]
                kk_1 = kk_1 + mv[1]
        if check_bound(screen.get_rect(), kk_rct) != (True, True):
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rct.move_ip(-mv[0], -mv[1])
        if kk_0 != 0 or kk_1 != 0:  # 飛ぶ方向に従ってこうかとん画像を切り替える
            kk_img = kk_imgs[kk_0, kk_1]
        screen.blit(kk_img, kk_rct)

        yoko, tate = check_bound(screen.get_rect(), bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        # 時間とともに爆弾が加速する and 大きくなる
        avx, avy = vx*accs[min(tmr//1000, 9)], vy*accs[min(tmr//1000, 9)]  # 時間とともに爆弾が加速する
        bb_rct.move_ip(avx, avy)
        bb_img = bb_imgs[min(tmr//1000, 9)]  # 時間とともに爆弾が大きくなる
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()