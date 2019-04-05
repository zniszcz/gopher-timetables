const ShiftCollection = require('./class/ShiftCollection');
const shiftCollection = new ShiftCollection();

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

shiftCollection.getAllShifts().forEach((obj) => {
    console.log(obj.getId());
});