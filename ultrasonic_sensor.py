# adapted from https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
import time
import RPi.GPIO as GPIO

SPEED_OF_SOUND = 13503.9 # inches per second

GPIO_TRIGGER = 17
GPIO_ECHO = 27


class UltrasonicSensor:
    def __init__(self, trigger, echo, poll_time):
        self.trigger = trigger
        self.echo = echo
        self.poll_time = poll_time

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def distance(self):
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)

        start_time = time.perf_counter()
        GPIO.wait_for_edge(self.echo, GPIO.FALLING)
        end_time = time.perf_counter()

        elapsed = end_time - start_time

        round_trip_distance = elapsed * SPEED_OF_SOUND
        return round_trip_distance / 2

if __name__ == '__main__':
    try:
        def print_distance(distance):
            print("distance: {}".format(distance))

        sensor = UltrasonicSensor(
            trigger=GPIO_TRIGGER,
            echo=GPIO_ECHO,
            poll_time=1,
        )

    finally:
        GPIO.cleanup()
