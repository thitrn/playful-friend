from picrawler import Picrawler
from vilib import Vilib
from time import sleep, time
import os

crawler = Picrawler()

PLAYER_SCORE = 0
ROBOT_SCORE = 0

WIN_SOUND = "/home/pi/picrawler/examples/win.wav"
LOSE_SOUND = "/home/pi/picrawler/examples/lose.wav"


def say(text):
    safe_text = text.replace('"', '')
    print("Robot says:", text)
    os.system('espeak --stdout "{}" | aplay -D plughw:2,0 -c 2'.format(safe_text))


def play_sound(sound_file):
    if os.path.exists(sound_file):
        os.system('aplay -D plughw:2,0 "{}"'.format(sound_file))
    else:
        print("Sound file not found:", sound_file)


def play_win_sound():
    play_sound(WIN_SOUND)


def play_lose_sound():
    play_sound(LOSE_SOUND)


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
    for action_name, steps, speed in sequence:
        if green_detected(threshold):
            stop_motion()
            return True

        safe_action(action_name, steps, speed)
        sleep(pause)

        if green_detected(threshold):
            stop_motion()
            return True

    stop_motion()
    return False


def play_challenge(title, prompt, sequence, round_time=5, threshold=80):
    global PLAYER_SCORE, ROBOT_SCORE

    say(title)
    sleep(0.5)
    say(prompt)
    sleep(1.0)

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
        play_win_sound()
        sleep(0.2)
        say("Green detected! You win this round!")
        return True
    else:
        ROBOT_SCORE += 1
        play_lose_sound()
        sleep(0.2)
        say("Too slow! I win this round!")
        return False


def play_redemption_round(level_name, redemption_round):
    say("Wait a second!")
    sleep(0.8)
    say("You unlocked a secret redemption round!")
    sleep(1.0)
    say("This one is easier. You can do it!")
    sleep(1.0)

    title, prompt, sequence, round_time, threshold = redemption_round
    won = play_challenge(title, prompt, sequence, round_time, threshold)

    if won:
        say("Amazing comeback! You passed the level!")
        sleep(0.8)
        return True
    else:
        say("Nice try! That was your redemption chance.")
        sleep(0.8)
        return False


def explain_rules():
    say("Welcome to Corner Quest!")
    sleep(1)
    say("Here is how to win.")
    sleep(0.8)
    say("Listen carefully to each challenge.")
    sleep(0.8)
    say("Do the action as fast as you can.")
    sleep(0.8)
    say("Then come back to me and show me your green game bracelet.")
    sleep(1)
    say("If I see green before I finish my move, you win the round.")
    sleep(1)
    say("Levels 1 and 2 need 2 wins out of 3 rounds to pass.")
    sleep(1)
    say("Level 3 only needs 1 win out of 3 rounds to pass.")
    sleep(1)
    say("If you do not pass a level, you may get a secret redemption round.")
    sleep(1)
    say("Get ready for Corner Quest!")
    sleep(1)


def play_level(level_name, rounds, wins_needed, redemption_round=None):
    level_wins = 0
    level_losses = 0

    say(level_name)
    sleep(0.8)

    for i, (title, prompt, sequence, round_time, threshold) in enumerate(rounds, start=1):
        won = play_challenge(title, prompt, sequence, round_time, threshold)

        if won:
            level_wins += 1
        else:
            level_losses += 1

        if level_wins >= wins_needed:
            say("You passed this level!")
            sleep(0.8)
            return True

        if i < len(rounds):
            say("Get ready for the next round!")
            sleep(0.8)

    if level_wins >= wins_needed:
        say("You passed this level!")
        sleep(0.8)
        return True

    if level_losses >= 2 and redemption_round is not None:
        return play_redemption_round(level_name, redemption_round)

    say("You did not pass this level.")
    sleep(0.8)
    return False


def main():
    try:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)
        Vilib.color_detect("green")

        safe_step('stand', 40)
        sleep(1)

        explain_rules()

        level1_rounds = [
            (
                "Level 1 round 1",
                "Can you go to corner A before I wave 2 arms? Then come back and show me your green game bracelet.",
                [
                    ('turn left', 1, 75),
                    ('turn right', 1, 75),
                    ('turn left', 1, 75),
                    ('turn right', 1, 75),
                ],
                4,
                80
            ),
            (
                "Level 1 round 2",
                "Can you do 2 jumping jacks before I do my turbo dash? Then come back and show me your green game bracelet.",
                [
                    ('forward', 1, 85),
                    ('forward', 1, 85),
                    ('backward', 1, 80),
                ],
                4,
                80
            ),
            (
                "Level 1 round 3",
                "Can you touch corner B and run back before my quick spin is over? Then show me your green game bracelet.",
                [
                    ('turn left', 1, 90),
                    ('turn right', 1, 90),
                    ('turn left', 1, 90),
                ],
                4,
                80
            ),
        ]

        level1_redemption = (
            "Level 1 redemption round",
            "Can you touch corner A and come back before I do my slow wave? Then show me your green game bracelet.",
            [
                ('turn left', 1, 55),
                ('turn right', 1, 55),
                ('turn left', 1, 55),
                ('turn right', 1, 55),
                ('turn left', 1, 55),
                ('turn right', 1, 55),
            ],
            7,
            80
        )

        level2_rounds = [
            (
                "Level 2 round 1",
                "Can you crab walk to corner D and come back before I do my zig zag burst? Then show me your green game bracelet.",
                [
                    ('forward', 1, 80),
                    ('turn left angle', 1, 80),
                    ('forward', 1, 80),
                    ('turn right angle', 1, 80),
                    ('forward', 1, 80),
                ],
                5,
                80
            ),
            (
                "Level 2 round 2",
                "Can you do 3 burpees before I complete my dance? Then come back and show me your green game bracelet.",
                [
                    ('turn left', 1, 85),
                    ('turn right', 1, 85),
                    ('turn left angle', 1, 80),
                    ('turn right angle', 1, 80),
                    ('forward', 1, 75),
                    ('backward', 1, 75),
                    ('turn left', 1, 90),
                    ('turn right', 1, 90),
                ],
                6,
                80
            ),
            (
                "Level 2 round 3",
                "Can you hop to corner C and back before I finish my fast zig zag? Then show me your green game bracelet.",
                [
                    ('forward', 1, 85),
                    ('turn left angle', 1, 85),
                    ('forward', 1, 85),
                    ('turn right angle', 1, 85),
                ],
                5,
                80
            ),
        ]

        level2_redemption = (
            "Level 2 redemption round",
            "Can you run to corner B and back before I finish my easy zig zag? Then show me your green game bracelet.",
            [
                ('forward', 1, 60),
                ('turn left angle', 1, 60),
                ('forward', 1, 60),
                ('turn right angle', 1, 60),
                ('backward', 1, 60),
                ('forward', 1, 60),
            ],
            8,
            80
        )

        level3_rounds = [
            (
                "Level 3 round 1",
                "Can you do 5 jumping jacks at corner A, then run to corner D, then do 3 karate kicks, then come all the way back and show me your green game bracelet before my lightning spin is over?",
                [
                    ('turn left', 1, 95),
                    ('turn left', 1, 95),
                    ('turn right', 1, 95),
                    ('turn right', 1, 95),
                ],
                5,
                80
            ),
            (
                "Level 3 round 2",
                "Can you touch corners B, C, B, A, and D in that order, then come back to me and show me your green game bracelet before my corner attack is over?",
                [
                    ('forward', 1, 85),
                    ('turn left', 1, 90),
                    ('forward', 1, 85),
                    ('turn right', 1, 90),
                    ('forward', 1, 85),
                ],
                5,
                80
            ),
            (
                "Level 3 round 3",
                "Can you do 3 burpees, then 4 hops, then spin once, then race back to me and show me your green game bracelet before my dance combo is over?",
                [
                    ('turn left', 1, 90),
                    ('turn right', 1, 90),
                    ('forward', 1, 85),
                    ('backward', 1, 85),
                    ('turn left angle', 1, 90),
                    ('turn right angle', 1, 90),
                    ('turn left', 1, 95),
                ],
                6,
                80
            ),
        ]

        passed_level_1 = play_level(
            "Level 1. Easy.",
            level1_rounds,
            wins_needed=2,
            redemption_round=level1_redemption
        )

        if passed_level_1:
            say("Now it is time for level 2. Get ready!")
            sleep(1)
            passed_level_2 = play_level(
                "Level 2. Intermediate.",
                level2_rounds,
                wins_needed=2,
                redemption_round=level2_redemption
            )
        else:
            passed_level_2 = False

        if passed_level_2:
            say("Commencing level 3 hard. Get ready!")
            sleep(1)
            play_level("Level 3. Hard.", level3_rounds, wins_needed=1)

        say("Corner Quest is over!")
        sleep(0.8)
        say("Your score is {}".format(PLAYER_SCORE))
        sleep(0.8)
        say("My score is {}".format(ROBOT_SCORE))
        sleep(0.8)

        if PLAYER_SCORE > ROBOT_SCORE:
            say("Amazing! You beat me at Corner Quest!")
        elif ROBOT_SCORE > PLAYER_SCORE:
            say("I win Corner Quest!")
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
