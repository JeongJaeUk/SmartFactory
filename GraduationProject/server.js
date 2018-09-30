/**
 * http://usejsdoc.org/
 */
var http = require("http");
var url = require('url');
var fs = require('fs');
var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');
var multer = require('multer');
var route = require('./route.js');

var app = express();
var upload = multer();


//미들웨어
app.use('/js', express.static(__dirname + '/node_modules/bootstrap/dist/js'));
app.use('/js', express.static(__dirname + '/node_modules/jquery/dist'));
app.use('/js', express.static(__dirname + '/node_modules/xlsx'));
app.use('/js', express.static(__dirname + '/node_modules/xlsx/dist'));
app.use('/js', express.static(__dirname + '/node_modules/sweetalert2/dist'));
app.use('/js', express.static(__dirname + '/node_modules/js-cookie/src'));

app.use('/css', express.static(__dirname + '/node_modules/bootstrap/dist/css'));
app.use('/css', express.static(__dirname + '/node_modules/sweetalert2/dist'));

app.use('/static', express.static(__dirname + '/public'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use('/', route);

app.use(function (req, res, next) {
	res.status(404).send('일치하는 주소가 없습니다!');
});
app.use(function (err, req, res, next) {
	console.error(err.stack);
	res.status(500).send('서버 에러!');
});

app.listen(8080, function() {
	console.log('Express App on port 8080!');
});