const Shift = require('./Shift');

module.exports = class GopherCollection {
    constructor() {
        this.collection = [];
        this.counter = 0;
    }

    createShift({gopherId, avalaibleFrom, avalaibleTo}) {
        const shift = new Shift({
            id: this.counter++,
            gopherId,
            avalaibleFrom,
            avalaibleTo,
        });

        this.collection.push(shift);

        return this;
    }

    getAllShifts() {
        return this.collection;
    }
};