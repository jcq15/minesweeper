import random

class MineCore:
    def __init__(self, row=10, col=10, mine_num=None):
        self.row = row
        self.col = col
        if not mine_num:
            # default: 10%
            self.mine_num = row * col // 10
        else:
            self.mine_num = mine_num

        # status code
        # 0~8表示翻开了，是数字
        self.COVERED = 100  # 没翻开
        self.FLAG = 101     # 用户插旗

        self.WAIT = 200     # 等待开局
        self.PLAYING = 201  # 进行中
        self.WIN = 202      # 赢麻了
        self.LOSE = 203     # 炸了

        self.status = self.WAIT

        # generate game
        # 雷
        mines = random.sample(range(row*col), mine_num)
        self.mines = set([(mine // col, mine % col) for mine in mines]) # (a, b) 是雷

        self.ground = [[self.COVERED for _ in range(col)] for _ in range(row)]

        # 每个格子周围有几个雷
        self.number = [[0 for _ in range(col)] for _ in range(row)]
        for mine in self.mines:
            neighbors = self.__get_neighbor(*mine)
            for nei in neighbors:
                self.number[nei[0]][nei[1]] += 1
            

    ### 交互接口 ###

    def start(self):
        self.status = self.PLAYING

    def get_ground(self):
        return self.ground


    # 输了调用这个
    def __lose(self):
        self.status = self.LOSE


    # 挖开一个格子：row, column
    def __discover(self, x, y):
        # 是雷，返回死讯
        if (x, y) in self.mines:
            self.__lose()
            return [(x, y, -1)]   # -1表示炸犊子了

        else:
            # 是1~8，直接显示，否则要递归
            if self.number[x][y] != 0:
                self.ground[x][y] = self.number[x][y]
                return [(x, y, self.number[x][y])]
            else:
                # 是0，递归
                res = []
                visited = set()

                # 深度优先搜素，懒得写递归，直接用stack干
                stack = [(x, y)]
                while stack:
                    a, b = stack.pop()

                    res.append((a, b, self.number[a][b]))
                    self.ground[a][b] = self.number[a][b]
                    visited.add((a, b))

                    if self.number[a][b] == 0:
                        for nei in self.__get_neighbor(a, b):
                            if self.ground[nei[0]][nei[1]] == self.COVERED and (nei not in visited):
                                stack.append(nei)
                                visited.add(nei)
                return res


    # 用户左键单击, row, column
    # 返回更新的list
    def left_click(self, x, y):
        if self.status != self.PLAYING:
            return []

        if self.ground[x][y] == self.COVERED:
            # 开盒
            return self.__discover(x, y)
        elif self.ground[x][y] == self.FLAG:
            return []  # 点flag上了
        else:
            # 是已经挖开的格子，转到双击开盒
            return self.__open(x, y)


    # 如果周围flag数量正好对，挖开所有没挖开的并看结果
    def __open(self, x, y):
        if self.status != self.PLAYING:
            return []
        
        neighbors = self.__get_neighbor(x, y)
        flag_count = 0
        for nei in neighbors:
            if self.ground[nei[0]][nei[1]] == self.FLAG:
                flag_count += 1

        if flag_count == self.number[x][y]:
            # 对了，自动挖开
            changes = []
            for nei in neighbors:
                if self.ground[nei[0]][nei[1]] == self.COVERED:
                    changes.extend(self.__discover(*nei))
            return changes
        else:
            # 不对，啥也不干
            return []


    # 用户给一个格子标雷，返回1表示原来不是flag，现在是了；返回0则原来是flag，现在清除
    # 返回-1表示这是个已经挖开的格子，无变化
    def right_click(self, x, y):
        if self.status != self.PLAYING:
            return []

        if self.ground[x][y] == self.COVERED:
            self.ground[x][y] = self.FLAG
            return 1
        elif self.ground[x][y] == self.FLAG:
            self.ground[x][y] = self.COVERED
            return 0
        else:
            return -1


    def __get_neighbor(self, x, y):
        neighbors = []
        if x > 0:
            neighbors.append((x-1, y))
            if y > 0:
                neighbors.append((x-1, y-1))
            if y < self.col - 1:
                neighbors.append((x-1, y+1))
        if x < self.row - 1:
            neighbors.append((x+1, y))
            if y > 0:
                neighbors.append((x+1, y-1))
            if y < self.col - 1:
                neighbors.append((x+1, y+1))
        if y > 0:
            neighbors.append((x, y-1))
        if y < self.col - 1:
            neighbors.append((x, y+1))
        return neighbors
