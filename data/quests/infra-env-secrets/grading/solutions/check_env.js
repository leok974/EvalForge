const rawMode = String(process.env.MODE || "").trim();
const rawPort = String(process.env.PORT || "").trim();
const apiKey = String(process.env.API_KEY || "").trim();

const MODE = rawMode ? rawMode : "dev";
const PORT = rawPort ? rawPort : "3000";

console.log(`MODE=${MODE}`);
console.log(`PORT=${PORT}`);

if (!apiKey) {
    console.log("API_KEY=MISSING");
    process.exit(3);
}

console.log("API_KEY=SET");
process.exit(0);
