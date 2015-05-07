var net = require('net');
var port = 3000;

var server = net.createServer(function (socket) {
  socket.write('Hello World\n');
  socket.on('data', function(data) {
  	console.log(data.toString('utf8'));
  	socket.write(data);
  });
});

server.listen(port);
console.log('Server running at ' + port);