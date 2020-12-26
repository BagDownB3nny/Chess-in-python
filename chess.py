import pygame
import os
pygame.init()


"""Setting of all variables"""
win_width=1920
win_height=1080
win=pygame.display.set_mode((win_width,win_height))    # window
win.fill((255,255,255))
board = [['Br','Bh','Bb','Bq','Bk','Bb','Bh','Br'],
         ['Bp','Bp','Bp','Bp','Bp','Bp','Bp','Bp'],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         ['Wp','Wp','Wp','Wp','Wp','Wp','Wp','Wp'],
         ['Wr','Wh','Wb','Wq','Wk','Wb','Wh','Wr']]
moves=[]
current_piece = ""
turn = ['W','B']
en_passant=[]
en_passant_capture=[]
castle=[(0,0),(4,0),(7,0),(0,7),(4,7),(7,7)]
temp_board=[row[:] for row in board]

def change_turn():
    """ Changes the turn """
    global turn
    if turn[0]=='W':
        turn[0]='B'
    else:
        turn[0]='W'
    if turn[1]=='W':
        turn[1]='B'
    else:
        turn[1]='W'


def draw_bg():
    """
    Finds the height of the window, and create a square board with a size that is 80% of window's height
    :return:
    """
    """The x and y coordinates of the top left hand corner of the board"""
    side=0.8*(win_height)
    tile_size=side/8
    top_left_x=(win_width-side)/2
    top_left_y=0.1*win_height
    """Draw the board face"""
    pygame.draw.rect(win,(255,255,255),(top_left_x,top_left_y,side,side))
    counter=0
    """Draw horizontal lines"""
    while counter<9:
        pygame.draw.line(win,(0,0,0),(top_left_x,top_left_y+counter*tile_size),(top_left_x+side,top_left_y+counter*tile_size))
        counter+=1
    counter=0
    """Draw vertical lines"""
    while counter<9:
        pygame.draw.line(win,(0,0,0),(top_left_x+counter*tile_size,top_left_y),(top_left_x+counter*tile_size,top_left_y+side))
        counter+=1

def draw(board):
    """
    Uses the board matrix to draw the correct pieces in their respective positions
    :param board:
    :return:
    """
    side = 0.8 * (win_height)
    tile_size = side / 8
    top_left_x = (win_width - side)/2 + tile_size/2
    top_left_y = 0.1 * win_height + tile_size/2

    for i,row in enumerate(board):
        for j,tile in enumerate(row):
            if tile=='Br':
                img='black_rook.png'
            if tile=='Bh':
                img='black_knight.png'
            if tile=='Bb':
                img='black_bishop.png'
            if tile=='Bq':
                img='black_queen.png'
            if tile=='Bk':
                img='black_king.png'
            if tile=='Bp':
                img='black_pawn.png'
            if tile=='Wr':
                img='white_rook.png'
            if tile=='Wh':
                img='white_knight.png'
            if tile=='Wb':
                img='white_bishop.png'
            if tile=='Wq':
                img='white_queen.png'
            if tile=='Wk':
                img='white_king.png'
            if tile=='Wp':
                img='white_pawn.png'
            if tile==0:
                img=0
            if img!=0:
                img=pygame.image.load(os.path.join("Assets",img))
                pygame.transform.scale(img,(round(0.9*tile_size),round(0.9*tile_size))) # setting image to have a side 0.9 times of the tile side
                win.blit(img,[top_left_x+j*tile_size-round(0.45*tile_size),top_left_y+i*tile_size-round(0.45*tile_size)])   # blitting the correct pieces into their correct places

def click(pos):
    """ Returns the tile clicked in the form of (x,y) where (0,0) is the top left tile
    Returns false if no tile is clicked"""
    x=pos[0]
    y=pos[1]
    side = 0.8 * (win_height)
    tile_size = side / 8
    top_left_x = (win_width - side)/2
    top_left_y = 0.1 * win_height
    """ Create a 8x8 matrix, where each tile is represented by [(x1,y1),(x2,y2)], representing the top left corner 
    coordinates and the bottom right corner coordinates"""
    tiles=[[[(top_left_x+tile_size*i,top_left_y+tile_size*j),(top_left_x+tile_size*(i+1),top_left_y+tile_size*(j+1))] for i in range(8)] for j in range(8)]
    for i, row in enumerate(tiles):
        for j, tile in enumerate(row):
            if tile[0][0]<x<tile[1][0] and tile[0][1]<y<tile[1][1]:
                return (j,i)
    return False

def is_piece(tile,board_arg):
    """Returns the piece currently sitting on the tile given
    If out of bounds, will return "OOB"
    If in between lines, will return "Line" """
    if tile == 1:
        return 0
    elif -1<tile[0]<8 and -1<tile[1]<8:
        return board_arg[abs(tile[1])][abs(tile[0])]
    return "OUT"

def highlight_tile(tiles,color=(255,200,0)):
    """Highlights tiles given"""
    side = 0.8 * (win_height)
    tile_size = side / 8
    top_left_x = (win_width - side) / 2
    top_left_y = 0.1 * win_height
    for tile in tiles:
        x = tile [0]
        y = tile [1]
        pygame.draw.rect(win,color,((top_left_x+x*tile_size,top_left_y+y*tile_size),(tile_size,tile_size)))
        pygame.draw.rect(win,(0,0,0),((top_left_x+x*tile_size+1,top_left_y+y*tile_size+1),(tile_size-1,tile_size-1)),1)




def show_moves(piece,tile,board_arg):
    """Highlights and stores a list of possible moves for the player to take"""
    global moves
    global current_piece
    global en_passant
    global en_passant_capture
    moves=[]
    eat_moves=[]
    x = tile[0]
    y = tile [1]
    current_piece = (piece,x,y)

    if piece=='Wr' or piece=='Br':  # return a list of moves the rook can take on its tile
        for i in range(8):  # finds the squares the rook can move to on its right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y),board_arg):
                if piece[0] not in is_piece((x+i+1,y),board_arg) and is_piece((x+i+1,y),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y))
                break
            else:
                moves.append((x+i+1,y))
        for i in range(8): # finds the squares the rook can move to on its left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y),board_arg):
                if piece[0] not in is_piece((x-i-1,y),board_arg) and is_piece((x-i-1,y),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y))
                break
            else:
                moves.append((x-i-1,y))
        for i in range(8): # finds the squares the rook can move to down
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y+i+1),board_arg):
                if piece[0] not in is_piece((x,y+i+1),board_arg) and is_piece((x,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x,y+i+1))
                break
            else:
                moves.append((x,y+i+1))
        for i in range(8): # finds the squares the rook can move to up
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y-i-1),board_arg):
                if piece[0] not in is_piece((x,y-i-1),board_arg) and is_piece((x,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x,y-i-1))
                break
            else:
                moves.append((x,y-i-1))

    if piece=='Wh' or piece=='Bh':  # return a list of moves the rook can take on its tile
        """ Iterate through possible knight moves in a clockwise sequence"""

        if is_piece((x+1,y-2),board_arg):   # top right 1
            if piece[0] not in is_piece((x+1,y-2),board_arg) and is_piece((x+1,y-2),board_arg)!='OUT':
                eat_moves.append((x+1,y-2))
        else:
            moves.append((x+1,y-2))

        if is_piece((x+2,y-1),board_arg):   # top right 2
            if piece[0] not in is_piece((x+2,y-1),board_arg) and is_piece((x+2,y-1),board_arg)!='OUT':
                eat_moves.append((x+2,y-1))
        else:
            moves.append((x+2,y-1))

        if is_piece((x+2,y+1),board_arg):   # bottom right 1
            if piece[0] not in is_piece((x+2,y+1),board_arg) and is_piece((x+2,y+1),board_arg)!='OUT':
                eat_moves.append((x+2,y+1))
        else:
            moves.append((x+2,y+1))

        if is_piece((x+1,y+2),board_arg):   # bottom right  2
            if piece[0] not in is_piece((x+1,y+2),board_arg) and is_piece((x+1,y+2),board_arg)!='OUT':
                eat_moves.append((x+1,y+2))
        else:
            moves.append((x+1,y+2))

        if is_piece((x-1,y+2),board_arg):   # bottom left 1
            if piece[0] not in is_piece((x-1,y+2),board_arg) and is_piece((x-1,y+2),board_arg)!='OUT':
                eat_moves.append((x-1,y+2))
        else:
            moves.append((x-1,y+2))

        if is_piece((x-2,y+1),board_arg):   # bottom left 2
            if piece[0] not in is_piece((x-2,y+1),board_arg) and is_piece((x-2,y+1),board_arg)!='OUT':
                eat_moves.append((x-2,y+1))
        else:
            moves.append((x-2,y+1))

        if is_piece((x-2,y-1),board_arg):   # top left 1
            if piece[0] not in is_piece((x-2,y-1),board_arg) and is_piece((x-2,y-1),board_arg)!='OUT':
                eat_moves.append((x-2,y-1))
        else:
            moves.append((x-2,y-1))

        if is_piece((x-1,y-2),board_arg):   # top left 2
            if piece[0] not in is_piece((x-1,y-2),board_arg) and is_piece((x-1,y-2),board_arg)!='OUT':
                eat_moves.append((x-1,y-2))
        else:
            moves.append((x-1,y-2))

    if piece=='Wb' or piece=='Bb':  # return a list of moves the rook can take on its tile

        for i in range(8):  # finds the squares the bishop can move bottom right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y+i+1),board_arg):
                if piece[0] not in is_piece((x+i+1,y+i+1),board_arg) and is_piece((x+i+1,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y+i+1))
                break
            else:
                moves.append((x+i+1,y+i+1))

        for i in range(8): # finds the squares the bishop can move bottom left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y+i+1),board_arg):
                if piece[0] not in is_piece((x-i-1,y+i+1),board_arg) and is_piece((x-i-1,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y+i+1))
                break
            else:
                moves.append((x-i-1,y+i+1))

        for i in range(8): # finds the squares the bishop can move top left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y-i-1),board_arg):
                if piece[0] not in is_piece((x-i-1,y-i-1),board_arg) and is_piece((x-i-1,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y-i-1))
                break
            else:
                moves.append((x-i-1,y-i-1))

        for i in range(8): # finds the squares the bishop can move top right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y-i-1),board_arg):
                if piece[0] not in is_piece((x+i+1,y-i-1),board_arg) and is_piece((x+i+1,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y-i-1))
                break
            else:
                moves.append((x+i+1,y-i-1))

    if piece=='Wq' or piece=='Bq':  # return a list of moves the queen can take on its tile

        for i in range(8):  # finds the squares the bishop can move bottom right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y+i+1),board_arg):
                if piece[0] not in is_piece((x+i+1,y+i+1),board_arg) and is_piece((x+i+1,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y+i+1))
                break
            else:
                moves.append((x+i+1,y+i+1))

        for i in range(8): # finds the squares the bishop can move bottom left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y+i+1),board_arg):
                if piece[0] not in is_piece((x-i-1,y+i+1),board_arg) and is_piece((x-i-1,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y+i+1))
                break
            else:
                moves.append((x-i-1,y+i+1))

        for i in range(8): # finds the squares the bishop can move top left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y-i-1),board_arg):
                if piece[0] not in is_piece((x-i-1,y-i-1),board_arg) and is_piece((x-i-1,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y-i-1))
                break
            else:
                moves.append((x-i-1,y-i-1))

        for i in range(8): # finds the squares the bishop can move top right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y-i-1),board_arg):
                if piece[0] not in is_piece((x+i+1,y-i-1),board_arg) and is_piece((x+i+1,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y-i-1))
                break
            else:
                moves.append((x+i+1,y-i-1))
        for i in range(8):  # finds the squares the rook can move to on its right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y),board_arg):
                if piece[0] not in is_piece((x+i+1,y),board_arg) and is_piece((x+i+1,y),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y))
                break
            else:
                moves.append((x+i+1,y))
        for i in range(8): # finds the squares the rook can move to on its left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y),board_arg):
                if piece[0] not in is_piece((x-i-1,y),board_arg) and is_piece((x-i-1,y),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y))
                break
            else:
                moves.append((x-i-1,y))
        for i in range(8): # finds the squares the rook can move to down
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y+i+1),board_arg):
                if piece[0] not in is_piece((x,y+i+1),board_arg) and is_piece((x,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x,y+i+1))
                break
            else:
                moves.append((x,y+i+1))

        for i in range(8): # finds the squares the rook can move to up
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y-i-1),board_arg):
                if piece[0] not in is_piece((x,y-i-1),board_arg) and is_piece((x,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x,y-i-1))
                break
            else:
                moves.append((x,y-i-1))

    if piece == 'Wk' or piece == 'Bk':  # return a list of moves the king can take on its tile, starting clockwise

        if is_piece((x,y-1),board_arg):
            if piece[0] not in is_piece((x,y-1),board_arg) and is_piece((x,y-1),board_arg) != "OUT":
                eat_moves.append((x,y-1))
        else:
            moves.append((x,y-1))

        if is_piece((x+1,y-1),board_arg):
            if piece[0] not in is_piece((x+1,y-1),board_arg) and is_piece((x+1,y-1),board_arg) != "OUT":
                eat_moves.append((x+1,y-1))
        else:
            moves.append((x+1,y-1))

        if is_piece((x+1,y),board_arg):
            if piece[0] not in is_piece((x+1,y),board_arg) and is_piece((x+1,y),board_arg) != "OUT":
                eat_moves.append((x+1,y))
        else:
            moves.append((x+1,y))

        if is_piece((x+1,y+1),board_arg):
            if piece[0] not in is_piece((x+1,y+1),board_arg) and is_piece((x+1,y+1),board_arg) != "OUT":
                eat_moves.append((x+1,y+1))
        else:
            moves.append((x+1,y+1))

        if is_piece((x,y+1),board_arg):
            if piece[0] not in is_piece((x,y+1),board_arg) and is_piece((x,y+1),board_arg) != "OUT":
                eat_moves.append((x,y+1))
        else:
            moves.append((x,y+1))

        if is_piece((x-1,y+1),board_arg):
            if piece[0] not in is_piece((x-1,y+1),board_arg) and is_piece((x-1,y+1),board_arg) != "OUT":
                eat_moves.append((x-1,y+1))
        else:
            moves.append((x-1,y+1))

        if is_piece((x-1,y),board_arg):
            if piece[0] not in is_piece((x-1,y),board_arg) and is_piece((x-1,y),board_arg) != "OUT":
                eat_moves.append((x-1,y))
        else:
            moves.append((x-1,y))

        if is_piece((x-1,y-1),board_arg):
            if piece[0] not in is_piece((x-1,y-1),board_arg) and is_piece((x-1,y-1),board_arg) != "OUT":
                eat_moves.append((x-1,y-1))
        else:
            moves.append((x-1,y-1))

        """ Check to see if king can castle by checking the squares between itself and the rook
        and checking to see if both itself and the rook are able to castle"""
        if piece=='Wk':
            if not is_piece((5,7),board_arg) and not is_piece((6,7),board_arg) and (7,7) in castle and (4,7) in castle:
                if check_state('W',board_arg,(5,7)) and check_state('W',board_arg,(6,7)):
                    moves.append((x+2,y))
        if piece=='Wk':
            if not is_piece((1,7),board_arg) and not is_piece((2,7),board_arg) and not is_piece((3,7),board_arg) and (0,7) in castle and (4,7) in castle:
                if check_state('W',board_arg,(1, 7)) and check_state('W',board_arg,(2, 7)) and check_state('W',board_arg,(3, 7)):
                    moves.append((x-2,y))
        if piece=='Bk':
            if not is_piece((5,0),board_arg) and not is_piece((6,0),board_arg) and (7,0) in castle and (4,0) in castle:
                if check_state('B',board_arg,(5, 0)) and check_state('B',board_arg,(6, 0)):
                    moves.append((x+2,y))
        if piece=='Bk':
            if not is_piece((1,0),board_arg) and not is_piece((2,0),board_arg) and not is_piece((3,0),board_arg) and (4,0) in castle and (0,0) in castle:
                if check_state('B',board_arg,(1, 0)) and check_state('B',board_arg,(2, 0)) and check_state('B',board_arg,(3, 0)):
                    moves.append((x-2,y))

    if piece == 'Wp':  # return a list of moves the white pawn can take on its tile
        """ If Wp at starting y-axis, allow it to travel 2 spaces if 2nd space is free"""
        if y == 6:
            if not is_piece((x,y-1),board_arg) and not is_piece((x,y-2),board_arg):
                moves.append((x,y-2))
        if not is_piece((x,y-1),board_arg):
            moves.append((x,y-1))
        """ Check diagonals for a capture"""
        if 'B' in str(is_piece((x-1,y-1),board_arg)):
            eat_moves.append((x-1,y-1))
        if 'B' in str(is_piece((x+1,y-1),board_arg)):
            eat_moves.append((x+1,y-1))
        """ Check for en-passant capture"""
        if 'Bp' in str(is_piece((x+1,y),board_arg)) and en_passant==[x+1,y]:
            eat_moves.append((x+1,y-1))
            en_passant_capture=[x+1,y-1]
        if 'Bp' in str(is_piece((x-1,y),board_arg)) and en_passant==[x-1,y]:
            eat_moves.append((x-1,y-1))
            en_passant_capture=[x-1,y-1]

    if piece == 'Bp':  # return a list of moves the black pawn can take on its tile
        """ If Bp at starting y-axis, allow it to travel 2 spaces if 2nd space is free"""
        if y == 1:
            if not is_piece((x,y+1),board_arg) and not is_piece((x,y+2),board_arg):
                moves.append((x,y+2))
        if not is_piece((x,y+1),board_arg):
            moves.append((x,y+1))
        """ Check diagonals for a capture"""
        if 'W' in str(is_piece((x-1,y+1),board_arg)):
            eat_moves.append((x-1,y+1))
        if 'W' in str(is_piece((x+1,y+1),board_arg)):
            eat_moves.append((x+1,y+1))
        """ Check for en-passant capture, and if capture is available, append to eat_moves and change
        en_passant_capture to match the capture tile"""
        if 'Wp' in str(is_piece((x+1,y),board_arg)) and en_passant == [x+1,y]:
            eat_moves.append((x+1,y+1))
            en_passant_capture=[x+1,y+1]
        if 'Wp' in str(is_piece((x-1,y),board_arg)) and en_passant == [x-1,y]:
            eat_moves.append((x-1,y+1))
            en_passant_capture=[x-1,y+1]

    draw_bg()
    highlight_tile(moves)
    highlight_tile(eat_moves,(255,0,0))
    for move in eat_moves:
        moves.append(move)
    moves.append(1)
    return moves

def check_moves(piece,tile,board_arg):
    """Highlights and stores a list of possible moves for the player to take"""
    moves=[]
    eat_moves=[]
    x = tile[0]
    y = tile [1]


    if piece=='Wr' or piece=='Br':  # return a list of moves the rook can take on its tile
        for i in range(8):  # finds the squares the rook can move to on its right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y),board_arg):
                if piece[0] not in is_piece((x+i+1,y),board_arg) and is_piece((x+i+1,y),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y))
                break
            else:
                moves.append((x+i+1,y))
        for i in range(8): # finds the squares the rook can move to on its left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y),board_arg):
                if piece[0] not in is_piece((x-i-1,y),board_arg) and is_piece((x-i-1,y),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y))
                break
            else:
                moves.append((x-i-1,y))
        for i in range(8): # finds the squares the rook can move to down
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y+i+1),board_arg):
                if piece[0] not in is_piece((x,y+i+1),board_arg) and is_piece((x,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x,y+i+1))
                break
            else:
                moves.append((x,y+i+1))
        for i in range(8): # finds the squares the rook can move to up
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y-i-1),board_arg):
                if piece[0] not in is_piece((x,y-i-1),board_arg) and is_piece((x,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x,y-i-1))
                break
            else:
                moves.append((x,y-i-1))

    if piece=='Wh' or piece=='Bh':  # return a list of moves the rook can take on its tile
        """ Iterate through possible knight moves in a clockwise sequence"""

        if is_piece((x+1,y-2),board_arg):   # top right 1
            if piece[0] not in is_piece((x+1,y-2),board_arg) and is_piece((x+1,y-2),board_arg)!='OUT':
                eat_moves.append((x+1,y-2))
        else:
            moves.append((x+1,y-2))

        if is_piece((x+2,y-1),board_arg):   # top right 2
            if piece[0] not in is_piece((x+2,y-1),board_arg) and is_piece((x+2,y-1),board_arg)!='OUT':
                eat_moves.append((x+2,y-1))
        else:
            moves.append((x+2,y-1))

        if is_piece((x+2,y+1),board_arg):   # bottom right 1
            if piece[0] not in is_piece((x+2,y+1),board_arg) and is_piece((x+2,y+1),board_arg)!='OUT':
                eat_moves.append((x+2,y+1))
        else:
            moves.append((x+2,y+1))

        if is_piece((x+1,y+2),board_arg):   # bottom right  2
            if piece[0] not in is_piece((x+1,y+2),board_arg) and is_piece((x+1,y+2),board_arg)!='OUT':
                eat_moves.append((x+1,y+2))
        else:
            moves.append((x+1,y+2))

        if is_piece((x-1,y+2),board_arg):   # bottom left 1
            if piece[0] not in is_piece((x-1,y+2),board_arg) and is_piece((x-1,y+2),board_arg)!='OUT':
                eat_moves.append((x-1,y+2))
        else:
            moves.append((x-1,y+2))

        if is_piece((x-2,y+1),board_arg):   # bottom left 2
            if piece[0] not in is_piece((x-2,y+1),board_arg) and is_piece((x-2,y+1),board_arg)!='OUT':
                eat_moves.append((x-2,y+1))
        else:
            moves.append((x-2,y+1))

        if is_piece((x-2,y-1),board_arg):   # top left 1
            if piece[0] not in is_piece((x-2,y-1),board_arg) and is_piece((x-2,y-1),board_arg)!='OUT':
                eat_moves.append((x-2,y-1))
        else:
            moves.append((x-2,y-1))

        if is_piece((x-1,y-2),board_arg):   # top left 2
            if piece[0] not in is_piece((x-1,y-2),board_arg) and is_piece((x-1,y-2),board_arg)!='OUT':
                eat_moves.append((x-1,y-2))
        else:
            moves.append((x-1,y-2))

    if piece=='Wb' or piece=='Bb':  # return a list of moves the rook can take on its tile

        for i in range(8):  # finds the squares the bishop can move bottom right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y+i+1),board_arg):
                if piece[0] not in is_piece((x+i+1,y+i+1),board_arg) and is_piece((x+i+1,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y+i+1))
                break
            else:
                moves.append((x+i+1,y+i+1))

        for i in range(8): # finds the squares the bishop can move bottom left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y+i+1),board_arg):
                if piece[0] not in is_piece((x-i-1,y+i+1),board_arg) and is_piece((x-i-1,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y+i+1))
                break
            else:
                moves.append((x-i-1,y+i+1))

        for i in range(8): # finds the squares the bishop can move top left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y-i-1),board_arg):
                if piece[0] not in is_piece((x-i-1,y-i-1),board_arg) and is_piece((x-i-1,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y-i-1))
                break
            else:
                moves.append((x-i-1,y-i-1))

        for i in range(8): # finds the squares the bishop can move top right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y-i-1),board_arg):
                if piece[0] not in is_piece((x+i+1,y-i-1),board_arg) and is_piece((x+i+1,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y-i-1))
                break
            else:
                moves.append((x+i+1,y-i-1))

    if piece=='Wq' or piece=='Bq':  # return a list of moves the queen can take on its tile

        for i in range(8):  # finds the squares the bishop can move bottom right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y+i+1),board_arg):
                if piece[0] not in is_piece((x+i+1,y+i+1),board_arg) and is_piece((x+i+1,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y+i+1))
                break
            else:
                moves.append((x+i+1,y+i+1))

        for i in range(8): # finds the squares the bishop can move bottom left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y+i+1),board_arg):
                if piece[0] not in is_piece((x-i-1,y+i+1),board_arg) and is_piece((x-i-1,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y+i+1))
                break
            else:
                moves.append((x-i-1,y+i+1))

        for i in range(8): # finds the squares the bishop can move top left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y-i-1),board_arg):
                if piece[0] not in is_piece((x-i-1,y-i-1),board_arg) and is_piece((x-i-1,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y-i-1))
                break
            else:
                moves.append((x-i-1,y-i-1))

        for i in range(8): # finds the squares the bishop can move top right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y-i-1),board_arg):
                if piece[0] not in is_piece((x+i+1,y-i-1),board_arg) and is_piece((x+i+1,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y-i-1))
                break
            else:
                moves.append((x+i+1,y-i-1))
        for i in range(8):  # finds the squares the rook can move to on its right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y),board_arg):
                if piece[0] not in is_piece((x+i+1,y),board_arg) and is_piece((x+i+1,y),board_arg)!="OUT":
                    eat_moves.append((x+i+1,y))
                break
            else:
                moves.append((x+i+1,y))
        for i in range(8): # finds the squares the rook can move to on its left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y),board_arg):
                if piece[0] not in is_piece((x-i-1,y),board_arg) and is_piece((x-i-1,y),board_arg)!="OUT":
                    eat_moves.append((x-i-1,y))
                break
            else:
                moves.append((x-i-1,y))
        for i in range(8): # finds the squares the rook can move to down
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y+i+1),board_arg):
                if piece[0] not in is_piece((x,y+i+1),board_arg) and is_piece((x,y+i+1),board_arg)!="OUT":
                    eat_moves.append((x,y+i+1))
                break
            else:
                moves.append((x,y+i+1))

        for i in range(8): # finds the squares the rook can move to up
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y-i-1),board_arg):
                if piece[0] not in is_piece((x,y-i-1),board_arg) and is_piece((x,y-i-1),board_arg)!="OUT":
                    eat_moves.append((x,y-i-1))
                break
            else:
                moves.append((x,y-i-1))

    if piece == 'Wk' or piece == 'Bk':  # return a list of moves the king can take on its tile, starting clockwise

        if is_piece((x,y-1),board_arg):
            if piece[0] not in is_piece((x,y-1),board_arg) and is_piece((x,y-1),board_arg) != "OUT":
                eat_moves.append((x,y-1))
        else:
            moves.append((x,y-1))

        if is_piece((x+1,y-1),board_arg):
            if piece[0] not in is_piece((x+1,y-1),board_arg) and is_piece((x+1,y-1),board_arg) != "OUT":
                eat_moves.append((x+1,y-1))
        else:
            moves.append((x+1,y-1))

        if is_piece((x+1,y),board_arg):
            if piece[0] not in is_piece((x+1,y),board_arg) and is_piece((x+1,y),board_arg) != "OUT":
                eat_moves.append((x+1,y))
        else:
            moves.append((x+1,y))

        if is_piece((x+1,y+1),board_arg):
            if piece[0] not in is_piece((x+1,y+1),board_arg) and is_piece((x+1,y+1),board_arg) != "OUT":
                eat_moves.append((x+1,y+1))
        else:
            moves.append((x+1,y+1))

        if is_piece((x,y+1),board_arg):
            if piece[0] not in is_piece((x,y+1),board_arg) and is_piece((x,y+1),board_arg) != "OUT":
                eat_moves.append((x,y+1))
        else:
            moves.append((x,y+1))

        if is_piece((x-1,y+1),board_arg):
            if piece[0] not in is_piece((x-1,y+1),board_arg) and is_piece((x-1,y+1),board_arg) != "OUT":
                eat_moves.append((x-1,y+1))
        else:
            moves.append((x-1,y+1))

        if is_piece((x-1,y),board_arg):
            if piece[0] not in is_piece((x-1,y),board_arg) and is_piece((x-1,y),board_arg) != "OUT":
                eat_moves.append((x-1,y))
        else:
            moves.append((x-1,y))

        if is_piece((x-1,y-1),board_arg):
            if piece[0] not in is_piece((x-1,y-1),board_arg) and is_piece((x-1,y-1),board_arg) != "OUT":
                eat_moves.append((x-1,y-1))
        else:
            moves.append((x-1,y-1))

    if piece == 'Wp':  # return a list of moves the white pawn can take on its tile
        """ If Wp at starting y-axis, allow it to travel 2 spaces if 2nd space is free"""
        """ Check diagonals for a capture"""
        if 'B' in str(is_piece((x-1,y-1),board_arg)):
            eat_moves.append((x-1,y-1))
        if 'B' in str(is_piece((x+1,y-1),board_arg)):
            eat_moves.append((x+1,y-1))
        """ If Wp at starting y-axis, allow it to travel 2 spaces if 2nd space is free"""
        if y == 6:
            if not is_piece((x, y - 1),board_arg) and not is_piece((x, y - 2),board_arg):
                moves.append((x, y - 2))
        if not is_piece((x, y - 1),board_arg):
            moves.append((x, y - 1))

    if piece == 'Bp':  # return a list of moves the black pawn can take on its tile
        """ If Bp at starting y-axis, allow it to travel 2 spaces if 2nd space is free"""
        """ Check diagonals for a capture"""
        if 'W' in str(is_piece((x-1,y+1),board_arg)):
            eat_moves.append((x-1,y+1))
        if 'W' in str(is_piece((x+1,y+1),board_arg)):
            eat_moves.append((x+1,y+1))
        """ If Bp at starting y-axis, allow it to travel 2 spaces if 2nd space is free"""
        if y == 1:
            if not is_piece((x, y + 1),board_arg) and not is_piece((x, y + 2),board_arg):
                moves.append((x, y + 2))
        if not is_piece((x, y + 1),board_arg):
            moves.append((x, y + 1))

    for move in eat_moves:
        moves.append(move)

    return moves

def find_king(color,board_arg):
    for i,row in enumerate(board_arg):
        for j, tile in enumerate(row):
            if tile == color+'k':
                return (j,i)

def check_state(color,board_arg,variable = 0):
    """ Checks the board state of the given team color, and return True if king is not threatened
    1. Iterate through each tile in the board to find the team's pieces
    2. Find the moves of that piece
    3. If the tile is in the is_piece of one of those moves, return False"""
    if not variable:
        search=find_king(color,board_arg)
    else:
        search=variable
    for i,row in enumerate(board_arg):
        for j,tile in enumerate(row):
            if board_arg[i][j] and color not in board_arg[i][j]:
                if search in check_moves(board_arg[i][j],(j,i),board_arg):
                    return False
    return True

def check_for_checkmate(color):
    """ Summary: return True if king is checkmated
    1. Find the number of attackers by checking moves of every opposing piece. If only one attacker, check own pieces to see which piece can capture it, then do
    check_state on a check_board to see if king is under threat if piece were to capture it. Then check own pieces to see which piece can move to one of the attacking
    piece's moves, then do check_state on a check_board to see if king is under threat if piece were to intercept.
    Return False if any of these attempts succeed. Proceed to step 2 if all attempts fail
    2. Check the 8 surrounding squares and see if they are under attack. If check_state returns False for every tile, king is checkmated. Return True"""
    attackers=[]
    check_board=[row[:] for row in board]
    for i,row in enumerate(board):
        for j,tile in enumerate(row):
            if type(tile)==str and color not in tile:
                if find_king(color,check_board) in check_moves(tile, (j,i),check_board):
                    attackers.append((j,i))
    if len(attackers)>1:
        return True
    for attacker in attackers:
        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                if type(tile)==str and color in tile:
                    for move in check_moves(tile,(j,i),check_board):
                        if move in check_moves(is_piece(attacker,check_board),attacker,check_board) or move==attacker:
                            check_board[move[1]][move[0]]=tile
                            check_board[i][j]=0
                            if check_state(color,check_board):
                                return False
                            else:
                                check_board = [row[:] for row in board]
    for move in check_moves(color+'k',find_king(color,check_board),check_board):
        check_board[move[1]][move[0]]=color+'k'
        check_board[find_king(color,check_board)[1]][find_king(color,check_board)[0]]=0
        if check_state(color,check_board):
            return False
        else:
            check_board = [row[:] for row in board]
    return True


def main():
    """
    Main loop runs the program
    :return:
    """
    draw_bg()
    global moves
    global current_piece
    global en_passant
    global en_passant_capture
    global board
    global temp_board
    global turn
    global castle
    run = True
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if pygame.mouse.get_pressed()[0]:
                """ A click will be checked in this order of priority:
                1. If it is a friendly piece, show moves and stores the piece in current_piece and moves
                2. If the click is in moves, the piece will move there
                3. If the click is in nowhere, current_piece, moves and en_passant are reset.
                4. If piece moved was a castleable piece, remove its pos from castle"""
                if click(pygame.mouse.get_pos()):
                    tile = click(pygame.mouse.get_pos())    # returns (x,y) for the tile clicked if a pos within board is clicked
                    if is_piece(tile,board) and turn[0] in is_piece(tile,board):  # if (x,y) tile has a piece on it, shows the possible moves for the piece on tile
                        show_moves(is_piece(tile,board),tile,board)

                    elif tile in moves:
                        """ Use a temporary board to store the information
                        If the move is illegal, the changes to the board will not be carried out
                        Current piece and moves will stay the same, tiles will still be highlighted, en-passant
                        will still be active"""
                        temp_board=[row[:] for row in board]
                        """Checking to see if an en-passant capture has occured, and then see if piece moving
                        there is a pawn"""
                        if en_passant_capture:
                            if tile[0]==en_passant_capture[0] and tile[1]==en_passant_capture[1]:
                                if turn[0]=='W':
                                    temp_board[tile[1]+1][tile[0]]=0
                                else:
                                    temp_board[tile[1]-1][tile[0]] = 0
                        """  Check if castling has occured and move pieces accordingly"""
                        if 'k' in current_piece[0] and abs(tile[0]-current_piece[1])==2:
                            rook_castle=current_piece[1]-tile[0]    # this indicates the direction the rook should move
                            if rook_castle>0:
                                temp_board[tile[1]][tile[0]+1]=turn[0]+'r'
                                temp_board[tile[1]][0]=0
                            if rook_castle<0:
                                temp_board[tile[1]][tile[0]-1]=turn[0]+'r'
                                temp_board[tile[1]][7]=0

                        temp_board[current_piece[2]][current_piece[1]]=0
                        temp_board[tile[1]][tile[0]]=current_piece[0]


                        if check_state(turn[0],temp_board):
                            """ If pawn moved forward 2 places, it is susceptible to en-passant, and the piece is
                            reflected in the en_passant variable. When a pawn from the opposing team is clicked while
                            en_passant has a variable, the pawn checks its left and right for the presence of 
                            that pawn, and adds it to eat_moves if the pawn is in those tiles"""
                            if abs(current_piece[2] - tile[1]) == 2:
                                en_passant = [tile[0], tile[1]]
                            else:
                                en_passant = []
                            """ Remove castle piece from castle if moved"""
                            if (current_piece[1], current_piece[2]) in castle:
                                castle.remove((current_piece[1], current_piece[2]))
                            if 'Wp' in temp_board[0]:
                                while True:
                                    white_queen = pygame.image.load(os.path.join("Assets", 'white_queen.png'))
                                    white_rook = pygame.image.load(os.path.join("Assets", 'white_rook.png'))
                                    white_bishop = pygame.image.load(os.path.join("Assets", 'white_bishop.png'))
                                    white_knight = pygame.image.load(os.path.join("Assets", 'white_knight.png'))
                                    promotion_img=[white_queen,white_rook,white_bishop,white_knight]
                                    for i,img in enumerate(promotion_img):
                                        img=pygame.transform.scale(img,(int(abs(win_width*0.14)),int(abs(win_width*0.14))))
                                        pygame.draw.rect(win, (255, 255, 255), (abs(win_width*0.16+i*0.18*win_width),abs((win_height-win_width*0.14)/2),int(abs(win_width*0.14)),int(abs(win_width*0.14))))
                                        pygame.draw.rect(win, (0, 0, 0), (abs(win_width*0.16+i*0.18*win_width),abs((win_height-win_width*0.14)/2),int(abs(win_width*0.14)),int(abs(win_width*0.14))),2)
                                        win.blit(img,(abs(win_width*0.16+i*0.18*win_width),abs((win_height-win_width*0.14)/2)))

                                    pygame.display.update()
                            board=[row[:] for row in temp_board]
                            current_piece=''
                            moves=[]
                            draw_bg()
                            change_turn()
                            if not check_state(turn[0],temp_board):
                                if check_for_checkmate(turn[0]):
                                    draw(board)
                                    pygame.display.update()
                                    font=pygame.font.Font('freesansbold.ttf',32)
                                    if turn[0]=='W':
                                        text=font.render('Checkmate! Black wins!',True,(0,0,0),(255,255,255))
                                    else:
                                        text=font.render('Checkmate! White wins!',True,(0,0,0),(255,255,255))
                                    text_rect=text.get_rect()
                                    text_rect.center=(win_width//2,win_height//2)
                                    win.blit(text,text_rect)
                                    pygame.display.update()
                                    asking=True
                                    while asking:
                                        answer=input("Play again?\nType y or n: ")
                                        if answer=='y':
                                            asking=False
                                            board=[['Br','Bh','Bb','Bq','Bk','Bb','Bh','Br'],
                                                    ['Bp','Bp','Bp','Bp','Bp','Bp','Bp','Bp'],
                                                    [0,0,0,0,0,0,0,0],
                                                    [0,0,0,0,0,0,0,0],
                                                    [0,0,0,0,0,0,0,0],
                                                    [0,0,0,0,0,0,0,0],
                                                    ['Wp','Wp','Wp','Wp','Wp','Wp','Wp','Wp'],
                                                    ['Wr','Wh','Wb','Wq','Wk','Wb','Wh','Wr']]
                                            moves = []
                                            current_piece = ""
                                            turn = ['W', 'B']
                                            en_passant = []
                                            en_passant_capture = []
                                            castle = [(0, 0), (4, 0), (7, 0), (0, 7), (4, 7), (7, 7)]
                                            temp_board = [row[:] for row in board]
                                            main()
                                        if answer=='n':
                                            asking=False
                                            pygame.quit()
                                            quit()

                        else:
                            temp_board=[row[:] for row in board]


                    else:
                        draw_bg()
                        moves=[]
                        current_piece=''


        draw(board)
        pygame.display.update()

main()

