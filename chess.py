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

def is_piece(tile):
    """Returns the piece currently sitting on the tile given
    If out of bounds, will return "OOB"
    If in between lines, will return "Line" """
    if tile == 1:
        return 0
    elif -1<tile[0]<8 and -1<tile[1]<8:
        return board[abs(tile[1])][abs(tile[0])]
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




def show_moves(piece,tile,highlight=True):
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
            if is_piece((x+i+1,y)) or is_piece((x+i+1,y))=="OUT":
                if turn[1] in is_piece((x+i+1,y)):
                    eat_moves.append((x+i+1,y))
                break
            else:
                moves.append((x+i+1,y))
        for i in range(8): # finds the squares the rook can move to on its left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y)) or is_piece((x-i-1,y))=="OUT":
                if turn[1] in is_piece((x-i-1,y)):
                    eat_moves.append((x-i-1,y))
                break
            else:
                moves.append((x-i-1,y))
        for i in range(8): # finds the squares the rook can move to down
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y+i+1)) or is_piece((x,y+i+1))=="OUT":
                if turn[1] in is_piece((x,y+i+1)):
                    eat_moves.append((x,y+i+1))
                break
            else:
                moves.append((x,y+i+1))
        for i in range(8): # finds the squares the rook can move to up
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y-i-1)) or is_piece((x,y-i-1))=="OUT":
                if turn[1] in is_piece((x,y-i-1)):
                    eat_moves.append((x,y-i-1))
                break
            else:
                moves.append((x,y-i-1))

    if piece=='Wh' or piece=='Bh':  # return a list of moves the rook can take on its tile
        """ Iterate through possible knight moves in a clockwise sequence"""

        if is_piece((x+1,y-2)) or is_piece((x+1,y-2))=='OUT':   # top right 1
            if turn[1] in is_piece((x+1,y-2)):
                eat_moves.append((x+1,y-2))
        else:
            moves.append((x+1,y-2))

        if is_piece((x+2,y-1)) or is_piece((x+2,y-1))=='OUT':   # top right 2
            if turn[1] in is_piece((x+2,y-1)):
                eat_moves.append((x+2,y-1))
        else:
            moves.append((x+2,y-1))

        if is_piece((x+2,y+1)) or is_piece((x+2,y+1))=='OUT':   # bottom right 1
            if turn[1] in is_piece((x+2,y+1)):
                eat_moves.append((x+2,y+1))
        else:
            moves.append((x+2,y+1))

        if is_piece((x+1,y+2)) or is_piece((x+1,y+2))=='OUT':   # bottom right  2
            if turn[1] in is_piece((x+1,y+2)):
                eat_moves.append((x+1,y+2))
        else:
            moves.append((x+1,y+2))

        if is_piece((x-1,y+2)) or is_piece((x-1,y+2))=='OUT':   # bottom left 1
            if turn[1] in is_piece((x-1,y+2)):
                eat_moves.append((x-1,y+2))
        else:
            moves.append((x-1,y+2))

        if is_piece((x-2,y+1)) or is_piece((x-2,y+1))=='OUT':   # bottom left 2
            if turn[1] in is_piece((x-2,y+1)):
                eat_moves.append((x-2,y+1))
        else:
            moves.append((x-2,y+1))

        if is_piece((x-2,y-1)) or is_piece((x-2,y-1))=='OUT':   # top left 1
            if turn[1] in is_piece((x-2,y-1)):
                eat_moves.append((x-2,y-1))
        else:
            moves.append((x-2,y-1))

        if is_piece((x-1,y-2)) or is_piece((x-1,y-2))=='OUT':   # top left 2
            if turn[1] in is_piece((x-1,y-2)):
                eat_moves.append((x-1,y-2))
        else:
            moves.append((x-1,y-2))

    if piece=='Wb' or piece=='Bb':  # return a list of moves the rook can take on its tile

        for i in range(8):  # finds the squares the bishop can move bottom right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y+i+1)) or is_piece((x+i+1,y+i+1))=="OUT":
                if turn[1] in is_piece((x+i+1,y+i+1)):
                    eat_moves.append((x+i+1,y+i+1))
                break
            else:
                moves.append((x+i+1,y+i+1))

        for i in range(8): # finds the squares the bishop can move bottom left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y+i+1)) or is_piece((x-i-1,y+i+1))=="OUT":
                if turn[1] in is_piece((x-i-1,y+i+1)):
                    eat_moves.append((x-i-1,y+i+1))
                break
            else:
                moves.append((x-i-1,y+i+1))

        for i in range(8): # finds the squares the bishop can move top left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y-i-1)) or is_piece((x-i-1,y-i-1))=="OUT":
                if turn[1] in is_piece((x-i-1,y-i-1)):
                    eat_moves.append((x-i-1,y-i-1))
                break
            else:
                moves.append((x-i-1,y-i-1))

        for i in range(8): # finds the squares the bishop can move top right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y-i-1)) or is_piece((x+i+1,y-i-1))=="OUT":
                if turn[1] in is_piece((x+i+1,y-i-1)):
                    eat_moves.append((x+i+1,y-i-1))
                break
            else:
                moves.append((x+i+1,y-i-1))

    if piece=='Wq' or piece=='Bq':  # return a list of moves the queen can take on its tile

        for i in range(8):  # finds the squares the bishop can move bottom right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y+i+1)) or is_piece((x+i+1,y+i+1))=="OUT":
                if turn[1] in is_piece((x+i+1,y+i+1)):
                    eat_moves.append((x+i+1,y+i+1))
                break
            else:
                moves.append((x+i+1,y+i+1))

        for i in range(8): # finds the squares the bishop can move bottom left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y+i+1)) or is_piece((x-i-1,y+i+1))=="OUT":
                if turn[1] in is_piece((x-i-1,y+i+1)):
                    eat_moves.append((x-i-1,y+i+1))
                break
            else:
                moves.append((x-i-1,y+i+1))

        for i in range(8): # finds the squares the bishop can move top left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y-i-1)) or is_piece((x-i-1,y-i-1))=="OUT":
                if turn[1] in is_piece((x-i-1,y-i-1)):
                    eat_moves.append((x-i-1,y-i-1))
                break
            else:
                moves.append((x-i-1,y-i-1))

        for i in range(8): # finds the squares the bishop can move top right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y-i-1)) or is_piece((x+i+1,y-i-1))=="OUT":
                if turn[1] in is_piece((x+i+1,y-i-1)):
                    eat_moves.append((x+i+1,y-i-1))
                break
            else:
                moves.append((x+i+1,y-i-1))
        for i in range(8):  # finds the squares the rook can move to on its right
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x+i+1,y)) or is_piece((x+i+1,y))=="OUT":
                if turn[1] in is_piece((x+i+1,y)):
                    eat_moves.append((x+i+1,y))
                break
            else:
                moves.append((x+i+1,y))
        for i in range(8): # finds the squares the rook can move to on its left
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x-i-1,y)) or is_piece((x-i-1,y))=="OUT":
                if turn[1] in is_piece((x-i-1,y)):
                    eat_moves.append((x-i-1,y))
                break
            else:
                moves.append((x-i-1,y))
        for i in range(8): # finds the squares the rook can move to down
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y+i+1)) or is_piece((x,y+i+1))=="OUT":
                if turn[1] in is_piece((x,y+i+1)):
                    eat_moves.append((x,y+i+1))
                break
            else:
                moves.append((x,y+i+1))

        for i in range(8): # finds the squares the rook can move to up
            """If the piece hits another piece or hits the end, break loop
            If piece hit is not friendly, append to eat_moves"""
            if is_piece((x,y-i-1)) or is_piece((x,y-i-1))=="OUT":
                if turn[1] in is_piece((x,y-i-1)):
                    eat_moves.append((x,y-i-1))
                break
            else:
                moves.append((x,y-i-1))

    if piece == 'Wk' or piece == 'Bk':  # return a list of moves the king can take on its tile, starting clockwise

        if is_piece((x,y-1)) or is_piece((x,y-1)) == "OUT":
            if turn[1] in is_piece((x,y-1)):
                eat_moves.append((x,y-1))
        else:
            moves.append((x,y-1))

        if is_piece((x+1,y-1)) or is_piece((x+1,y-1)) == "OUT":
            if turn[1] in is_piece((x+1,y-1)):
                eat_moves.append((x+1,y-1))
        else:
            moves.append((x+1,y-1))

        if is_piece((x+1,y)) or is_piece((x+1,y)) == "OUT":
            if turn[1] in is_piece((x+1,y)):
                eat_moves.append((x+1,y))
        else:
            moves.append((x+1,y))

        if is_piece((x+1,y+1)) or is_piece((x+1,y+1)) == "OUT":
            if turn[1] in is_piece((x+1,y+1)):
                eat_moves.append((x+1,y+1))
        else:
            moves.append((x+1,y+1))

        if is_piece((x,y+1)) or is_piece((x,y+1)) == "OUT":
            if turn[1] in is_piece((x,y+1)):
                eat_moves.append((x,y+1))
        else:
            moves.append((x,y+1))

        if is_piece((x-1,y+1)) or is_piece((x-1,y+1)) == "OUT":
            if turn[1] in is_piece((x-1,y+1)):
                eat_moves.append((x-1,y+1))
        else:
            moves.append((x-1,y+1))

        if is_piece((x-1,y)) or is_piece((x-1,y)) == "OUT":
            if turn[1] in is_piece((x-1,y)):
                eat_moves.append((x-1,y))
        else:
            moves.append((x-1,y))

        if is_piece((x-1,y-1)) or is_piece((x-1,y-1)) == "OUT":
            if turn[1] in is_piece((x-1,y-1)):
                eat_moves.append((x-1,y-1))
        else:
            moves.append((x-1,y-1))

        """ Check to see if king can castle by checking the squares between itself and the rook
        and checking to see if both itself and the rook are able to castle"""
        if piece=='Wk':
            if not is_piece((5,7)) and not is_piece((6,7)) and (7,7) in castle and (4,7) in castle:
                moves.append((x+2,y))
        if piece=='Wk':
            if not is_piece((1,7)) and not is_piece((2,7)) and not is_piece((3,7)) and (0,7) in castle and (4,7) in castle:
                moves.append((x-2,y))
        if piece=='Bk':
            if not is_piece((5,0)) and not is_piece((6,0)) and (7,0) in castle and (4,0) in castle:
                moves.append((x+2,y))
        if piece=='Bk':
            if not is_piece((1,0)) and not is_piece((2,0)) and not is_piece((3,0)) and (4,0) in castle and (0,0) in castle:
                moves.append((x-2,y))

    if piece == 'Wp':  # return a list of moves the white pawn can take on its tile
        """ If Wp at starting y-axis, allow it to travel 2 spaces if 2nd space is free"""
        if y == 6:
            if not is_piece((x,y-1)) and not is_piece((x,y-2)):
                moves.append((x,y-2))
        if not is_piece((x,y-1)):
            moves.append((x,y-1))
        """ Check diagonals for a capture"""
        if 'B' in str(is_piece((x-1,y-1))):
            eat_moves.append((x-1,y-1))
        if 'B' in str(is_piece((x+1,y-1))):
            eat_moves.append((x+1,y-1))
        """ Check for en-passant capture"""
        if 'Bp' in str(is_piece((x+1,y))) and en_passant==[x+1,y]:
            eat_moves.append((x+1,y-1))
            en_passant_capture=[x+1,y-1]
        if 'Bp' in str(is_piece((x-1,y))) and en_passant==[x-1,y]:
            eat_moves.append((x-1,y-1))
            en_passant_capture=[x-1,y-1]

    if piece == 'Bp':  # return a list of moves the black pawn can take on its tile
        """ If Bp at starting y-axis, allow it to travel 2 spaces if 2nd space is free"""
        if y == 1:
            if not is_piece((x,y+1)) and not is_piece((x,y+2)):
                moves.append((x,y+2))
        if not is_piece((x,y+1)):
            moves.append((x,y+1))
        """ Check diagonals for a capture"""
        if 'W' in str(is_piece((x-1,y+1))):
            eat_moves.append((x-1,y+1))
        if 'W' in str(is_piece((x+1,y+1))):
            eat_moves.append((x+1,y+1))
        """ Check for en-passant capture, and if capture is available, append to eat_moves and change
        en_passant_capture to match the capture tile"""
        if 'Wp' in str(is_piece((x+1,y))) and en_passant == [x+1,y]:
            eat_moves.append((x+1,y+1))
            en_passant_capture=[x+1,y+1]
        if 'Wp' in str(is_piece((x-1,y))) and en_passant == [x-1,y]:
            eat_moves.append((x-1,y+1))
            en_passant_capture=[x-1,y+1]

    draw_bg()
    if highlight:
        highlight_tile(moves)
        highlight_tile(eat_moves,(255,0,0))
    for move in eat_moves:
        moves.append(move)
    moves.append(1)
    return moves

def check_state(color):
    """ Checks the board state of the given team color, and return True if king is not threatened
    1. Iterate through each tile in the board to find the team's pieces
    2. Find the moves of that piece
    3. If the king is in the is_piece of one of those moves, return False"""
    for i,row in enumerate(board):
        for j,tile in enumerate(row):
            if color in str(tile):
                for move in show_moves(is_piece((j,i)),(j,i)):
                    if 'k' in str(is_piece(move)):
                        return False




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

    run = True
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if pygame.mouse.get_pressed()[0]:
                print(castle)
                """ A click will be checked in this order of priority:
                1. If it is a friendly piece, show moves and stores the piece in current_piece and moves
                2. If the click is in moves, the piece will move there
                3. If the click is in nowhere, current_piece, moves and en_passant are reset.
                4. If piece moved was a castleable piece, remove its pos from castle"""
                if click(pygame.mouse.get_pos()):
                    tile = click(pygame.mouse.get_pos())    # returns (x,y) for the tile clicked if a pos within board is clicked
                    if is_piece(tile) and turn[0] in is_piece(tile):  # if (x,y) tile has a piece on it, shows the possible moves for the piece on tile
                        show_moves(is_piece(tile),tile)
                    elif tile in moves:
                        """ If pawn moved forward 2 places, it is susceptible to en-passant, and the piece is
                        reflected in the en_passant variable. When a pawn from the opposing team is clicked while
                        en_passant has a variable, the pawn checks its left and right for the presence of 
                        that pawn, and adds it to eat_moves if the pawn is in those tiles"""
                        if abs(current_piece[2]-tile[1])==2:
                            en_passant=[tile[0],tile[1]]
                        else:
                            en_passant=[]
                        """Checking to see if an en-passant capture has occured, and then see if piece moving
                        there is a pawn"""
                        if en_passant_capture:
                            if tile[0]==en_passant_capture[0] and tile[1]==en_passant_capture[1]:
                                if turn[0]=='W':
                                    board[tile[1]+1][tile[0]]=0
                                else:
                                    board[tile[1]-1][tile[0]] = 0
                        if 'k' in current_piece[0] and abs(tile[0]-current_piece[1])==2:
                            rook_castle=current_piece[1]-tile[0]    # this indicates the direction the rook should move
                            if rook_castle>0:
                                board[tile[1]][tile[0]+1]=turn[0]+'r'
                                board[tile[1]][0]=0
                            if rook_castle<0:
                                board[tile[1]][tile[0]-1]=turn[0]+'r'
                                board[tile[1]][7]=0
                        print((current_piece[1],current_piece[2]))
                        if (current_piece[1],current_piece[2]) in castle:
                            castle.remove((current_piece[1],current_piece[2]))
                        board[current_piece[2]][current_piece[1]]=0
                        board[tile[1]][tile[0]]=current_piece[0]
                        current_piece=''
                        moves=[]
                        draw_bg()

                        change_turn()
                    else:
                        draw_bg()
                        moves=[]
                        current_piece=''

        draw(board)
        pygame.display.update()

main()


