"use strict";
exports.__esModule = true;
var rpio = require("rpio");
var sleep_1 = require("sleep");
var PINS = [
    {
        id: 'front',
        trigger: 17,
        echo: 27
    },
    {
        id: 'back',
        trigger: 27,
        echo: 22
    },
];
console.log('initiating...');
rpio.init({ mapping: 'gpio' });
PINS.forEach(function (_a) {
    var trigger = _a.trigger, echo = _a.echo;
    rpio.open(trigger, rpio.OUTPUT, rpio.LOW);
    rpio.open(echo, rpio.INPUT);
});
var getDistance = function (_a) {
    var trigger = _a.trigger, echo = _a.echo;
    rpio.write(trigger, rpio.HIGH);
    sleep_1.usleep(1);
    rpio.write(trigger, rpio.LOW);
    while (rpio.read(echo) === 0)
        ;
    var start = process.hrtime();
    while (rpio.read(echo) === 1)
        ;
    var _b = process.hrtime(start), seconds = _b[0], nanoseconds = _b[1];
    var distance = (seconds * 1e9 + nanoseconds) * 3.43e-5;
    return distance / 2;
};
while (true) {
    console.log(getDistance(PINS[0]));
}
