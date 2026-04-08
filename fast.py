from picrawler import Picrawler
from time import sleep

crawler = Picrawler()

def main():
    try:
        print("Standing up...")
        crawler.do_step('stand', 40)
        sleep(1)

        print("Fast forward burst")
        crawler.do_action('forward', 2, 80)
        sleep(0.4)

        print("Fast backward burst")
        crawler.do_action('backward', 2, 80)
        sleep(0.4)

        print("Fast left turn")
        crawler.do_action('turn left', 2, 85)
        sleep(0.4)

        print("Fast right turn")
        crawler.do_action('turn right', 2, 85)
        sleep(0.4)

        print("Quick zig zag")
        crawler.do_action('forward', 1, 75)
        sleep(0.15)
        crawler.do_action('turn left angle', 1, 80)
        sleep(0.15)
        crawler.do_action('forward', 1, 75)
        sleep(0.15)
        crawler.do_action('turn right angle', 1, 80)
        sleep(0.15)
        crawler.do_action('forward', 1, 75)
        sleep(0.15)
        crawler.do_action('turn left angle', 1, 80)
        sleep(0.15)

        print("Spin burst")
        crawler.do_action('turn left', 3, 90)
        sleep(0.4)

        print("Done. Standing still...")
        crawler.do_step('stand', 40)
        sleep(1)

    except KeyboardInterrupt:
        print("Stopped by user.")

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
