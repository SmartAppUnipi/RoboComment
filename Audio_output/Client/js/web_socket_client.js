// const url        = 'ws://10.101.15.48:4000';
const url        = 'ws://10.101.18.19:4000';
let queue        = new Queue();
let ws = null;

function connect() {
    ws = new WebSocket(url);
    ws.onopen = function() {
        // subscribe to some channels
        ws.send(JSON.stringify("New Connection"));
        userHello();
        console.log("Web Socket connection established")
    };

    ws.onmessage = function(e) {
        console.log(e.data);
        let message = JSON.parse(e.data);
        switch (message.reply_type) {
            case "comment":
                try {
                    queue.enqueue(new CommentOBJ(message.reply, new XMLHttpRequest(),0));
                } catch {
                    console.log("Comment is not received, Message is:: ", e.data);
                }
                break;
            case "user_login":
                console.log("login reply: "+message.reply.id);
                if (message.status === "400")
                    alert("Login failed");
                else if (message.status === "200") {
                    console.log("Login ok:");
                    setCookie("userId", message.reply.id);
                    console.log(getCookie("userId"));
                    window.location.href = "cards.html";
                    console.log(message.reply.id);
                }
                break;
            case "user_registration":
                console.log("registration reply");
                if (message.status === "400")
                    alert("Registration failed");
                else if (message.status === "200") {
                    console.log("Registration ok, id = " + message.reply.id);
                    login();
                }
                break;
            default:
                console.log("Unknown reply");
                console.log(message.reply_type);
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