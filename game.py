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

    def get_ground(self):
        return self.ground

    # 用户点开一个格子, row, column
    # 返回更新的list
    def discover(self, x, y):
        # 是雷，返回死讯
        if (x, y) in self.mines:
            return [(x, y, -1)]   # -1表示炸犊子了
        else:
            # 是1~8，直接显示，否则要递归
            if self.number[x][y] != 0:
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
                    visited.add((a, b))

                    if self.number[a][b] == 0:
                        for nei in self.__get_neighbor(a, b):
                            if nei not in visited:
                                stack.append(nei)
                                visited.add(nei)

                return res


    # 用户给一个格子标雷，这个应该是纯前端标记一下就行，哦不可能涉及游戏结束
    def flag(self, x, y):
        pass


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
