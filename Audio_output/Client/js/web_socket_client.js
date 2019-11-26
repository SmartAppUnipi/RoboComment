// const url        = 'ws://10.101.15.48:4000';
const url        = 'ws://localhost:4000';
let queue        = new Queue();
let ws = null;

function connect() {
    ws = new WebSocket(url);
    ws.onopen = function() {
        // subscribe to some channels
        ws.send(JSON.stringify("New Connection"));
        console.log("Web Socket connection established")
    };

    ws.onmessage = function(e) {
        let message = JSON.parse(e.data);
        console.log(message);
        switch (message.replyType) {
            case "comment":
                try {
                    queue.enqueue(new CommentOBJ(message.reply, new XMLHttpRequest(),0));
                } catch {
                    console.log("Comment is not received, Message is:: ", e.data);
                }
                break;
            case "user_login":
                console.log("login reply: "+message.reply);
                break;
            case "user_registration":
                console.log("registration reply");
                break;
            default:
                console.log("Unknown reply");
                break;
        }



    };

    ws.onclose = function(e) {
        console.log('Socket is closed. Reconnect will be attempted in 5 second.', e.reason);
        setTimeout(function() {
            connect();
        }, 500);
    };

    ws.onerror = function(err) {
        console.error('Socket encountered error: ', err.message, 'Closing socket');
        ws.close();
    };
}

connect();