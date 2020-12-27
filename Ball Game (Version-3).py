from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
import keyboard  # using module keyboard

FRAME_RATE = 1000 / 100   # 120 frames per second.
NUM_LIVES = 5
start = False
screen_start = False


def main():
    graphics = BreakoutGraphics()

    # Player need to press Space to start.
    while True:
        pause(10)
        # pause(FRAME_RATE)
        if keyboard.read_key() == "space":
            print("You pressed space")
            graphics.remove_start_screen()
            start = True
            break
        else:
            pass
    graphics.create_all()

    lives = NUM_LIVES
    while start:
        if lives <= 0:
            graphics.game_over_screen()
            # break
        else:
            pause(FRAME_RATE)

            graphics.reflect()
            graphics.move()
            graphics.remove_and_score()
            graphics.countlives()

            # graphics.window.remove(graphics.life)
            # graphics.life.text = "Lives: " + str(lives)
            # graphics.window.add(graphics.life)
            if graphics.ball.y >= graphics.window.height:
                lives -= 1
                graphics.window.remove(graphics.life)
                graphics.life.text = "Lives: " + str(lives)
                graphics.window.add(graphics.life)
                graphics.reset_ball()
                graphics.switch_off()

            if lives <= 0:
                graphics.game_over_screen()
                if keyboard.read_key() == "esc":
                    print("You pressed space")
                    graphics.remove_start_screen()
                    situation = 2
                    break
                else:
                    pass
                # break
            finished = graphics.finished()
            if finished:
                break
    graphics.clear_window()

    if situation == 2:
        graphics.close_window()


if __name__ == '__main__':
    main()