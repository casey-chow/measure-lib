# adapted from https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
from threading import Thread
import time
import RPi.GPIO as GPIO

SPEED_OF_SOUND = 13503.9 # inches per second

GPIO_TRIGGER = 17
GPIO_ECHO = 27

GPIO.setmode(GPIO.BCM)

class DistanceMeasurementWorker(Thread):
    def __init__(self, trigger, echo, poll_time, cb):
        Thread.__init__(self)
        self.trigger = trigger
        self.echo = echo
        self.poll_time = poll_time
        self.cb = cb

        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def run(self):
        while True:
            dist = self.distance()
            self.cb(distance)
            time.sleep(self.poll_time)

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
        print_distance = lambda distance: print("distance: {}".format(distance))

        worker = DistanceMeasurementWorker(
            trigger=GPIO_TRIGGER,
            echo=GPIO_ECHO,
            poll_time=1,
            cb=print_distance,
        )
        worker.start()

    finally:
        GPIO.cleanup()