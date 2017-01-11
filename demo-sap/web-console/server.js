"use strict";

var fs = require('fs');
var express = require('express');
var app = express();  
var server = require('http').createServer(app);  
var io = require('socket.io')(server);

var config = require('./config/default');
var port = config.app.port

var hbs = require('hbs');

var mqtt = require('mqtt');
var client  = mqtt.connect("mqtt://localhost:1883");

client.on('connect', function () {
  console.log("mqtt client connected");
  client.subscribe("gv/sensor/#");
  client.subscribe("gv/status/#");
  client.publish("gv/req/status", "{}"); // sensor status request
})

app.set('view engine', 'hbs');
app.use('/', require('./controllers/GET'));
app.use(express.static(__dirname + '/views/public'));

app.engine('html', require('hbs').__express);

hbs.registerPartials(__dirname + '/views/partials');

server.listen(port);  

console.log("Web Server listen to port: " + port);

var dutyCycle = 0;

// ================================================================
client.on('message', (topic, message) => {  

  if(topic == "gv/status") {
    console.log("Message arrived: " +  topic);
    var payload = JSON.parse(message);

    console.log("gv/status: " + message);

    io.emit("btn1", (payload.btn1.toLowerCase() === 'true'));
    io.emit("btn2", (payload.btn2.toLowerCase() === 'true'));
    io.emit("btn3", (payload.btn3.toLowerCase() === 'true'));
    io.emit("btn4", (payload.btn4.toLowerCase() === 'true'));
    io.emit("btn5", (payload.btn5.toLowerCase() === 'true'));
  }
  else if(topic == "gv/sensor/button") {
    console.log("Message arrived: " +  topic);
    var payload = JSON.parse(message);

    var id = payload.id;
    var status = (payload.status.toLowerCase() === 'true');
    console.log(topic + ":" + message);

    io.emit(id, status);
  }
  else if(topic == "gv/sensor/proximity") {
    console.log("Message arrived: " +  topic);
    var payload = JSON.parse(message);

    var id = payload.id;
    var status = true;
    console.log(topic + ":" + message);

    io.emit(id, status);
  }
})

// ============================ SOCKET ============================
io.on('connection', function(socket) {
    socket.on('btnStatus', function() {
      client.publish("gv/req/status", "{}");
    });
});