
const url        = 'ws://10.101.15.48:4000';
let queue        = new Queue();

function connect() {
    let ws = new WebSocket(url);
    ws.onopen = function() {
        // subscribe to some channels
        ws.send(JSON.stringify("New Connection"));
        console.log("Web Socket connection established")
    };

    ws.onmessage = function(e) {
        console.log(e.data);
        try {
            let obj = JSON.parse(e.data);
            queue.enqueue(obj);
        } catch {
            console.log("Object is not received, Message is:: ", e.data);
        }

};

    ws.onclose = function(e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
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