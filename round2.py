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


def green_detected(threshold=100):
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


def jumping_jacks_motion():
    say("Watch this. I am doing five jumping jacks!")
    for i in range(5):
        print("Jumping jack", i + 1)
        safe_step('stand', 45)
        sleep(0.25)
        safe_action('turn left', 1, 70)
        sleep(0.2)
        safe_action('turn right', 1, 70)
        sleep(0.2)
    safe_step('stand', 40)
    sleep(0.5)


def wiggle_motion():
    say("Now I will do a wiggle!")
    for _ in range(3):
        safe_action('turn left', 1, 75)
        sleep(0.15)
        safe_action('turn right', 1, 75)
        sleep(0.15)
    safe_step('stand', 40)
    sleep(0.5)


def corner_b_motion():
    say("Can you crawl to corner B and come back before I wave my arms?")
    sleep(1)

    # Go out
    for _ in range(2):
        safe_action('forward', 1, 55)
        sleep(0.2)

    safe_action('turn left', 1, 65)
    sleep(0.25)

    for _ in range(2):
        safe_action('forward', 1, 55)
        sleep(0.2)

    # Come back
    safe_action('turn right', 1, 65)
    sleep(0.25)

    for _ in range(2):
        safe_action('forward', 1, 55)
        sleep(0.2)

    safe_step('stand', 40)
    sleep(0.5)


def wave_arms_motion():
    say("Here comes my arm wave!")
    for _ in range(4):
        safe_action('turn left', 1, 80)
        sleep(0.15)
        safe_action('turn right', 1, 80)
        sleep(0.15)
    safe_step('stand', 40)
    sleep(0.5)


def race_spin_motion():
    say("Ready set go!")
    for _ in range(4):
        safe_action('turn left', 1, 80)
        sleep(0.15)
    safe_step('stand', 40)
    sleep(0.5)


def play_challenge(name, intro_line, motion_func, round_time=8, threshold=100):
    global PLAYER_SCORE, ROBOT_SCORE

    say(name)
    sleep(1)
    say(intro_line)
    sleep(1)

    start_time = time()
    detected = False

    while time() - start_time < round_time:
        motion_func()

        if green_detected(threshold):
            detected = True
            break

        sleep(0.2)

    safe_step('stand', 40)
    sleep(0.5)

    if detected:
        PLAYER_SCORE += 1
        say("You got it! You win this challenge!")
    else:
        ROBOT_SCORE += 1
        say("Too slow! I win this challenge!")

    sleep(1.5)


def main():
    try:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        Vilib.color_detect("green")

        safe_step('stand', 40)
        sleep(1)

        say("Welcome to round 2!")
        sleep(1)
        say("This round has different challenges.")
        sleep(1)
        say("Show me green before I finish each challenge.")
        sleep(1)

        play_challenge(
            "Challenge 1",
            "Can you do five jumping jacks before I do a wiggle?",
            jumping_jacks_motion,
            round_time=8,
            threshold=100
        )

        say("Get ready for the next challenge!")
        sleep(1)

        play_challenge(
            "Challenge 2",
            "Can you crawl to corner B and come back before I wave my arms?",
            corner_b_motion,
            round_time=9,
            threshold=100
        )

        say("One more challenge!")
        sleep(1)

        play_challenge(
            "Challenge 3",
            "Last one! Can you beat my race spin?",
            race_spin_motion,
            round_time=7,
            threshold=100
        )

        say("Round 2 is over!")
        sleep(1)

        say("Your score is {}".format(PLAYER_SCORE))
        sleep(1)

        say("My score is {}".format(ROBOT_SCORE))
        sleep(1)

        if PLAYER_SCORE > ROBOT_SCORE:
            say("You are the round 2 champion!")
        elif ROBOT_SCORE > PLAYER_SCORE:
            say("I win round 2!")
        else:
            say("Round 2 is a tie!")

        sleep(2)

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
