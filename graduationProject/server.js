/**
 * http://usejsdoc.org/
 */
const http = require("http");
const url = require('url');
const fs = require('fs');
const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const multer = require('multer');
const route = require('./route.js');

const app = express();
const upload = multer();

//미들웨어
app.use('/static', express.static(__dirname + '/resources'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use('/', route);

app.use((req, res, next) => {
	res.status(404).send('일치하는 주소가 없습니다!');
})
app.use((err, req, res, next) => {
	console.error(err.stack);
	res.status(500).send('서버 에러!');
})

app.listen(8080, () => {
	console.log('Express App on port 8080!');
});