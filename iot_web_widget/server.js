var express = require('express');
var app = express();
var config = require('./config/default');
var port = config.app.port

app.set('view engine', 'hbs');
app.use('/', require('./routes/GET'));
app.use(express.static(__dirname + '/views/public'));
app.engine('html', require('hbs').__express);

app.listen(port);

console.log("Listen to port: " + port);