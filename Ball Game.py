from campy.gui.events.timer import pause
from campy.graphics.gobjects import GOval, GRect, GLabel, GArc
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 130   # 120 frames per second.
NUM_LIVES = 8


def main():
    graphics = BreakoutGraphics()
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
                break
            finished = graphics.finished()
            if finished:
                break


if __name__ == '__main__':
    main()
