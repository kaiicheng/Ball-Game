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

INITIAL_Y_SPEED = 3  # Initial vertical speed for the ball.
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

    def lives_label(self):
        label_lives_label = GLabel("Lives:", x=0, y=20)
        label_lives_label.font = "Helvetica-50-bold"
        self.window.add(label_lives_label)

    def lives(self, lives):
        label_lives = GLabel(lives, x=40, y=21)
        label_lives.font = "Helvetica-100-bold"
        self.window.add(label_lives)

    def score_label(self):
        label_score = GLabel("Score:", x=370, y=20)
        label_score.font = "Helvetica-50-bold"
        self.window.add(label_score)

    def points(self):
        label_point = GLabel(point, x=410, y=21)
        label_point.font = "Helvetica-50-bold"
        self.window.add(label_point)

    def remove_lives(self):
        lives_object = self.window.get_object_at(40, 21)
        self.window.remove(lives_object)

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

        # Vertex of the outer square.
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

        # Middle point of the square.
        # The upper middle point of the ball.
        point5_x = self.ball.x + BALL_RADIUS
        point5_y = self.ball.y - 2
        # The lower middle point of the ball.
        point6_x = self.ball.x + BALL_RADIUS
        point6_y = self.ball.y + BALL_RADIUS * 2 + 2
        # The left middle point of the ball.
        point7_x = self.ball.x - 2
        point7_y = self.ball.y + BALL_RADIUS
        # The right middle point of the ball.
        point8_x = self.ball.x + BALL_RADIUS * 2 + 1
        point8_y = self.ball.y + BALL_RADIUS + 2

        # Circle.
        # Left-lower circle.
        point9_x = self.ball.x + BALL_RADIUS - BALL_RADIUS / (1.41) - 1
        point9_y = self.ball.y + BALL_RADIUS - BALL_RADIUS / (1.41) - 1
        # Right-upper circle.
        point10_x = self.ball.x + BALL_RADIUS + BALL_RADIUS / (1.41) + 1
        point10_y = self.ball.y + BALL_RADIUS - BALL_RADIUS / (1.41) - 1
        # Right-lower circle.
        point11_x = self.ball.x + BALL_RADIUS + BALL_RADIUS / (1.41) + 1
        point11_y = self.ball.y + BALL_RADIUS + BALL_RADIUS / (1.41) + 1
        # Left-lower circle.
        point12_x = self.ball.x + BALL_RADIUS - BALL_RADIUS / (1.41) - 1
        point12_y = self.ball.y + BALL_RADIUS + BALL_RADIUS / (1.41) + 1

        maybe_obj1 = self.window.get_object_at(point1_x, point1_y)
        maybe_obj2 = self.window.get_object_at(point2_x, point2_y)
        maybe_obj3 = self.window.get_object_at(point3_x, point3_y)
        maybe_obj4 = self.window.get_object_at(point4_x, point4_y)

        maybe_obj5 = self.window.get_object_at(point5_x, point5_y - 1)
        maybe_obj6 = self.window.get_object_at(point6_x, point6_y + 1)
        maybe_obj7 = self.window.get_object_at(point7_x - 3, point7_y)
        maybe_obj8 = self.window.get_object_at(point8_x + 3, point8_y)

        maybe_obj9 = self.window.get_object_at(point9_x, point9_y)
        maybe_obj10 = self.window.get_object_at(point10_x, point10_y)
        maybe_obj11 = self.window.get_object_at(point11_x, point11_y)
        maybe_obj12 = self.window.get_object_at(point12_x, point12_y)

        a = BRICK_COLS * (BRICK_WIDTH + BRICK_SPACING) - BRICK_SPACING
        b = BRICK_OFFSET + 3 * (BRICK_ROWS * (BRICK_HEIGHT + BRICK_SPACING) - BRICK_SPACING)

        # Situation when the lowest part of the ball pass y coordinates of the upper part of the paddle.
        if (self.ball.y + BALL_RADIUS * 1.75) - (b - PADDLE_OFFSET) > 0:
            # print("Situation 1")
            if maybe_obj11 is self.paddle:
                self.__dx = -self.__dx
            elif maybe_obj12 is self.paddle:
                self.__dx = -self.__dx
            # if maybe_obj7 is self.paddle:
            #     self.__dx = -self.__dx
            # elif maybe_obj8 is self.paddle:
            #     self.__dx = -self.__dx
        else:
            if maybe_obj5 is not None:
                print("1")
                if maybe_obj5 is not self.paddle:
                    print("2")
                    self.window.remove(maybe_obj5)
                    point += 1
                self.__dy = -self.__dy

            elif maybe_obj7 is not None:
                print("3!")
                if maybe_obj7 is not self.paddle:
                    print("4!")
                    self.window.remove(maybe_obj7)
                    point += 1
                # self.__dy = -self.__dy

            elif maybe_obj8 is not None:
                print("5!")
                if maybe_obj8 is not self.paddle:
                    print("6!")
                    self.window.remove(maybe_obj8)
                    point += 1
                # self.__dy = -self.__dy

            # elif maybe_obj6 is not None:
            #     print("3")
            #     if maybe_obj6 is not self.paddle:
            #         print("4")
            #         self.window.remove(maybe_obj6)
            #     self.__dy = -self.__dy

            elif maybe_obj1 is not None:
                print("7!")
                if maybe_obj1 is not self.paddle:
                    print("8!")
                    self.window.remove(maybe_obj1)
                    point += 1
                self.__dy = -self.__dy
            elif maybe_obj2 is not None:
                print("9!")
                if maybe_obj2 is not self.paddle:
                    print("10!")
                    self.window.remove(maybe_obj2)
                    point += 1
                self.__dy = -self.__dy
            elif maybe_obj3 is not None:
                print("11!")
                if maybe_obj3 is not self.paddle:
                    print("12!")
                    self.window.remove(maybe_obj3)
                    point += 1
                self.__dy = -self.__dy
            elif maybe_obj4 is not None:
                print("13!")
                if maybe_obj4 is not self.paddle:
                    print("14!")
                    self.window.remove(maybe_obj4)
                    point += 1
                self.__dy = -self.__dy

        # print(point != original_point)
        if point != original_point:
            print("Point changed!")
            self.remove_score()
            self.points()
