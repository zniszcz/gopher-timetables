const moment = require('moment');

module.exports = class Track {
    constructor({gopherId, avalaibleFrom, avalaibleTo}) {
        this.id = gopherId;
        this.avalaibleFrom = avalaibleFrom;
        this.avalaibleTo = avalaibleTo;
    }
};