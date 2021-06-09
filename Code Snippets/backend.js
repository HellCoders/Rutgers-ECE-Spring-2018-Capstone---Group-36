const express = require('express'), app = express(), server = require('http').createServer(app);
const bodyParser = require('body-parser'), cookieParser = require('cookie-parser');

app.set('views', __dirname);
app.set('view engine', 'ejs');
app.use(express.static(__dirname));
app.use(cookieParser());
app.use(bodyParser.urlencoded({extended: true}));
server.listen(2018);

const mysql = require('mysql2');
const mysqlconnect = {host: 'localhost', port: 3306,
	user: 'root', database: 'capstone', connectionLimit: 1}
const pool = mysql.createPool(mysqlconnect);

// dummy readout -> login page
app.get('/', function(req, res) {
	var data = "testing, 1, 2, 3!";
	res.render('dashboard', {data: data});

	/*
	// for testing, redirect to this device that we've setup
	res.redirect('/164005505/');
	*/
});
// data display page for device
app.get('/:deviceid/', function(req, res) {
	// [UNIMPLEMENTED]
	// Check if device in cache and data not older than 30 minutes.
	// If not in cache, populate cache entry.
	var timeDay = Math.trunc(Date.now()/60000 - 1440); // lower bound
	pool.query('SELECT light, temperature, humidity, motion, timestamp FROM data WHERE device_id = ?and timestamp > ? order by timestamp asc limit 1440', [req.params.deviceid, timeDay], function(err,results) {
		console.log(results);
		process.nextTick(function() {
			if (err) console.log(err);
			res.render('dashboard', {data: results});
		});
	});

});

const mqtt = require('mqtt'), client = mqtt.connect('mqtt://test.mosquitto.org');

var cache = {};

const testSerial = '164005505';
client.on('connect', function () {
	client.subscribe(testSerial);
	client.publish(testSerial, "Server is subscribed!");
});
client.on('message', function (topic, message) {
	console.log("[MQTT] " + message.toString());
	var device_id = parseInt(topic);
	var data = message.toString().split(', ');
	if (data.length === 5) { // four sensors, four columns + timestamp
		// need additional validation -- Bobby Tables, is that you?
		var light = parseInt(data[0]),
			temp = parseInt(data[1]),
			humidity = parseInt(data[2]),
			motion = parseInt(data[3]),
			time = parseInt(data[4]);
		pool.query('INSERT INTO data SET device_id=?, light=?, temperature=?, humidity=?, motion=?, timestamp=?', [device_id, light, temp, humidity, motion, time], function(err, results) {
			if (err) {
				console.log(err);
			}
		});
	}

	// Check if device data is in cache - if so, append to display arrays and renew timestamp.
});

/*const fs = require('fs');
const fifoPath = 'pipe';

var data = '';
const fd = fs.openSync(fifoPath, 'r+');
const stream = fs.createReadStream(null, {fd});
stream.on('data', data => {
	console.log(data.toString());
});*/
