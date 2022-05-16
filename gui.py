import sys
import pygame
from game import MineCore


class Gui:
    # adjust: 界面缩放; fps: 帧率
    def __init__(self, rows=9, columns=12, mines=10, adjust=1, fps=30):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.fps = fps
        self.adjust = 1

        self.caption = '傻雷游戏'

        self.game = MineCore(rows, columns, mines)


    # 加载图儿们, size=(50, 50)
    def __load_img(self, path, size=None):
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img


    # 初始化gui
    def __run(self):
        pygame.init()

        # 设定窗口大小
        grid = 24 * self.adjust
        rim = 18 * self.adjust
        bar_height = 48 * self.adjust

        board_size = (self.columns * grid, self.rows * grid)  # 棋盘大小，无边框
        board_bord_size = (board_size[0] + rim * 2, board_size[1] + rim * 2)  # 带边框的棋盘大小
        screen_size = (board_bord_size[0], board_bord_size[1] + rim + bar_height) # 整个屏幕大小，多个bar

        # 窗口有了
        screen = pygame.display.set_mode(screen_size)
        game_board_bord = screen.subsurface((0, rim + bar_height, *board_bord_size))  # 带边框的主区域
        game_board = game_board_bord.subsurface((rim, rim, *board_size))              # 格子们

        # 载入素材
        img_closed = self.__load_img('image/closed.jpg', (grid, grid))
        img_corner_up_left = self.__load_img('image/corner_up_left_2x.png', (rim, rim))
        img_corner_up_right = self.__load_img('image/corner_up_right_2x.png', (rim, rim))
        img_corner_bottom_left = self.__load_img('image/corner_bottom_left_2x.png', (rim, rim))
        img_corner_bottom_right = self.__load_img('image/corner_bottom_right_2x.png', (rim, rim))
        img_border_vert = self.__load_img('image/border_vert_2x.png', (rim, board_size[1]))
        img_border_hor = self.__load_img('image/border_hor_2x.png', (board_size[0], rim))
        img_t_left = self.__load_img('image/t_left_2x.png', (rim, rim))
        img_t_right = self.__load_img('image/t_right_2x.png', (rim, rim))

        img_numbers = [
            self.__load_img(f'image/type{i}.jpg', (grid, grid))
            for i in range(9)
        ]

        # 标题
        pygame.display.set_caption(self.caption)

        # 放closed格子们
        for i in range(self.rows):
            for j in range(self.columns):
                game_board.blit(img_closed, (j * grid, i * grid))

        # 角
        game_board_bord.blit(img_t_left, (0, 0))
        game_board_bord.blit(img_t_right, (rim + board_size[0], 0))
        game_board_bord.blit(img_corner_bottom_left, (0, rim + board_size[1]))
        game_board_bord.blit(img_corner_bottom_right, (rim + board_size[0], rim + board_size[1]))

        # 边
        game_board_bord.blit(img_border_vert, (0, rim))
        game_board_bord.blit(img_border_vert, (rim + board_size[0], rim))
        game_board_bord.blit(img_border_hor, (rim, 0))
        game_board_bord.blit(img_border_hor, (rim, rim + board_size[1]))

        #game_board_bord.blit(game_board, (rim, rim))
        #screen.blit(game_board_bord, (0, rim + bar_height))

        # bar的边框
        screen.blit(img_corner_up_left, (0, 0))
        screen.blit(img_corner_up_right, (board_size[0] + rim, 0))
        screen.blit(img_border_hor, (rim, 0))
        screen.blit(img_border_vert, (0, rim), area=(0, 0, rim, bar_height))
        screen.blit(img_border_vert, (board_size[0] + rim, rim), area=(0, 0, rim, bar_height))

        # 上面的bar
        bar = pygame.Surface((board_size[0], bar_height))
        bar.fill((192, 192, 192))

        screen.blit(bar, (rim, rim))

        pygame.display.flip()

        # main loop
        clock = pygame.time.Clock()  # 计时器，可以设置fps
        while True:
            # 循环获取事件，监听事件状态
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    b1, b2, b3 = pygame.mouse.get_pressed()  # 左中右
                    mouse_click_type = ''
                    if b1 and not b3:
                        mouse_click_type = 'left'
                    elif not b1 and b3:
                        mouse_click_type = 'right'
                    elif b1 and b3:
                        mouse_click_type = 'left_right'    # 左右双击
                    mouse_x, mouse_y = event.pos

                    board_rect = game_board.get_rect(topleft=game_board.get_abs_offset())
                    if board_rect.collidepoint(event.pos):
                        # 点了格子！算算是哪个
                        row = (mouse_y - board_rect.top) // grid
                        col = (mouse_x - board_rect.left) // grid
                        if mouse_click_type == 'left':
                            update = self.game.discover(row, col)
                            for u in update:
                                x, y, num = u
                                if num != -1:
                                    game_board.blit(img_numbers[num], (y * grid, x * grid))
                                else:
                                    print('你输了')

                # 判断用户是否点了"X"关闭按钮,并执行if代码段
                elif event.type == pygame.QUIT:
                    #卸载所有模块
                    pygame.quit()
                    #终止程序，确保退出程序
                    sys.exit()

            # pygame.display.update() # 更新屏幕内容 #可用update部分更新
            pygame.display.update(game_board.get_rect(topleft=game_board.get_abs_offset()))  # 省资源
            clock.tick(self.fps)    # 设置fps

            
    def run(self):
        self.__run()


if __name__ == '__main__':
    app = Gui()
    app.run()