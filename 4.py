from picrawler import Picrawler
from vilib import Vilib
from time import sleep, time
import os

crawler = Picrawler()

PLAYER_SCORE = 0
ROBOT_SCORE = 0


def say(text):
    safe_text = text.replace('"', '')
    print("Robot says:", text)
    os.system('espeak --stdout "{}" | aplay -D plughw:2,0 -c 2'.format(safe_text))


def green_detected(threshold=80):
    n = Vilib.detect_obj_parameter.get('color_n', 0)
    w = Vilib.detect_obj_parameter.get('color_w', 0)
    print("green patches:", n, "width:", w)
    return n > 0 and w > threshold


def safe_action(action, steps=1, speed=60):
    try:
        crawler.do_action(action, steps, speed)
        return True
    except Exception as e:
        print("Action failed:", action, e)
        return False


def safe_step(step_name, speed=40):
    try:
        crawler.do_step(step_name, speed)
        return True
    except Exception as e:
        print("Step failed:", step_name, e)
        return False


def stop_motion():
    try:
        crawler.do_step('stand', 40)
    except Exception as e:
        print("Stop failed:", e)


def do_move_with_green_check(sequence, threshold=80, pause=0.08):
    """
    sequence = list of tuples: (action_name, steps, speed)
    Returns True if green detected during motion, else False.
    """
    for action_name, steps, speed in sequence:
        if green_detected(threshold):
            stop_motion()
            return True

        ok = safe_action(action_name, steps, speed)
        sleep(pause)

        if green_detected(threshold):
            stop_motion()
            return True

        if not ok:
            print("Skipping failed action:", action_name)

    stop_motion()
    return False


def play_challenge(title, prompt, sequence, round_time=5, threshold=80):
    global PLAYER_SCORE, ROBOT_SCORE

    say(title)
    sleep(0.5)
    say(prompt)
    sleep(0.6)

    start_time = time()
    detected = False

    while time() - start_time < round_time:
        if do_move_with_green_check(sequence, threshold=threshold, pause=0.08):
            detected = True
            break
        sleep(0.05)

    stop_motion()
    sleep(0.3)

    if detected:
        PLAYER_SCORE += 1
        say("Green detected! You win this round!")
    else:
        ROBOT_SCORE += 1
        say("Too slow! I win this round!")

    sleep(1.0)


def main():
    try:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        Vilib.color_detect("green")

        safe_step('stand', 40)
        sleep(1)

        say("Welcome to the fast round!")
        sleep(0.8)
        say("Show me green before I finish each challenge.")
        sleep(0.8)

        # Challenge 1
        play_challenge(
            "Challenge 1",
            "Can you do 3 jumping jacks before my turbo dash is over?",
            [
                ('forward', 1, 85),
                ('forward', 1, 85),
                ('backward', 1, 80),
            ],
            round_time=4,
            threshold=80
        )

        say("Next challenge!")
        sleep(0.5)

        # Challenge 2
        play_challenge(
            "Challenge 2",
            "Can you spin around one time before my lightning spin is over?",
            [
                ('turn left', 1, 90),
                ('turn left', 1, 90),
                ('turn right', 1, 90),
                ('turn right', 1, 90),
            ],
            round_time=4,
            threshold=80
        )

        say("Next challenge!")
        sleep(0.5)

        # Challenge 3
        play_challenge(
            "Challenge 3",
            "Can you touch your head and your knees before my zig zag burst is over?",
            [
                ('forward', 1, 80),
                ('turn left angle', 1, 80),
                ('forward', 1, 80),
                ('turn right angle', 1, 80),
                ('forward', 1, 80),
            ],
            round_time=4,
            threshold=80
        )

        say("Final challenge!")
        sleep(0.5)

        # Challenge 4
        play_challenge(
            "Challenge 4",
            "Can you wave both arms high before my corner attack is over?",
            [
                ('forward', 1, 80),
                ('turn left', 1, 85),
                ('forward', 1, 80),
                ('turn right', 1, 85),
                ('forward', 1, 80),
            ],
            round_time=5,
            threshold=80
        )

        say("Fast round is over!")
        sleep(0.8)
        say("Your score is {}".format(PLAYER_SCORE))
        sleep(0.8)
        say("My score is {}".format(ROBOT_SCORE))
        sleep(0.8)

        if PLAYER_SCORE > ROBOT_SCORE:
            say("You beat me this time!")
        elif ROBOT_SCORE > PLAYER_SCORE:
            say("I win the fast round!")
        else:
            say("It is a tie!")

        sleep(1.5)

    except KeyboardInterrupt:
        print("Stopping...")

    except Exception as e:
        print("Error:", e)

    finally:
        try:
            Vilib.color_detect_switch(False)
        except:
            pass
        try:
            Vilib.camera_close()
        except:
            pass
        try:
            safe_step('sit', 40)
        except:
            pass
        sleep(1)


if __name__ == "__main__":
    main()
