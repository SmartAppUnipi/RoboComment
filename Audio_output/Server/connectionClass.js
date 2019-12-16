class ConnectionUser {
    constructor(socket, id, page) {
        this.socket      = socket;
        this.id          = id;
        this.new_comment = null;
        this.old_comment = null;
        this.user_page   = page;
    }
}

module.exports = ConnectionUser;