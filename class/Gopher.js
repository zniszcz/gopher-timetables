const Moment = require('moment');
const MomentRange = require('moment-range');

const moment = MomentRange.extendMoment(Moment);

module.exports = class Gopher {
    constructor({id, name, avalaibleFrom, avalaibleTo}) {
        this.id = id;
        this.name = name;
        this.avalaibleFrom = avalaibleFrom;
        this.avalaibleTo = avalaibleTo;
    }
    isAvalaibleBetween(from, to) {

    }
};