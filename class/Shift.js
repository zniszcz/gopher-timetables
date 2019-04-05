const moment = require('moment');

module.exports = class Shift {
    constructor({id, gopherId, avalaibleFrom, avalaibleTo}) {
        this.id = id;
        this.gopherId = gopherId;
        this.avalaibleFrom = avalaibleFrom;
        this.avalaibleTo = avalaibleTo;
    }

    getId() {
        return this.id;
    }
};