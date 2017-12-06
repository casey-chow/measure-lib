# Adapted from https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
import RPi.GPIO as GPIO
import time

SPEED_OF_SOUND = 13503.9 # inches per second

GPIO_TRIGGER = 17
GPIO_ECHO = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance(trigger, echo):
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)
 
    while GPIO.input(echo) == 0:
        pass
    start_time = time.perf_counter()

    while GPIO.input(echo) == 1:
        pass
    end_time = time.perf_counter()

    elapsed = end_time - start_time

    round_trip_distance = elapsed * SPEED_OF_SOUND
    return round_trip_distance / 2


if __name__ == '__main__':
    try:
        while True:
            dist = distance(GPIO_TRIGGER, GPIO_ECHO)
            print("distance: {}".format(dist))
            time.sleep(1)
    # reset by pressing CTRL + C
    except KeyboardInterrupt:
        GPIO.cleanup()