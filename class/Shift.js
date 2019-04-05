const moment = require('moment');

module.export = class Shift {
    consturctor({gopherId, avalaibleFrom, avalaibleTo}) {
        this.id = gopherId;
        this.avalaibleFrom = avalaibleFrom;
        this.avalaibleTo = avalaibleTo;
    }
};