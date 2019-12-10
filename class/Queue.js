module.exports = class Queue {
    constructor({}) {
        this.steps = [];
    }
    addStep({shiftId}) {
        this.steps.push(shiftId);
    }

};