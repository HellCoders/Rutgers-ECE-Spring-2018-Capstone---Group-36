// DEVICE-SIDE CODE (Thorson Dai)

// CONFIGURATION
	const mqtt = require('mqtt');
	// serial is 32 character case-sensitive alphanumeric (2e93)
	const serial = 'IqxiyascD121QO5ZwJ5tSq111BSz3HGLi';
	// connect to the mqtt broker we setup (placeholder)
	const client = mqtt.connect('mqtt://test.mosquitto.org');
	client.on('connect', function () {
		// subscribe to the channel to listen for commands / debug?
		client.subscribe(serial);
	});
	client.on('message', function (topic, message) {
		console.log(message.toString());
	});

// SENSOR VARIABLES & FUNCTIONS
	var motion; // last recorded time of motion event
	function deltaMotion() {
		client.publish(serial, "motion: " + motion);
	}

	var temp; // last recorded temperature
	function deltaTemp() {
		client.publish(serial, "temp: " + temp);
	}

	var humid; // last recorded humidity
	function deltaHumid() {
		client.publish(serial, "humid: " + humid);
	}

	var air; // last recorded air quality
	function deltaAir() {
		client.publish(serial, "air: " + air);
	}

	var lux; // last recorded light level
	function deltaLux() {
		client.publish(lux, "lux: " + lux);
	}

// PIPE HANDLER
	var data = '';
	process.stdin.resume();
	process.stdin.setEncoding('utf8');
	process.stdin.on('data', function(chunk) {
		data += chunk;
	});
	process.stdin.on('end', function() {
		data = data.split('\n').slice(0,-1);
		for (i=0; i<data.length; i++) {
			var entry = data[i].split(': ');
			if (entry.length !== 2) {
				console.log("[PIPE] Invalid data format: " + "\"" + data[i] + "\"");
			} else {
				switch (entry[0]) {
					// NOTE: We need to check the values for a change before publish -- such functionality has yet to be implemented.
					case "motion":
						motion = entry[1];
						deltaMotion();
						break;
					case "temp":
						temp = entry[1];
						deltaTemp();
						break;
					case "humid":
						humid = entry[1];
						deltaHumid();
						break;
					case "air":
						air = entry[1];
						deltaAir();
						break;
					case "lux":
						lux = entry[1];
						deltaLux();
						break;
					default:
						console.log("[PIPE] Sensor keyword not found: " + "\"" + entry[0] + "\"");
				}
			}
		}
	});

/* PIPE HANDLER EXPLAINED
"motion: 1517686559
temp: 31F
humid: 37%
air: delicious
lux: bright"

Which is equivalent to:
"motion: 1517686559\ntemp: 31F\nhumid: 37%\nair: delicious\nlux: bright\n"

Thus, splitting the data by '\n' delimiter results in the following array:
[ 'motion: 1517686559',
  'temp: 31F',
  'humid: 37%',
	'air: delicious',
	'lux: bright',
	'' ]

To eliminate the empty entry, the slice method is used.
Each remaining element in the array is iterated over, and split using ': '
After comparisons are made, information can be transmitted over MQTT.
*/
