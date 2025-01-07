"""Gomoku starter functions print_board(board), score(board), play_gomoku(board_size), put_seq_on_board(board, y, x, d_y, d_x, length, col), analysis(board) provided by Michael Guerzhoy with tests contributed by Siavash Kazemian. 

All other functions implemented by Farzin.
"""



def is_sq_in_board(board, y, x):
    ''' Return True iff the square (y, x) is a valid square in the Gomoku board board '''
    
    if y < len(board) and y >= 0:
        if x < len(board[y]) and x >= 0:
            return True
    
    return False



def find_pre_sqr(y_end, x_end, length, d_y, d_x):
    ''' Return a tuple (y_coord, x_coord) of the square immediately before the sequence ending at (y_end, x_end) of length <length> in the direction (d_y, d_x) '''    
    
    # out of board coordinates not considered; use with is_sq_in_board
    pre_y = y_end - (length * d_y)
    pre_x = x_end - (length * d_x)
    return (pre_y, pre_x)



def find_post_sqr(y_end, x_end, length, d_y, d_x):
    ''' Return a tuple (y_coord, x_coord) of the square immediately after the sequence ending at (y_end, x_end) of length <length> in the direction (d_y, d_x) '''
    
    # out of board coordinates not considered; use with is_sq_in_board
    post_y = y_end + d_y
    post_x = x_end + d_x
    return (post_y, post_x)



def find_end_coord(y_start, x_start, length, d_y, d_x):
    ''' Return a tuple (y_coord, x_coord) of the last square in the sequence starting at (y_start, x_start) of length <length> in the direcion (d_y, d_x) '''
    
    y_end = y_start + (length * d_y) - (1 * d_y)
    x_end = x_start + (length * d_x) - (1 * d_x)
    return y_end, x_end
    


def is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):
    ''' Return True if there is a sequence of exactly <length> stones starting at location (y_start, x_start) of colour <col>. Return False if there is a stone of colour <col> either immediately before or immediately after the sequence. Return False if there is no sequence of length <length> starting at location (y_start, x_start). '''

    y = y_start
    x = x_start

    if is_sq_in_board(board, y_start - d_y, x_start - d_x):
        if board[y_start - d_y][x_start - d_x] == col:
            return False

    for i in range(length):
        if is_sq_in_board(board, y, x):
            if board[y][x] == col:
                y += d_y
                x += d_x
            else:
                return False
        else:
            return False
    
    if is_sq_in_board(board, y, x):
        if board[y][x] == col:
            return False

    return True



def is_full(board):
    ''' Return True iff there are no empty squares on the board <board>. '''
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == " ":
                return False
    
    return True



##F1
def is_empty(board):
    ''' Return True iff there are no stones on the board <board>. '''
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != " ":
                return False
    
    return True



##F2
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    ''' Return "OPEN", "CLOSED", or "SEMIOPEN" for the sequence of length <length> that ends at location (y_end, x_end). Assume the sequence is complete, valid and contains stones of only one color. '''
    
    pre_coord = find_pre_sqr(y_end, x_end, length, d_y, d_x)
    post_coord = find_post_sqr(y_end, x_end, length, d_y, d_x)
    
    pre_in_board = is_sq_in_board(board, pre_coord[0], pre_coord[1]) # boolean value
    post_in_board = is_sq_in_board(board, post_coord[0], post_coord[1]) # boolean value
    
    if pre_in_board and post_in_board:  # not a boundary position
        if board[pre_coord[0]][pre_coord[1]] == " " and board[post_coord[0]][post_coord[1]] == " ":
            return "OPEN"
        elif board[pre_coord[0]][pre_coord[1]] != " " and board[post_coord[0]][post_coord[1]] != " ":
            return "CLOSED"
        else:
            return "SEMIOPEN"
    
    elif not pre_in_board and not post_in_board:    # boundary position
        return "CLOSED"
    
    elif not pre_in_board or not post_in_board: # semi-boundary position
        if pre_in_board:
            if board[pre_coord[0]][pre_coord[1]] == " ":
                return "SEMIOPEN"
            return "CLOSED"
        if post_in_board:
            if board[post_coord[0]][post_coord[1]] == " ":
                return "SEMIOPEN"
            return "CLOSED"
        
    else:
        return None     # for testing



##F3
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    ''' Analyse the row R of squares that starts at the location (y_start, x_start) and goes in the direction (d_y, d_x). Return a tuple whose 1st element is the number of open sequences, and 2nd element is the number of semi-open sequences of colour <col> of length <length> in the row R. Assume that (y_start,x_start) is located on the edge of the board. Only complete sequences count. Assume length is an int >= 2. '''
    
    open_seq_count, semi_open_seq_count = 0, 0
    y = y_start
    x = x_start
    
    if (d_y, d_x) == (0, 1):
        while x < 8:
            if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                
                if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1
                    
            y += d_y
            x += d_x
        return open_seq_count, semi_open_seq_count
    
    if (d_y, d_x) == (1, 0):
        while y < 8:
            if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                 
                if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1
                    
            y += d_y
            x += d_x
        return open_seq_count, semi_open_seq_count
    
    if (d_y, d_x) == (1, 1):
        
        if x_start == 0:
            while y < 8:
                if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                    y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                    
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1
                
                y += d_y
                x += d_x
            return open_seq_count, semi_open_seq_count
        
        if y_start == 0:
            while x < 8:
                if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                    y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                    
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1
                y += d_y
                x += d_x
            return open_seq_count, semi_open_seq_count
    
    if (d_y, d_x) == (1, -1):
        
        if x_start == 7:
            while y < 8:
                if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                    y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                    
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1
                y += d_y
                x += d_x
            return open_seq_count, semi_open_seq_count
        
        if y_start == 0:
            while x > 0:
                if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                    y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                    
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1
                y += d_y
                x += d_x
            return open_seq_count, semi_open_seq_count

    return open_seq_count, semi_open_seq_count



##F4
def detect_rows(board, col, length):
    ''' Analyse the board <board> and return a tuple, whose 1st element is the number of open sequences, and 2nd element is the number of semi-open sequences of colour <col> of length <length> on the entire board. Only complete sequences count. Assume length is an int >= 2. '''

    open_seq_count, semi_open_seq_count = 0, 0

    # (d_y, d_x) == (1, 0)
    for i in range(8):
        seq_count = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += seq_count[0]
        semi_open_seq_count += seq_count[1]
    
    # (d_y, d_x) == (0, 1)
    for i in range(8):
        seq_count = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += seq_count[0]
        semi_open_seq_count += seq_count[1]
    
    # (d_y, d_x) == (1, 1):
    for i in range(8):
        seq_count = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += seq_count[0]
        semi_open_seq_count += seq_count[1]
    
    for i in range(1, 8):
        seq_count = detect_row(board, col, i, 0, length, 1, 1)
        open_seq_count += seq_count[0]
        semi_open_seq_count += seq_count[1]
    
    # (d_y, d_x) == (1, -1):
    for i in range(8):
        seq_count = detect_row(board, col, 0, i, length, 1, -1)
        open_seq_count += seq_count[0]
        semi_open_seq_count += seq_count[1]
    
    for i in range(1, 8):
        seq_count = detect_row(board, col, i, 7, length, 1, -1)
        open_seq_count += seq_count[0]
        semi_open_seq_count += seq_count[1]
    
    return open_seq_count, semi_open_seq_count



def detect_closed_seq(board, col, y_start, x_start, length, d_y, d_x):
    ''' Analyse the board <board> and return the number of closed sequences of colour <col> of length <length> based on the starting position, direction and length given. Only complete sequences count. Assume length is an int >= 2. '''
    
    closed_seq_count = 0
    y = y_start
    x = x_start
    
    if (d_y, d_x) == (0, 1):
        while x < 8:
            if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                
                if is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                    closed_seq_count += 1
                    
            y += d_y
            x += d_x
        return closed_seq_count
    
    if (d_y, d_x) == (1, 0):
        while y < 8:
            if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                 
                if is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                    closed_seq_count += 1
                    
            y += d_y
            x += d_x
        return closed_seq_count
    
    if (d_y, d_x) == (1, 1):
        
        if x_start == 0:
            while y < 8:
                if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                    y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                    
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                        closed_seq_count += 1
                
                y += d_y
                x += d_x
            return closed_seq_count
        
        if y_start == 0:
            while x < 8:
                if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                    y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                    
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                        closed_seq_count += 1

                y += d_y
                x += d_x
            return closed_seq_count
    
    if (d_y, d_x) == (1, -1):
        
        if x_start == 7:
            while y < 8:
                if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                    y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                    
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                        closed_seq_count += 1

                y += d_y
                x += d_x
            return closed_seq_count
        
        if y_start == 0:
            while x > 0:
                if is_sequence_complete(board, col, y, x, length, d_y, d_x):
                    y_end, x_end = find_end_coord(y, x, length, d_y, d_x)
                    
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                        closed_seq_count += 1

                y += d_y
                x += d_x
            return closed_seq_count

    return closed_seq_count



def closed_seq_all(board, col, length):
    ''' Analyse the board <board> and return the total number of closed sequences of colour <col> of length <length> on the entire board. Only complete sequences count. Assume length is an int >= 2. '''

    closed_seq_count = 0
    # detect_closed_seq(board, col, y_start, x_start, length, d_y, d_x)

    # (d_y, d_x) == (1, 0)
    for i in range(8):
        seq_count = detect_closed_seq(board, col, 0, i, length, 1, 0)
        closed_seq_count += seq_count
    
    # (d_y, d_x) == (0, 1)
    for i in range(8):
        seq_count = detect_closed_seq(board, col, i, 0, length, 0, 1)
        closed_seq_count += seq_count
    
    # (d_y, d_x) == (1, 1):
    for i in range(8):
        seq_count = detect_closed_seq(board, col, 0, i, length, 1, 1)
        closed_seq_count += seq_count
    
    for i in range(1, 8):
        seq_count = detect_closed_seq(board, col, i, 0, length, 1, 1)
        closed_seq_count += seq_count
    
    # (d_y, d_x) == (1, -1):
    for i in range(8):
        seq_count = detect_closed_seq(board, col, 0, i, length, 1, -1)
        closed_seq_count += seq_count
    
    for i in range(1, 8):
        seq_count = detect_closed_seq(board, col, i, 7, length, 1, -1)
        closed_seq_count += seq_count
    
    return closed_seq_count




##F5
def search_max(board):
    ''' Find and return a tuple of an empty location (y, x) such that putting a black stone in coordinates (y, x) maximizes the score of the board as calculated by score(). Return any one tuple if there are multiple such locations. After Return, the contents of board must remain unchanged. '''
    
    empty_coords = []
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == " ":
                empty_coords.append((i, j))
    
    coord_scores = {}
    loc_board = board
    for i in range(len(empty_coords)):
        # empty_coords[i] has the tuple (y, x)
        y = empty_coords[i][0]
        x = empty_coords[i][1]
        loc_board[y][x] = "b"
        
        coord_scores[(y, x)] = score(loc_board)
        loc_board[y][x] = " "
    
    for k, v in coord_scores.items():
        if v == max(coord_scores.values()):
            return k
    
    # return move_y, move_x



def score(board):
    MAX_SCORE = 100000 # score if b/computer is winning
    
    open_b = {}                 # dictionary for "b" open sequences
    semi_open_b = {}            # dictionary for "b" semi-open sequences
    open_w = {}                 # dictionary for "w" open sequences
    semi_open_w = {}            # dictionary for "w" semi-open sequences
    
    for i in range(2, 6):       # looping for length of sequence 2, 3, 4, 5
        # appending the tuple of (open, semi-open) into each dictionary
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:       
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
    
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])



##F6
def is_win(board):
    ''' Determine current status of the game, and return one of ["White won", "Black won", "Draw", "Continue playing"]. Return "Draw" only when board is full. '''
    
    game_status = ["White won", "Black won", "Draw", "Continue playing"]
    open_b = {}                 # dictionary for "b" open sequences
    semi_open_b = {}            # dictionary for "b" semi-open sequences
    closed_b = {}               # dictionary for "b" closed sequences
    open_w = {}                 # dictionary for "w" open sequences
    semi_open_w = {}            # dictionary for "w" semi-open sequences
    closed_w = {}               # dictionary for "w" closed sequences
    
    for i in range(2, 6):
        # appending open, semi-open and closed seq number into each dictionary
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        closed_b[i] = closed_seq_all(board, "b", i)
        closed_w[i] = closed_seq_all(board, "w", i)

    
    if open_b[5] >= 1 or semi_open_b[5] >= 1 or closed_b[5] >= 1:       
        return game_status[1]
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1 or closed_w[5] >= 1:
        return game_status[0]
    
    elif is_full(board):
        return game_status[2]
    
    else:
        return game_status[3]
    
    



def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)    



def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))



def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
           


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x



## Test F1
def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


## Test F2
def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


## Test F3
def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")


## Test F4
def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")


## Test F5
def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")


## Test F6
def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()


## Test F7
def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0



def test_is_sq_in_board():
    board = make_empty_board(8)
    for i in range (8):
        for j in range(8):
            if not is_sq_in_board(board, i, j):
                print("TEST CASE for is_sq_in_board FAILED")
    for i in range(8, 100):
        for  j in range(100):
            if is_sq_in_board(board, i, j):
                print("TEST CASE for is_sq_in_board FAILED")
    
    for i in range(0, -100):
        for j in range(0, -100):
            if is_sq_in_board(board, i, j):
                print("TEST CASE for is_sq_in_board FAILED")
    
    print("TEST CASE for is_sq_in_board PASSED")



if __name__ == '__main__':

    board = make_empty_board(8)
    print_board(board)
    put_seq_on_board(board, 1, 3, 1, 0, 4, "b")
    put_seq_on_board(board, 5, 5, 1, 1, 2, "b")
    put_seq_on_board(board, 0, 7, 1, -1, 4, "w")
    put_seq_on_board(board, 2, 0, 0, 1, 2, "w")
    put_seq_on_board(board, 5, 0, 1, 1, 3, "b")
    print_board(board)
    
    # testing is_sequence_complete
    is_sequence_complete(board, "b", 1, 3, 4, 1, 0)
    is_sequence_complete(board, "b", 1, 3, 4, 1, 0)
    is_sequence_complete(board, "b", 5, 5, 2, 1, 1)
    is_sequence_complete(board, "w", 0, 7, 4, 1, -1)
    is_sequence_complete(board, "w", 2, 0, 2, 0, 1)
    
    # testing is_bounded
    print(is_bounded(board, 2, 1, 2, 0, 1))         # Should return semi-open;  PASSED
    print(is_bounded(board, 4, 3, 4, 1, 0))         # Should return open;       PASSED
    print(is_bounded(board, 3, 4, 4, 1, -1))        # Should return closed;     PASSED
    print(is_bounded(board, 6, 6, 2, 1, 1))         # Should return open;       PASSED
    print(is_bounded(board, 7, 2, 3, 1, 1))         # Should return closed;     PASSED
    
    # reset
    board = make_empty_board(8)
    print_board(board)
    put_seq_on_board(board, 1, 3, 1, 0, 4, "b")
    put_seq_on_board(board, 5, 5, 1, 1, 2, "b")
    put_seq_on_board(board, 0, 7, 1, -1, 4, "w")
    put_seq_on_board(board, 2, 0, 0, 1, 2, "w")
    put_seq_on_board(board, 5, 0, 1, 1, 3, "b")
    put_seq_on_board(board, 0, 0, 1, 1, 3, "b")
    put_seq_on_board(board, 4, 2, 1, 0, 2, "b")
    put_seq_on_board(board, 3, 5, 1, -1, 2, "w")
    print_board(board)
    
    # testing detect_row
    print(detect_row(board, "w", 0, 7, 4, 1, -1))           # should return (0, 0);  PASSED
    print(detect_row(board, "b", 5, 0, 3, 1, 1))            # should return (0, 0);  PASSED
    print(detect_row(board, "w", 2, 0, 1, 0, 1))            # should return (1, 0);  PASSED
    print(detect_row(board, "b", 0, 0, 2, 1, 1))            # should return (0, 1);  PASSED
    print(detect_row(board, "b", 0, 2, 1, 1, 0))            # should return (1, 1);  PASSED
    print(detect_row(board, "b", 0, 7, 3, 1, -1))           # should return (0, 1);  PASSED
    print()

    # testing find_end_coord
    print(find_end_coord(0, 0, 4, 1, 1))            # should return (3, 3)      PASSED
    print(find_end_coord(4, 3, 3, 1, -1))           # should return (6, 1)      PASSED
    print(find_end_coord(2, 0, 2, 0, 1))            # should return (2, 1)      PASSED
    print(find_end_coord(1, 3, 4, 1, 0))            # should return (4, 3)      PASSED
    
    print(detect_rows(board, "b", 2))               #
    easy_testset_for_main_functions()
    some_tests()
    
    # play_gomoku(8)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

