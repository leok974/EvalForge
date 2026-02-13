const fs = require('fs');
const path = require('path');
const inp = path.join(__dirname, 'input.txt');
const out = path.join(__dirname, 'output.txt');
const content = fs.readFileSync(inp, 'utf8');
fs.writeFileSync(out, content.toUpperCase());