var walk    = require('walk');
var fs = require('fs');
var files   = [];
var config = {};

var IMG_PATH = "../assets/img_device/";
var IMG_FORMAT = ".png";

var STATUS_UNKNOWN = "UNKNOWN";
var STATUS_ON = "ON";
var STATUS_OFF = "OFF";
var STATUS_DEMO = "DEMO";

/************************************************
 * Returns whole configuration
 ************************************************/
var getAllConfig = function() {
	return config;
}

/************************************************
 * Returns a JSON formatted device configuration
 ************************************************/
var getConfig = function(device_id) {
	return config[device_id];
}

/************************************************
 * Returns a JSON formatted device configuration
 ************************************************/
var getPicture = function(device_id) {
	return IMG_PATH + device_id + IMG_FORMAT;
}

/************************************************
 * 
 ************************************************/
var getDevices = function() {
	var dev = {};

	for(var key in config) {
		var mode = {}
		mode["mode"] = STATUS_UNKNOWN;
		dev[key] = {};
		dev[key] = mode;
	}

	return dev;
}

/************************************************
 * 
 ************************************************/
var readFile = function(file_path, callback) {
	fs.readFile(file_path, function (err, data) {
		if (err) {
			throw err; 
		}

		var payload = JSON.parse(data);
		var id = payload["id"];

		callback(id, payload);
	});
}

/************************************************
 * Load configuration
 ************************************************/
var init = function(callback) {
	var walker = walk.walk(__dirname + '/../config/devices', { followLinks: false });

	walker.on('file', function(root, stat, next) {
		var file_path = root + '/' + stat.name
	    files.push(file_path);

	    fs.readFile(file_path, function (err, data) {
			if (err) {
				throw err; 
			}

			var payload = JSON.parse(data);
			var id = payload["id"];
			config[id] = payload;

			next();
		});
	});

	walker.on('end', function() {
	    return callback();
	});
}

exports.getAllConfig = getAllConfig
exports.getConfig = getConfig;
exports.getPicture = getPicture;
exports.init = init;
exports.getDevices = getDevices;

exports.STATUS_UNKNOWN = STATUS_UNKNOWN;
exports.STATUS_ON = STATUS_ON;
exports.STATUS_OFF = STATUS_OFF;
exports.STATUS_DEMO = STATUS_DEMO;