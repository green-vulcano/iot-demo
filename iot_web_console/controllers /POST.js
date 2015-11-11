/******************************************************************************************
 *   res.sendStatus(200); // equivalent to res.status(200).send('OK')
 *   res.sendStatus(403); // equivalent to res.status(403).send('Forbidden')
 *   res.sendStatus(404); // equivalent to res.status(404).send('Not Found')
 *   res.sendStatus(500); // equivalent to res.status(500).send('Internal Server Error')
 ******************************************************************************************/

module.exports = function() {

    var express = require('express');
    var app = express();
    // var auth = require('http-auth');
    // var basic = auth.basic({
    //     realm: "Private Area",
    //     file: __dirname + "/../config/htpasswd"
    // });

    // app.use(auth.connect(basic));

    /**************************************************************************
     *
     **************************************************************************/
    app.post('/login', function(req, res) {
        var body = '';

        req.on('data', function(chunk) {
            body += chunk.toString();
        });

        req.on('end', function() {
            var data = body.split("&");
            var access = {};

            data.forEach(function(d) {
                r = d.split("=");
                access[r[0]] = r[1];
            });

            var usr = access["username"];
            var pwd = access["password"];

            if(usr == "admin" && pwd == "admin") {
                res.redirect('/device/GVDEV001');
            }
            else {
                res.redirect('/');
            }
        });

        // var user = auth(req);

        // if (!user || user.name !== username || user.pass !== password) {
        //     res.set('WWW-Authenticate', 'Basic realm=Authorization Required');
        //     return res.send(401);
        // }
        // else {
        //     res.redirect('/home');
        // }
    });

    return app;
}();