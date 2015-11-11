/******************************************************************************************
 *   res.sendStatus(200); // equivalent to res.status(200).send('OK')
 *   res.sendStatus(403); // equivalent to res.status(403).send('Forbidden')
 *   res.sendStatus(404); // equivalent to res.status(404).send('Not Found')
 *   res.sendStatus(500); // equivalent to res.status(500).send('Internal Server Error')
 ******************************************************************************************/

module.exports = function() {
    var express = require('express');
    var app = express();

    /**************************************************************************
     *
     **************************************************************************/
    app.get('/', function(req, res) {
        res.render('home');
    });

    /**************************************************************************
     *
     **************************************************************************/
    app.get('/chars', function(req, res) {
        res.render('chars');
    });    


    /**************************************************************************
     *
     **************************************************************************/
    app.get('/colors', function(req, res) {
        res.render('colors');
    });    

    /**************************************************************************
     *
     **************************************************************************/
    app.get('/joystick', function(req, res) {
        res.render('joystick');
    });    


    return app;
}();