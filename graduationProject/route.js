/**
 * http://usejsdoc.org/
 */
const express = require('express');
const path = require('path');
const router = express.Router();

//routing
router.get('/', (req, res) => {
	res.sendFile(path.join(__dirname, 'html', 'main.html'));
});
router.get('/excel', (req, res) => {
	res.sendFile(path.join(__dirname, 'html', 'excel.html'));
});
router.get('/about', (req, res) => {
	res.sendFile(path.join(__dirname, 'html', 'about.html'));
});
router.get('/input', (req, res) => {
	res.sendFile(path.join(__dirname, 'html', 'input.html'));
});
router.get('/output', (req, res) => {
	res.sendFile(path.join(__dirname, 'html', 'output.html'));
});

//export
module.exports = router;