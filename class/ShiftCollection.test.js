const ShiftCollection = require('./ShiftCollection');
const _ = require('lodash');

const Moment = require('moment');
const MomentRange = require('moment-range');

const moment = MomentRange.extendMoment(Moment);

describe('Shift Collection', () => {

    let shiftCollection;

    beforeEach(() => {
        shiftCollection = new ShiftCollection();

        shiftCollection
            .createShift({
                gopherId: 0,
                from: '2018-01-01 08:00',
                to: '2018-01-01 16:00',
            })
            .createShift({
                gopherId: 1,
                from: '2018-01-01 12:00',
                to: '2018-01-01 14:00',
            });
    });


    it('should gave some ID', () => {
        expect(shiftCollection.getAllShifts()[0].getId()).toBe(0);
        expect(shiftCollection.getAllShifts()[1].getId()).toBe(1);
    });

    it('should return two elements', () => {
        const result = shiftCollection
            .findShiftsClosedInPeriod('2018-01-01 13:00', '2018-01-01 13:30');

        const result2 = shiftCollection
            .findShiftsClosedInPeriod('2018-01-01 07:00', '2018-01-01 13:30');

        const result3 = shiftCollection
            .findShiftsClosedInPeriod('2018-01-01 13:00', '2018-01-01 23:30');

        const result4 = shiftCollection
            .findShiftsClosedInPeriod('2018-01-01 07:00', '2018-01-01 23:30');

        expect(result.length).toBe(2);
        expect(result2.length).toBe(2);
        expect(result3.length).toBe(2);
        expect(result4.length).toBe(2);
    });
});