#!/usr/bin/env node

/**
 * Module dependencies and variables
 */
let app             = require('../app');
let commentApp      = require('../app2');
const KBApp         = require('axios');
const VideoApp      = require('axios');
let debug           = require('debug')('websportserver:server');
let http            = require('http');
let WebSocketServer = require('websocket').server;
let connections     = [];
let old_comment     = null;
let new_comment     = null;
const WSIP          = 'localhost';
const commentIP     = 'localhost';
const KBIP          = 'localhost';
// const video_url     = 'http://localhost:3000/video_url';
const url_video     = 'http://localhost:3000';
const url_match     = 'http://localhost/match';
const url_login     = 'http://localhost/user/login';
const url_user      = 'http://localhost/user/';
const config = {
    headers: {
        'Content-Type': 'application/json'
    }
};



/**
 * Get port from environment and store in Express.
 */
let webSocketPort   = normalizePort(process.env.PORT || '4000');
let commentPort     = normalizePort(process.env.PORT || '3003');
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
  debug('Listening on ' + commentPort);
}

/**
 * Event listener for WebSocket server "listening" event.
 */
wsServer.on('request', function(request) {
  console.log("New web socket connection");
  let connection = request.accept(null, request.origin);
  connections.push(connection);
  // console.log(connection);
  connection.on('message', function(message) {
    // on message received
    if (message.type === 'utf8') {
      // if it is a string we can read as usual
      console.log('the message received is:\n' + message.utf8Data);
      handleClientMessage(message.utf8Data, connection);
    }
  }).on('close', function(event) {
    console.log("Web socket connection closed");
    // remove the closed connection
    connections.splice(connections.indexOf(connection));
  });
});

commentApp.post("/", function (req, res) {
  console.log("New comment");
  console.log(req.body);
  new_comment = JSON.parse(JSON.stringify(req.body));
  // if (connections.length !== 0) {
  //   for (let i = 0; i < connections.length; i++) {
  //     console.log("Broadcast to clients");
  //     connections[i].send(JSON.stringify(req.body));
  //   }
  //
  // }
  res.sendStatus(200);
  sendComment();
});


/**
 * Utils functions
 */

function sendComment() {
    if (old_comment == null) {
        for (let i = 0; i < connections.length; i++) {
            console.log("Broadcast to clients");
            connections[i].send(JSON.stringify(new_comment));
        }
         old_comment = new_comment;
    }
    else {
        if (overlaps(old_comment, new_comment)) {
            console.log(overlaps(old_comment, new_comment));
            if (!checkPriority(old_comment, new_comment)) {
                for (let i = 0; i < connections.length; i++) {
                    console.log("Broadcast to clients");
                    connections[i].send(JSON.stringify(new_comment));
                }
                old_comment = new_comment;
            }
        } else {
            for (let i = 0; i < connections.length; i++) {
                console.log("Broadcast to clients");
                connections[i].send(JSON.stringify(new_comment));
            }
            old_comment = new_comment;
        }
    }
}

function overlaps(comment1, comment2) {
    return comment1.startTime >= comment2.startTime && comment1.startTime <= comment2.endTime ||
        comment2.startTime >= comment1.startTime && comment2.startTime <= comment1.endTime;
}

function checkPriority(comment1, comment2) {
    return comment1.priority >= comment2.priority;
}

function handleClientMessage(body, connection) {


    let response = {
        reply_type:'',
        reply:''
    };

    let message = JSON.parse(body);

    if (message.request_type === "user_login") {

        KBApp.post(url_login, body.request, config)
            .then((result) => {
                response.reply_type = "user_login";
                response.reply = result.data;
                if (result.readyState === 4 && result.status === 200) {
                    connection.send(response)
                }else{
                    connection.send(response);
                    console.log("Email or password are wrong");
                }
            })
            .catch((err) => {
                console.log(err);
                response.reply=err;
                connection.send(response)
            })
    }

    else if (message.request_type === "user_registration"){
        KBApp.post(url_user,body.request,config)
            .then((result) => {
                response.reply_type = "user_registration";
                response.reply = result.data;
                if (result.readyState === 4 && result.status === 200) {
                    connection.send(response);
                }else{
                    connection.send(response);
                    console.log("Can't register user, email already present");
                }
            })
            .catch((err) => {
                console.log(err);
                response.reply=err;
                connection.send(response);
            })
    }

    else if (message.request_type === "user_update"){

        KBApp.post(url_user,body.request,config)
            .then((result) => {
                response.reply_type = "user_update";
                response.reply = result.data;
                if (result.readyState === 4 && result.status === 200) {
                    connection.send(response);
                }else{
                    connection.send(response);
                    console.log("User not found");
                }
            })
            .catch((err) => {
                console.log(err);
                response.reply=err;
                connection.send(response);
            })
    }

    else if (message.request_type === "get_video"){

        VideoApp.get(url_video)
            .then(result => {

                if (result.readyState === 4 && result.status === 200) {
                    console.log(response.data.url);
                    response.reply_type = "get_video";
                    response.reply = result.data;
                    connection.send(response);
                }else {
                    console.log("Video not found")
                }
            })
            .catch(error => {
                console.log(error);
                response.reply_type="get_video";
                response.reply=error;
                connection.send(response);
            });

    }

    else if(message.request_type === "get_matchID"){
        let home = message.request.home;
        let away = message.request.away;
        let date = message.request.date;
        KBApp.post(url_match+"/"+home+"/"+away+"/"+"/"+date,body.request,config)
            .then((result) => {
                console.log("Match_ID arrived, now sending to Video Group");
                response.reply_type = "get_matchID";
                response.reply = result.data;
                if (result.readyState === 4 && result.status === 200) {
                    let video_post = {
                        match_id: response.reply.id,
                        match_url:message.request.url
                    };
                    VideoApp.post(url_video, video_post, config )
                        .then((result_video)=>{
                            if (result_video.readyState === 4 && result_video.status === 200) {
                                response.reply = result_video.data;
                                connection.send(response);
                            }else{
                                console.log("Fail send Match ID to video Group")
                            }
                        })
                        .catch((err_video)=>{
                            console.log(err_video);
                            console.log("Catch: Fail send Match ID to video Group")
                        });
                }else{
                    connection.send(response);
                    console.log("Match ID not found")
                }
            })
            .catch((err) => {
                console.log("Catch: Match ID not found");
                console.log(err);
                response.reply=err;
                connection.send(response);
            })
    }
}