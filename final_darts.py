import pygame
import math
from bitalino import BITalino

macAddress = "98:D3:11:FE:02:2B"
acqChannels = [2, 3]  # A3 A4
samplingRate = 1000
nSamples = 1000//30
tap_threshold = 650  # ダーツを投げる筋電の閾値
ave_ac_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #ダーツを投げる加速度10フレーム分
max_tap_list = [0, 0, 0, 0 , 0, 0, 0] #ダーツを投げる筋電7フレーム分


# BITalino接続
device = BITalino(macAddress)



# Pygameの初期化
pygame.init()

# 画面サイズ
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ダツDEダーツ")

# 日本語フォントの設定
font_path = "C:/Windows/Fonts/YuGothM.ttc"  # フォントファイルのパス
font_size = 36
font = pygame.font.Font(font_path, font_size)


# 色の定義
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 画像の読み込み
datu_img = pygame.image.load("bitalino/chara/datu1.png")  # ダーツの画像
datu_img = pygame.transform.scale(datu_img, (SCREEN_WIDTH*0.15, SCREEN_WIDTH*0.025))

suna_img = pygame.image.load("bitalino/chara/suna.jpg")  # 地面の画像
suna_img = pygame.transform.scale(suna_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

sea_img = pygame.image.load("bitalino/chara/sea.jpg")  # 地面の画像
sea_img = pygame.transform.scale(sea_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

sea2_img = pygame.image.load("bitalino/chara/sea2.jpg")  # 地面の画像
sea2_img = pygame.transform.scale(sea2_img, (SCREEN_WIDTH*0.3, SCREEN_HEIGHT*0.3))

ground_img = pygame.image.load("bitalino/chara/ground.jpg")  # 地面の画像
ground_img = pygame.transform.scale(ground_img, (SCREEN_WIDTH*0.5, SCREEN_WIDTH*0.15))

maru_img = pygame.image.load("bitalino/chara/maru.png")
maru_img = pygame.transform.scale(maru_img, (SCREEN_WIDTH*0.07, SCREEN_WIDTH*0.07))

human1_img = pygame.image.load("bitalino/chara/human1.png")  # 人１の画像
human1_img = pygame.transform.scale(human1_img, (SCREEN_WIDTH*0.24, SCREEN_WIDTH*0.42))

arm2_img = pygame.image.load("bitalino/chara/arm2.png")  # 腕２の画像
arm2_img = pygame.transform.scale(arm2_img, (SCREEN_WIDTH*0.3, SCREEN_WIDTH*0.3))

mato_img = pygame.image.load("bitalino/chara/mato.png")  # 的の画像
mato_img = pygame.transform.scale(mato_img, (SCREEN_WIDTH * 0.1, SCREEN_WIDTH * 0.2))

retry_img = pygame.image.load("bitalino/chara/retry.png")  # リトライの画像
retry_img = pygame.transform.scale(retry_img, (SCREEN_WIDTH * 0.08, SCREEN_WIDTH * 0.08))

title_img = pygame.image.load("bitalino/chara/title3.png")  # タイトル画像
title_img = pygame.transform.scale(title_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

num_imgs = []  # 画像をリストに格納
# ステージ選択ボタンの設定
num_rects = [0]
for i in range(4):
    img = pygame.image.load(f"bitalino/chara/num_{i}.png")  # 数字画像の読み込み
    img = pygame.transform.scale(img, (SCREEN_WIDTH * 0.08, SCREEN_WIDTH * 0.08))
    num_imgs.append(img)  # リストに追加
    k = i + 1
    k = k %  3
    
    if k == 0:
        k = 3
    num_rect = pygame.Rect(SCREEN_WIDTH * (0.2 * k + 0.03), SCREEN_HEIGHT * 0.4, SCREEN_WIDTH * 0.1, SCREEN_WIDTH * 0.1)
    num_rects.append(num_rect)

print(len(num_rects))


obj_l = SCREEN_WIDTH * 0.08

# 障害物の画像
obstacle_img = pygame.image.load("bitalino/chara/sango1.png")  # 障害物1の画像
obstacle_img = pygame.transform.scale(obstacle_img, (obj_l, obj_l))

obstacle2_img = pygame.image.load("bitalino/chara/sango2.png")  # 障害物2の画像
obstacle2_img = pygame.transform.scale(obstacle2_img, (obj_l, obj_l))

obstacle3_img = pygame.image.load("bitalino/chara/sango3.png")  # 障害物3の画像
obstacle3_img = pygame.transform.scale(obstacle3_img, (obj_l, obj_l))

tetora_img = pygame.image.load("bitalino/chara/sango1.png")  # 障害物3の画像
tetora_img = pygame.transform.scale(tetora_img, (obj_l, obj_l))


# **リトライボタンの設定**
button_rect = pygame.Rect(SCREEN_WIDTH * 0.05, SCREEN_HEIGHT // 8, SCREEN_WIDTH * 0.07, SCREEN_WIDTH * 0.07)
show_retry_button = True  # 初期状態では表示


# ダーツの初期位置
datu_pos = [SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.47]
ball_vel = [0, 0]
ball_in_motion = False  # ボールが動いているかどうか
angle = 0

# 腕の長さ
l = SCREEN_WIDTH * 0.3 / 2 * 0.9

#　人１の初期位置
human1_pos = [0, SCREEN_HEIGHT * 0.4]

#　腕２の初期位置
arm2_pos = [SCREEN_WIDTH * 0.21, SCREEN_HEIGHT * 0.68]
arm2_speed = 1  # 回転速度
arm2_angle = 0  # 初期角度
sea2_pos = [SCREEN_WIDTH * 0.21, SCREEN_HEIGHT * 0.55]
# 丸の位置
maru_pos = [SCREEN_WIDTH * 0.21, SCREEN_HEIGHT * 0.68]

# ゴールの位置
mato_pos = (SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2 - 50)

# 物理パラメータ
gravity = 0.4  # 重力
friction = 0.99  # 摩擦（徐々にボールが減速）

# スプライトクラス
class Darts(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.vel = [0, 0]
        self.i_g = 0
        self.angle = 0  # 角度を追加

    def update(self):
        # 座標の更新
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.rect.center = self.pos

        # 重力と摩擦
        if self.vel[1] > 0 or self.i_g <= 30:
            self.vel[1] += gravity
            self.i_g += 1
            if self.vel[1] < 0:
                self.vel[1] -= 0.05 / self.i_g + 0.005
        else:
            self.vel[1] += gravity

        self.vel[0] *= friction
        self.vel[1] *= friction

        # ダーツの角度更新
        if self.vel[0] != 0 or self.vel[1] != 0:
            self.angle = -math.degrees(math.atan2(self.vel[1], self.vel[0]))
        # 回転処理
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # 外に出たら削除
        if self.pos[0] > SCREEN_WIDTH or self.pos[1] > SCREEN_HEIGHT:
            self.kill()
            reset_game()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.rect.inflate_ip(-10, -10)

# 障害物グループの作成
obstacle_group = pygame.sprite.Group()
obstacle1 = Obstacle(obstacle_img, (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5))
obstacle2 = Obstacle(obstacle2_img, (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5 + obj_l))
obstacle3 = Obstacle(obstacle3_img, (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5 + obj_l * 2))
obstacle4 = Obstacle(tetora_img, (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5 + obj_l * 3))
obstacle_group.add(obstacle1, obstacle2, obstacle3, obstacle4)

# ダーツグループの作成
darts_group = pygame.sprite.Group()
darts = Darts(datu_img, datu_pos)
darts_group.add(darts)


# 取得したセンサのデータのうちA3最大値とA4平均値を返す
def max_tap_and_ave_ac_values(data):
    max_value = max(row[-2] for row in data)  # 筋電最大値
    ave_value = sum(row[-1] for row in data) / len(data)  # 加速度平均値
    return [max_value, ave_value]  # リストで返す

def get_power(ac_list):
    max_ac = max(ac_list)
    power = 0.0625 * max_ac - 20.5
    return power

def check_collision(darts, obstacle_group):
    """ダーツの先端で当たり判定を行う"""
    # ダーツの中心座標
    center_x, center_y = darts.rect.center

    # ダーツの角度に基づいて先端座標を計算
    tip_length = darts.rect.width // 2
    tip_x = center_x + math.cos(math.radians(darts.angle)) * tip_length
    tip_y = center_y + math.sin(math.radians(darts.angle)) * tip_length

    # 先端を小さい矩形で判定
    tip_rect = pygame.Rect(tip_x - 2, tip_y - 2, 4, 4)

    for obstacle in obstacle_group:
        if tip_rect.colliderect(obstacle.rect):
            return True
    return False


# 修正①：check_goal_collision関数でダーツの角度を使用
def check_goal_collision(darts, mato_rect):
    center_x, center_y = darts.rect.center

    # ダーツの角度を取得して先端座標を計算
    tip_length = darts.rect.width // 2
    tip_x = center_x + math.cos(math.radians(darts.angle)) * tip_length
    tip_y = center_y + math.sin(math.radians(darts.angle)) * tip_length

    return mato_rect.collidepoint((tip_x, tip_y))

# ゲームリセット関数
def reset_game():
    global ball_vel, ball_in_motion, arm2_angle, show_retry_button, darts, dragging
    ball_vel = [0, 0]
    ball_in_motion = False
    arm2_angle = 0
    show_retry_button = True
    darts.kill()  # ダーツを削除
    darts = Darts(datu_img, datu_pos)  # 新しいダーツを作成
    darts_group.add(darts)

    # 背景 
    ground_rect2 = ground_img.get_rect(center=(SCREEN_WIDTH*0.75, SCREEN_HEIGHT - SCREEN_WIDTH * 0.15 / 2))
    ground_rect1 = ground_img.get_rect(center=(SCREEN_WIDTH*0.25, SCREEN_HEIGHT - SCREEN_WIDTH * 0.15 / 2))
    sea_rect = sea_img.get_rect(center=(SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.5))
    screen.blit(sea_img, sea_rect)
    screen.blit(ground_img, ground_rect1)
    screen.blit(ground_img, ground_rect2)
    screen.blit(mato_img, mato_pos)
        
# ステージ選択画面
def select_stege_screen():
    # 背景
    suna_rect = suna_img.get_rect(center=suna_img.get_rect(center=(SCREEN_WIDTH*0.5, 
                                                                         SCREEN_HEIGHT * 0.5)).center)
    screen.blit(suna_img, suna_rect)
    select_text = font.render("ステージセレクト", True, BLACK)

    screen.blit(select_text, (SCREEN_WIDTH * 0.4 , SCREEN_HEIGHT * 0.25 ))
    for i in range(3):
        i += 1
        stage_num = num_imgs[i]
        num_rect = num_rects[i]
        pygame.draw.rect(screen, WHITE, num_rect)
        screen.blit(stage_num, (num_rect.x + (SCREEN_WIDTH * 0.009), num_rect.y + (SCREEN_WIDTH * 0.008) ))
    pygame.display.flip()
    # ユーザーの入力待ち
    waiting = True
    while waiting:
        screen.blit(suna_img, suna_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # リトライボタンが表示されている場合の処理
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(num_rects)):
                    if i != 0:
                        if num_rects[i].collidepoint(event.pos):
                            waiting = False
    game_screen()


# スタート画面
def show_start_screen():
    # 背景
    title_rect = title_img.get_rect(center=title_img.get_rect(center=(SCREEN_WIDTH*0.5, 
                                                                         SCREEN_HEIGHT * 0.5)).center)
    screen.blit(title_img, title_rect)
    pygame.display.flip()

    # ユーザーの入力待ち
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
    select_stege_screen()
    


# 成功画面
def show_completed_screen():
    title_text = font.render("クリア！！", True, WHITE)
    start_text = font.render("クリックまたはスペースキーでステージ選択画面へ", True, WHITE)

    screen.blit(title_text, (SCREEN_WIDTH * 0.2 , SCREEN_HEIGHT * 0.2 ))
    screen.blit(start_text, (SCREEN_WIDTH *0.2,  SCREEN_HEIGHT * 0.3))

    pygame.display.flip()

    # ユーザーの入力待ち
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
    select_stege_screen()


def game_screen():
    clock = pygame.time.Clock()
    running = True
    global ball_in_motion, arm2_angle, arm2_speed, darts
    device.start(samplingRate, acqChannels)

    # 背景
    ground_rect2 = ground_img.get_rect(center=(SCREEN_WIDTH*0.75, SCREEN_HEIGHT - SCREEN_WIDTH * 0.15 / 2))
    ground_rect1 = ground_img.get_rect(center=(SCREEN_WIDTH*0.25, SCREEN_HEIGHT - SCREEN_WIDTH * 0.15 / 2))
    maru_rect = maru_img.get_rect(center=maru_img.get_rect(center=(maru_pos[0], maru_pos[1])).center)
    sea_rect = sea_img.get_rect(center=(SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.5))
    sea2_rect = sea2_img.get_rect(center=sea2_pos)
    mato_rect = pygame.Rect(mato_pos[0], mato_pos[1] +10, 100, 210)
    pygame.draw.rect(screen, WHITE, button_rect)
    screen.blit(sea_img, sea_rect)
    screen.blit(ground_img, ground_rect1)
    screen.blit(ground_img, ground_rect2)
    screen.blit(mato_img, mato_pos)
    screen.blit(retry_img, (button_rect.x - (SCREEN_WIDTH * 0.005), button_rect.y - (SCREEN_WIDTH * 0.005)))

    while running:
        # 背景やオブジェクトの描画
        screen.blit(sea2_img, sea2_rect)
        screen.blit(human1_img, human1_pos)
        
        # BITalinoからデータを取得
        data = device.read(nSamples)
        values = max_tap_and_ave_ac_values(data)
        # A3とA4のデータを保存
        max_tap = values[0]
        max_tap_list.append(max_tap) #新しい筋電をリストに追加
        popped_item = max_tap_list.pop(0) #一番古い筋電を削除

        ave_ac = values[1]
        ave_ac_list.append(ave_ac) #新しい加速度をリストに追加
        popped_item = ave_ac_list.pop(0) #一番古い加速度を削除
        power = get_power(ave_ac_list) 


        # 腕の描画
        if not ball_in_motion and not check_goal_collision(darts, mato_rect):
            arm2_angle += arm2_speed
            if arm2_angle >= 70 or arm2_angle <= -30:
                arm2_speed *= -1
            rotated_arm2 = pygame.transform.rotate(arm2_img, arm2_angle)
            arm2_rect = rotated_arm2.get_rect(center=arm2_pos)
            screen.blit(rotated_arm2, arm2_rect)
        else :
            # 腕の描画
            after_arm2 = pygame.transform.rotate(arm2_img, angle)
            after_arm2 = pygame.transform.rotate(arm2_img, -75)
            arm2_rect = after_arm2.get_rect(center=arm2_img.get_rect(center=(arm2_pos[0], arm2_pos[1])).center)
            screen.blit(after_arm2, arm2_rect)

        # 丸の描画
        screen.blit(maru_img, maru_rect)
        
        obstacle_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and show_retry_button:
                if button_rect.collidepoint(event.pos):
                    reset_game()

            if max_tap_list[0] > tap_threshold and not ball_in_motion:
                ball_in_motion = True
                power = get_power(ave_ac_list)
                # **古いダーツを削除**
                darts_group.empty()

                # ダーツ生成位置と角度計算
                datu_pos = [arm2_pos[0] - l * math.sin(math.radians(arm2_angle)),
                            arm2_pos[1] - l * math.cos(math.radians(arm2_angle))]

                # **角度を記録してダーツ生成**
                darts = Darts(datu_img, datu_pos)
                darts.angle = arm2_angle  # 角度を記録
                darts.vel = [power * math.cos(math.radians(darts.angle)), 
                             -power * math.sin(math.radians(darts.angle))]

                darts_group.add(darts)

        if ball_in_motion:
            darts_group.update()
            darts_group.draw(screen)

        # 衝突判定
        if check_collision(darts, obstacle_group) or darts.pos[1] >= SCREEN_HEIGHT - 50:
            # time.sleep(1)
            reset_game()

        if check_goal_collision(darts, mato_rect):
            device.stop()
            reset_game()
            show_completed_screen()


        pygame.display.flip()
        clock.tick(60)
    # データ取得終了・接続終了
    device.stop()
    pygame.quit()


if __name__ == "__main__":
    show_start_screen()
    device.close()
    pygame.quit()