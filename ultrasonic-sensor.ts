import * as rpio from 'rpio';
import { usleep } from 'sleep';

const timeout = (ms: number) : Promise<void> => 
    new Promise((resolve: (() => void)) => setTimeout(resolve, ms));

type pin = { id: string, input: number, output: number };
const PINS : pin[] = [
    {
        id: 'front',
        input: 4,
        output: 17,
    },
    {
        id: 'back',
        input: 27,
        output: 22,
    },
];

PINS.forEach(({ input, output }) => {
    rpio.open(input, rpio.INPUT);
    rpio.open(output, rpio.OUTPUT, rpio.LOW);
});

const getDistance = ({ input, output}: pin) => {
    rpio.write(input, rpio.HIGH);
    usleep(1);
    rpio.write(input, rpio.LOW);

    while (rpio.read(input) === 0);
    const start = process.hrtime();
    while (rpio.read(input) === 1);
    const [seconds, nanoseconds] = process.hrtime(start);
    const distance = (seconds * 1e9 + nanoseconds) * 3.43e-5;

    return distance / 2;
}

while (true) {
    console.log(getDistance(PINS[0]));
}