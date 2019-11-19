#!/usr/bin/env node

/**
 * Module dependencies and variables
 */
let app             = require('../app');
let commentApp      = require('../app2');
let debug           = require('debug')('websportserver:server');
let http            = require('http');
let WebSocketServer = require('websocket').server;
const WSIP          = '10.101.52.39';
const commentIP     = '10.101.52.39';
let connections     = [];
let old_comment     = null;
let new_comment     = null;

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
      handleClientMessage(message.utf8Data)
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
    return comment1.startTime >= comment2.startTime && comment1.startTime <= comment2.endTime || comment2.startTime >= comment1.startTime && comment2.startTime <= comment1.endTime;
}

function checkPriority(comment1, comment2) {
    return comment1.priority >= comment2.priority;
}

function handleClientMessage(body) {
    message = JSON.parse(body)
    if (message.request_type === "user_login") {

    }
    else if (message.request_type === "user_registration"){

    }
    else if (message.request_type === "user_update"){

    }
    else if (message.request_type === "get_video"){

    }
}