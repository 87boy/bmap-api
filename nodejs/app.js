var config = require('./config.js');
var mysql = require('mysql');
var connection = mysql.createConnection(config);
connection.connect(function(err) {
    if (err) {
        console.error('error connecting: ' + err.stack);
        return;
    }
    console.log('connected as id ' + connection.threadId);
});

var insertSQL = 'insert ';