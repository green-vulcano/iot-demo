var express = require('express');  
var app = express();  
var server = require('http').createServer(app);  
var io = require('socket.io')(server);

var config = require('./config/default');
var port = config.app.port

var hbs = require('hbs');

var devices =  require('./helpers/devices');
exports.devices = devices;

app.set('view engine', 'hbs');
app.use('/', require('./controllers /GET'));
app.use('/data', require('./controllers /POST'));
app.use(express.static(__dirname + '/views/public'));

app.engine('html', require('hbs').__express);

hbs.registerPartials(__dirname + '/views/partials');

var devicesStatus; // last device configuration
devices.init(function() {
  devicesStatus = devices.getDevices();
});

server.listen(port);  

console.log("Listen to port: " + port);

/***************************************************************************
 *
 ***************************************************************************/
io.on('connection', function(socket) {    
    // socket.emit("server_message", socket.id, "connesso");

    socket.on('device_connected', function(client_id) {
      var status = devicesStatus[client_id];

      if(status.mode != devices.STATUS_UNKNOWN) {
        socket.emit("last_mode-" + client_id, status.mode);
      }
    });

    // =========================================================
    socket.on('change_mode', function(client_id, mode, value) {
      //  console.log(client_id + ": " + mode + " = " + value);
      devicesStatus[client_id]["mode"] = value.toUpperCase();
    });

    // =========================================================
    socket.on('disconnect', function() {
      // TODO
    });
});

