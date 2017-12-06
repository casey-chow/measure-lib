import * as rpio from 'rpio';
import { usleep } from 'sleep';
import { getDiffieHellman } from 'crypto';
import { ENGINE_METHOD_DIGESTS } from 'constants';

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

console.log('initiating...');
rpio.init({mapping: 'gpio'}); 

PINS.forEach(({ trigger, echo }) => {
    rpio.open(trigger, rpio.OUTPUT, rpio.LOW);
    rpio.open(echo, rpio.INPUT);
});
console.log('pins opened...');

const getDistance = ({ trigger, echo }: pin) => {
    rpio.write(trigger, rpio.HIGH);
    usleep(1);
    rpio.write(trigger, rpio.LOW);

    while (rpio.read(echo) === 0);
    const start = process.hrtime();
    while (rpio.read(echo) === 1);
    const [seconds, nanoseconds] = process.hrtime(start);
    const distance = (seconds * 1e9 + nanoseconds) * 3.43e-5;

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
    console.log(getDistance(PINS[0]));
    process.nextTick(getDistanceRecursive);
}
getDistanceRecursive();

