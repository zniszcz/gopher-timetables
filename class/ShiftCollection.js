const _ = require('lodash');
const Shift = require('./Shift');
const Moment = require('moment');
const MomentRange = require('moment-range');

const moment = MomentRange.extendMoment(Moment);

module.exports = class ShiftCollection {
    constructor() {
        this.collection = [];
        this.counter = 0;
    }

    createShift({gopherId, from, to}) {
        const shift = new Shift({
            id: this.counter++,
            gopherId,
            from,
            to,
        });

        this.collection.push(shift);

        return this;
    }

    getAllShifts() {
        return this.collection;
    }

    findShiftsClosedInPeriod(from, to) {
        const askedFrom = moment(from);
        const askedTo = moment(to);
        const askedRange = moment.range(askedFrom, askedTo);
    
        return _.filter(this.collection, (shift) => 
            (askedRange.contains(shift.getRange())));
    }

    findShiftsInAllPeriods(from, to) {
        const askedFrom = moment(from);
        const askedTo = moment(to);
        const askedRange = moment.range(askedFrom, askedTo);

    }
};