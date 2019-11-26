class ConnectionUser {
    constructor(socket, id) {
        this.socket      = socket;
        this.id          = id;
        this.new_comment = null;
        this.old_comment = null;
    }
}