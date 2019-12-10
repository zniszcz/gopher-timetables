module.exports = class Plan {
    constructor() {
        this.tracks = [];
    }
    addTrack(track) {
        this.tracks.push(track);
    }
};