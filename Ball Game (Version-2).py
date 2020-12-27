from campy.gui.events.timer import pause
from campy.graphics.gobjects import GOval, GRect, GLabel, GArc
from breakoutgraphics import BreakoutGraphics
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import keyboard  # using module keyboard

FRAME_RATE = 1000 / 130  # 120 frames per second.
NUM_LIVES = 8
screen_start = False


def main():
    graphics = BreakoutGraphics()

    # Player need to press space to start.
    while True:
        pause(FRAME_RATE)
        if keyboard.read_key() == "space":
            print("You pressed space")
            graphics.remove_start_screen()
            break
    graphics.create_all()

    lives = NUM_LIVES
    graphics.lives_label()
    graphics.lives(lives)
    graphics.score_label()
    graphics.points()
    while True:
        if lives <= 0:
            break
        else:
            pause(FRAME_RATE)
            graphics.move()
            # graphics.reflect()
            graphics.remove_brick()
            if graphics.ball.y >= graphics.window.height:
                lives -= 1
                graphics.reset_ball()
                graphics.switch_off()

                graphics.remove_lives()
                graphics.lives(lives)
            if lives <= 0:
                graphics.game_over_screen()
                # break
            finished = graphics.finished()
            if finished:
                break



if __name__ == '__main__':
    main()
