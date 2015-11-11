/******************************************************************************************
 *   res.sendStatus(200); // equivalent to res.status(200).send('OK')
 *   res.sendStatus(403); // equivalent to res.status(403).send('Forbidden')
 *   res.sendStatus(404); // equivalent to res.status(404).send('Not Found')
 *   res.sendStatus(500); // equivalent to res.status(500).send('Internal Server Error')
 ******************************************************************************************/
var config = require('../config/default');
var mqtt_host = config.mqtt.host;
var mqtt_port = config.mqtt.port;
var devices = require('../server').devices;

module.exports = function() {
    var express = require('express');
    var app = express();

    /**************************************************************************
     *
     **************************************************************************/
    app.get('/', function(req, res) {
        res.render('login');
    });

    /**************************************************************************
     *
     **************************************************************************/
    app.get('/home', function(req, res) {
        res.render('device');
    });

    /**************************************************************************
     *
     **************************************************************************/
    app.get('/config', function(req, res) {
        res.render('config');
    });

    /**************************************************************************
     *
     **************************************************************************/
    app.get('/logout', function(req, res){
        req.logOut(function (err) {
            res.redirect('/');
        });
    });

    /**************************************************************************
     *
     **************************************************************************/
    app.get('/device/:id', function(req, res) {
        var dev = devices.getConfig(req.params.id);
        var img = devices.getPicture(req.params.id);

        if(dev != undefined) {
            var id = dev["id"];
            var name =  dev["nm"];
            var ip = dev["ip"] != "" ? dev["ip"] : "<unknown>";
            var mac = dev["mac"] != "" ? dev["mac"] : "<unknown>";
            var sens = dev["sens"].length;
            var acts = dev["acts"].length;
            var sleep = dev["mode"].indexOf("sleep") > -1;
            var demo = dev["mode"].indexOf("demo") > -1;

            res.render('device', {
                dev_id: id,
                dev_name: name,
                dev_num_sens: sens,
                dev_num_acts: acts,
                dev_ip: ip,
                dev_mac: mac,
                dev_img: img,
                dev_sleep: sleep,
                dev_demo: demo,
                config: JSON.stringify(dev), 
                mqtt_host: mqtt_host,
                mqtt_port: mqtt_port
            });
        }
        else {
            res.sendStatus(404);
        }
    });

    return app;
}();