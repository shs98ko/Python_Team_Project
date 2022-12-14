import pygame
import time
import sys
import os
import random

# 초기화(반드시 필요)
pygame.init()
pygame.mixer.init()
# 화면 크기 설정
screen_width = 940  # 화면 가로 크기
screen_height = 550  # 화면 세로 크기
screen = pygame.display.set_mode(
    (screen_width, screen_height))  # 화면 크기설정
pygame.display.set_caption("Ball_Game")  # 타이틀
clock = pygame.time.Clock()  # FPS

# 사용자 게임 초기화 (이미지나 음악 불러오기, 캐릭터 정의, 공 정의, 스테이지 정의, 폰트 정의)
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환
game_image_path = os.path.join(current_path, "game_images")
init_image_path = os.path.join(current_path, "init_images")
finish_image_path = os.path.join(current_path, "finish_images")

# 초기화면 이미지
mainmenu_background = pygame.image.load(
    os.path.join(init_image_path, "background.png"))
img1 = pygame.image.load(
    os.path.join(init_image_path, "ball.png"))
img1 = pygame.transform.scale(img1, (100, 100))
img2 = pygame.image.load(
    os.path.join(init_image_path, "Human.png"))
mainmenu_easy = pygame.image.load(os.path.join(init_image_path, "Easy.png"))
mainmenu_normal = pygame.image.load(
    os.path.join(init_image_path, "Normal.png"))
mainmenu_hard = pygame.image.load(os.path.join(init_image_path, "Hard.png"))
mainmenu_easy_click = pygame.image.load(
    os.path.join(init_image_path, "Easy_click.png"))
mainmenu_normal_click = pygame.image.load(
    os.path.join(init_image_path, "Normal_click.png"))
mainmenu_hard_click = pygame.image.load(
    os.path.join(init_image_path, "Hard_click.png"))

# 게임 진행 이미지
game_background = pygame.image.load(
    os.path.join(game_image_path, "background.png"))  # 배경
game_stage = pygame.image.load(os.path.join(
    game_image_path, "stage.png"))  # 스테이지
game_character = pygame.image.load(
    os.path.join(game_image_path, "character.png"))  # 캐릭터
game_ball_images = [
    pygame.image.load(os.path.join(game_image_path, "ballon0.png")),
    pygame.image.load(os.path.join(game_image_path, "ballon1.png")),
    pygame.image.load(os.path.join(game_image_path, "ballon2.png")),
    pygame.image.load(os.path.join(game_image_path, "ballon3.png")),
    pygame.image.load(os.path.join(game_image_path, "ballon4.png"))
]

# hard mode 랜덤 벽
game_wall_1 = pygame.image.load(
    os.path.join(game_image_path, "wall_1.png"))
game_wall_2 = pygame.image.load(
    os.path.join(game_image_path, "wall_2.png"))
a = random.randint(300, 500)
b = random.randint(600, 800)

# 스테이지
# 스테이지 크기 불러오기
stage_size = game_stage.get_rect().size
stage_height = stage_size[1]

# 캐릭터
character_size = game_character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 10

# 공
# 공 크기에 따른 최초 스피드
ball_speed_y = [-30, -30, -31, -32, -32]  # index 0,1,2,3에 해당하는 값

# 공들
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x": 50,  # 공의 x좌표
    "pos_y": 50,  # 공의 y좌표
    "img_idx": 0,  # 공의 이미지 인덱스
    "to_x": 3,  # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
    "to_y": -6,  # y축 이동방향
    "init_spd_y": ball_speed_y[0]  # y 최초 속도
})

# 사라질 공 정보 저장 변수
ball_to_remove = -1

# font 정의
game_font = pygame.font.Font(None, 40)
# 게임 종료 메시지
#  Mission Complete(성공)
#  Game Over (캐릭터 공에 맞음, 실패)
game_result = "Game Over"


# 음악
sfx1 = pygame.mixer.Sound(os.path.join(
    game_image_path, "start.ogg"))
sfx2 = pygame.mixer.Sound(os.path.join(
    game_image_path, "gameover.ogg"))
sfx3 = pygame.mixer.Sound(os.path.join(
    game_image_path, "clear.ogg"))
bgm1 = pygame.mixer.Sound(os.path.join(
    init_image_path, "init_bgm.ogg"))
bgm2 = pygame.mixer.Sound(os.path.join(
    game_image_path, "main_bgm.ogg"))


class Button:  # 버튼
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  # 마우스 좌표
        click = pygame.mouse.get_pressed()  # 클릭여부
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 마우스가 버튼안에 있을 때
            screen.blit(img_act, (x_act, y_act))  # 버튼 이미지 변경
            if click[0] and action is not None:  # 마우스가 버튼안에서 클릭되었을 때
                time.sleep(0.2)
                action()
        else:
            screen.blit(img_in, (x, y))


def mainmenu():  # 시작메뉴

    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(mainmenu_background, (0, 0))
        screen.blit(img1, (750, 350))
        screen.blit(img2, (100, 350))
        bgm1.set_volume(0.1)
        bgm1.play()
        Button(mainmenu_easy, 380, 235, 150, 80,
               mainmenu_easy_click, 360, 220, easy)
        Button(mainmenu_normal, 380, 335, 150, 80,
               mainmenu_normal_click, 360, 320, normal)
        Button(mainmenu_hard, 380, 435, 150, 80,
               mainmenu_hard_click, 360, 420, hard)

        pygame.display.update()
        clock.tick(15)


def easy():  # easy모드
    global character_x_pos, character_to_x, ball_to_remove, game_result
    running = True
    bgm1.stop()  # 음향
    sfx1.set_volume(0.5)
    sfx1.play(0)
    bgm2.set_volume(0.3)
    bgm2.play()
    while running:
        pygame.init()
        clock.tick(30)

        # 이벤트 처리(키보트, 마우스 등)
        for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가?
            if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가?
                running = False  # 게임이 진행중이 아님

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                    character_to_x -= character_speed
                elif event.key == pygame.K_RIGHT:  # 캐릭터를 오른쪽으로
                    character_to_x += character_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_to_x = 0

        # 게임 캐릭터 위치 정의
        character_x_pos += character_to_x

        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        # 공 위치 정의
        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            ball_size = game_ball_images[ball_img_idx].get_rect().size
            ball_width = ball_size[0]
            ball_height = ball_size[1]

            # 가로벽에 닿았을 때 공 이동 위치 변경(튕겨 나오는 효과)
            if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"] = ball_val["to_x"] * -1

            # 세로 위치
            # 스테이지에 튕겨서 올라가는 처리
            if ball_pos_y >= screen_height - stage_height - ball_height:
                ball_val["to_y"] = ball_val["init_spd_y"]
            # 천장에 튕겨서 내려가는 처리
            elif ball_pos_y <= 0:
                ball_val["to_y"] = 0.5
            else:  # 그 외의 모든 경우에는 속도를 증가
                ball_val["to_y"] += 1

            ball_val["pos_x"] += ball_val["to_x"]
            ball_val["pos_y"] += ball_val["to_y"]

        # 충돌처리

        # 캐릭터 rect 정보 업데이트
        character_rect = game_character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            # 공 rect 정보 업데이트
            ball_rect = game_ball_images[ball_img_idx].get_rect()
            ball_rect.left = ball_pos_x
            ball_rect.top = ball_pos_y

            # 공과 캐릭터 충돌처리
            if character_rect.colliderect(ball_rect):
                running = False
                bgm2.stop()
                sfx2.set_volume(0.5)
                sfx2.play()
                break

            if ball_pos_y == 0:  # 천장에 부딪혔을 때
                ball_to_remove = ball_idx
                if ball_img_idx < 3:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = game_ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        # 공의 x좌표
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        # 공의 y좌표
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": -7,  # x축 이동방향
                        "to_y": -3,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})  # y 최초 속도

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        # 공의 x좌표
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        # 공의 y좌표
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": 6,  # x축 이동방향
                        "to_y": -1,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})  # y 최초 속도
                break

        # 충돌된 공 없애기
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1

        # 모든 공을 없앤 경우 게임 종료 (성공)
        if len(balls) == 0:
            game_result = "Clear"
            bgm2.stop()
            sfx3.set_volume(0.2)
            sfx3.play()
            running = False

        # 화면에 그리기
        screen.blit(game_background, (0, 0))  # 배경

        for idx, val in enumerate(balls):  # 공
            ball_pos_x = val["pos_x"]
            ball_pos_y = val["pos_y"]
            ball_img_idx = val["img_idx"]
            screen.blit(game_ball_images[ball_img_idx],
                        (ball_pos_x, ball_pos_y))

        screen.blit(game_stage, (0, screen_height - stage_height))  # 스테이지
        screen.blit(game_character, (character_x_pos, character_y_pos))  # 캐릭터
        pygame.display.update()

    # 게임 오버 메시지
    msg = game_font.render(game_result, True, (255, 255, 0))  # 노란색
    msg_rect = msg.get_rect(
        center=(int(screen_width) / 2, int(screen_height / 2)))
    screen.blit(msg, msg_rect)
    pygame.display.update()

    # 2초 대기
    pygame.time.delay(2000)

    pygame.quit()


def normal():  # normal모드
    global character_x_pos, character_to_x, ball_to_remove, game_result
    running = True
    bgm1.stop()
    sfx1.set_volume(0.5)
    sfx1.play(0)
    bgm2.play()
    while running:
        pygame.init()
        clock.tick(30)

        # 이벤트 처리(키보트, 마우스 등)
        for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가?
            if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가?
                running = False  # 게임이 진행중이 아님

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                    character_to_x -= character_speed
                elif event.key == pygame.K_RIGHT:  # 캐릭터를 오른쪽으로
                    character_to_x += character_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_to_x = 0

        # 게임 캐릭터 위치 정의
        character_x_pos += character_to_x

        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        # 공 위치 정의
        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            ball_size = game_ball_images[ball_img_idx].get_rect().size
            ball_width = ball_size[0]
            ball_height = ball_size[1]

            # 가로벽에 닿았을 때 공 이동 위치 변경( 튕겨 나오는 효과)
            if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
                ball_val["to_x"] = ball_val["to_x"] * -1

            # 세로 위치
            # 스테이지에 튕겨서 올라가는 처리
            if ball_pos_y >= screen_height - stage_height - ball_height:
                ball_val["to_y"] = ball_val["init_spd_y"]
            # 천장에 튕겨서 내려가는 처리
            elif ball_pos_y <= 0:
                ball_val["to_y"] = 0.5
            else:  # 그 외의 모든 경우에는 속도를 증가
                ball_val["to_y"] += 1

            ball_val["pos_x"] += ball_val["to_x"]
            ball_val["pos_y"] += ball_val["to_y"]

        # 충돌처리

        # 캐릭터 rect 정보 업데이트
        character_rect = game_character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            # 공 rect 정보 업데이트
            ball_rect = game_ball_images[ball_img_idx].get_rect()
            ball_rect.left = ball_pos_x
            ball_rect.top = ball_pos_y

            # 공과 캐릭터 충돌처리
            if character_rect.colliderect(ball_rect):
                running = False
                bgm2.stop()
                sfx2.set_volume(0.5)
                sfx2.play()
                break

            if ball_pos_y == 0:  # 천장에 부딪혔을 때
                ball_to_remove = ball_idx
                if ball_img_idx < 4:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = game_ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        # 공의 x좌표
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        # 공의 y좌표
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": -6,  # x축 이동방향
                        "to_y": -1,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})  # y 최초 속도

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        # 공의 x좌표
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        # 공의 y좌표
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": 7,  # x축 이동방향
                        "to_y": -3,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})  # y 최초 속도
                break

        # 충돌된 공 없애기
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1

         # 모든 공을 없앤 경우 게임 종료 (성공)
        if len(balls) == 0:
            game_result = "Clear"
            bgm2.stop()
            sfx3.set_volume(0.2)
            sfx3.play()
            running = False

        # 화면에 그리기
        screen.blit(game_background, (0, 0))

        for idx, val in enumerate(balls):
            ball_pos_x = val["pos_x"]
            ball_pos_y = val["pos_y"]
            ball_img_idx = val["img_idx"]
            screen.blit(game_ball_images[ball_img_idx],
                        (ball_pos_x, ball_pos_y))

        screen.blit(game_stage, (0, screen_height - stage_height))
        screen.blit(game_character, (character_x_pos, character_y_pos))
        pygame.display.update()

    # 게임 오버 메시지
    msg = game_font.render(game_result, True, (255, 255, 0))  # 노란색
    msg_rect = msg.get_rect(
        center=(int(screen_width) / 2, int(screen_height / 2)))
    screen.blit(msg, msg_rect)
    pygame.display.update()

    # 2초 대기
    pygame.time.delay(2000)

    pygame.quit()


def hard():  # hard 모드
    global character_x_pos, character_to_x, ball_to_remove, game_result, a, b
    running = True
    bgm1.stop()
    sfx1.set_volume(0.5)
    sfx1.play(0)
    bgm2.play()
    while running:
        pygame.init()
        clock.tick(30)

        # 이벤트 처리(키보트, 마우스 등)
        for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가?
            if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가?
                running = False  # 게임이 진행중이 아님

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                    character_to_x -= character_speed
                elif event.key == pygame.K_RIGHT:  # 캐릭터를 오른쪽으로
                    character_to_x += character_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_to_x = 0

        # 게임 캐릭터 위치 정의
        character_x_pos += character_to_x

        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        # 공 위치 정의
        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            ball_size = game_ball_images[ball_img_idx].get_rect().size
            ball_width = ball_size[0]
            ball_height = ball_size[1]

            # 가로벽에 닿았을 때 공 이동 위치 변경( 튕겨 나오는 효과)
            if ball_pos_x < 0:  # 왼쪽
                ball_val["to_x"] = ball_val["to_x"] * -1 + 1

            elif ball_pos_x > screen_width - ball_width:  # 오른쪽
                ball_val["to_x"] = ball_val["to_x"] * -1 - 1
            # 세로 위치
            # 스테이지에 튕겨서 올라가는 처리
            elif ball_pos_y >= screen_height - stage_height - ball_height:
                ball_val["to_y"] = ball_val["init_spd_y"]

            # 천장에 튕겨서 내려가는 처리
            elif ball_pos_y <= 0:
                ball_val["to_y"] = 0.5
            else:  # 그 외의 모든 경우에는 속도를 증가
                ball_val["to_y"] += 1

            ball_val["pos_x"] += ball_val["to_x"]
            ball_val["pos_y"] += ball_val["to_y"]

        # 충돌처리

        # 캐릭터 rect 정보 업데이트
        character_rect = game_character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        for ball_idx, ball_val in enumerate(balls):
            ball_pos_x = ball_val["pos_x"]
            ball_pos_y = ball_val["pos_y"]
            ball_img_idx = ball_val["img_idx"]

            # 공 rect 정보 업데이트
            ball_rect = game_ball_images[ball_img_idx].get_rect()
            ball_rect.left = ball_pos_x
            ball_rect.top = ball_pos_y

            # 공과 캐릭터 충돌처리
            if character_rect.colliderect(ball_rect):
                running = False
                bgm2.stop()
                sfx2.set_volume(0.5)
                sfx2.play()
                break

            if ball_pos_x == a or ball_pos_x == b:
                if ball_img_idx < 4:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = game_ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        # 공의 x좌표
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        # 공의 y좌표
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": -7,  # x축 이동방향
                        "to_y": 0,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})  # y 최초 속도

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        # 공의 x좌표
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        # 공의 y좌표
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": 5,  # x축 이동방향
                        "to_y": -3,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})  # y 최초 속도

            elif ball_pos_y == 0:
                ball_to_remove = ball_idx
                if ball_img_idx < 4:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = game_ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        # 공의 x좌표
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        # 공의 y좌표
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": -3,  # x축 이동방향
                        "to_y": -3,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})  # y 최초 속도

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        # 공의 x좌표
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        # 공의 y좌표
                        "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": 7,  # x축 이동방향
                        "to_y": -3,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})  # y 최초 속도
                break

        # 충돌된 공
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1

        if len(balls) == 0:
            game_result = "Clear"
            bgm2.stop()
            sfx3.set_volume(0.2)
            sfx3.play()
            running = False

        # 화면에 그리기
        screen.blit(game_background, (0, 0))

        # 랜덤 벽 그리기
        screen.blit(game_wall_1, (a, 0))
        screen.blit(game_wall_2, (b, 0))

        for idx, val in enumerate(balls):
            ball_pos_x = val["pos_x"]
            ball_pos_y = val["pos_y"]
            ball_img_idx = val["img_idx"]
            screen.blit(game_ball_images[ball_img_idx],
                        (ball_pos_x, ball_pos_y))

        screen.blit(game_stage, (0, screen_height - stage_height))
        screen.blit(game_character, (character_x_pos, character_y_pos))
        pygame.display.update()

    # 게임 오버 메시지
    msg = game_font.render(game_result, True, (255, 255, 0))  # 노란색
    msg_rect = msg.get_rect(
        center=(int(screen_width) / 2, int(screen_height / 2)))
    screen.blit(msg, msg_rect)
    pygame.display.update()

    # 2초 대기
    pygame.time.delay(2000)
    pygame.quit()


mainmenu()
