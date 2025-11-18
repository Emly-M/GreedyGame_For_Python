import random
import pygame
import sys
from pygame.locals import *

# 贪吃蛇速度
sanke_speed=6
window_width=800
window_height=600
#方块大小
cell_size=20

# 贪吃蛇有尺寸， 地图尺寸相对于贪吃蛇大小尺寸而言的
map_width=(int)(window_width/cell_size)
map_height=(int)(window_height/cell_size)

# 颜色定义
white=(255,255,255)
black=(0,0,0)
gray=(230,230,230)
dark_gray=(40,40,40)
DARKGreen=(0,150,0)
Green=(0,250,0)
Red=(255,0,0)
blue=(0,0,255)
dark_blue=(0,0,139)
BGColor=black

# 定义方向
UP=1
DOWN=2
LEFT=3
RIGHT=4
HEAD =0

def main():
  #模块初始化
  pygame.init()
  #创建时钟对象
  sanke_speed_clock = pygame.time.Clock()
  # 屏幕宽度与高度
  screen = pygame.display.set_mode((window_width,window_height))
  screen.fill(white)

  #设置标题
  pygame.display.set_caption("Python 贪吃蛇小游戏")
  show_start_info(screen)
  while True:
     running_game(screen,sanke_speed_clock)
     show_gameover_info(screen)

# 游戏主体
# 游戏主体
def running_game(screen, sanke_speed_clock):
    # --- BUG 修复 2： 初始坐标应基于 map_width 和 map_height ---
    # startx = random.randint(3,window_width-8)  # 错误，坐标太大
    # starty = random.randint(3,window_height-8) # 错误
    startx = random.randint(3, map_width - 8)
    starty = random.randint(3, map_height - 8)

    # 贪吃蛇初始位置
    # --- 优化：让蛇的初始身体是直的 ---
    snake_coords = [{'x': startx, 'y': starty},
                    {'x': startx - 1, 'y': starty},  # 原来是 starty-1 (对角线)
                    {'x': startx - 2, 'y': starty}  # 原来是 starty-2 (对角线)
                    ]
    # 开始向右走
    direction = RIGHT
    food = get_random_location()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminateGame()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_SPACE:
                    terminateGame()

        move_snake(direction, snake_coords)
        ret = snake_is_alive(snake_coords)
        if not ret:
            break  # 蛇死了，跳出循环

        # ------------------- BUG 修复 1：缩进 -------------------
        # 以下所有代码都需要在 while True 循环内部
        # 这样才能保证游戏“每一帧”都执行

        # 蛇是否迟到食物
        snake_is_eat_food(snake_coords, food)
        # 背景色填充
        screen.fill(BGColor)
        # (可选) 定义了画网格的函数，可以在这里调用它
        # draw_grid(screen)
        draw_snake(screen, snake_coords)
        draw_food(screen, food)
        draw_score(screen, len(snake_coords) - 3)
        # 刷新屏幕
        pygame.display.update()
        # 控制游戏速度
        sanke_speed_clock.tick(sanke_speed)

# 循环结束 (蛇死了)，函数自动返回到 main，
# main 会接着调用 show_gameover_info

# 开机信息
def show_start_info(screen):
    font = pygame.font.Font("myfont.ttf", 40)
    tip = font.render('按任意键开始游戏...', True, (65, 105, 225))
    gamestart = pygame.image.load('gamestart.jpg')
    screen.blit(gamestart, (140, 30))
    screen.blit(tip, (240, 550))
    pygame.display.update()
    # 键盘监听
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminateGame()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: #终止程序
                    terminateGame()
                else:
                    return

def show_gameover_info(screen):
    font = pygame.font.Font("myfont.ttf",40)
    tip = font.render('按Q或者ESE退出游戏，任意键开始游戏...',True,(65,105,225))
    gameover =pygame.image.load('gameover.png')
    screen.blit(gameover,(140,30))
    screen.blit(tip,(80,300))
    pygame.display.update()

    # 键盘监听
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminateGame()
            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE or event.key == K_q):
                    terminateGame()
                else:
                    return




# 画贪吃蛇
def draw_snake(screen,snake_coords):
 for coord in snake_coords:
      x = coord['x'] * cell_size
      y = coord['y'] * cell_size
      greedySnakeRect = pygame.Rect(x,y,cell_size,cell_size)
      pygame.draw.rect(screen,dark_blue,greedySnakeRect)

      greedySnakeInnnerRect= pygame.Rect(x+4,y+4,cell_size-8,cell_size-8)
      # 蛇身子内部颜色蓝色
      pygame.draw.rect(screen,blue,greedySnakeInnnerRect)

# 画网格
def draw_grid(screen):
    # 画水平的
    for x in range(0,window_width,cell_size):
        pygame.draw.line(screen,dark_gray,(x,0),(x,window_height))

    # 垂直画线
    for y in range(0,window_height,cell_size):
        pygame.draw.line(screen,dark_gray,(0,y),(window_width,y))
# 画食物
def draw_food(screen,food):
    x = food['x'] * cell_size
    y = food['y'] * cell_size
    appleRect = pygame.Rect(x,y,cell_size,cell_size)
    pygame.draw.rect(screen,Red,appleRect)

# 移动贪吃蛇
def move_snake(direction,snake_coords):
    if direction == UP:
        newHead = {'x':snake_coords[HEAD]['x'],'y': snake_coords[HEAD]['y']-1}
    elif direction == DOWN:
        newHead = {'x':snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y']+1}
    elif direction == LEFT:
        newHead = {'x':snake_coords[HEAD]['x']-1, 'y': snake_coords[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': snake_coords[HEAD]['x'] + 1, 'y': snake_coords[HEAD]['y']}
    snake_coords.insert(0,newHead)

def snake_is_alive(snake_coords):
    HEAD = 0
    tag = True
    # 撞墙了 (增加了 y == -1 的判断)
    if snake_coords[HEAD]['x'] == -1 or snake_coords[HEAD]['x'] == map_width or snake_coords[HEAD]['y'] == -1 or snake_coords[HEAD]['y'] == map_height:
       tag = False
    # 撞到自己的身体
    for snake_body in snake_coords[1:]:
      if snake_body['x'] == snake_coords[HEAD]['x'] and snake_body['y'] == snake_coords[HEAD]['y']:
         tag = False
    return tag

# 判断蛇是否吃到食物
def snake_is_eat_food(snake_coords,food):
    if snake_coords[HEAD]['x'] == food['x'] and snake_coords[HEAD]['y'] == food['y']:
        food['x'] = random.randint(0,map_width-1)
        food['y'] = random.randint(0,map_height-1)
    else:
        # 没有吃到食物，删除尾部一格
        del snake_coords[-1]

# 食物随机生成
def get_random_location():
    return {'x':random.randint(0,map_width-1),'y':random.randint(0,map_height-1)}



# 画分数
def draw_score(screen,score):
    font = pygame.font.Font("myfont.ttf",30)
    scoreSurf = font.render('得分:%s'%score,True,Green)
    scoreReact= scoreSurf.get_rect()
    scoreReact.topleft=(window_width-120,10)
    screen.blit(scoreSurf,scoreReact)


def terminateGame():
    pygame.quit()
    sys.exit()

main()


