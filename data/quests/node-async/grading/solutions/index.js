async function run() {
 console.log('Steps: 1');
 await new Promise(r => setTimeout(r, 10));
 console.log('Steps: 2');
}
run();