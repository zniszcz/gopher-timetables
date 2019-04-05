const ShiftCollection = require('./ShiftCollection');
const shiftCollection = new ShiftCollection();

describe('Shift Collection', () => {

    it('should have some ID', () => {
        shiftCollection
            .createShift({
                gopherId: 0,
                avalaibleFrom: 22,
                avalaibleTo: 23,
            })
            .createShift({
                gopherId: 0,
                avalaibleFrom: 22,
                avalaibleTo: 23,
            });

        expect(shiftCollection.getAllShifts()[0].getId()).toBe(0);
        expect(shiftCollection.getAllShifts()[1].getId()).toBe(1);
    });
});