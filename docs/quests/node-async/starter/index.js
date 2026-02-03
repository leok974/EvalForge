import { getUserName } from "./src/users.js";

async function main() {
    console.log("ID 1:", await getUserName(1));
    console.log("ID -1:", await getUserName(-1));
}

main();
