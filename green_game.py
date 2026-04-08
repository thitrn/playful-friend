from picrawler import Picrawler
from vilib import Vilib
from time import sleep, time
import os

crawler = Picrawler()

def say(text):
    safe_text = text.replace('"', '')
    os.system('espeak "{}"'.format(safe_text))

def main():
    try:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=True)

        Vilib.color_detect("green")

        crawler.do_step('stand', 40)
        sleep(1)

        say("Come in front of me wearing green before I finish moving!")
        sleep(1)

        start_time = time()
        detected = False

        while time() - start_time < 8:
            crawler.do_action('turn left', 1, 60)

            n = Vilib.detect_obj_parameter.get('color_n', 0)
            w = Vilib.detect_obj_parameter.get('color_w', 0)

            print("green patches:", n, "width:", w)

            if n > 0 and w > 100:
                detected = True
                break

            sleep(0.2)

        crawler.do_step('stand', 40)

        if detected:
            say("You win!")
        else:
            say("Too slow! I win this round!")

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
            crawler.do_step('sit', 40)
        except:
            pass
        sleep(1)

if __name__ == "__main__":
    main()
