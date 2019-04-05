const Gopher = require('./Gopher');

module.exports = class GopherCollection {
    constructor() {
        this.collection = [];
        this.gophersCounter = 0;
    }

    addGopher({name, avalaibleFrom, avalaibleTo}) {
        const gopher = new Gopher({
            id: this.gophersCounter++,
            name,
            avalaibleFrom,
            avalaibleTo,
        });

        this.collection.push(gopher);
    }
};