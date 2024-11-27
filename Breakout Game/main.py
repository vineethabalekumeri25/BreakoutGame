import turtle

# Screen setup
screen = turtle.Screen()
screen.title("Breakout Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Paddle
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=6)
paddle.penup()
paddle.goto(0, -250)

# Ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = -2

# Score display
score = 0  # Initialize score
score_display = turtle.Turtle()  # Create the score display turtle

# Bricks
bricks = []
brick_colors = ["red", "orange", "yellow", "green", "blue"]

def create_bricks():
    global bricks
    for row in range(5):
        for col in range(-350, 400, 75):
            brick = turtle.Turtle()
            brick.shape("square")
            brick.color(brick_colors[row])
            brick.shapesize(stretch_wid=1, stretch_len=3)
            brick.penup()
            brick.goto(col, 250 - row * 30)
            bricks.append(brick)

create_bricks()

# Score update
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

# Game Over message
game_over_display = turtle.Turtle()
game_over_display.color("red")
game_over_display.penup()
game_over_display.hideturtle()
game_over_display.goto(0, 0)

# Function to move paddle with mouse click
def move_paddle(x, y):
    # Move the paddle based on mouse click, restrict within screen bounds
    new_x = x
    if new_x < -350:
        new_x = -350  # Left boundary
    elif new_x > 350:
        new_x = 350  # Right boundary
    paddle.setx(new_x)

# Function to reset the game
def reset_game(x, y):
    global score, ball, paddle, bricks
    score = 0
    score_display.clear()
    score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

    # Reset paddle position
    paddle.goto(0, -250)

    # Reset ball position and speed
    ball.goto(0, 0)
    ball.dx = 2
    ball.dy = -2

    # Reset bricks
    for brick in bricks:
        brick.hideturtle()
    bricks.clear()
    create_bricks()  # Recreate bricks

    # Hide the "Game Over" message
    game_over_display.clear()

    # Start the game loop again
    game_loop()

# Bind mouse click to move paddle
screen.listen()

# Main game loop
def game_loop():
    global score

    # Bind the paddle movement function to the screen click
    screen.onscreenclick(move_paddle)

    while True:
        screen.update()

        # Ball movement
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Ball collision with walls
        if ball.xcor() > 390 or ball.xcor() < -390:
            ball.dx *= -1

        if ball.ycor() > 290:
            ball.dy *= -1

        # Ball collision with paddle
        if (
            ball.ycor() < -230
            and paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50
        ):
            ball.dy *= -1
            score += 10  # Increase score when ball hits the paddle
            score_display.clear()  # Clear old score
            score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

        # Ball goes out of bounds (Game Over)
        if ball.ycor() < -290:
            ball.goto(0, 0)
            ball.dy *= -1
            game_over_display.clear()  # Clear "Game Over" message
            game_over_display.write("Game Over! Click to Restart", align="center", font=("Courier", 24, "normal"))
            screen.update()  # Update screen to show the message
            break  # Stop the game loop, awaiting a click to reset

        # Ball collision with bricks
        for brick in bricks:
            if brick.isvisible() and ball.distance(brick) < 30:
                brick.hideturtle()
                ball.dy *= -1
                score += 10
                score_display.clear()
                score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

        # Win condition
        if all(not brick.isvisible() for brick in bricks):
            game_over = True
            score_display.goto(0, 0)
            score_display.write("You Win!", align="center", font=("Courier", 36, "normal"))
            score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

    # After game over, wait for mouse click to restart
    screen.onscreenclick(reset_game)  # This listens for a click to restart the game
    screen.update()
    screen.mainloop()

game_loop()  # Start the game loop