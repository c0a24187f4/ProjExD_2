import os  # 標準ライブラリ
import random
import sys
import time
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


def gameover(screen: pg.Surface) -> None:  # ゲームオーバー時の動き
    """
    引数: main関数内のSurface screen
    戻り値: なし
    こうかとんと爆弾が接触した際に画面がブラックアウトしGameOverという文字列とこうかとんが出現する。5秒後に再度main関数が実行される
    """
    black_bg = pg.Surface((1100, 650))
    pg.draw.rect(black_bg, (0, 0, 0), (0, 0, 0, 0))  # 黒色の四角形を作成する
    black_bg.set_alpha(200)  # 不透明度200に設定

    game_over = pg.font.Font(None,80)  # フォントGame Overの設定
    txt = game_over.render("Game Over", True, (255, 255, 255))  # txtに文字列情報を代入する
    black_bg.blit(txt, [400, 325])  # Game Overの文字列をblack_bgにblit

    kk_img = pg.image.load("fig/8.png")
    black_bg.blit(kk_img, [340, 315])
    black_bg.blit(kk_img, [720, 315])  # 2体のこうかとんをblack_bgにblit

    screen.blit(black_bg, [0, 0])  # black_bgをscreenにblit

    pg.display.update()
    time.sleep(5)  # 5秒間スリープして再度main関数を実行する


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数: なし
    戻り値: 爆弾のサイズ・加速度タプル(10段階分)
    無限に拡大、加速するのはおかしいため、10段階分の爆弾サイズと加速度を格納した2つのlistを返す
    """
    bb_imgs = []  # Surface保存用の空リストの生成

    for r in range(1, 11):  # 10段階の爆弾サイズを用意するfor文
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    bb_accs = [a for a in range(1, 11)]  # 10段階の加速度を用意しbb_accsに格納する

    return bb_imgs, bb_accs


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

    bb_imgs, bb_accs = init_bb_imgs()  # 関数を呼び出して変数bb_imgs・bb_accsにリストを格納

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾がぶつかったらmain関数からreturnする
            gameover(screen)  # ゲームオーバー
            return

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

        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]

        center = bb_rct.center
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct = bb_img.get_rect()  # 当たり判定を画像サイズに合わせて再度生成する
        bb_rct.center = center  # 爆弾のワープを防ぐ

        side, vrtcl = check_bound(bb_rct)
        if not side:  # 横にはみ出ていたら
            avx *= -1
            vx *= -1
        if not vrtcl:  # 縦にはみ出ていたら
            avy *= -1
            vy *= -1  # 計算上はvx,vyが使用されているため、avx,avyだけ反転してしまうと外に行ってしまうので両方とも反転する

        bb_rct.move_ip(avx, avy)  # meve_ipに渡すのはavxとavyに変更
        screen.blit(bb_img, bb_rct)

        pg.display.update()

        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
