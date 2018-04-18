# Python Code .. Have Fun ^_^
# note that code read your initial state puzzle from file 


from copy import deepcopy


starting_Puzzle = []
puzzle_of_strings = []
with open('puzzle.txt','r') as f:
    for line in f:
        puzzle_of_strings.append(line.strip().split(' '))

for row in range(3):
    starting_Puzzle.append(map(int, puzzle_of_strings[row]))

def print_puzzle(p):
    res = ''
    for row in range(3):
        res += ' '.join(map(str, p[row]))
        res += '\r\n'
    return res

goal_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

class puzzle:
    def __init__ (self, _goal_puzzle, parent):
        self.board = _goal_puzzle
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

    def manhattan(self):
        h = 0
        for i in range(3):
            for j in range(3):
                if starting_Puzzle[i][j] != 0:
                    pos_a = self.find(starting_Puzzle[i][j])
                    h += abs(pos_a[0] - i) + abs(pos_a[1] - j)

        return h

    def goal(self):
        inc = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != starting_Puzzle[i][j]:#inc:
                    return False

                inc += 1
        return True

    def __eq__(self, other):
        return self.board == other.board

    def find(self, value):
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == value:
                    return row, col

def move_function(curr):
    curr = curr.board
    for i in range(3):
        for j in range(3):
            if curr[i][j] == 0:
                x, y = i, j
                break
    q = []
    if x-1 >= 0:
        b = deepcopy(curr)
        b[x][y] = b[x-1][y]
        b[x-1][y] = 0
        succ = puzzle(b, curr)
        q.append(succ)
    if x+1 < 3:
        b = deepcopy(curr)
        b[x][y] = b[x+1][y]
        b[x+1][y] = 0
        succ = puzzle(b, curr)
        q.append(succ)
    if y-1 >= 0:
        b = deepcopy(curr)
        b[x][y] = b[x][y-1]
        b[x][y-1] = 0
        succ = puzzle(b, curr)
        q.append(succ)
    if y+1 < 3:
        b = deepcopy(curr)
        b[x][y] = b[x][y+1]
        b[x][y+1] = 0
        succ = puzzle(b, curr)
        q.append(succ)

    return q

def best_fvalue(openList):
    f = openList[0].f
    index = 0
    for i, item in enumerate(openList):
        if i == 0:
            continue
        if(item.f < f):
            f = item.f
            index  = i

    return openList[index], index

def AStar(start):
    openList = []
    closedList = []
    openList.append(start)

    while openList:
        current, index = best_fvalue(openList)
        if current.goal():
            return current
        openList.pop(index)
        closedList.append(current)

        X = move_function(current)
        for move in X:
            ok = False   #checking in closedList
            for i, item in enumerate(closedList):
                if item == move:
                    ok = True
                    break
            if not ok:              #not in closed list
                newG = current.g + 1
                present = False

                #openList includes move
                for j, item in enumerate(openList):
                    if item == move:
                        present = True
                        if newG < openList[j].g:
                            openList[j].g = newG
                            openList[j].f = openList[j].g + openList[j].h
                            openList[j].parent = current
                if not present:
                    move.g = newG
                    move.h = move.manhattan()
                    move.f = move.g + move.h
                    move.parent = current
                    openList.append(move)

    return None


start = puzzle(goal_puzzle, None)

result = AStar(start)
no_of_Moves = 0

if(not result):
    print ("No solution")
else:
    print print_puzzle(result.board)
    print '------------------------------------------'
    t = result.parent
    while t:
        no_of_Moves += 1
        print print_puzzle(t.board)
        t = t.parent
print ("Length: " + str(no_of_Moves))
print ("Manhattan Distance: " + str(start.manhattan()))
