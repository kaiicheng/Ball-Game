from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random
import tkinter as tk
import tkinter.messagebox

BRICK_SPACING = 3  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 75  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 5  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.

point = 0  # Create a space to store the point.
win = False  # When all bricks are disappeared, the player win the the game. "win" will be changed into True.
screen_start = False


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):
        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create the starting screen
        # window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        # window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        start_screen = GRect(window_width, window_height)
        start_screen.color = "black"
        # cover.fill_color = "white"
        start_screen.filled = True
        self.window.add(start_screen)

        # Create the "BRICKS BREAKOUT" label.
        bricks_breakout_label = GLabel("BRICKS BREAKOUT", x=window_width / 2 - 50, y=40)
        bricks_breakout_label.color = "blue"
        bricks_breakout_label.font = "Helvetica-80"
        self.window.add(bricks_breakout_label)

        # Create the "START" label.
        start_label = GLabel("START", x=window_width / 2 - 40, y=200)
        start_label.color = "purple"
        start_label.font = "Helvetica-150"
        self.window.add(start_label)

    def create_all(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                   paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                   brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                   brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                   brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING):

        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)

        # Create a black paddle.
        self.paddle = GRect(width=paddle_width, height=paddle_height, x=(window_width - paddle_width) / 2,
                            y=window_height - paddle_offset)
        self.paddle.filled = True
        self.paddle.color = "black"
        self.paddle.fill_color = "black"
        self.window.add(self.paddle)

        # Center a ball in the graphical window.
        self.ball = GOval(ball_radius * 2, ball_radius * 2, x=(window_width - ball_radius) / 2,
                          y=(window_height - ball_radius) / 2)
        self.ball.filled = True
        self.ball.fill_color = "black"
        self.window.add(self.ball)
        self.start = False
        self.__dy = 0
        self.__dx = 0

        # Initialize our mouse listeners and connect the the paddle with the mouse.
        onmousemoved(self.track)
        onmouseclicked(self.switch_on)

        # Draw bricks.
        times_col = BRICK_COLS
        times_row = BRICK_ROWS
        y_co = 0
        x_co = 0
        reset = False
        color = 0
        for i in range(times_row):

            # Set the default color of bricks.
            if 0 <= i <= 1:
                color = "red"
            elif 2 <= i <= 3:
                color = "orange"
            elif 4 <= i <= 5:
                color = "yellow"
            elif 6 <= i <= 7:
                color = "green"
            elif 8 <= i <= 9:
                color = "blue"
            elif 10 <= i <= 11:
                color = "indigo"
            elif 12 <= i <= 13:
                color = "purple"
            if reset:
                x_co = 0
            for j in range(times_col):
                if x_co >= window_width:
                    pass
                else:
                    self.brick = GRect(width=BRICK_WIDTH, height=BRICK_HEIGHT, x=x_co,
                                       y=BRICK_OFFSET + y_co)  # Center of not?
                    self.brick.filled = True
                    self.brick.fill_color = color
                    self.brick.color = color
                    self.window.add(self.brick)
                    x_co += BRICK_SPACING + BRICK_WIDTH
            y_co += BRICK_SPACING + BRICK_HEIGHT
            reset = True

        # Default initial velocity for the ball.
        self.set_ball_velocity()

    # Create a black paddle.
    def create_paddle(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                      paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                      brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                      brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                      brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                      title='Breakout'):

        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)

        paddle = GRect(width=paddle_width, height=paddle_height, x=(window_width - paddle_width) / 2,
                       y=window_height - paddle_offset)
        paddle.filled = True
        paddle.color = "black"
        paddle.fill_color = "black"
        self.window.add(paddle)

    # Create a ball and center it in the graphical window.
    def create_ball(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                    paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                    brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                    brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                    brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                    title='Breakout'):

        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)

        self.ball = GOval(ball_radius * 2, ball_radius * 2, x=(window_width - ball_radius) / 2,
                          y=(window_height - ball_radius) / 2)
        self.ball.filled = True
        self.ball.fill_color = "black"
        self.window.add(self.ball)
        self.start = False
        self.__dy = 0
        self.__dx = 0

    def connect_mouse(self):
        # Initialize our mouse listeners and connect the the paddle with the mouse.
        onmousemoved(self.track)
        onmouseclicked(self.switch_on)

    def create_brick(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                     paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                     brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                     brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                     brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                     title='Breakout'):

        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)

        # Draw bricks.
        times_col = BRICK_COLS
        times_row = BRICK_ROWS
        y_co = 0
        x_co = 0
        reset = False
        color = 0
        for i in range(times_row):

            # Set the default color of bricks.
            if 0 <= i <= 1:
                color = "red"
            elif 2 <= i <= 3:
                color = "orange"
            elif 4 <= i <= 5:
                color = "yellow"
            elif 6 <= i <= 7:
                color = "green"
            elif 8 <= i <= 9:
                color = "blue"
            elif 10 <= i <= 11:
                color = "indigo"
            elif 12 <= i <= 13:
                color = "purple"
            if reset:
                x_co = 0
            for j in range(times_col):
                if x_co >= window_width:
                    pass
                else:
                    self.brick = GRect(width=BRICK_WIDTH, height=BRICK_HEIGHT, x=x_co,
                                       y=BRICK_OFFSET + y_co)  # Center of not?
                    self.brick.filled = True
                    self.brick.fill_color = color
                    self.brick.color = color
                    self.window.add(self.brick)
                    x_co += BRICK_SPACING + BRICK_WIDTH
            y_co += BRICK_SPACING + BRICK_HEIGHT
            reset = True

    # Default initial velocity for the ball.
    def set_velocity(self):
        self.set_ball_velocity()

    # Default initial velocity for the ball.
    def set_ball_velocity(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        print(random.random())
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def lives_label(self):
        label_lives_label = GLabel("Lives:", x=0, y=20)
        label_lives_label.font = "Helvetica-50-bold"
        self.window.add(label_lives_label)

    def lives(self, lives):
        label_lives = GLabel(lives, x=40, y=21)
        label_lives.font = "Helvetica-100-bold"
        self.window.add(label_lives)

    def remove_lives(self):
        lives_object = self.window.get_object_at(40, 21)
        self.window.remove(lives_object)

    def score_label(self):
        label_score = GLabel("Score:", x=370, y=20)
        label_score.font = "Helvetica-50-bold"
        self.window.add(label_score)

    def points(self):
        label_point = GLabel(point, x=410, y=21)
        label_point.font = "Helvetica-50-bold"
        self.window.add(label_point)

    def remove_score(self):
        score_object = self.window.get_object_at(410, 21)
        self.window.remove(score_object)

    # Function to move.
    def move(self):

        # Set a switch to start.
        if self.start:
            self.ball.move(self.__dx, self.__dy)
        else:
            pass

        # Condition when ball touches border.
        if self.window.width - self.ball.width <= self.ball.x or self.ball.x <= 0:
            self.__dx = -self.__dx
        if self.ball.y <= 0:
            self.__dy = -self.__dy

    # Function to reflect the ball when it touches paddle.
    def reflect(self):

        # Right-lower circle.
        point11_x = self.ball.x + BALL_RADIUS + BALL_RADIUS / (1.41) + 1
        point11_y = self.ball.y + BALL_RADIUS + BALL_RADIUS / (1.41) + 1
        # Left-lower circle.
        point12_x = self.ball.x + BALL_RADIUS - BALL_RADIUS / (1.41) - 1
        point12_y = self.ball.y + BALL_RADIUS + BALL_RADIUS / (1.41) + 1

        maybe_obj11 = self.window.get_object_at(point11_x, point11_y)
        maybe_obj12 = self.window.get_object_at(point12_x, point12_y)

        a = BRICK_COLS * (BRICK_WIDTH + BRICK_SPACING) - BRICK_SPACING
        b = BRICK_OFFSET + 3 * (BRICK_ROWS * (BRICK_HEIGHT + BRICK_SPACING) - BRICK_SPACING)

        if (self.ball.y + BALL_RADIUS * 2) - (b - PADDLE_OFFSET) > 0:
            # print("Situation 1")
            if maybe_obj11 is self.paddle:
                self.__dx = -self.__dx
            if maybe_obj12 is self.paddle:
                self.__dx = -self.__dx

    # Function to switch on when the game starts.
    def switch_on(self, event):
        self.start = True

    # Function to switch off when the game pauses.
    def switch_off(self):
        self.start = False

    # Function to track the mouse and connect it with the paddle.
    def track(self, event):
        x_smallest = 0
        self.paddle.x = event.x - self.paddle.width / 2

        if self.paddle.x > self.window.width - self.paddle.width or self.paddle.x == self.window.width - self.paddle.width:
            self.paddle.x = self.window.width - self.paddle.width
        elif self.paddle.x < x_smallest or self.paddle.x == x_smallest:
            self.paddle.x = x_smallest

    # Function to create a new ball when the ball is going out of the border.
    def reset_ball(self):
        self.set_ball_position()
        self.set_ball_velocity()
        self.ball.filled = True
        self.ball.fill_color = "black"
        self.window.add(self.ball)
        self.switch_off()

    # Function to set the new ball in the middle of the window.
    def set_ball_position(self):
        self.ball.x = (self.window.width - BALL_RADIUS) / 2
        self.ball.y = (self.window.height - BALL_RADIUS * 2) / 2

    # Situation when the player wins the game.
    def finished(self):
        global win
        if point >= BRICK_ROWS * BRICK_COLS:
            win = True
        return win

    # Function to remove bricks when four vertex touches any brick.
    def remove_brick(self):

        # Count the point of the game.
        global point

        original_point = point

        # top middle point of the ball.
        point1_x = self.ball.x + BALL_RADIUS
        point1_y = self.ball.y
        # left middle point of the ball.
        point2_x = self.ball.x
        point2_y = self.ball.y + BALL_RADIUS
        # botoom middle point of the ball.
        point3_x = self.ball.x + BALL_RADIUS
        point3_y = self.ball.y + BALL_RADIUS*2
        # right middle point of the ball.
        point4_x = self.ball.x + BALL_RADIUS*2
        point4_y = self.ball.y + BALL_RADIUS

        # Minus 0.1 to prevent the function from detecting the ball itself.
        maybe_obj1 = self.window.get_object_at(point1_x, point1_y - 0.1)
        maybe_obj2 = self.window.get_object_at(point2_x - 0.1, point2_y)
        maybe_obj3 = self.window.get_object_at(point3_x, point3_y + 0.1)
        maybe_obj4 = self.window.get_object_at(point4_x + 0.1, point4_y)

        if maybe_obj1 is not None and maybe_obj1 is not self.paddle:
            print("8!")
            self.window.remove(maybe_obj1)
            point += 1
            self.__dy = -self.__dy
        elif maybe_obj2 is not None and maybe_obj2 is not self.paddle:
            print("10!")
            self.window.remove(maybe_obj2)
            point += 1
            self.__dy = -self.__dy
        elif maybe_obj3 is not None and maybe_obj3 is not self.paddle:
            print("12!")
            self.window.remove(maybe_obj3)
            point += 1
            self.__dy = -self.__dy
        elif maybe_obj4 is not None and maybe_obj4 is not self.paddle:
            print("14!")
            self.window.remove(maybe_obj4)
            point += 1
            self.__dy = -self.__dy

        # print(point != original_point)
        if point != original_point:
            print("Point changed!")
            self.remove_score()
            self.points()

    def remove_start_screen(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                            paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                            brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                            brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                            brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING):

        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)

        start_screen = self.window.get_object_at(10, 10)
        self.window.remove(start_screen)

        bricks_breakout_label = self.window.get_object_at(x=window_width / 2 - 50, y=40)
        self.window.remove(bricks_breakout_label)

        start_label = self.window.get_object_at(x=window_width / 2 - 40, y=200)
        self.window.remove(start_label)

    def game_over_screen(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                         paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                         brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                         brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                         brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING):

        # Create the starting screen
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        game_over_screen = GRect(window_width, window_height)
        game_over_screen.color = "black"
        # cover.fill_color = "white"
        game_over_screen.filled = True
        self.window.add(game_over_screen)

        # Create the "GAME OVER" label.
        bricks_breakout_label = GLabel("GAME OVER", x=window_width / 2 - 50, y=40)
        bricks_breakout_label.color = "blue"
        bricks_breakout_label.font = "Helvetica-80"
        self.window.add(bricks_breakout_label)
