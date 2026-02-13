
const http = require('http');
const server = http.createServer((req, res) => {
  res.end('Hello HTTP');
});
server.listen(3000, () => { console.log('Listening'); });
