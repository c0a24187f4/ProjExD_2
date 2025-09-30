import os  # 標準ライブラリ
import random
import sys
import pygame as pg  # サードパーティー性ライブラリ
# ここ以下に自作ライブラリ。ライブラリは基本五十音順らしい


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0),  # Pythonではリストや辞書の最後にも「,」を付けることが一般的
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数： こうかとんRect or 爆弾Rect
    戻り値: 横・縦方向の判定結果タプル(True: 画面内, False: 画面外)
    Rectオブジェクトのleft, right, top, bottomの値から画面内(True)・外(False)を判定する
    """
    side, vrtcl = True, True
    if rct.left < 0 or WIDTH < rct.right:
        side = False  # 横にはみ出たらFalse
    if rct.top < 0 or HEIGHT < rct.bottom:
        vrtcl = False  # 縦にはみ出たFalse
    return side, vrtcl


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img = pg.image.load("fig/pg_bg.jpg")  

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  # サイズのみ設定された空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 中心座標(10, 10)半径10の赤丸(爆弾)
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒い部分を透明に
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾Rectの初期位置がランダムになりつつ画面外にならないように

    vx, vy = +5, +5  # 爆弾の移動速度
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        """
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5
        """
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        side, vrtcl = check_bound(bb_rct)
        if not side:  # 横にはみ出ていたら
            vx *= -1.1
        if not vrtcl:  # 縦にはみ出ていたら
            vy *= -1.1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)

        pg.display.update()

        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
