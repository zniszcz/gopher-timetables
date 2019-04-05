const moment = require('moment');

module.exports = class Gopher {
    constructor({id, name, avalaibleFrom, avalaibleTo}) {
        this.id = id;
        this.name = name;
        this.avalaibleFrom = avalaibleFrom;
        this.avalaibleTo = avalaibleTo;
    }
};