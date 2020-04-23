import itertools


board = []
for n in range(10):
    board.append(["O"]*10)

num = []
testnumerals = []
for n in range(1,11):
    testnumerals.append(str(n))
for n in range(1,10):
    num.append(str(n))
num.append("X")
num.insert(0," ")
board.insert(0,num)

alpha = []

for i in range(ord("A"),ord("K")):
    alpha.append(chr(i))
    
for i in alpha:
    board[alpha.index(i)+1].insert(0,i)

    
board[5][3]=" "
board[5][4]=" "
board[5][7]=" "
board[5][8]=" "
board[6][3]=" "
board[6][4]=" "
board[6][7]=" "
board[6][8]=" "




pieces = []
display = []
one=[]
two=[]
tock = 0

def custom_print(board):
    global tock
    print(tock)
    temp_board=[]
    for row in board:
        temp_board.append([])
        y = -1
        if tock == 2:
            for item in row:
                x = board.index(row)
                y = y + 1
                if (x,y) in one:
                    temp_board[-1].append("X")
                else:
                    temp_board[-1].append(item)
        elif tock == 1:
            for item in row:
                x = board.index(row)
                y = y + 1
                if (x,y) in two:
                    temp_board[-1].append("X")     
                else:
                    temp_board[-1].append(item)
        else:
            for item in row:
                temp_board[-1].append(item)                            
    for row in temp_board:            
        print(" ".join(row))
    

def stock_piece(qual,quant):
    pieces.append([qual]*quant)


stock_piece("#",1)
stock_piece("B",6)
stock_piece("S",1)
stock_piece(9,8)
stock_piece(8,5)
stock_piece(7,4)
stock_piece(6,4)
stock_piece(5,4)
stock_piece(4,3)
stock_piece(3,2)
stock_piece(2,1)
stock_piece(1,1)

def stock_chest():
    for piece in pieces:
        if isinstance(piece[0],int)==True:
            for i in piece:
               display.append(str(i))
        else:
            for i in piece:
                display.append(i)
stock_chest()

def display_print(lst):
    for x in (lst[i:i + 20] for i in range(0, len(lst), 20)):
        print(" ".join(x))
def P1P2 (player):
    print("Player" + str(player))
    
def stamp(letter,number):
    
    if tock == 1:
        one.append((letter,number))
    elif tock == 2:
        two.append((letter,number))
        
    

print()
display_print(display)    
def place(piece,letter,number):
    if piece in display:
        display.remove(piece)
        for row in board:
            if row[0]==letter:
                if row[number]=="O":
                    row[number]=piece
                    f = board.index(row)
                    g = int(number)
                    if tock == 1:
                            one.append((f,g))
                    elif tock == 2:
                        two.append((f,g))
        
                    
                              
    else:
        print()
        print("None left! Try again")
        
print()        
def set_board (player):
    global tock
    tock = player           
    custom_print(board)
    while display != []:     
        P1P2(player)
        print()
        piece = input("Piece:")
        print() 
        while (piece not in display):
            print("Whoops! Piece not found. Try again.")
            print()
            piece = input("Piece:")
            print()
        if piece in display:
            letter = input("Row:")
            print()

            if tock == 1:
                while (letter not in alpha[:4]):
                    print("Invalid Row! Try again.")
                    letter = input("Row:")
                    print()      
                if letter in alpha[:4]:
                        number = input("Column:")
                        print()
                        while number not in testnumerals:
                            print("Column not found! Try again.")
                            print()
                            number = input("Column:")
                            print()
                        if int(number) in range(0,11):
                            if board[alpha.index(letter)+1][int(number)]=="O":
                                place(piece,letter,int(number))
                                stamp(letter,int(number))
                                custom_print(board)
                                print()
                                display_print(display)
                                print()
                                if display ==[]:
                                    print("Done!")
                            else:
                                print("Space Occupied! Try Again")
            elif tock == 2:
                while (letter not in alpha[6:]):
                    print("Invalid Row! Try again.")
                    letter = input("Row:")
                    print()
                if letter in alpha[6:]:
                        number = input("Column:")
                        print()
                        while number not in testnumerals:
                            print("Column not found! Try again.")
                            print()
                            number = input("Column:")
                            print()
                        if number in testnumerals:
                            if board[alpha.index(letter)+1][int(number)]=="O":
                                place(piece,letter,int(number))
                                stamp(letter,int(number))
                                custom_print(board)
                                print()
                                display_print(display)
                                print()
                                if display ==[]:
                                    print("Done!")
                            else:
                                print("Space Occupied! Try Again")
            

#set_board(1)                  
#stock_chest()  #reset board and lists
#print()
#custom_print(board)
#print()
#display_print(display)
#print()
#set_board(2)  #Player 2 setup
print(display)
tock = 1
for row in board[1:5]:
    for thing in row[1:]:
        place(display[0],row[0],row.index(thing))
        
stock_chest()        
tock = 2
for row in board[7:]:
    for thing in row[1:]:
        place(display[0],row[0],row.index(thing))
        
        






def turn(player):
    global tock
    P1P2(player)
    tock = player
    if tock == 1:
        tocklist = one
    elif tock == 2:
        tocklist = two



                        


    custom_print(board)
    

    def input_checks():
        def invalid():
            print("Invalid Move\n")
        valid = False

        def win():
            board[startrow][startcolumn] = "O"
            stamp(endrow,endcolumn)
            if tock == 1:
                one.remove((startrow,startcolumn))
            elif tock == 2:
                two.remove((startrow,startcolumn))
            board[endrow][endcolumn] = YourPiece
        def lose():
            board[startrow][startcolumn] = "O"
            if tock == 1:
                one.remove((startrow,startcolumn))
            elif tock == 2:
                two.remove((startrow,startcolumn))
        def tie():
            board[startrow][startcolumn] = "O"
            if tock == 1:
                one.remove((startrow,startcolumn))
            elif tock == 2:
                two.remove((startrow,startcolumn))
            board[endrow][endcolumn] = "O"
            if tock == 1:
                one.remove((startrow,startcolumn))
            elif tock == 2:
                two.remove((startrow,startcolumn))
        print("Piece\n")
        startrow = input("Row:")
        print()
        while startrow not in alpha:
            print("Invalid Row! Try again.")
            startrow = input("Row:")
            print()
        if startrow in alpha:
            startcolumn = input("Column:")
            print()
            while startcolumn not in testnumerals:
                print("Column not found! Try again.")
                print()
                startcolumn = input("Column:")
                print()
            if startcolumn in testnumerals:
                startrow = alpha.index(startrow)+1
                startcolumn = int(startcolumn)
                YourPiece = board[startrow][startcolumn]
                while YourPiece == "B" or YourPiece == "#" or (startrow,startcolumn) not in tocklist:
                    print("Invalid move! Try again.")
                    print()
                    print("Piece\n")
                    startrow = input("Row:")
                    print()
                    while startrow not in alpha:
                        print("Invalid Row! Try again.")
                        startrow = input("Row:")
                        print()
                    if startrow in alpha:
                        startcolumn = input("Column:")
                        print()
                        while startcolumn not in testnumerals:
                            print("Column not found! Try again.")
                            print()
                            startcolumn = input("Column:")
                            print()
                        if startcolumn in testnumerals:
                            startrow = alpha.index(startrow)+1
                            startcolumn = int(startcolumn)
                            YourPiece = board[startrow][startcolumn]
                if YourPiece != "B" and YourPiece != "#" and (startrow,startcolumn) in tocklist :
                    print("Destination:\n")
                    endrow = input("Row:")
                    print()
                    while endrow not in alpha:
                        print("Invalid Row! Try again.")
                        endrow = input("Row:")
                        print()
                    if endrow in alpha:
                        endcolumn = input("Column:")
                        print()
                        while endcolumn not in testnumerals:
                            print("Column not found! Try again.")
                            print()
                            endcolumn = input("Column:")
                            print()
                        if endcolumn in testnumerals:
                            endrow = alpha.index(endrow)+1
                            endcolumn = int(endcolumn)
                            TheirPiece = board[endrow][endcolumn]
                            while (endrow,endcolumn) in tocklist:
                                print("That's your piece! Try again")
                                print("Piece\n")
                                startrow = input("Row:")
                                print()
                                while startrow not in alpha:
                                    print("Invalid Row! Try again.")
                                    startrow = input("Row:")
                                    print()
                                if startrow in alpha:
                                    startcolumn = input("Column:")
                                    print()
                                    while startcolumn not in testnumerals:
                                        print("Column not found! Try again.")
                                        print()
                                        startcolumn = input("Column:")
                                        print()
                                    if startcolumn in testnumerals:
                                        startrow = alpha.index(startrow)+1
                                        startcolumn = int(startcolumn)
                                        YourPiece = board[startrow][startcolumn]
                                        while YourPiece == "B" or YourPiece == "#" or (startrow,startcolumn) not in tocklist:
                                            print("Invalid move! Try again.")
                                            print()
                                            print("Piece\n")
                                            startrow = input("Row:")
                                            print()
                                            while startrow not in alpha:
                                                print("Invalid Row! Try again.")
                                                startrow = input("Row:")
                                                print()
                                            if startrow in alpha:
                                                startcolumn = input("Column:")
                                                print()
                                                while startcolumn not in testnumerals:
                                                    print("Column not found! Try again.")
                                                    print()
                                                    startcolumn = input("Column:")
                                                    print()
                                                if startcolumn in testnumerals:
                                                    startrow = alpha.index(startrow)+1
                                                    startcolumn = int(startcolumn)
                                                    YourPiece = board[startrow][startcolumn]
                                        if YourPiece != "B" and YourPiece != "#" and (startrow,startcolumn) in tocklist :
                                            print("Destination:\n")
                                            endrow = input("Row:")
                                            print()
                                            while endrow not in alpha:
                                                print("Invalid Row! Try again.")
                                                endrow = input("Row:")
                                                print()
                                            if endrow in alpha:
                                                endcolumn = input("Column:")
                                                print()
                                                while endcolumn not in testnumerals:
                                                    print("Column not found! Try again.")
                                                    print()
                                                    number = input("Column:")
                                                    print()
                                                if endcolumn in testnumerals:
                                                    endrow = alpha.index(endrow)+1
                                                    endcolumn = int(endcolumn)
                                                    TheirPiece = board[endrow][endcolumn]
                            if (endrow,endcolumn) not in tocklist:
                                if YourPiece == "9":
                                    print("Nine recognized")
                                    if (endcolumn == startcolumn):
                                        print("Columns recognized")
                                        bs=[]
                                        if startrow < endrow:
                                            x = startrow+1
                                            y = endrow
                                        elif endrow < startrow:
                                            x = endrow+1
                                            y = startrow
                                        for row in board[x:y]:
                                            if row[startcolumn]== "O":
                                                bs.append("X")
                                                print ("X Appended")
                                            else:
                                                invalid()
                                                print("not reading zeroes")
                                        if len(bs) == len(board[x:y]):
                                            if TheirPiece == "O":
                                                win()
                                                valid = True
                                        

                                            else:
                                                if TheirPiece == "S":
                                                    win()
                                                    valid = True
                                                elif TheirPiece == YourPiece:
                                                    tie()
                                                    valid = True
                                                elif TheirPiece == "B":
                                                    lose()
                                                    valid = True
                                                elif TheirPiece == "#":
                                                    win()
                                                    valid = True
                                                else:
                                                    if int(YourPiece) > int(TheirPiece):
                                                        lose()
                                                        valid = True
                                        else:
                                            print("wrong length")
                                    elif (endrow == startrow):
                                        print("rows recognized")
                                        crap = []
                                        if startcolumn < endcolumn:
                                            x = startcolumn+1
                                            y = endcolumn
                                        elif endcolumn < startcolumn:
                                            x = endcolumn+1
                                            y = startcolumn
                                        for stuff in board[startrow][x:y]:
                                            if stuff == "O":
                                                crap.append("X")
                                                print("X Appended")
                                        if len(crap) == len(board[startrow][x:y]):
                                            print("Length equal")
                                            if TheirPiece == "O":
                                                win()
                                                valid = True
                                            else:
                                                if TheirPiece == "S":
                                                    win()
                                                    valid = True
                                                elif TheirPiece == YourPiece:
                                                    tie()
                                                    valid = True
                                                elif TheirPiece == "B":
                                                    lose()
                                                    valid = True
                                                elif TheirPiece == "#":
                                                    win()
                                                    valid = True
                                                else:
                                                    if int(YourPiece) > int(TheirPiece):
                                                        lose()
                                                        valid = True
                                        else:
                                            invalid()
                                            print("list length")
                                    else:
                                        invalid()
                                        print("input issues")
                                elif YourPiece == "8":
                                                if ((startrow == endrow - 1 or startrow == endrow + 1) and startcolumn == endcolumn) or ((startcolumn == endcolumn - 1 or startcolumn == endcolumn + 1) and startrow == endrow):
                                                        if TheirPiece == "O":
                                                            win()
                                                            valid = True
                                                        else:
                                                            if TheirPiece == "B" or TheirPiece == "S":
                                                                win()
                                                                valid = True
                                                            elif TheirPiece == YourPiece:
                                                                tie()
                                                                valid = True
                                                            elif TheirPiece == "#":
                                                                win()
                                                                valid = True
                                                            else:
                                                                if int(TheirPiece) < int(YourPiece):
                                                                    lose()
                                                                    valid = True
                                                                elif int(TheirPiece) > int(YourPiece): 
                                                                    win()
                                                                    valid = True
                                                else:
                                                    invalid()
                                elif YourPiece == "S":
                                                if ((startrow == endrow - 1 or startrow == endrow + 1) and startcolumn == endcolumn) or ((startcolumn == endcolumn - 1 or startcolumn == endcolumn + 1) and startrow == endrow):
                                                    if TheirPiece == "O":
                                                        win()
                                                        valid = True
                                                    else:
                                                        if TheirPiece == YourPiece:
                                                            tie()
                                                            valid = True
                                                        if TheirPiece == "1":
                                                            win()
                                                            valid = True
                                                        elif TheirPiece == "#":
                                                            win()
                                                            valid = True
                                                        else:
                                                            lose()
                                                            valid = True
                                                else:
                                                    invalid()
                                elif YourPiece == "1":
                                                if ((startrow == endrow - 1 or startrow == endrow + 1) and startcolumn == endcolumn) or ((startcolumn == endcolumn - 1 or startcolumn == endcolumn + 1) and startrow == endrow):        
                                                    if TheirPiece == "O":
                                                        win()
                                                        valid = True
                                                    else:
                                                        if TheirPiece == "S" or TheirPiece == "B":
                                                            lose()
                                                            valid = True
                                                        elif TheirPiece == YourPiece:
                                                            tie()
                                                            valid = True
                                                        elif TheirPiece == "#":
                                                            win()
                                                            valid = True
                                                        else:
                                                            win()
                                                            valid = True
                                                else:
                                                    invalid()    
                                else:               
                                    if ((startrow == endrow - 1 or startrow == endrow + 1) and startcolumn == endcolumn) or ((startcolumn == endcolumn - 1 or startcolumn == endcolumn + 1) and startrow == endrow):
                                            if TheirPiece == "O":
                                                win()
                                                valid = True
                                            else:
                                                if TheirPiece == "B":
                                                    lose()
                                                    valid = True
                                                elif TheirPiece == YourPiece:
                                                    tie()
                                                    valid = True
                                                elif TheirPiece == "#":
                                                    win()
                                                    valid = True
                                                else:
                                                    if int(TheirPiece) > int(YourPiece):
                                                        win()
                                                        valid = True
                                                    elif int(TheirPiece) < int(YourPiece):
                                                        lose()
                                                        valid = True
                                    else:
                                        invalid()
                                        print("Complicated")
        print(valid)
        if valid != True:
            input_checks()
        
    
    input_checks()
    
    

                            
    
    

while ("#" in board[1] or "#" in board[2] or "#" in board[3] or "#" in board[4]) and ("#" in board[7] or "#" in board[8] or "#" in board[9] or "#" in board[10]):
    turn(1)
    if "#" in board[7] or "#" in board[8] or "#" in board[9] or "#" in board[10]:
        turn(2)
        
    
if "#" in board[1] or "#" in board[2] or "#" in board[3] or "#" in board[4]:
    print("Player 1 Wins!")
else:
    print("Player 2 Wins!")



    

      
