
import imp
import math
import time
#======================================================================
def BoardPrint(board,move=[],num =0):

    print("====== The current board(",num,")is (after move): ======")
    if move:
        print("move = ",move)
    for i in [7,6,5,4,3,2,1,0]:
        print(i,":", end=" ")
        for j in range(8):
            print(board[i][j], end=" ")
        print()
    print("   ",0,1,2,3,4,5,6,7)
    print("")

def BoardCopy(board):
    new_board = [[]]*8
    for i in range(8):
        new_board[i] = [] + board[i]
    return new_board

#======================================================================

def doit(move,state):
    new_state = BoardCopy(state)
    #Move one step
    #example: [(2,2),(3,3)] or [(2,2),(3,1)]
    if len(move) == 2 and abs(move[1][0] - move[0][0]) == 1:
        new_state[move[0][0]][move[0][1]] = '.'
        if state[move[0][0]][move[0][1]] == 'b' and move[1][0] == 7:
            new_state[move[1][0]][move[1][1]] = 'B'
        elif state[move[0][0]][move[0][1]] == 'r' and move[1][0] == 0:
            new_state[move[1][0]][move[1][1]] = 'R'
        else:
            new_state[move[1][0]][move[1][1]] = state[move[0][0]][move[0][1]]
    #elif abs(move[1][0] - move[0][0]) == 1 and (state[move[0][0]][move[0][1]] == 'B'
    #                                            or state[move[0][0]][move[0][1]] == 'R'):
    #    for i in range(len(move)-1):
    #        new_state[move[i][0]][move[i][1]]='.'
    #    new_state[move[len(move)-1][0]][move[len(move)-1][1]] = state[move[0][0]][move[0][1]]
    elif state[move[0][0]][move[0][1]] == 'B' or state[move[0][0]][move[0][1]] == 'R':
        temp=BoardCopy(state)
        for l in range(len(move)-1):
            step=0
            if move[l+1][1]>move[l][1]:
                j=range(move[l][1],move[l+1][1])
            else:
                j=range(move[l][1],move[l+1][1],-1)
            if move[l+1][0]>move[l][0]:
                cells=range(move[l][0],move[l+1][0])
            else:
                cells=range(move[l][0],move[l+1][0],-1)
            for i in cells:
                new_state[i][j[step]]='.'
                step+=1
            new_state[move[l+1][0]][move[l+1][1]] = temp[move[l][0]][move[l][1]]
            temp=BoardCopy(new_state)
    #Jump
    #example: [(1,1),(3,3),(5,5)] or [(1,1),(3,3),(5,1)]
    else:
        step = 0
        new_state[move[0][0]][move[0][1]] = '.'
        while step < len(move)-1:
            new_state[int(math.floor((move[step][0]+ move[step+1][0])/2))][int(math.floor((move[step][1]+ move[step+1][1])/2))] = '.'
            step = step+1
        if state[move[0][0]][move[0][1]] == 'b' and move[step][0] == 7:
            new_state[move[step][0]][move[step][1]] = 'B'
        elif state[move[0][0]][move[0][1]] == 'r' and move[step][0] == 0:
            new_state[move[step][0]][move[step][1]] = 'R'
        else:
            new_state[move[step][0]][move[step][1]] = state[move[0][0]][move[0][1]]
    return new_state

#======================================================================
# Initial_Board = [ ['b','.','b','.','b','.','b','.'],\
#                   ['.','b','.','b','.','b','.','b'],\
#                   ['b','.','b','.','b','.','b','.'],\
#                   ['.','.','.','.','.','.','.','.'],\
#                   ['.','.','.','.','.','.','.','.'],\
#                   ['.','r','.','r','.','r','.','r'],\
#                   ['r','.','r','.','r','.','r','.'],\
#                   ['.','r','.','r','.','r','.','r'] \
#                 ]
Initial_Board = [ ['.','.','b','.','B','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','b','.','.','.','.','.'],\
                  ['.','r','.','.','.','.','.','.'] \
                ]
 # 7 : . r . r . r . r
 # 6 : r . r . r . r .
 # 5 : . r . r . r . r
 # 4 : . . . . . . . .
 # 3 : . . . . . . . .
 # 2 : b . b . b . b .
 # 1 : . b . b . b . b
 # 0 : b . b . b . b .
 #     0 1 2 3 4 5 6 7
#======================================================================
def play(student_A, student_B,start_state = Initial_Board):
    Aplayer = imp.load_source(student_A, student_A + ".py")
    Bplayer = imp.load_source(student_B, student_B + ".py")

    A = Aplayer.Player('r')
    B = Bplayer.Player('b')

    currPlayer = A
    state = start_state

    board_num = 0

    BoardPrint(state)

    for x in range(0,1):
        print("It is ", currPlayer ,"'s turn")

        start = time.time()
        move = currPlayer.nextMove(state)
        elapse = time.time() - start

        #print(move)

        if not move:
            break

        print("The move is : ",move, end=" ")
        print(" (in %.2f ms)" % (elapse*1000), end=" ")
        if elapse > 3.0:
            print(" ** took more than three second!!", end=" ")
            break
        if board_num > 200:
            print("Game Over")
            break
        print()
        #check_move
        state = doit(move,state)

        board_num = board_num + 1
        BoardPrint(state,num = board_num)

        if currPlayer == A:
            currPlayer = B
        else:
            currPlayer = A

    print("Game Over")
    if currPlayer == A:
        print("The Winner is:",student_B, 'b')
    else:
        print("The Winner is:",student_A, 'r')

play("checkers_2017","checkers_2017")
#play(sys.argv[1],sys.argv[2])
