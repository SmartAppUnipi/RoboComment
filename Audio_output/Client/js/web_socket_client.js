// const url        = 'ws://localhost:4020';
const url        = 'ws://131.114.137.237:4020';
let queue        = new Queue();
let ws           = null;
let AlreadySend1 = false;
let AlreadySend2 = false;

function insertCards(id, url, home, away, type) {

    let card = document.createElement("div");
    card.className = "card";
    let videoChild = document.createElement("video");
    videoChild.className = "videoCard";
    videoChild.src = url;
    videoChild.metadata = id;
    videoChild.type ="video/mp4";
    // videoChild.poster = "../assets/image/pic11.jpg";


    let card_body1 = document.createElement("div");
    card_body1.className = "card-body";
    let card_body2 = document.createElement("div");
    card_body2.className = "card-body";


    let card_title = document.createElement("div");
    card_title.className = "card-title";
    card_title.textContent = home + " VS " + away ;
    let card_desc  = document.createElement("div");
    card_desc.className = "card-desc";
    card_desc.textContent = type;

    card.appendChild(videoChild);
    card.appendChild(card_body1);
    card.appendChild(card_body2);
    card_body2.appendChild(card_title);
    card_body2.appendChild(card_desc);


    document.getElementById('Cards').appendChild(card);

    card.addEventListener('click', (event) => {

        let id = card.childNodes[0].metadata;
        let url = card.childNodes[0].src;
        let type = card.childNodes[2].childNodes[1].textContent;
        console.log(card.childNodes[0].src);
        console.log(card.childNodes[0].metadata);


        console.log(set_matchInfo(id,url, ifCookie("userId")));
        // sendInfoVideo(set_matchInfo(id,url, ifCookie("userId"), type));

        setCookie("videoID",id,2);
        setCookie("videoURL",url,2);
        setCookie("videoType",type,2);
        window.location.href = "video.html";

    });

}

function connect() {
    ws = new WebSocket(url);
    ws.onopen = function() {
        // subscribe to some channels
        ws.send(JSON.stringify("New Connection"));
        userHello();
        if (window.location.pathname.split("/").pop() === "catalog.html"){
            if(!AlreadySend2){
                videoListRequest();
                AlreadySend2 = true;
            }
        }else if(window.location.pathname.split("/").pop() === "video.html"){
            if(!AlreadySend1){
                console.log("Sending information about the video to Comment Group");
                sendInfoVideo(set_matchInfo(getCookie("videoID"),getCookie("videoURL"),
                    ifCookie("userId"), getCookie("videoType")));
                AlreadySend1 = true;
            }
        }

        console.log("Web Socket connection established")
    };

    ws.onmessage = function(e) {
        // console.log("Message: "+e.data);
        let message = JSON.parse(e.data);
        switch (message.reply_type) {
            case "comment":
                try {
                    let freshComment = new CommentOBJ(message.reply, new XMLHttpRequest(),0);
                    checkFlagAudio(freshComment);
                    queue.enqueue(freshComment);
                } catch {
                    console.log("Comment is not received, Message is:: ", e.data);
                }
                break;

            case "user_login":
                console.log("login reply: "+message.reply.id);
                if (message.status === 400)
                    showSnack("Login failed");
                else if (message.status === 200) {
                    console.log("Login ok:");
                    setCookie("userId", message.reply.id, 15*24);
                    console.log(ifCookie("userId"));
                    window.location.href = "catalog.html";
                    console.log("User ID: "+ message.reply.id);
                }
                break;

            case "user_registration":
                console.log("registration reply: "+message.status);
                if (message.status === 400)
                    showSnack("Registration failed");
                else if (message.status === 200) {
                    showSnack("Registration confirmed, log in!");
                    if (ifCookie('userId') !== 0)
                        setCookie("userID", message.reply.id, 15*24);
                    console.log("Registration ok, id = " + message.reply.id);
                    login();
                }
                break;

            case "get_videoList":
                console.log("Result of video list");
                // console.log(message.reply);
                let videoList = message.reply.urls;
                for (let i = 0; i < videoList.length; i++) {
                    // console.log(videoList[i]);
                    insertCards(videoList[i].id, videoList[i].url, videoList[i].home, videoList[i].away, videoList[i].type);
                }
                break;

            case "post_matchID":
                console.log("Sent info match");
                console.log(message.reply);
                break;

            default:
                console.log("Unknown reply");
                console.log(message.reply_type);
                break;
        }
    };

    ws.onclose = function(e) {
        console.log('Socket is closed. Reconnect will be attempted in 5 m.second.', e.reason);
        setTimeout(function() {
            connect();
        }, 500);
    };

    ws.onerror = function(err) {
        console.error('Socket encountered error: ', err.message, 'Closing socket');
        ws.close();
    };
}

function set_matchInfo(match_id, url, user_id, type) {

    let start_time;
    if(type==="realtime"){
        // start_time = Math.floor(Math.random() * 20);
        start_time = 0;
    }else {
        start_time = 0;
    }

    return {
        match_id: match_id,
        match_url: url,
        user_id: user_id,
        start_time: start_time
    };
}

connect();