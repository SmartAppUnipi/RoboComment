const url        = 'ws://10.101.52.39:4000';
// const url        = 'ws://localhost:4000';
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
        console.log(e.data);
        try {
            queue.enqueue(new CommentOBJ(JSON.parse(e.data),new XMLHttpRequest(),0));
        } catch {
            console.log("Comment is not received, Message is:: ", e.data);
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