from picrawler import Picrawler
from time import sleep
import random
import os

crawler = Picrawler()

challenges = [
    ("corner A", "a spin"),
    ("corner B", "a dance"),
    ("corner C", "a twist"),
]

def say(text):
    safe_text = text.replace('"', '')
    os.system('espeak "{}"'.format(safe_text))

def do_robot_action(action_name):
    if action_name == "a spin":
        crawler.do_action('turn left', 2, 60)
    elif action_name == "a dance":
        crawler.do_action('turn right angle', 2, 60)
        crawler.do_action('turn left angle', 2, 60)
    elif action_name == "a twist":
        crawler.do_action('turn left angle', 1, 60)
        crawler.do_action('turn right angle', 1, 60)

def main():
    try:
        crawler.do_step('stand', 40)
        sleep(1)

        for _ in range(3):
            target, robot_action = random.choice(challenges)

            line = f"Can you touch {target} before I do {robot_action}?"
            print(line)
            say(line)
            sleep(0.5)

            do_robot_action(robot_action)
            sleep(1)

            say("Nice try! Ready for the next round?")
            sleep(1.5)

    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print("Error:", e)
    finally:
        crawler.do_step('sit', 40)
        sleep(1)

if __name__ == "__main__":
    main()
