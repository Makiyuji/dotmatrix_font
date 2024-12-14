# Dotmatrix Font Designer

import os
import shutil
import pygame
import pygame.freetype

# コード範囲の定数
CODE_OFFSET = 0x00
CODE_START = 0x00
CODE_END = 0x7F
CODE_LENGTH = CODE_END - CODE_START + 1

# 表示領域の設定
DISPLAY_COLS = 16
DISPLAY_ROWS = CODE_LENGTH // DISPLAY_COLS

# 文字数がDISPLAY_COLSの倍数でない場合、文字数を増やす
if CODE_LENGTH % DISPLAY_COLS != 0:
    CODE_LENGTH = DISPLAY_COLS * (CODE_LENGTH // DISPLAY_COLS + 1)

# ドットマトリクスの設定
SMALL_DOT_SIZE = 4
LARGE_DOT_SIZE = 16
SMALL_MARGIN = 1
LARGE_MARGIN = 4
WINDOW_MARGIN = 8
DISPLAY_COL_MARGIN = 6
DISPLAY_ROW_MARGIN = 6
COLS = 5
ROWS = 7
SMALL_DOT_INTV = SMALL_DOT_SIZE + SMALL_MARGIN
LARGE_DOT_INTV = LARGE_DOT_SIZE + LARGE_MARGIN
DISPLAY_COL_INTV = COLS * SMALL_DOT_INTV + DISPLAY_COL_MARGIN
DISPLAY_ROW_INTV = ROWS * SMALL_DOT_INTV + DISPLAY_ROW_MARGIN

# 画面の設定
WINDOW_WIDTH = DISPLAY_COLS * DISPLAY_COL_INTV - DISPLAY_COL_MARGIN + WINDOW_MARGIN * 2
if WINDOW_WIDTH < 500:
    WINDOW_WIDTH = 500
WINDOW_HEIGHT = DISPLAY_ROWS * DISPLAY_ROW_INTV - DISPLAY_ROW_MARGIN + WINDOW_MARGIN * 2 + ROWS * LARGE_DOT_INTV + 80

# 初期化
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Dotmatrix Font Designer')

# フレームレートの設定
clock = pygame.time.Clock()
FPS = 20

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LAVENDER = (230, 230, 250)
DARK_RED = (139, 0, 0)
LIGHT_RED = (255, 182, 193)
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)
PURPLE = (128, 0, 128)
LIGHT_PURPLE = (216, 191, 216)

# フォントの設定
FONT_PATH = 'fonts/natumemozi.ttf'
font1 = pygame.freetype.Font(FONT_PATH, 24)
large_font = pygame.freetype.Font(FONT_PATH, 48)
SAVE_MESSAGE_STAY = 1500

# 参照用文字とデザイン用文字の表示位置
REF_CHAR_X = (WINDOW_WIDTH // 3) - (COLS * LARGE_DOT_INTV // 2)
REF_CHAR_Y = WINDOW_HEIGHT - 40 - ROWS * LARGE_DOT_INTV

# デザイン領域の設定
DESIGN_CHAR_X = (2 * WINDOW_WIDTH // 3) - (COLS * LARGE_DOT_INTV // 2) + LARGE_MARGIN
DESIGN_CHAR_Y = WINDOW_HEIGHT - 40 - ROWS * LARGE_DOT_INTV

# DESIGN_CHAR_INDEXの初期化
DESIGN_CHAR_INDEX = 0

# 初期データの読み込みまたは初期化
FONT_FILE = 'font.txt'
BACKUP_FILE = 'font.txt.bak'
if os.path.exists(FONT_FILE):
    shutil.copy(FONT_FILE, BACKUP_FILE)  # バックアップを作成
    with open(FONT_FILE, 'r', encoding='utf-8') as f:
        font_data = f.read().splitlines()
    # 空のデータを挿入
    if CODE_OFFSET > CODE_START:
        empty_data = ['0' * COLS for _ in range(ROWS * (CODE_OFFSET - CODE_START))]
        font_data = empty_data + font_data
    elif CODE_OFFSET < CODE_START:
        font_data = font_data[(CODE_START - CODE_OFFSET) * ROWS:]
else:
    font_data = ['0' * COLS for _ in range(ROWS * CODE_LENGTH)]

# データが不足している場合の初期化
if len(font_data) < ROWS * CODE_LENGTH:
    font_data.extend(['0' * COLS for _ in range(ROWS * CODE_LENGTH - len(font_data))])


# デザイン用文字のスライスを取得する関数
def get_design_char_data(index):
    return font_data[index * ROWS:(index + 1) * ROWS]


def set_design_char_data(index, data):
    font_data[index * ROWS:(index + 1) * ROWS] = data


# 矢印アイコンの読み込み
arrow_image = pygame.image.load('images/right_arrow.png')
arrow_rect = arrow_image.get_rect()
arrow_rect.center = (WINDOW_WIDTH // 2,
                     REF_CHAR_Y + (ROWS * LARGE_DOT_INTV) // 2)

# チェックマークアイコンの読み込み
check_image = pygame.image.load('images/check.png')
check_rect = check_image.get_rect()
check_rect.center = (arrow_rect.centerx, arrow_rect.centery - arrow_rect.height)

# 鉛筆アイコンの読み込み
pencil_image = pygame.image.load('images/pencil.png')
pencil_rect = pencil_image.get_rect()
pencil_rect.topleft = (DESIGN_CHAR_X + COLS * LARGE_DOT_INTV + 10,
                       DESIGN_CHAR_Y)

# 選択状態の初期化
blue_selection = [0, 0]
red_selection = [0, 0]

# デザイン用文字の一時データ
design_char_data = font_data[DESIGN_CHAR_INDEX * ROWS:(DESIGN_CHAR_INDEX + 1) * ROWS]

# クリック状態の追跡
MOUSE_DOWN = False
SHIFT_PRESSED = False

# メインループ
SAVE_MESSAGE_TIME = 0
RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                blue_selection[1] = (blue_selection[1] - 1) % DISPLAY_ROWS
            elif event.key == pygame.K_s:
                blue_selection[1] = (blue_selection[1] + 1) % DISPLAY_ROWS
            elif event.key == pygame.K_a:
                blue_selection[0] = (blue_selection[0] - 1) % DISPLAY_COLS
            elif event.key == pygame.K_d:
                blue_selection[0] = (blue_selection[0] + 1) % DISPLAY_COLS
            elif event.key == pygame.K_UP:
                red_selection[1] = (red_selection[1] - 1) % DISPLAY_ROWS
                DESIGN_CHAR_INDEX = red_selection[1] * DISPLAY_COLS + red_selection[0]
                if DESIGN_CHAR_INDEX < CODE_LENGTH:
                    design_char_data = get_design_char_data(DESIGN_CHAR_INDEX)
            elif event.key == pygame.K_DOWN:
                red_selection[1] = (red_selection[1] + 1) % DISPLAY_ROWS
                DESIGN_CHAR_INDEX = red_selection[1] * DISPLAY_COLS + red_selection[0]
                if DESIGN_CHAR_INDEX < CODE_LENGTH:
                    design_char_data = get_design_char_data(DESIGN_CHAR_INDEX)
            elif event.key == pygame.K_LEFT:
                red_selection[0] = (red_selection[0] - 1) % DISPLAY_COLS
                DESIGN_CHAR_INDEX = red_selection[1] * DISPLAY_COLS + red_selection[0]
                if DESIGN_CHAR_INDEX < CODE_LENGTH:
                    design_char_data = get_design_char_data(DESIGN_CHAR_INDEX)
            elif event.key == pygame.K_RIGHT:
                red_selection[0] = (red_selection[0] + 1) % DISPLAY_COLS
                DESIGN_CHAR_INDEX = red_selection[1] * DISPLAY_COLS + red_selection[0]
                if DESIGN_CHAR_INDEX < CODE_LENGTH:
                    design_char_data = get_design_char_data(DESIGN_CHAR_INDEX)
            elif event.key == pygame.K_RETURN:
                # エンターキーでデザイン用文字の変更を表示領域に反映
                DESIGN_CHAR_INDEX = red_selection[1] * DISPLAY_COLS + red_selection[0]
                if DESIGN_CHAR_INDEX < CODE_LENGTH:
                    set_design_char_data(DESIGN_CHAR_INDEX, design_char_data)
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                SHIFT_PRESSED = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                SHIFT_PRESSED = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MOUSE_DOWN = True
            mouse_x, mouse_y = event.pos
            cond1 = 0 <= mouse_x < DISPLAY_COLS * DISPLAY_COL_INTV
            cond2 = 0 <= mouse_y < DISPLAY_ROWS * DISPLAY_ROW_INTV
            if event.button == 1:  # 左クリック
                if SHIFT_PRESSED:
                    # 参照用文字の指定
                    if cond1 and cond2:
                        blue_selection[0] = mouse_x // DISPLAY_COL_INTV
                        blue_selection[1] = mouse_y // DISPLAY_ROW_INTV
                else:
                    # デザイン用文字の指定
                    if cond1 and cond2:
                        red_selection[0] = mouse_x // DISPLAY_COL_INTV
                        red_selection[1] = mouse_y // DISPLAY_ROW_INTV
                        DESIGN_CHAR_INDEX = red_selection[1] * DISPLAY_COLS + red_selection[0]
                        if DESIGN_CHAR_INDEX < CODE_LENGTH:
                            design_char_data = get_design_char_data(DESIGN_CHAR_INDEX)
            # デザイン領域のクリック処理
            cond1 = DESIGN_CHAR_X <= mouse_x < DESIGN_CHAR_X + COLS * LARGE_DOT_INTV
            cond2 = DESIGN_CHAR_Y <= mouse_y < DESIGN_CHAR_Y + ROWS * LARGE_DOT_INTV
            if cond1 and cond2:
                c = (mouse_x - DESIGN_CHAR_X) // LARGE_DOT_INTV
                r = (mouse_y - DESIGN_CHAR_Y) // LARGE_DOT_INTV
                new_row = list(design_char_data[r])
                if SHIFT_PRESSED:
                    new_row[c] = '0'
                else:
                    new_row[c] = '1'
                design_char_data[r] = ''.join(new_row)
            # アイコンのクリック処理
            if arrow_rect.collidepoint(mouse_x, mouse_y):
                # 矢印アイコンがクリックされた場合、参照用文字をデザイン用文字にコピー
                REF_CHAR_INDEX = blue_selection[1] * DISPLAY_COLS + blue_selection[0]
                if REF_CHAR_INDEX < CODE_LENGTH:
                    design_char_data = get_design_char_data(REF_CHAR_INDEX)
            elif pencil_rect.collidepoint(mouse_x, mouse_y):
                # 鉛筆アイコンがクリックされた場合、デザイン用文字の変更を表示領域に反映
                DESIGN_CHAR_INDEX = red_selection[1] * DISPLAY_COLS + red_selection[0]
                if DESIGN_CHAR_INDEX < CODE_LENGTH:
                    set_design_char_data(DESIGN_CHAR_INDEX, design_char_data)
            elif check_rect.collidepoint(mouse_x, mouse_y):
                # チェックマークアイコンがクリックされた場合、表示領域の全てのデータをfont.txtに書き出し
                with open(FONT_FILE, 'w', encoding='utf-8') as f:
                    for i in range(CODE_LENGTH):
                        char_data = get_design_char_data(i)
                        for line in char_data:
                            f.write(line + '\n')
                SAVE_MESSAGE_TIME = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONUP:
            MOUSE_DOWN = False
        elif event.type == pygame.MOUSEMOTION and MOUSE_DOWN:
            mouse_x, mouse_y = event.pos
            cond1 = DESIGN_CHAR_X <= mouse_x < DESIGN_CHAR_X + COLS * LARGE_DOT_INTV
            cond2 = DESIGN_CHAR_Y <= mouse_y < DESIGN_CHAR_Y + ROWS * LARGE_DOT_INTV
            if cond1 and cond2:
                c = (mouse_x - DESIGN_CHAR_X) // LARGE_DOT_INTV
                r = (mouse_y - DESIGN_CHAR_Y) // LARGE_DOT_INTV
                new_row = list(design_char_data[r])
                if SHIFT_PRESSED:
                    new_row[c] = '0'
                else:
                    new_row[c] = '1'
                design_char_data[r] = ''.join(new_row)

    # 画面のクリア
    screen.fill(LAVENDER)

    # 表示領域の描画（上部）
    for row in range(DISPLAY_ROWS):
        for col in range(DISPLAY_COLS):
            char_index = row * DISPLAY_COLS + col
            if char_index < CODE_LENGTH:
                char_data = font_data[char_index * ROWS:(char_index + 1) * ROWS]
                for r in range(ROWS):
                    for c in range(COLS):
                        x = col * DISPLAY_COL_INTV + c * SMALL_DOT_INTV + WINDOW_MARGIN
                        y = row * DISPLAY_ROW_INTV + r * SMALL_DOT_INTV + WINDOW_MARGIN
                        if char_data[r][c] == '1':
                            if [col, row] == blue_selection and [col, row] == red_selection:
                                color = PURPLE
                            elif [col, row] == blue_selection:
                                color = DARK_BLUE
                            elif [col, row] == red_selection:
                                color = DARK_RED
                            else:
                                color = BLACK
                        else:
                            if [col, row] == blue_selection and [col, row] == red_selection:
                                color = LIGHT_PURPLE
                            elif [col, row] == blue_selection:
                                color = LIGHT_BLUE
                            elif [col, row] == red_selection:
                                color = LIGHT_RED
                            else:
                                color = WHITE
                        pygame.draw.rect(screen, color, (x, y, SMALL_DOT_SIZE, SMALL_DOT_SIZE))

    # 参照用文字の描画（左下）
    REF_CHAR_INDEX = blue_selection[1] * DISPLAY_COLS + blue_selection[0]
    if REF_CHAR_INDEX < CODE_LENGTH:
        ref_char_data = font_data[REF_CHAR_INDEX * ROWS:(REF_CHAR_INDEX + 1) * ROWS]
        for r in range(ROWS):
            for c in range(COLS):
                color = DARK_BLUE if ref_char_data[r][c] == '1' else LIGHT_BLUE
                pygame.draw.rect(screen, color,
                                 (REF_CHAR_X + c * LARGE_DOT_INTV,
                                  REF_CHAR_Y + r * LARGE_DOT_INTV,
                                  LARGE_DOT_SIZE, LARGE_DOT_SIZE))

    # デザイン用文字の描画（右下）
    for r in range(ROWS):
        for c in range(COLS):
            color = DARK_RED if design_char_data[r][c] == '1' else LIGHT_RED
            pygame.draw.rect(screen, color, (DESIGN_CHAR_X + c * LARGE_DOT_INTV,
                                             DESIGN_CHAR_Y + r * LARGE_DOT_INTV,
                                             LARGE_DOT_SIZE, LARGE_DOT_SIZE))

    # 矢印アイコンの描画
    screen.blit(arrow_image, arrow_rect)

    # 鉛筆アイコンの描画
    screen.blit(pencil_image, pencil_rect)

    # チェックマークアイコンの描画
    screen.blit(check_image, check_rect)

    # 現在選択されているコードの表示
    ref_code = f"0x{CODE_START + blue_selection[1] * DISPLAY_COLS + blue_selection[0]:02X}"
    design_code = f"0x{CODE_START + red_selection[1] * DISPLAY_COLS + red_selection[0]:02X}"
    ref_code_surface, _ = font1.render(ref_code, BLACK, None)
    design_code_surface, _ = font1.render(design_code, BLACK, None)
    screen.blit(ref_code_surface, (REF_CHAR_X + 24, REF_CHAR_Y + ROWS * LARGE_DOT_INTV + 10))
    screen.blit(design_code_surface, (DESIGN_CHAR_X + 24, DESIGN_CHAR_Y + ROWS * LARGE_DOT_INTV + 10))

    # キーガイドの表示
    w_surface, _ = font1.render("W", BLACK, None)
    a_surface, _ = font1.render("A", BLACK, None)
    s_surface, _ = font1.render("S", BLACK, None)
    d_surface, _ = font1.render("D", BLACK, None)
    up_surface, _ = font1.render("↑", BLACK, None)
    left_surface, _ = font1.render("←", BLACK, None)
    down_surface, _ = font1.render("↓", BLACK, None)
    right_surface, _ = font1.render("→", BLACK, None)

    screen.blit(w_surface, (REF_CHAR_X - 40, REF_CHAR_Y + 70))
    screen.blit(a_surface, (REF_CHAR_X - 60, REF_CHAR_Y + 100))
    screen.blit(s_surface, (REF_CHAR_X - 40, REF_CHAR_Y + 100))
    screen.blit(d_surface, (REF_CHAR_X - 20, REF_CHAR_Y + 100))

    screen.blit(up_surface, (DESIGN_CHAR_X + COLS * LARGE_DOT_INTV + 34, DESIGN_CHAR_Y + 70))
    screen.blit(left_surface, (DESIGN_CHAR_X + COLS * LARGE_DOT_INTV, DESIGN_CHAR_Y + 100))
    screen.blit(down_surface, (DESIGN_CHAR_X + COLS * LARGE_DOT_INTV + 34, DESIGN_CHAR_Y + 100))
    screen.blit(right_surface, (DESIGN_CHAR_X + COLS * LARGE_DOT_INTV + 54, DESIGN_CHAR_Y + 100))

    # 保存メッセージの表示
    if SAVE_MESSAGE_TIME and pygame.time.get_ticks() - SAVE_MESSAGE_TIME < SAVE_MESSAGE_STAY:
        save_message_surface, _ = font1.render("デザインをfont.txtに保存しました。",
                                               BLACK, None)
        screen.blit(save_message_surface,
                    (WINDOW_WIDTH // 2 - save_message_surface.get_width() // 2, DESIGN_CHAR_Y - 40))
    else:
        SAVE_MESSAGE_TIME = 0

    # 画面の更新
    pygame.display.flip()
    # フレームレートの制御
    clock.tick(FPS)

pygame.quit()
