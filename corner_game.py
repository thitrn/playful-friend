from picrawler import Picrawler
from time import sleep
import random
import os

crawler = Picrawler()

rounds = [
    ("corner A", "my quick twist"),
    ("corner B", "my happy dance"),
    ("corner C", "my spin move"),
    ("corner A", "my zig zag turn"),
    ("corner B", "my robot wiggle"),
    ("corner C", "my fake out"),
]

def say(text):
    safe_text = text.replace('"', '')
    os.system('espeak "{}"'.format(safe_text))

def left():
    crawler.do_action('turn left angle', 1, 60)
    sleep(0.2)

def right():
    crawler.do_action('turn right angle', 1, 60)
    sleep(0.2)

def quick_twist():
    left()
    right()

def happy_dance():
    left()
    right()
    left()
    right()

def spin_move():
    for _ in range(6):
        crawler.do_action('turn left', 1, 80)
        sleep(0.1)

def zig_zag_turn():
    left()
    left()
    right()
    right()
    left()

def robot_wiggle():
    for _ in range(3):
        left()
        right()

def fake_out():
    left()
    sleep(0.3)
    right()
    sleep(0.2)
    left()
    sleep(0.5)

def do_robot_action(action_name):
    if action_name == "my quick twist":
        quick_twist()
    elif action_name == "my happy dance":
        happy_dance()
    elif action_name == "my spin move":
        spin_move()
    elif action_name == "my zig zag turn":
        zig_zag_turn()
    elif action_name == "my robot wiggle":
        robot_wiggle()
    elif action_name == "my fake out":
        fake_out()

def main():
    try:
        crawler.do_step('stand', 40)
        sleep(1)

        say("Lets play the corner challenge!")
        sleep(1)

        shuffled_rounds = rounds[:]
        random.shuffle(shuffled_rounds)

        for target, robot_action in shuffled_rounds[:4]:
            line = f"Can you touch {target} before I do {robot_action}?"
            print(line)
            say(line)
            sleep(1)

            do_robot_action(robot_action)
            sleep(1)

            feedback = random.choice([
                "Nice try! Ready for the next round?",
                "Good job! Here comes another challenge!",
                "That was fun! Lets do one more!",
                "Great! Get ready for the next move!"
            ])
            print(feedback)
            say(feedback)
            sleep(1.5)

        say("Game over! Thanks for playing!")
        sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print("Error:", e)
    finally:
        try:
            crawler.do_step('sit', 40)
        except:
            pass
        sleep(1)

if __name__ == "__main__":
    main()