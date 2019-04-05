module.exports = class Track {
    constructor() {
        this.tracks = [];
    }
    addTrack(track) {
        this.tracks.push(track);
    }
};