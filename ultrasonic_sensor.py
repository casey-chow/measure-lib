# adapted from https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
import time
import signal
import sys
import numpy as np
import RPi.GPIO as GPIO

from ring_buffer import RingBuffer

DEBUG = True

SPEED_OF_SOUND = 13503.9 # inches per second

GPIO_TRIGGER = 4
GPIO_ECHO = 17

THRESHOLD = 40

class UltrasonicSensor:
    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def distance(self):
        GPIO.output(self.trigger, True)
        start_time = time.perf_counter()
        time.sleep(0.0001)
        GPIO.output(self.trigger, False)

        GPIO.wait_for_edge(self.echo, GPIO.FALLING, timeout=100)
        end_time = time.perf_counter()

        elapsed = end_time - start_time

        round_trip_distance = elapsed * SPEED_OF_SOUND
        return round_trip_distance / 2

    def poll(self, poll_time, on_enter=None, on_exit=None):
        print('starting polling')
        history = RingBuffer(capacity=20, dtype=np.float)
        entered = False
        while True:
            dist = self.distance()
            history.append(dist)

            if len(history) < 10:
                continue

            avg = np.median(history)
            if DEBUG:
                sys.stdout.write('\rdist: {} avg: {}'.format(dist, avg))

            if not entered and avg < THRESHOLD:
                entered = True
                if on_enter:
                    on_enter()
            elif entered and avg > THRESHOLD:
                entered = False
                if on_exit:
                    on_exit()
            time.sleep(poll_time)


if __name__ == '__main__':
    def signal_handler(sig, frame):
        print()
        GPIO.cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    time.sleep(1)

    sensor = UltrasonicSensor(
        trigger=GPIO_TRIGGER,
        echo=GPIO_ECHO,
    )

    sensor.poll(
        poll_time=.01,
        on_enter=lambda: print('entered!'),
        on_exit=lambda: print('exited'),
    )
