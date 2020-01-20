#!/usr/bin/env node

/**
 * Module dependencies and variables
 */
let app              = require('../app');
let commentApp       = require('../app2');
let debug            = require('debug')('websportserver:server');
let http             = require('http');
let WebSocketServer  = require('websocket').server;
let connections      = [];
let connectionUser   = require('../connectionClass');

const KBApp          = require('axios');
const VideoApp       = require('axios');
const CommentaryApp  = require('axios');
const routes         = require('../../../routes.json');
const video_list     = require('../../videolist');

// Ui
const WSIP           = routes.ui.toString().split(":")[1].split("/")[2];
const WS_PORT        = routes.ui.toString().split(":")[2].split("/")[0];

//Fabula
const commentIP      = routes.fabula.toString().split(":")[1].split("/")[2];
const COMMENT_PORT   = routes.fabula.toString().split(":")[2].split("/")[0];

// Commentary Session
const CommentAppIP   = routes.commentary_session;

const kb_url         = routes.qi;
const url_video      = routes.video;

let url_login        = kb_url + "users/login";
let url_user         = kb_url + "users";
let url_match        = kb_url + "/match/";

const DEBUGERR       = false;
const DEBUG_MODE     = false;
const config = {
    headers: {
        'Content-Type': 'application/json'
    }
};


/**
 * Get port from environment and store in Express.
 */
let webSocketPort   = normalizePort(process.env.PORT || WS_PORT);
let commentPort     = normalizePort(process.env.PORT || COMMENT_PORT);
app.set('port', webSocketPort);
commentApp.set('port', commentPort);


/**
 * Create HTTP server for websocket
 */

let server = http.createServer(app);
wsServer = new WebSocketServer({
    httpServer: server
});

/**
 * Listen on provided port, on all network interfaces.
 */
server.listen(webSocketPort, WSIP);
commentApp.listen(commentPort, commentIP, onListeningComment);
server.on('error', onError);
server.on('listening', onListening);

/**
 * Normalize a port into a number, string, or false.
 */
function normalizePort(val) {
    let port = parseInt(val, 10);
    if (isNaN(port)) {
        // named pipe
        return val;
    }
    if (port >= 0) {
        // port number
        return port;
    }
    return false;
}

/**
 * Event listener for HTTP server "error" event.
 */
function onError(error) {
    if (error.syscall !== 'listen') {
        throw error;
    }

    let bind = typeof webSocketPort === 'string'
        ? 'Pipe ' + webSocketPort
        : 'Port ' + webSocketPort;

    // handle specific listen errors with friendly messages
    switch (error.code) {
        case 'EACCES':
            console.error(bind + ' requires elevated privileges');
            process.exit(1);
            break;
        case 'EADDRINUSE':
            console.error(bind + ' is already in use');
            process.exit(1);
            break;
        default:
            throw error;
    }
}

/**
 * Event listener for HTTP server "listening" event.
 */
function onListening() {
    let addr = server.address();
    let bind = typeof addr === 'string'
        ? 'pipe ' + addr
        : 'port ' + addr.port;
    console.log('Listening on ' + bind);
}

/**
 * Event listener for HTTP server "listening" event.
 */
function onListeningComment() {
    debug('Listening on ' + commentPort + " for Fabula");
}

/**
 * Event listener for WebSocket server "listening" event.
 */
wsServer.on('request', function(request) {
    console.log("New web socket connection");
    let connection = request.accept(null, request.origin);

    connection.on('message', function(message) {
        // on message received
        if (message.type === 'utf8') {
            // if it is a string we can read as usual
            console.log('the message received is:\n' + message.utf8Data);
            handleClientMessage(message.utf8Data, connection);
        }
    }).on('close', function(event) {
        // remove the closed connection

        for(let i=0; i<connections.length; i++){
            if(connections[i].socket === connection){
                console.log("Web socket connection closed of the user: " + connections[i].id);
                if (connections[i].user_page === "video.html"){
                    // console.log("Sending DELETE to the comment group for the user id: " + connections[i].id);
                    // CommentaryApp.delete(CommentAppIP+"/"+ connections[i].id.toString())
                    //     .then((result) => {})
                    //     .catch((err) => {})
                }
                connections.splice(connections[i]);
            }
        }
    });
});

commentApp.post("/", function (req, res) {
    console.log("New comment/position");

    // console.log(req.body);
    res.sendStatus(200);

    let comment = JSON.parse(JSON.stringify(req.body));
    if(comment.players){

        console.log("Arrived position");
        if (comment.id) {
            for(let i=0; i< connections.length; i++) {
                if(comment.id === connections[i].id){
                    sendPosition(connections[i], comment.id, req.body);
                }
            }
        }
        else {
            console.log("No id, broadcast to all");
            for (let i = 0; i < connections.length; i++) {
                sendPosition(connections[i], 0, req.body);
            }
        }

    }else if(comment.comment){

        comment.endTime = comment.startTime + estimateTime(comment.comment);
        console.log("Start-stop: "+comment.startTime + "-"+comment.endTime);

        if (comment.id) {
            for(let i=0; i< connections.length; i++) {
                if(comment.id === connections[i].id){
                    connections[i].new_comment = comment;
                    sendComment(connections[i], comment.id);
                }
            }
        }
        else {
            console.log("No id, broadcast to all");
            for(let i=0; i< connections.length; i++) {
                connections[i].new_comment = comment;
                sendComment(connections[i], 0);
            }
        }
    }

});


/**
 * Utils functions
 */

function sendComment(item, id) {

    let connection = item.socket;
    let new_comment = item.new_comment;
    let old_comment = item.old_comment;

    if (old_comment == null) {
        console.log("Broadcast to client of ID: "+ id);
        let reply = {
            reply_type: "comment",
            reply: new_comment
        };
        connection.send(JSON.stringify(reply));
        item.old_comment = new_comment;
    }
    else {
        if(!DEBUG_MODE){
            if (overlaps(old_comment, new_comment)) {
                console.log("OVERLAPS COMMENT: " + overlaps(old_comment, new_comment));
                if (!checkPriority(old_comment, new_comment)) {
                    console.log("Broadcast to client of ID: "+ id);
                    let reply = {
                        reply_type: "comment",
                        reply: new_comment
                    };
                    connection.send(JSON.stringify(reply));

                    item.old_comment = new_comment;
                }
            } else {
                console.log("Broadcast to client of ID: "+ id);
                // new_comment.endTime += 5;
                let reply = {
                    reply_type: "comment",
                    reply: new_comment
                };
                connection.send(JSON.stringify(reply));
                item.old_comment = new_comment;
            }
        }
    }
}


function sendPosition(item, id, positions) {

    let connection = item.socket;

        //console.log("Broadcast to client of ID : "+ id);
        let reply = {
            reply_type: "position",
            reply: positions
        };
        connection.send(JSON.stringify(reply));
}


function estimateTime(comment) {
    return comment.split(' ').length / 2;
}

function overlaps(comment1, comment2) {
    return comment1.startTime >= comment2.startTime && comment1.startTime <= comment2.endTime ||
        comment2.startTime >= comment1.startTime && comment2.startTime <= comment1.endTime;
}

function checkPriority(comment1, comment2) {
    return comment1.priority >= comment2.priority;
}

function handleClientMessage(body, connection) {

    let response;
    let message = JSON.parse(body);

    if (message.request_type === "user_login") {

        console.log("Sending request to KB");
        KBApp.post(url_login, JSON.stringify(message.request), config)
            .then((result) => {
                response = set_response("user_login", result.data, result.status);

                if (result.status === 200) {
                    console.log("User Login: Status OK and Sending to Client");
                    connection.send(response)
                }else{
                    connection.send(response);
                    console.log("Email or password are wrong");
                }
            })
            .catch((err) => {
                if(DEBUGERR){
                    console.log(err);
                }
                if (err.response) {
                    response = set_response("user_login", err.response.data, 400);
                    console.log("User Login: Status NOT_OK and Sending to Client: " + err.response.data);
                    connection.send(response)
                }
                else {
                    console.log(err);
                }
            })
    }

    else if (message.request_type === "user_registration"){

        KBApp.post(url_user,JSON.stringify(message.request),config)
            .then((result) => {
                response = set_response("user_registration", result.data, result.status);
                if (result.status === 200) {
                    console.log("User Registration: Status OK and Sending to Client");
                    connection.send(response);
                }else{
                    connection.send(response);
                    console.log("Can't register user, email already present");
                }
            })
            .catch((err) => {
                if(DEBUGERR){
                    console.log(err)
                }
                if (err.response) {
                    console.log(JSON.stringify(err.response.data));
                    response = set_response("user_registration", err.response.data, 400);
                    console.log("User Registration: Status NOT_OK and Sending to Client. " + err.response.data.error);
                    connection.send(response);
                }
                else {
                    console.log(err)
                }
            })
    }

    else if (message.request_type === "user_update"){

        KBApp.post(url_user,body.request,config)
            .then((result) => {
                response = set_response("user_update", result.data, result.status);
                if (result.status === 200) {
                    console.log("User Update: Status OK and Sending to Client");
                    connection.send(response);
                }else{
                    connection.send(response);
                    console.log("User not found");
                }
            })
            .catch((err) => {
                if(DEBUGERR){
                    console.log(err);
                }
                if (err.response) {
                    response = set_response("user_update", err.response.data, 400);
                    console.log("User Update: Status NOT_OK and Sending to Client");
                    connection.send(response);
                }
                else
                    console.log(err)
            })
    }

    else if(message.request_type === "post_matchID"){

        console.log("Match_ID arrived, now sending to Comment Group");

        // console.log(message.request);

        let idUser   = message.request.user_id;

        CommentaryApp.post(CommentAppIP +"/"+ idUser.toString(), JSON.stringify(message.request), config)
            .then((result) => {
                if(result.status === 200){
                    response = set_response("post_matchID","OK", result.status);
                    connection.send(response);
                }else if(result.status === 201){

                    console.log("Video not in cache, now sending to Video Group");
                    // console.log((JSON.stringify(message.request)));
                    VideoApp.post(url_video, JSON.stringify(message.request), config )
                        .then((result_video)=>{
                            console.log(result_video.status);
                            // console.log(result_video);
                            if (result_video.status === 200 || result_video.statusText === 'ok') {
                                response = set_response("post_matchID","OK", result.status);
                                connection.send(response);
                            }else{
                                console.log("Fail send Match ID to video Group")
                            }
                        })
                        .catch((err_video)=>{
                            if(DEBUGERR){
                                console.log(err_video);
                            }
                            console.log("Catch: Fail send Match ID to video Group")
                        });
                }
            });
    }

    else if(message.request_type === "get_infoMatch"){
        KBApp.get(url_match + message.request)
            .then((result) => {
                response = set_response("get_infoMatch",result.data, result.status);

                if (result.status === 200) {
                    console.log("Info match arrived, now sending to the Client");
                    connection.send(response);

                }else{
                    console.log("Match information not found. " + result.data);
                    response = set_response("get_infoMatch", result.data, 400);
                    connection.send(response);
                }
            })
            .catch((err) => {
                if (DEBUGERR){
                    console.log(err);
                }
                if (err.response) {
                    console.log("Catch: Match information not found. " + err.response.data);
                    response = set_response("get_infoMatch", err.response.data, 400);
                    connection.send(response);
                }
                else
                    console.log(err)
            })
    }

    else if(message.request_type === "hello"){
        connections.push(new connectionUser(connection, message.user_id, message.request));
    }

    else if(message.request_type === "get_videoList"){
        response = set_response("get_videoList", video_list, 200);
        console.log("Send videos list");
        connection.send(response);
    }
}

function set_response(reply_type, reply, status) {
    return JSON.stringify({
        reply_type: reply_type,
        reply: reply,
        status: status
    });
}