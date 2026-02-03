const port = process.env.PORT || 3000;
const dbUrl = process.env.DB_URL;

if (!dbUrl) {
    console.error("Error: DB_URL environment variable is required.");
    process.exit(1);
}

export const config = {
    port,
    dbUrl
};
