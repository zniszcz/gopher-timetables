const Moment = require('moment');
const MomentRange = require('moment-range');

const moment = MomentRange.extendMoment(Moment);

module.exports = class Shift {
    constructor({id, gopherId, from, to}) {
        this.id = id;
        this.gopherId = gopherId;
        this.from = from;
        this.to = to;
    }

    getId() {
        return this.id;
    }

    getRange() {
        const from = moment(this.from);
        const to = moment(this.to);

        return moment.range(from, to);
    }
};