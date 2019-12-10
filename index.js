const Moment = require('moment');
const MomentRange = require('moment-range');

const moment = MomentRange.extendMoment(Moment);

const A = moment('2018-01-01 08:00');
const B = moment('2018-01-31 16:00');

const a = moment('2018-01-31 08:00');
const b = moment('2018-01-10 16:05');

const bigRange = moment.range(A, B);
const smallRange = moment.range(a, b);

console.log(bigRange.contains(smallRange));