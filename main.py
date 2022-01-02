# importing libraries
import turtle
import random
import time

# change to use ai or play the game as a user
USE_AI = True

class Stats:

    def __init__(self):
        pass

    @staticmethod
    def record_score(curr_score):
        if not curr_score:
            curr_score = 0

        print("write highscore")
        file = open("highscore.txt", "w+")
        file.write(str(curr_score))
        file.close()

    @staticmethod
    def read_score():
        try:
            file = open("highscore.txt", "r")
            curr_score = file.readline().strip()
            file.close()
        except Exception as e:
            print(e)
            return 0

        if curr_score:
            return int(curr_score)
        return 0

    @staticmethod
    def calc_avg(curr_score):
        file = open("avg.txt", "r")
        line = file.readline()
        file.close()

        data = line.split(",")

        num_items = int(data[1])
        avg = float(data[0])

        total = avg * num_items
        num_items += 1
        total = (total + curr_score) / num_items

        file = open("avg.txt", "w")
        file.write(str(total) + "," + str(num_items))
        file.close()


# creating turtle screen
screen = turtle.Screen()
screen.title('SNAKE GAME')
screen.setup(width=700, height=700)
screen.tracer(0)
turtle.bgcolor('turquoise')

##creating a border for our game

turtle.speed(5)
turtle.pensize(4)
turtle.penup()
turtle.goto(-310, 250)
turtle.pendown()
turtle.color('black')
turtle.forward(600)
turtle.right(90)
turtle.forward(500)
turtle.right(90)
turtle.forward(600)
turtle.right(90)
turtle.forward(500)
turtle.penup()
turtle.hideturtle()

stat = Stats()

# score
score = 0
delay = 0.1
high_score = stat.read_score()

# snake
snake = turtle.Turtle()
snake.speed(1)
snake.shape('square')
snake.color("black")
snake.penup()
snake.goto(0, 0)

if USE_AI:
    snake.direction = 'right'
else:
    snake.direction = 'stop'
snake.next_turn = [0, 0, 0, 0]

# food
fruit = turtle.Turtle()
fruit.speed(0)
fruit.shape('circle')
fruit.color('red')
fruit.penup()
fruit.goto(30, 30)

old_fruit = []
num_tries = 0

# scoring
scoring = turtle.Turtle()
scoring.speed(0)
scoring.color("black")
scoring.penup()
scoring.hideturtle()
scoring.goto(0, 300)
scoring.write("Score:0", align="center", font=("Courier", 24, "bold"))


def set_next_turn(i=None):
    j = 0
    for turn in snake.next_turn:
        snake.next_turn[j] = 0
        j += 1

    if i:
        snake.next_turn[i] = 1


def snake_go_up():
    print("going up")
    if snake.direction != "down":
        snake.direction = "up"


def snake_go_down():
    print("going down")
    if snake.direction != "up":
        snake.direction = "down"


def snake_go_left():
    print("going left")
    if snake.direction != "right":
        snake.direction = "left"


def snake_go_right():
    print("going right")
    if snake.direction != "left":
        snake.direction = "right"


def snake_move(old_fruit, new_fruit):
    if USE_AI:
        def go_left():
            if snake.direction != "right":
                print("Turn left")
                snake.direction = 'left'
                snake.setx(snake_x - 20)

        def go_right():
            if snake.direction != "left":
                print("turn right")
                snake.direction = 'right'
                snake.setx(snake_x + 20)

        def go_down():
            if snake.direction != "up":
                print("turn down")
                snake.direction = 'down'
                snake.sety(snake_y - 20)

        def go_up():
            if snake.direction != "down":
                print("turn up")
                snake.direction = 'up'
                snake.sety(snake_y + 20)

        def calc_optimal():
            f_x = new_fruit.xcor()
            f_y = new_fruit.ycor()
            s_x = snake.xcor()
            s_y = snake.ycor()

            if s_x > f_x:
                optimal_dir[0] = 1
            elif s_x < f_x:
                optimal_dir[1] = 1

            if s_y < f_y:
                optimal_dir[2] = 1
            elif s_y > f_y:
                optimal_dir[3] = 1

        def is_overlapping(fruit, snake, dir):
            s_top = snake.ycor() + 10
            s_bottom = snake.ycor() - 10
            s_right = snake.xcor() + 10
            s_left = snake.xcor() - 10

            try:
                f_top = fruit.top
                f_bottom = fruit.bottom
                f_left = fruit.left
                f_right = fruit.right
            except Exception as e:
                print(e)
                return True

            if dir == 0:
                if f_left <= s_left - 20 < f_right and s_top == f_top:
                    return True
            elif dir == 1:
                if f_right >= s_right + 20 > f_left and s_top == f_top:
                    return True
            elif dir == 2:
                if f_top >= s_top + 20 > f_bottom and s_right == f_right:
                    return True
            elif dir == 3:
                if f_bottom <= s_bottom - 20 < f_top and s_right == f_right:
                    return True

            return False

        print("New fruit x,y: " + str(new_fruit.xcor()) + ", " + str(new_fruit.ycor()))
        print("snake x,y: " + str(snake.xcor()) + ", " + str(snake.ycor()))

        # get coordinates
        snake_x = snake.xcor()
        snake_y = snake.ycor()
        fruit_x = new_fruit.xcor()
        fruit_y = new_fruit.ycor()
        snake_dir = snake.direction
        rnd_dir = random.randint(0, 10)
        tried = 0

        # left, right, up, down
        can_turn = [1, 1, 1, 1]
        optimal_dir = [0, 0, 0, 0]

        # find the optimal direction to go
        calc_optimal()

        # find if you can turn that direction
        for i, fruit in enumerate(old_fruit):
            for index, dir in enumerate(can_turn):
                if index == 0:
                    if snake.direction == 'right':
                        can_turn[index] = 0
                    elif is_overlapping(fruit, snake, 0):
                        can_turn[index] = 0
                    elif snake_x <= -300 + 10:
                        can_turn[index] = 0
                elif index == 1:
                    if snake.direction == 'left':
                        can_turn[index] = 0
                    elif is_overlapping(fruit, snake, 1):
                        can_turn[index] = 0
                    elif snake_x >= 280 - 10:
                        can_turn[index] = 0
                elif index == 2:
                    if snake.direction == 'down':
                        can_turn[index] = 0
                    elif is_overlapping(fruit, snake, 2):
                        can_turn[index] = 0
                    elif snake_y >= 240 - 10:
                        can_turn[index] = 0
                elif index == 3:
                    if snake.direction == 'up':
                        can_turn[index] = 0
                    elif is_overlapping(fruit, snake, 3):
                        can_turn[index] = 0
                    elif snake_y <= -240 + 10:
                        can_turn[index] = 0

        # check if there was a move from the previous round
        if num_tries != 2:
            if snake.next_turn[0] == 1 and can_turn[0] == 1:
                go_left()
                set_next_turn()
                return -1
            elif snake.next_turn[1] == 1 and can_turn[1] == 1:
                go_right()
                set_next_turn()
                return -1
            elif snake.next_turn[2] == 1 and can_turn[2] == 1:
                go_up()
                set_next_turn()
                return -1
            elif snake.next_turn[3] == 1 and can_turn[3] == 1:
                go_down()
                set_next_turn()
                return -1
        else:
            if can_turn[0] == 1:
                go_left()
                set_next_turn(0)
            elif can_turn[1] == 1:
                go_right()
                set_next_turn(1)
            elif can_turn[2] == 1:
                go_up()
                set_next_turn(2)
            elif can_turn[3] == 1:
                go_down()
                set_next_turn(3)
            return 1

        # is behind to the left
        if can_turn[0] == 1 and snake_x > fruit_x and 20 > snake_y - fruit_y >= 0 and snake.direction != 'left':
            go_left()

        # is behind to the right
        elif can_turn[1] == 1 and snake_x < fruit_x and -20 <= snake_y - fruit_y < 0 and snake.direction != 'right':
            go_right()

        # is below
        elif can_turn[3] == 1 and snake_y > fruit_y and 20 > snake_x - fruit_x >= 0 and snake.direction != 'down':
            go_down()

        # is above
        elif can_turn[2] == 1 and snake_y < fruit_y and -20 <= snake_x - fruit_x < 0 and snake.direction != 'up':
            go_up()

        elif snake_y > fruit_y and snake.direction == 'up':
            calc_optimal()

            if optimal_dir[0] == 1 and can_turn[0] == 0:
                if can_turn[2] == 1:
                    go_up()
                else:
                    go_right()
            elif optimal_dir[1] == 1 and can_turn[1] == 0:
                if can_turn[2] == 1:
                    go_up()
                else:
                    go_left()
            else:
                # turn around
                if can_turn[0] == 1 and optimal_dir[0] == 1:
                    go_left()
                elif can_turn[1] == 1 and optimal_dir[1] == 1:
                    go_right()
                elif can_turn[0] == 1:
                    go_left()
                elif can_turn[1] == 1:
                    go_right()
                else:
                    if (rnd_dir % 2) == 0:
                        go_right()
                    else:
                        go_left()
                set_next_turn(3)
                tried = 1

        elif snake_y < fruit_y and snake.direction == 'down':
            calc_optimal()
            if optimal_dir[0] == 1 and can_turn[0] == 0:
                if can_turn[3] == 1:
                    go_down()
                else:
                    go_right()
            elif optimal_dir[1] == 1 and can_turn[1] == 0:
                if can_turn[3] == 1:
                    go_down()
                else:
                    go_left()
            else:
                # turn around
                if can_turn[0] == 1 and optimal_dir[0] == 1:
                    go_left()
                elif can_turn[1] == 1 and optimal_dir[1] == 1:
                    go_right()
                elif can_turn[0] == 1:
                    go_left()
                elif can_turn[1] == 1:
                    go_right()
                else:
                    if (rnd_dir % 2) == 0:
                        go_right()
                    else:
                        go_left()
                set_next_turn(2)
                tried = 1

        elif snake_x > fruit_x and snake.direction == 'right':
            calc_optimal()

            if optimal_dir[2] == 1 and can_turn[2] == 0:
                if can_turn[1] == 1:
                    go_right()
                else:
                    go_up()
            elif optimal_dir[3] == 1 and can_turn[3] == 0:
                if can_turn[1] == 1:
                    go_right()
                else:
                    go_down()
            else:
                if can_turn[2] == 1 and optimal_dir[2] == 1:
                    go_up()
                elif can_turn[3] == 1 and optimal_dir[3] == 1:
                    go_down()
                elif can_turn[2] == 1:
                    go_up()
                elif can_turn[3] == 1:
                    go_down()
                else:
                    if (rnd_dir % 2) == 0:
                        go_up()
                    else:
                        go_down()
                set_next_turn(0)
                tried = 1

        elif snake_x < fruit_x and snake.direction == 'left':
            calc_optimal()

            if optimal_dir[2] == 1 and can_turn[2] == 0:
                if can_turn[0] == 1:
                    go_left()
                else:
                    go_up()
            elif optimal_dir[3] == 1 and can_turn[3] == 0:
                if can_turn[0] == 1:
                    go_left()
                else:
                    go_down()
            else:
                if can_turn[2] == 1 and optimal_dir[2] == 1:
                    go_up()
                elif can_turn[3] == 1 and optimal_dir[3] == 1:
                    go_down()
                elif can_turn[2] == 1:
                    go_up()
                elif can_turn[3] == 1:
                    go_down()
                else:
                    if (rnd_dir % 2) == 0:
                        go_up()
                    else:
                        go_down()
                set_next_turn(1)
                tried = 1

        # is out of bounds
        elif snake_y >= 240 - 20 and snake.direction == 'up':
            if can_turn[0] == 1 and optimal_dir[0] == 1:
                go_left()
            elif can_turn[1] == 1 and optimal_dir[1] == 1:
                go_right()
            elif can_turn[0] == 1:
                go_left()
            elif can_turn[1] == 1:
                go_right()
            else:
                if (rnd_dir % 2) == 0:
                    go_right()
                else:
                    go_left()
            tried = 1

        elif snake_y <= -240 + 20 and snake.direction == 'down':
            if can_turn[0] == 1 and optimal_dir[0] == 1:
                go_left()
            elif can_turn[1] == 1 and optimal_dir[1] == 1:
                go_right()
            elif can_turn[0] == 1:
                go_left()
            elif can_turn[1] == 1:
                go_right()
            else:
                if (rnd_dir % 2) == 0:
                    go_right()
                else:
                    go_left()
            tried = 1

        elif snake_x >= 280 - 20 and snake.direction == 'right':
            if can_turn[2] == 1 and optimal_dir[2] == 1:
                go_up()
            elif can_turn[3] == 1 and optimal_dir[3] == 1:
                go_down()
            elif can_turn[2] == 1:
                go_up()
            elif can_turn[3] == 1:
                go_down()
            else:
                if (rnd_dir % 2) == 0:
                    go_up()
                else:
                    go_down()
            tried = 1

        elif snake_x <= -300 + 20 and snake.direction == 'left':
            if can_turn[2] == 1 and optimal_dir[2] == 1:
                go_up()
            elif can_turn[3] == 1 and optimal_dir[3] == 1:
                go_down()
            elif can_turn[2] == 1:
                go_up()
            elif can_turn[3] == 1:
                go_down()
            else:
                if (rnd_dir % 2) == 0:
                    go_up()
                else:
                    go_down()
            tried = 1

        else:
            if snake.direction == 'up' and can_turn[2] == 1:
                go_up()
            elif snake.direction == 'down' and can_turn[3] == 1:
                go_down()
            elif snake.direction == 'left' and can_turn[0] == 1:
                go_left()
            elif snake.direction == 'right' and can_turn[1] == 1:
                go_right()
            else:
                for index, turn in enumerate(can_turn):
                    if turn == 1:
                        if index == 0:
                            go_left()
                            break
                        elif index == 1:
                            go_right()
                            break
                        elif index == 2:
                            go_up()
                            break
                        elif index == 3:
                            go_down()
                            break
        return tried
    else:
        if snake.direction == 'up':
            y = snake.ycor()
            snake.sety(y + 20)
        if snake.direction == 'down':
            y = snake.ycor()
            snake.sety(y - 20)
        if snake.direction == 'left':
            x = snake.xcor()
            snake.setx(x - 20)
        if snake.direction == 'right':
            x = snake.xcor()
            snake.setx(x + 20)
        return 0


# Keyboard bindings
if not USE_AI:
    screen.listen()
    screen.onkeypress(snake_go_up, "Up")
    screen.onkeypress(snake_go_down, "Down")
    screen.onkeypress(snake_go_left, "Left")
    screen.onkeypress(snake_go_right, "Right")

# main loop
game_loop = True

while game_loop:
    screen.update()

    # snake and fruit coliisions
    if snake.distance(fruit) < 20:
        x = random.randint(-290, 270)
        y = random.randint(-240, 240)
        fruit.goto(x, y)
        scoring.clear()
        score += 1
        scoring.write("Score:{}".format(score), align="center", font=("Courier", 24, "bold"))
        delay -= 0.001

        ## creating new_ball
        new_fruit = turtle.Turtle()
        new_fruit.speed(0)
        new_fruit.shape('square')
        new_fruit.color('red')
        new_fruit.penup()
        old_fruit.append(new_fruit)

    # adding ball to snake
    for index in range(len(old_fruit) - 1, 0, -1):
        a = old_fruit[index - 1].xcor()
        b = old_fruit[index - 1].ycor()

        old_fruit[index].goto(a, b)

        old_fruit[index].top = b + 10
        old_fruit[index].bottom = b - 10
        old_fruit[index].left = a - 10
        old_fruit[index].right = a + 10

    if len(old_fruit) > 0:
        a = snake.xcor()
        b = snake.ycor()
        old_fruit[0].goto(a, b)

        old_fruit[0].top = b + 10
        old_fruit[0].bottom = b - 10
        old_fruit[0].left = a - 10
        old_fruit[0].right = a + 10
    rnd_try = snake_move(old_fruit, fruit)

    if USE_AI:
        if rnd_try == 1:
            num_tries += 1

            if num_tries > 2:
                num_tries = 0
        elif rnd_try == 0:
            num_tries = 0

    ##snake and border collision
    if snake.xcor() > 280 or snake.xcor() < -300 or snake.ycor() > 240 or snake.ycor() < -240:
        print("game over: snake x,y: " + str(snake.xcor()) + ", " + str(snake.ycor()))
        time.sleep(1)
        screen.clear()
        screen.bgcolor('turquoise')
        scoring.goto(0, 0)
        scoring.write("   GAME OVER \n Your Score is {}".format(score), align="center", font=("Courier", 30, "bold"))
        time.sleep(2)
        game_loop = False

    ## snake collision
    for food in old_fruit:
        if food.distance(snake) < 20:
            time.sleep(1)
            screen.clear()
            screen.bgcolor('turquoise')
            scoring.goto(0, 0)
            scoring.write("    GAME OVER \n Your Score is {}".format(score), align="center",
                          font=("Courier", 30, "bold"))
            time.sleep(2)
            game_loop = False
            break

    time.sleep(delay)

screen.clear()
screen.bgcolor('turquoise')
scoring.goto(0, 0)
scoring.write("Saving. . .", align="center",
              font=("Courier", 30, "bold"))

stat.calc_avg(score)

if high_score < score:
    stat.record_score(score)
    screen.clear()
    screen.bgcolor('turquoise')
    scoring.goto(0, 0)
    scoring.write("New High Score: {}!!".format(score), align="center",
                  font=("Courier", 30, "bold"))
    time.sleep(3)
else:
    print("No new high score")

turtle.Terminator()
