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
        while GPIO.input(self.echo): 
            pass

        start_time = time.perf_counter()
        GPIO.output(self.trigger, True)
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
                sys.stdout.write('\rdist: {:06.10f} avg: {:06.10f}'.format(dist, avg))

            if not entered and avg < THRESHOLD:
                entered = True
                if on_enter:
                    on_enter()
            elif entered and avg > THRESHOLD:
                entered = False
                if on_exit:
                    on_exit()
            time.sleep(poll_time)


def poll_two(sensor1, sensor2):
    while True:
        dist1 = sensor1.distance()
        time.sleep(0.1)
        dist2 = sensor2.distance()

        sys.stdout.write('\r {:06.10f} : {:06.10f}'.format(dist1, dist2))

        time.sleep(0.1)


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
    sensor2 = UltrasonicSensor(
        trigger=13,
        echo=19,
    )

    poll_two(sensor, sensor2)

    # sensor.poll(
    #     poll_time=.01,
    #     on_enter=lambda: print('entered!'),
    #     on_exit=lambda: print('exited'),
    # )
