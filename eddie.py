#MASON HARLAN ID63263805
#ASSIGNMENT 6
from graphics import *
from time import sleep
import random

WIDTH = 32
NUM_H_TILES = 17
NUM_V_TILES = 15

SNAKE_BLUE = color_rgb(78,124,246)
UCI_BLUE = color_rgb(0, 100, 164)
WALL_GREEN = color_rgb(87,138,52)
BOARD_GREEN1 = color_rgb(170,215,81)
BOARD_GREEN2 = color_rgb(162,209,73)

INIT_APPLE_COORD = (13,8)
INIT_SNAKE_COORD = ((5,8),(4,8),(3,8))
INIT_DIRECTION = (1,0)
def drawBackground(win):
    for h in range(NUM_H_TILES+2):      # Repeat coordinates along the horizontal direction
        for v in range(NUM_V_TILES+2):  # Repeat coordinates along for the vertical direction
            r = Rectangle(Point(h*WIDTH, v*WIDTH), Point((h+1)*WIDTH, (v+1)*WIDTH))  # Create a rectangle with the pixels converted from the coordinates
            r.setWidth(0)               # Clear the border of rectangle
            # If the coordinate is located at the wall, fill with the colr WALL_GREEN
            if h == 0 or v == 0 or h == NUM_H_TILES+2-1 or v == NUM_V_TILES+2-1:
                r.setFill(WALL_GREEN)
            elif (h + v) % 2 == 0:
                r.setFill(BOARD_GREEN1) # If it is one of the chessboard with the even sum of its two coordintaes, fill with the color BOAD_GREEN1
            else:
                r.setFill(BOARD_GREEN2) # Otherwise, fill with the color BOARD_GREEN2
            r.draw(win)
def drawSnake(win, snake_coords):
    snake = []
    for i in range(len(snake_coords)):  # Snake is composed of rectangles using pixels converted from the coordinates
        cr = Rectangle(Point(snake_coords[i][0]*WIDTH, snake_coords[i][1]*WIDTH),
            Point((snake_coords[i][0]+1)*WIDTH, (snake_coords[i][1]+1)*WIDTH))
        cr.setWidth(0)
        cr.draw(win)
        if i == 0: cr.setFill(UCI_BLUE) # The head is UCI_BLUE
        else: cr.setFill(SNAKE_BLUE)    # The body is SNAKE_BLUE
        snake.append(cr) # Note that the list of snake rectangles starts from the head to the tail

    return snake
def drawReplay(win, score, highscore):
    screen_width = WIDTH*(NUM_H_TILES+2)
    screen_height = WIDTH*(NUM_V_TILES+2)
    black_bg = Rectangle(Point(0, 0), Point(screen_width, screen_height))
    black_bg.setWidth(0)
    black_bg.setFill("black")
    black_bg.draw(win)  # Draw the black background

    white_sb = Rectangle(Point(0.25*screen_width, 0.20*screen_height), Point(0.75*screen_width, 0.60*screen_height))
    white_sb.setWidth(0)
    white_sb.setFill("white")
    white_sb.draw(win)  # Draw the white score backgraound

    img = Image(Point(0.5*screen_width, 0.35*screen_height), "apple_32.gif")
    img.draw(win)       # Draw the apple icon

    st = Text(Point(0.5*screen_width, 0.45*screen_height), str(score))
    st.draw(win)        # Draw the score text above the score background
    hst = Text(Point(0.5*screen_width, 0.5*screen_height), ("Highscore:", str(highscore)))
    hst.draw(win)
    btn = Rectangle(Point(0.25*screen_width, 0.60*screen_height), Point(0.75*screen_width, 0.80*screen_height))
    btn.setWidth(0)
    btn.setFill(UCI_BLUE)
    btn.draw(win)       # Draw the butoon next to the score

    btn_text = Text(Point(0.5*screen_width, 0.70*screen_height), "Play Again")
    btn_text.setTextColor("white")
    btn_text.draw(win)  # Draw the text on the button

    return [black_bg, white_sb, img, hst, st, btn, btn_text] # [-2] is the button and [-3] is the score text

def handleKey(k,  direction, win):
    if k == "Up" and  direction != (0,1):      # It is not feasible for snake to go UP while it is going down
        return (0,-1)
    elif k == "Down" and  direction != (0,-1): # It is not feasible for snake to go DOWN while it is going up
        return (0,1)
    elif k == "Right" and  direction != (-1,0):# It is not feasible for snake to go RIGHT while it is going left
        return (1,0)
    elif k == "Left"  and  direction != (1,0): # It is not feasible for snake to go LEFT while it is going right
        return (-1,0)
    else:
        return direction # Don't change the direction if all above tests fail
    
def findEmptySpace(snake, apple_coord):
    coords = [apple_coord]
    for s in snake: # Create a list of occupied coordinates (apple + snake)
        coords.append((s.getP1().x // WIDTH, s.getP1().y // WIDTH))

    table = [] # Find all pairs of unoccupied coordinates
    for i in range(1, NUM_H_TILES+1):
        for j in range(1, NUM_V_TILES+1):
            if (i, j) not in coords:
                table.append((i,j))

    return random.choice(table) # Random pick one from unoccupied ones

def moveSnake(snake, direct):
    # Move the head rectangle of the snake using the offset from direction
    dx, dy = direct
    head = snake[0]
    old_head_point = head.getP1()
    head.move(dx*WIDTH,dy*WIDTH)
    tail = snake.pop()
    tailpoint= tail.getP1()
    tail.move(old_head_point.getX() - tailpoint.getX(), old_head_point.getY() - tailpoint.getY())
    snake.insert(1,tail)
    # Move the tail rectangle of the snake to the old (x, y) of the head rectangle

    # Remove the tail rectangle and insert to be the second position "neck" of the snake list
def growSnake(win, snake):
    # Copy the tail rectangle of the snake, draw it, and append it to the end of the list of snake rectangle
    tail = snake[-1].clone()
    snake.append(tail)
    snake[-1].draw(win)  
def isGameOver(snake):
    head = snake[0]
    headpoint = head.getP1()
    body = snake[1:]
    # For each of the body pixel location, test if the head pixel location is equal to it. Return True if anyone matches
    for r in body:
        px, py = r.getP1().x//WIDTH, r.getP1().y//WIDTH
        if px == headpoint.x//WIDTH and py == headpoint.y//WIDTH:
            return True
        if px == 0 or px == NUM_H_TILES+1 or py == 0 or py == NUM_V_TILES+1:
            return True

    return False
def main():
    window = GraphWin("Snake", WIDTH*(NUM_H_TILES+2), WIDTH*(NUM_V_TILES+2))

    drawBackground(window)
    apple_coord = INIT_APPLE_COORD

    apple = Image(Point((apple_coord[0]+0.5)*WIDTH, (apple_coord[1]+0.5)*WIDTH), "apple_32.gif")
    apple.draw(window)

    snake = drawSnake(window, list(INIT_SNAKE_COORD))
    direction = INIT_DIRECTION
    counter1 = 0
    score = 0
    bruh = Text(Point(0.5*WIDTH*(NUM_H_TILES+2), 0.03*WIDTH*(NUM_V_TILES+2)), str(score))
    bruh.draw(window)
    highscore = 0
    interval = 10
    while True:

        key = window.checkKey()              # Get the key
        d = handleKey(key , direction, window)   # Check if the direction has changed by calling handleKey()

        # Test if the direction change or time is up with counter1 equals to 125
        if d != direction or counter1 >= interval :
            # Make the new direction to replace the old direction
            direction = d
            # Move the snake
            moveSnake(snake,direction)
            # Reset counter1
            counter1 = 0
        if score > highscore:
            highscore = score
        if isGameOver(snake):
            replay_screen = drawReplay(window,score, highscore)
            while True:
                pt = window.getMouse()# Get the mouse Point
                button = replay_screen[-2]# Find the button
                p1, p2 = button.getP1(), button.getP2()
                if pt.x > p1.x and pt.y > p1.y and pt.x < p2.x and pt.y < p2.y:
                    for i in replay_screen:
                        i.undraw()
                    break
            sleep(2)            
            apple.move((INIT_APPLE_COORD[0]-apple_coord[0])*WIDTH,(INIT_APPLE_COORD[1]-apple_coord[1])*WIDTH)
            apple_coord=INIT_APPLE_COORD
            for i in snake:
                i.undraw()
            snake = drawSnake(window, list(INIT_SNAKE_COORD))
            direction = INIT_DIRECTION
            counter1 = 0
            score = 0
            bruh.setText(score)
            interval = 10
            
        if (snake[0].getP1().x)//WIDTH == apple_coord[0] and (snake[0].getP1().y)//WIDTH == apple_coord[1]:
            new_coord = findEmptySpace(snake,apple_coord)
            apple.move((new_coord[0]-apple_coord[0])*WIDTH,(new_coord[1]-apple_coord[1])*WIDTH)
            apple_coord = new_coord
            growSnake(window,snake)
            if interval > 7:
                interval = interval-.25
            score += 1
            bruh.setText(score)
        window.flush()
        counter1 += 1
        sleep(.01)
main()
high_score = 49
