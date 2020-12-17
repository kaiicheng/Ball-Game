from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

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

INITIAL_Y_SPEED = 3.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.

point = 0   # Create a space to store the point.
win = False   # When all bricks are disappeared, the player win the the game. "win" will be changed into True.


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

    # Default initial velocity for the ball.
    def set_ball_velocity(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        print(random.random())
        if random.random() > 0.5:
            self.__dx = -self.__dx

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

    # Function to reflect the ball when it touches border.
    def reflect(self):

        # Plus 1 to prevent the function from detecting the ball itself.
        maybe_obj5 = self.window.get_object_at(self.ball.x + BALL_RADIUS, self.ball.y + BALL_RADIUS*2 + 1)
        if maybe_obj5 is self.paddle:
            self.__dy = -self.__dy

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

    # Function to remove bricks when four vertex touches any brick.
    def remove(self):

        # Count the point of the game.
        global point

        # Left-upper vertex.
        point1_x = self.ball.x
        point1_y = self.ball.y

        # Right-upper vertex.
        point2_x = self.ball.x + BALL_RADIUS * 2
        point2_y = self.ball.y

        # Right-lower vertex.
        point3_x = self.ball.x + BALL_RADIUS * 2
        point3_y = self.ball.y + BALL_RADIUS * 2

        # Left-lower vertex.
        point4_x = self.ball.x
        point4_y = self.ball.y + BALL_RADIUS * 2

        # The upper middle point of the ball.
        point5_x = self.ball.x + BALL_RADIUS
        point5_y = self.ball.y

        maybe_obj1 = self.window.get_object_at(point1_x, point1_y)
        maybe_obj2 = self.window.get_object_at(point2_x, point2_y)
        maybe_obj3 = self.window.get_object_at(point3_x, point3_y)
        maybe_obj4 = self.window.get_object_at(point4_x, point4_y)

        # Minus 1 to prevent the function from detecting the ball itself.
        maybe_obj5 = self.window.get_object_at(point5_x, point5_y - 1)

        if maybe_obj1 is not None and maybe_obj1 is not self.paddle:
            self.window.remove(maybe_obj1)
            self.__dy = -self.__dy
            point += 1

        elif maybe_obj2 is not None and maybe_obj2 is not self.paddle:
            self.window.remove(maybe_obj2)
            self.__dy = -self.__dy
            point += 1
        elif maybe_obj3 is not None and maybe_obj3 is not self.paddle:
            self.window.remove(maybe_obj3)
            self.__dy = -self.__dy
            point += 1
        elif maybe_obj4 is not None and maybe_obj4 is not self.paddle:
            self.window.remove(maybe_obj4)
            self.__dy = -self.__dy
            point += 1
        elif maybe_obj5 is not None and maybe_obj5 is not self.paddle:
            self.window.remove(maybe_obj5)
            self.__dy = -self.__dy

    # Situation when the player wins the game.
    def finished(self):
        global win
        if point >= BRICK_ROWS * BRICK_COLS:
            win = True
        return win

