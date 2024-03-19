from copy import deepcopy
import random
from math import ceil
import pickle
import pygame

board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

board_copy=deepcopy(board)

da_ting1 = {}
da_ting2 = {}

result1 = {'win': 0, 'lose': 0, 'draw': 0}
result2 = {'win': 0, 'lose': 0, 'draw': 0}

da_ting_hist1 = []
da_ting_hist2 = []

player_turn = 1

learning_rate = 0.1
decay = 0.8

exploration_rate = 0.3

available = []

def result():
    global available
    # column
    for i in board:
        if len(set(i)) == 1 and i[0] != 0:
            available = []
            return i[0]

    # row
    for i in range(3):
        row = []
        for j in range(3):
            row.append(board[j][i])
        if len(set(row)) == 1 and row[0] != 0:
            available = []
            return row[0]

    # diagonal
    diag = []
    for i in range(3):
        diag.append(board[i][i])
    if len(set(diag)) == 1 and diag[0] != 0:
        available = []
        return diag[0]

    # other diagonal
    diag = []
    for i in range(3):
        diag.append(board[i][3 - i - 1])
    if len(set(diag)) == 1 and diag[0] != 0:
        available = []
        return diag[0]

    return 0


def possible_moves():
    global available
    available = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                fake_board = deepcopy(board)
                fake_board[i][j] = player_turn
                available.append(str(fake_board))
    if result() != 0:
        available = []


def move():
    global available, board
    if random.uniform(0, 1) <= exploration_rate:
        best_move = random.choice(available) if len(available) != 0 else 0
    else:
        max_val = float("-inf")
        best_move = available[0] if len(available) != 0 else 0
        if available != 0:
            if player_turn==1:
                for i in available:
                    if not da_ting1.get(i, False):
                        da_ting1[i] = 0
                    if da_ting1.get(i) > max_val:
                        max_val = da_ting1.get(i)
                        best_move = i
            else:
                for i in available:
                    if not da_ting2.get(i, False):
                        da_ting2[i] = 0
                    if da_ting2.get(i) > max_val:
                        max_val = da_ting2.get(i)
                        best_move = i

    if len(available) != 0:
        board = [[int(best_move[2]), int(best_move[5]), int(best_move[8])],
                 [int(best_move[13]), int(best_move[16]), int(best_move[19])],
                 [int(best_move[24]), int(best_move[27]), int(best_move[30])]
                 ]
        if player_turn == 1:
            da_ting_hist1.append(best_move)
        else:
            da_ting_hist2.append(best_move)


def rewarding(reward1, reward2):
    for i in reversed(da_ting_hist1):
        if not da_ting1.get(i, False):
            da_ting1[i] = 0
        da_ting1[i] += learning_rate * (reward1 * decay - da_ting1[i])
        reward1 = da_ting1[i]
    for i in reversed(da_ting_hist2):
        if not da_ting2.get(i, False):
            da_ting2[i] = 0
        da_ting2[i] += learning_rate * (reward2 * decay - da_ting2[i])
        reward2 = da_ting2[i]

train_bool=input('would you like to retrain bertha? - ')
if train_bool=='yes':
    train=int(input('how many iterations would you like bertha to be trained on? - '))
    for i in range(train):
        print(i)
        da_ting_hist1 = []
        da_ting_hist2 = []
        board = board_copy
        possible_moves()
        while len(available) != 0:
            possible_moves()
            move()
            # time.sleep(0.1)
            result()
            # print(result())
            if player_turn == 1:
                player_turn = 2
            else:
                player_turn = 1
        if result() == 1:
            rewarding(1, -1)
            result1['win'] += 1
            result2['lose'] += 1
        elif result() == 2:
            rewarding(-1, 1)
            result2['win'] += 1
            result1['lose'] += 1
        else:
            rewarding(-0.5, -0.5)
            result1['draw'] += 1
            result2['draw'] += 1

    da_ting1_out = open('da_ting1.pickle', 'wb')
    da_ting2_out = open('da_ting2.pickle', 'wb')
    da_ting1_out.truncate(0)
    da_ting2_out.truncate(0)
    pickle.dump(da_ting1, da_ting1_out)
    pickle.dump(da_ting2, da_ting2_out)
    da_ting1_out.close()
    da_ting2_out.close()

da_ting1_in=open('da_ting1.pickle', 'rb')
da_ting2_in=open('da_ting2.pickle', 'rb')
da_ting1=pickle.load(da_ting1_in)
da_ting2=pickle.load(da_ting2_in)
da_ting1_in.close()
da_ting2_in.close()


print(len(da_ting1), len(da_ting2))
print(result1)
print(result2)


board = board_copy

exploration_rate = 0
print(exploration_rate)

### pygame stuff ###
pygame.init()
white=((255),(255),(255))

x_cord=375
y_cord=375


game=True

while game:

    board = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]
             ]
    display = pygame.display.set_mode((x_cord, y_cord))
    pygame.display.set_caption('Tic Tac Toe')
    display.fill(white)

    clock = pygame.time.Clock()

    board_img = pygame.image.load('tictactoe_board.png')
    nought_img = pygame.image.load('nought_2.png')
    cross_img = pygame.image.load('cross.png')

    display.blit(board_img, ((8), (8)))

    which_side=int(input('would you like to play first or second - '))
    possible_moves()
    while game and len(available) != 0:
        movement = False
        display.blit(board_img, ((8), (8)))
        clock.tick()
        pygame.display.update()
        if which_side==1:
            player_turn=1
            possible_moves()
            movement=False
            while len(available) != 0:
                if player_turn == 2:
                    possible_moves()
                    move()
                    player_turn = 1
                    movement = False
                else:
                    while not movement:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                game=False

                            if event.type == pygame.MOUSEBUTTONUP:
                                mouse_position=pygame.mouse.get_pos()
                                print(mouse_position)
                                if mouse_position[0]>((2*(x_cord-16)/3)+8):
                                    if mouse_position[1]>((2*(x_cord-16)/3)+8):
                                        x=9
                                        movement = True
                                        player_turn = 2
                                    elif mouse_position[1]>(((x_cord-16)/3)+8):
                                        x=6
                                        movement = True
                                        player_turn = 2
                                    else:
                                        x=3
                                        movement = True
                                        player_turn = 2
                                elif mouse_position[0]>(((x_cord-16)/3)+8):
                                    if mouse_position[1]>((2*(x_cord-16)/3)+8):
                                        x=8
                                        movement = True
                                        player_turn = 2
                                    elif mouse_position[1]>(((x_cord-16)/3)+8):
                                        x=5
                                        movement = True
                                        player_turn = 2
                                    else:
                                        x=2
                                        movement = True
                                        player_turn = 2
                                else:
                                    if mouse_position[1]>((2*(x_cord-16)/3)+8):
                                        x=7
                                        movement = True
                                        player_turn = 2
                                    elif mouse_position[1]>(((x_cord-16)/3)+8):
                                        x=4
                                        movement = True
                                        player_turn = 2
                                    else:
                                        x=1
                                        movement = True
                                        player_turn = 2

                    player_move = ceil(x / 3) - 1
                    board[player_move][(x - 3 * player_move) - 1] = 1 if board[player_move][(x - 3 * player_move) - 1] == 0 else \
                    board[player_move][(x - 3 * player_move)]

                print(board[0])
                print(board[1])
                print(board[2])
                print()
                possible_moves()

                for i in range(3):
                    for j in range(3):
                        board_num=board[i][j]
                        if board_num==2:
                            display.blit(nought_img, ((120*j+8), ((i*120)+8)))
                        elif board_num==1:
                            display.blit(cross_img, ((120*j+8), ((i*120)+8)))
                pygame.display.update()

                result()
        elif which_side==2:
            player_turn = 1
            possible_moves()
            movement=False
            while len(available) != 0:
                if player_turn == 1:
                    possible_moves()
                    move()
                    player_turn = 2
                    movement=False
                else:
                    while not movement:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                game = False
                            if event.type == pygame.MOUSEBUTTONUP:
                                mouse_position = pygame.mouse.get_pos()
                                if mouse_position[0] > ((2 * (x_cord - 16) / 3) + 8):
                                    if mouse_position[1] > ((2 * (x_cord - 16) / 3) + 8):
                                        x = 9
                                        player_turn = 1
                                        movement=True
                                    elif mouse_position[1] > (((x_cord - 16) / 3) + 8):
                                        x = 6
                                        player_turn = 1
                                        movement = True
                                    else:
                                        x = 3
                                        player_turn = 1
                                        movement=True
                                elif mouse_position[0] > (((x_cord - 16) / 3) + 8):
                                    if mouse_position[1] > ((2 * (x_cord - 16) / 3) + 8):
                                        x = 8
                                        player_turn = 1
                                        movement = True
                                    elif mouse_position[1] > (((x_cord - 16) / 3) + 8):
                                        x = 5
                                        player_turn = 1
                                        movement = True
                                    else:
                                        x = 2
                                        player_turn = 1
                                        movement = True
                                else:
                                    if mouse_position[1] > ((2 * (x_cord - 16) / 3) + 8):
                                        x = 7
                                        player_turn = 1
                                        movement = True
                                    elif mouse_position[1] > (((x_cord - 16) / 3) + 8):
                                        x = 4
                                        player_turn = 1
                                        movement = True
                                    else:
                                        x = 1
                                        player_turn = 1
                                        movement = True

                    player_move = ceil(x / 3) - 1
                    board[player_move][(x - 3 * player_move) - 1] = 2 if board[player_move][(x - 3 * player_move) - 1] == 0 else \
                    board[player_move][(x - 3 * player_move)]

                print(board[0])
                print(board[1])
                print(board[2])
                print()
                possible_moves()

                for i in range(3):
                    for j in range(3):
                        board_num=board[i][j]
                        if board_num==2:
                            display.blit(nought_img, ((120*j+8), ((i*120)+8)))
                        elif board_num==1:
                            display.blit(cross_img, ((120*j+8), ((i*120)+8)))
                pygame.display.update()
                result()




    print('Nice Game')
    game_input = input('would you like to play again - ').lower()
    if game_input in ['false', 'no']:
        game = False
    else:
        game = True

    if result() == 1:
        rewarding(1, -1)
        result1['win'] += 1
        result2['lose'] += 1
    elif result() == 2:
        rewarding(-1, 1)
        result2['win'] += 1
        result1['lose'] += 1
    else:
        rewarding(0.1, 0.1)
        result1['draw'] += 1
        result2['draw'] += 1

print('goodbye')