import * as rpio from 'rpio';
import { usleep } from 'sleep';
import { getDiffieHellman } from 'crypto';
import { ENGINE_METHOD_DIGESTS } from 'constants';

const SPEED_OF_SOUND = 1.35039e-5; // speed of sound in inches per nanosecond

type pin = { id: string, trigger: number, echo: number };
const PINS : pin[] = [
    {
        id: 'front',
        trigger: 17,
        echo: 27,
    },
    // {
    //     id: 'back',
    //     trigger: 27,
    //     echo: 22,
    // },
];

console.log('initializing');
rpio.init({mapping: 'gpio'}); 

PINS.forEach(({ trigger, echo }) => {
    rpio.open(trigger, rpio.OUTPUT, rpio.LOW);
    rpio.open(echo, rpio.INPUT);
});

const getDistance = ({ trigger, echo }: pin) => {
    rpio.write(trigger, rpio.HIGH);
    usleep(1000);
    rpio.write(trigger, rpio.LOW);

    while (rpio.read(echo) === 0);
    const start = process.hrtime();
    while (rpio.read(echo) === 1);
    const [seconds, nanoseconds] = process.hrtime(start);
    const distance = (seconds * 1e9 + nanoseconds) * SPEED_OF_SOUND;

    return distance / 2;
}

process.on('SIGINT', function() {
    console.log('exiting...');

    PINS.forEach(({ trigger, echo }) => {
        rpio.close(trigger);
        rpio.close(echo);
    });

    process.exit();
});

const getDistanceRecursive = () => {
    console.log('logging');
    console.log(getDistance(PINS[0]));
    process.nextTick(getDistanceRecursive);
}
getDistanceRecursive();

