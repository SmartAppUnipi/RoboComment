const url        = 'ws://localhost:4020';
let queue        = new Queue();
let ws = null;

function insertCards(id, url) {
    console.log("ID video: "+id+ " and URL video: "+ url);
    let video = document.getElementById('video');
    video.src = url;
    video.type ="video/mp4";
    //TODO: just a demo, here the cards have to be populated
}

function connect() {
    ws = new WebSocket(url);
    ws.onopen = function() {
        // subscribe to some channels
        ws.send(JSON.stringify("New Connection"));
        userHello();
        videoListRequest();
        console.log("Web Socket connection established")
    };

    ws.onmessage = function(e) {
        console.log("Message: "+e.data);
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
                    showSnack("Login failed");
                else if (message.status === "200") {
                    console.log("Login ok:");
                    setCookie("userId", message.reply.id, 15);
                    console.log(getCookie("userId"));
                    window.location.href = "index.html";
                    console.log(message.reply.id);
                }
                break;

            case "user_registration":
                console.log("registration reply");
                if (message.status === "400")
                    showSnack("Registration failed");
                else if (message.status === "200") {
                    showSnack("Registration confirmed, log in!");
                    if (getCookie('userId') !== "")
                        setCookie("userID", message.reply.id);
                    console.log("Registration ok, id = " + message.reply.id);
                    login();
                }
                break;

            case "get_videoList":
                if (window.location.pathname.split("/").pop() === "index.html") {
                    console.log("Result of video list");
                    console.log(message.reply);
                    let videoList = message.reply.urls;
                    for (let i = 0; i < videoList.length; i++) {
                        console.log(videoList[i])
;                        insertCards(videoList[i].id, videoList[i].url);
                    }
                }
                else
                    console.log("bad html page check");
                break;

            case "get_infoMatch":
                console.log("Info of the Matches");
                console.log(message.reply);
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