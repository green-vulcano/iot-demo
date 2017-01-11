var config = {};

config.app = {};
config.app.port = 8181;

config.mqtt = {};
config.mqtt.host = "localhost";
config.mqtt.port = 1883;

// GPIO configuration
config.gpio = {};
config.gpio.button1 = 18;
config.gpio.button2 = 17;
config.gpio.button3 = 27;
config.gpio.button4 = 22;
config.gpio.proximity1 = 5;
config.gpio.proximity2 = 6;
config.gpio.proximity3 = 13;
config.gpio.proximity4 = 19;
config.gpio.servo1 = 20;

module.exports = config;