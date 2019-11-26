#!/usr/bin/env node

/**
 * Module dependencies and variables
 */
let app             = require('../app');
let commentApp      = require('../app2');
let debug           = require('debug')('websportserver:server');
let http            = require('http');
let WebSocketServer = require('websocket').server;
let connections     = [];
let old_comment     = null;
let new_comment     = null;

const KBApp         = require('axios');
const VideoApp      = require('axios');
const routes        = require('../../routes.json');
const WSIP          = routes.ui.toString().split(":")[1].split("/")[2];
const WS_PORT       = routes.ui.toString().split(":")[2].split("/")[0];
const commentIP     = routes.fabula.toString().split(":")[1].split("/")[2];
const COMMENT_PORT  = routes.fabula.toString().split(":")[2].split("/")[0];
const kb_url        = routes.qi;
const url_video     = routes.video;
let url_login       = kb_url+"/users/login";
let url_user        = kb_url+ "/users";
console.log(COMMENT_PORT);
const DEBUGERR      = false;
const DEBUG_MODE     = true;

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
  debug('Listening on ' + commentPort);
}

/**
 * Event listener for WebSocket server "listening" event.
 */
wsServer.on('request', function(request) {
  console.log("New web socket connection");
  let connection = request.accept(null, request.origin);


  // connections.push(connection);
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

  res.sendStatus(200);

  if (new_comment.id!==0){
      for(let i=0; i< connections.length; i++) {
          if(new_comment.id === connections[i].id){
              sendComment(connections[i].socket);
          }
      }
  }
  // sendComment();
});


/**
 * Utils functions
 */

function sendComment(connection) {
    if (old_comment == null) {
        console.log("Broadcast to clients");
        let reply = {
            reply_type: "comment",
            reply: new_comment
        };
        connection.socket.send(JSON.stringify(reply));
        old_comment = new_comment;
    }
    else {
        if(!DEBUG_MODE){
            if (overlaps(old_comment, new_comment)) {
                console.log("OVERLAPS COMMENT: " + overlaps(old_comment, new_comment));
                if (!checkPriority(old_comment, new_comment)) {
                    console.log("Broadcast to clients");
                    let reply = {
                        reply_type: "comment",
                        reply: new_comment
                    };
                    connection.socket.send(JSON.stringify(reply));

                    old_comment = new_comment;
                }
            } else {
                console.log("Broadcast to clients");
                let reply = {
                    reply_type: "comment",
                    reply: new_comment
                };
                connection.socket.send(JSON.stringify(reply));
                old_comment = new_comment;
            }
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

    let response, video_response;
    let message = JSON.parse(body);

    if (message.request_type === "user_login") {

        console.log("Sending request to KB");
        KBApp.post(url_login, JSON.stringify(message.request), config)
            .then((result) => {
                response = set_response("user_login",result.data, result.status);

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
                response = set_response("user_login",JSON.stringify(err.response.data), 400);
                console.log("User Login: Status NOT_OK and Sending to Client: "+err.response.data);
                connection.send(response)
            })
    }

    else if (message.request_type === "user_registration"){

        KBApp.post(url_user,JSON.stringify(message.request),config)
            .then((result) => {
                response = set_response("user_registration",result.data, result.status);
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
                    console.log(err);
                }
                response = set_response("user_registration",JSON.stringify(err.response.data), 400);
                console.log("User Registration: Status NOT_OK and Sending to Client. "+err.response.data.error);
                connection.send(response);
            })
    }

    else if (message.request_type === "user_update"){

        KBApp.post(url_user,body.request,config)
            .then((result) => {
                response = set_response("user_update",result.data, result.status);
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
                response = set_response("user_update",JSON.stringify(err.response.data), 400);
                console.log("User Update: Status NOT_OK and Sending to Client");
                connection.send(response);
            })
    }

    else if(message.request_type === "get_matchID"){
        let home = message.request.home;
        let away = message.request.away;
        let date = message.request.date;
        KBApp.post(url_match+"/"+home+"/"+away+"/"+"/"+date,body.request,config)
            .then((result) => {
                console.log("Match_ID arrived, now sending to Video Group");
                response = set_response("get_matchID",result.data, result.status);

                if (result.status === 200) {

                    video_response = set_video_response(response.reply.id, message.request.url);
                    VideoApp.post(url_video, video_response, config )
                        .then((result_video)=>{
                            if (result_video.readyState === 4 && result_video.status === 200) {
                                response = set_response("get_matchID",result_video.data, result_video.status);
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
                }else{
                    connection.send(response);
                    console.log("Match ID not found")
                }
            })
            .catch((err) => {
                if (DEBUGERR){
                    console.log(err);
                }
                console.log("Catch: Match ID not found. "+ err.response.data);
                response = set_response("get_matchID",err.response.data, 400);
                connection.send(response);
            })
    }

    else if(message.request_type === "hello"){
        connections.push(new ConnectionUser(connection,message.user_id));

    }
}

function set_response(reply_type, reply, status) {
    return "{\"reply_type\": \""+reply_type+"\",\n" +
        "\"reply\": "+reply+",\n" +
        "\"status\": \"" +status+ "\"\n}";
}

function set_video_response(id, url) {
    return "{\"match_id\": \""+id+"\",\n" +
        "\"match_url\": \"" +url+ "\"\n}";
}

class ConnectionUser {
    constructor(socket, id) {
        this.socket          = socket;
        this.id     = id;
    }
}

// function jsonParser() {
//     // let routses = JSON.parse(filepath);
//     // WSIP = routses.ui;
//     // commentIP = routses.fabula;
//     // kb_url = routses.qi;
//     // url_video = routses.video;
//
//
//     fs.readFile('../../routes.json', 'utf8', (err, jsonString) => {
//         if (err) {
//             console.log("Error reading file from disk:", err);
//             return
//         }
//         try {
//             const routses = JSON.parse(jsonString);
//             WSIP = routses.ui.toString().split(":")[1].split("/")[2];
//             console.log(WSIP);
//             WS_PORT = routses.ui.toString().split(":")[2].split("/")[0];
//             console.log(WS_PORT);
//             commentIP = routses.fabula.toString().split(":")[1].split("/")[2];
//             console.log(commentIP);
//             COMMENT_PORT = routses.fabula.toString().split(":")[2].split("/")[0];
//             console.log(COMMENT_PORT);
//             kb_url = routses.qi;
//             url_video = routses.video;
//         }catch (e) {
//             console.log(e);
//         }
//     });
// }