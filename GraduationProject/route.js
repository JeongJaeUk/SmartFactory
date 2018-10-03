/**
 * http://usejsdoc.org/
 */
var express = require('express');
var path = require('path');
var router = express.Router();
var fs = require('fs');
var spawn = require("child_process").spawn;

//routing
router.get('/', function(req, res) {
	res.sendFile(path.join(__dirname, '/views', 'home.html'));
});
router.get('/input', function(req, res) {
	res.sendFile(path.join(__dirname, '/views', 'input.html'));
});
router.get('/output', function(req, res) {
	res.sendFile(path.join(__dirname, '/views', 'output.html'));
});
router.get('/about', function(req, res) {
	res.sendFile(path.join(__dirname, '/views', 'about.html'));
});

router.post('/getColorTable', function(req, res) {
	console.log("getColorTable");
	
	var jsonData = JSON.parse(fs.readFileSync(path.join(__dirname, "/public/resource/", "colorTable.json"), 'utf8'));
	res.json(jsonData);
	res.end();
});

router.post('/addHistory', function(req, res) {
	console.log("addHistory called");
	
	var resultList = req.body.resultList || req.query.resultList;
	var fileName = req.body.fileName || req.query.fileName;
	
	//history에 저장
	console.log(fileName);
	
	var jsonData = JSON.stringify(resultList, null, 2);
	
	try {
		fs.writeFileSync(path.join(__dirname, "/history/", fileName + ".json"), jsonData);		
	} catch (e) {
		// TODO: handle exception
		console.log("err");
		res.end('{"error" : "작업 계획 기록 추가  실패"}');
	}
	res.end('{"success" : "작업 계획 기록 추가 성공"}');
});

router.post('/getResult', function(req, res) {
	console.log("getResult called");
	
	var resultList = req.body.resultList || req.query.resultList;
	var fileName = req.body.fileName || req.query.fileName;
	
	//history에 저장
	console.log(fileName);
	
	var jsonData = JSON.stringify(resultList, null, 2);
	
	fs.writeFile(path.join(__dirname, "/py/", "input.json"), jsonData, 'utf-8', function(e){
    if(e){
        console.log(e);
    }
    else{
        console.log('01 WRITE DONE!');
    }
    });
    
/*    var process = spawn('python',["writejson.py"],{cwd : './py/'});
    console.log("pre");
    process.stdout.on('data',function(chunk){
        var textChunk = chunk.toString('utf8'); // buffer to string
    });

	console.log("end");
*/
    var resultJson = JSON.parse(fs.readFileSync(path.join(__dirname, "/saveresult/", "result.json"), 'utf-8'));
    res.json(resultJson);
    res.end();
});

router.post('/readHistoryList', function(req, res) {
	console.log("readHistoryList called");
	
	var jsonData = {};
	var array = [];
	
	fs.readdir(path.join(__dirname, "/history/"), function(err, files) {
		files.forEach(function(file) {
			array.push(file);
		});
		jsonData.fileNames = array;
		res.json(jsonData);
		res.end();
	});
		
});

router.post('/callHistory', function(req, res) {
	console.log("callHistory called");
		
	var fileName = req.body.fileName || req.query.fileName;

	var jsonData = JSON.parse(fs.readFileSync(path.join(__dirname, "/history/", fileName), 'utf8'));
	res.json(jsonData);
	res.end();		
});

router.get('/machine', function(req, res) {
	res.sendFile(path.join(__dirname, '/views', 'machine.html'));
});

//export
module.exports = router;